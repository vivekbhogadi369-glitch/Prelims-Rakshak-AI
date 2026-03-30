from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import json

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

CACHE_FILE = "topic_cache.json"

if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            topic_cache = json.load(f)
    except Exception:
        topic_cache = {}
else:
    topic_cache = {}


def normalize_topic(text):
    text = text.lower().strip()
    text = text.replace("subject:", "").strip()
    text = text.replace("topic:", "").strip()
    text = text.replace("indian history", "").strip()
    text = text.replace("history", "").strip()
    text = " ".join(text.split())
    text = text.strip(", ").strip()
    return text


def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(topic_cache, f, ensure_ascii=False, indent=2)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"answer": "Please enter topic, subject."})

        cache_key = normalize_topic(user_message)

        if cache_key in topic_cache:
            return jsonify({"answer": topic_cache[cache_key]})

        prompt = f"""
You are Prelims Rakshak AI created by Vivek Sir for UPSC aspirants.

Use uploaded documents as the primary source.

GLOBAL RULES:
- Do NOT include references
- Do NOT include citations
- Do NOT include source names
- Do NOT include follow-up questions
- Do NOT include supplementary questions
- Do NOT print divider lines
- Do NOT print separator lines like --- or ____ or ===
- Do NOT add any extra section beyond A, B and C
- Do NOT use tables
- Do NOT use markdown tables
- Do NOT use raw symbols like | for formatting
- Do NOT use emojis
- Do NOT use words like Easy, Moderate, Tough inside question titles
- Do NOT write labels like "Question 1:", "Question 2:", "MCQ 1:", "Statement Based", "Match the Following", "Factual Type"
- Do NOT write commentary outside the required format
- Keep the answer simple, clean, mobile-friendly, and easy to read
- Make the answer look like classroom coaching notes, not AI output
- End the full answer with exactly this sentence:
All the best for your preparation.

Student query:
{user_message}

Answer strictly in this structure only:

A. UPSC PRELIMS PYQs (Past 10 Years)

Rules:
- Search uploaded PYQ PDFs first
- Use exact topic match first
- If exact PYQs are limited, include closely related PYQs from the same chapter/topic family
- Do NOT invent PYQs
- Do NOT invent years
- Do NOT copy explanation text from the PDF
- Extract only the question, options and answer from the uploaded PYQ PDFs
- Generate your own fresh short analysis
- Keep PYQ format simple and readable

For every PYQ use this exact format only:

2019 - UPSC Prelims
Question:
[full question with options if available]
Correct Answer:
[answer only]
PYQ INSIGHT:
- Concept Tested:
- Why UPSC asked this:
- Elimination Hint:
- One-line Takeaway:
PYQ TAG:
- Topic Frequency:
- Last Asked Year:
- Nature:
- Difficulty:

For Topic Frequency use only:
High / Medium / Low

For Nature use only:
Factual / Conceptual / Analytical

For Difficulty use only:
Easy / Moderate / Tough

If no exact or closely related PYQs are found, write exactly:
No PYQs came from this subtopic so far.

B. QUICK REVISION NOTES

At the beginning of this section, write exactly:
Here are your quick revision notes on {user_message} for your exam.

At the end of this section, write exactly:
Best wishes for your preparation.

Rules:
- Minimum around 700 words
- Prefer short, crisp bullet points
- Avoid long dull paragraphs
- Use only simple headings and bullets
- Do NOT use tables
- Do NOT use box drawings
- Do NOT use raw symbols like | or -> or /
- Do NOT make it look technical
- Make it easy enough for a beginner student to revise quickly on mobile
- Include only these headings whenever relevant, and write each heading exactly as given below:

Introduction
Background
Core Features
Important Sites
Chronology
UPSC Trap Zone
Revision Takeaway

Formatting style for Important Sites:
Use this exact style only:

Harappa
- Location:
- Importance:

Mohenjo-Daro
- Location:
- Importance:

Formatting style for Chronology:
Use simple bullet points only, for example:
- 1921 - Harappa discovered
- 1922 - Mohenjo-Daro discovered
- 2600 BCE to 1900 BCE - Mature phase

Formatting style for Revision Takeaway:
Use 4 to 6 very short bullets only

Other rules:
- Mention important sites, rivers, capitals, regions, or geographic references wherever relevant
- Include one UPSC Trap Zone
- Include one one-line revision takeaway
- Keep the tone crisp, factual, exam-oriented, and revision-friendly
- No clutter
- No decorative formatting

C. PRACTICE MCQs

Generate exactly 10 UPSC Prelims standard MCQs.

Distribution:
- 5 statement-based questions
- 3 match-the-following questions
- 2 factual but tricky questions

Difficulty:
- 3 easy
- 5 moderate
- 2 tough

Strict format for every MCQ:
Question:
[full question only]
Options:
[a full set of options]
Correct Answer:
[answer only]
Elimination Logic:
[2 to 4 short lines only]
Why other options are wrong:
[2 to 4 short lines only]
Trap Zone:
[1 to 2 short lines only]

Very important MCQ rules:
- Do NOT write any title before a question
- Do NOT write "Question 1", "Question 2", "MCQ 1", "Easy", "Moderate", "Tough"
- Start every MCQ directly with the label "Question:"
- Do NOT split one MCQ into multiple cards or sections
- Keep each MCQ self-contained
- Do NOT repeat PYQs directly unless absolutely necessary
- Keep MCQs linked to the same concept family as the user query
- Make them UPSC-style, not school-style
- Keep wording simple and clean
- Avoid very long option blocks
- Avoid decorative formatting

Before sending the final answer, silently check:
- Did you use only A, B, C sections?
- Did you avoid tables and raw symbols?
- Did every MCQ begin directly with "Question:"?
- Did you avoid labels like "Question 2 (Moderate)"?
- Did you avoid any extra commentary?

If any rule is broken, rewrite the answer before sending.
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [VECTOR_STORE_ID],
                    "max_num_results": 30
                }
            ]
        )

        answer = "Error: No answer generated."

        for item in response.output:
            if getattr(item, "type", "") == "message":
                contents = getattr(item, "content", [])
                for content in contents:
                    if getattr(content, "type", "") in ["output_text", "text"]:
                        answer = getattr(content, "text", "Error: No answer generated.")
                        break
                if answer != "Error: No answer generated.":
                    break

        topic_cache[cache_key] = answer
        save_cache()

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
