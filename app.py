from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import re

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")


def normalize_topic(text):
    text = text.lower().strip()
    text = text.replace("subject:", "").strip()
    text = text.replace("topic:", "").strip()
    text = text.replace("indian history", "").strip()
    text = text.replace("history", "").strip()
    text = " ".join(text.split())
    text = text.strip(", ").strip()
    return text


ALIASES = {
    "alexander": "alexander the great",
    "alexander the great": "alexander the great",
    "alexander invasion": "alexander the great",

    "sangam era": "sangam age",
    "sangam period": "sangam age",
    "sangam age": "sangam age",

    "mauryan age": "mauryan empire",
    "mauryan period": "mauryan empire",
    "mauryan era": "mauryan empire",
    "age of mauryans": "mauryan empire",
    "mauryan empire": "mauryan empire"
}


def canonical_topic(text):
    normalized = normalize_topic(text)
    return ALIASES.get(normalized, normalized)


# ===== LOAD PYQ TXT =====
def load_pyq_text():
    try:
        with open("ancient_pyqs.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


PYQ_TEXT = load_pyq_text()


def get_pyqs_from_txt(topic):
    if not PYQ_TEXT.strip():
        return "No PYQs came from this subtopic so far."

    topic = canonical_topic(topic)
    topic_norm = normalize_topic(topic)

    pattern = re.compile(r"\[(.*?)\](.*?)(?=\n\s*\[.*?\]|\Z)", re.DOTALL)
    matches = pattern.findall(PYQ_TEXT)

    exact_block = None
    partial_block = None

    for raw_title, raw_content in matches:
        title_norm = normalize_topic(raw_title)

        if title_norm == topic_norm:
            exact_block = raw_content.strip()
            break

        if topic_norm in title_norm or title_norm in topic_norm:
            partial_block = raw_content.strip()

    selected = exact_block or partial_block

    if not selected:
        return "No PYQs came from this subtopic so far."

    return selected
# ========================


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

        topic_key = canonical_topic(user_message)

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

Topic:
{topic_key}

Answer strictly in this structure only:

A. UPSC PRELIMS PYQs (Past 10 Years)

Rules:
- This section will be replaced separately by the system
- Still keep the section heading in the answer
- If no PYQs are found, write exactly:
No PYQs came from this subtopic so far.

B. QUICK REVISION NOTES

At the beginning of this section, write exactly:
Here are your quick revision notes on {topic_key} for your exam.

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
Use simple bullet points only

Formatting style for Revision Takeaway:
Use 4 to 6 very short bullets only

Other rules:
- Mention important sites, rivers, capitals, regions, or geographic references wherever relevant
- Include one UPSC Trap Zone
- Include one one-line revision takeaway
- Keep the tone crisp, factual, exam-oriented, and revision-friendly
- No clutter
- No decorative formatting
- Cover complete syllabus scope of the topic, not partial content

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
- Each MCQ must test a different sub-concept from the topic
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

        # ===== REPLACE PYQ SECTION FROM TXT =====
        pyq_content = get_pyqs_from_txt(topic_key)

        a_heading = "A. UPSC PRELIMS PYQs (Past 10 Years)"
        b_heading = "B. QUICK REVISION NOTES"

        if a_heading in answer and b_heading in answer:
            before_b, after_b = answer.split(b_heading, 1)
            answer = (
                f"{a_heading}\n\n"
                f"{pyq_content.strip()}\n\n"
                f"{b_heading}{after_b}"
            )
        # =======================================

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
