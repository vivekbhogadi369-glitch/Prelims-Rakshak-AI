from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import re

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")


def normalize_topic(text):
    text = (text or "").lower().strip()

    # remove only leading labels
    text = re.sub(r"^subject\s*:\s*", "", text)
    text = re.sub(r"^topic\s*:\s*", "", text)

    # remove subject tags only at the end
    text = re.sub(r",?\s*indian history\s*$", "", text)
    text = re.sub(r",?\s*history\s*$", "", text)

    # normalize punctuation
    text = text.replace("&", " and ")
    text = re.sub(r"[\[\]\(\)\{\}]", " ", text)
    text = re.sub(r"[-_/,:;]", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)

    # collapse spaces
    text = " ".join(text.split())

    return text.strip()


def canonical_topic(text):
    return normalize_topic(text)


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

    topic_norm = normalize_topic(topic)
    if not topic_norm:
        return "No PYQs came from this subtopic so far."

    text = PYQ_TEXT.replace("\r\n", "\n").replace("\r", "\n")

    # block format:
    # [Heading]
    # content...
    # [Next Heading]
    pattern = re.compile(r"\[(.*?)\]\s*(.*?)(?=\n\s*\[.*?\]\s*|\Z)", re.DOTALL)
    matches = pattern.findall(text)

    if not matches:
        return "No PYQs came from this subtopic so far."

    topic_words = set(topic_norm.split())

    best_score = -1
    best_content = None

    for raw_title, raw_content in matches:
        title_norm = normalize_topic(raw_title)
        content = raw_content.strip()

        if not title_norm or not content:
            continue

        # exact match
        if title_norm == topic_norm:
            return content

        # full containment
        if topic_norm in title_norm or title_norm in topic_norm:
            score = 100
        else:
            title_words = set(title_norm.split())
            common = topic_words.intersection(title_words)
            score = len(common)

        if score > best_score:
            best_score = score
            best_content = content

    # safe fallback:
    # - if single-word topic, 1 common word is enough
    # - if multi-word topic, require at least 2 common words
    if best_content:
        if len(topic_words) == 1 and best_score >= 1:
            return best_content
        if len(topic_words) >= 2 and best_score >= 2:
            return best_content

    return "No PYQs came from this subtopic so far."
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
            _, after_b = answer.split(b_heading, 1)
            answer = (
                f"{a_heading}\n\n"
                f"{pyq_content.strip()}\n\n"
                f"{b_heading}{after_b}"
            )

        # Force exact headings for frontend formatter
        answer = answer.replace("A. UPSC PRElims PYQs (Past 10 Years)", "A. UPSC PRELIMS PYQs (Past 10 Years)")
        answer = answer.replace("A. UPSC PRElims PYQs", "A. UPSC PRELIMS PYQs")
        answer = answer.replace("A. UPSC PRELims PYQs", "A. UPSC PRELIMS PYQs")
        answer = answer.replace("A. UPSC Prelims PYQs", "A. UPSC PRELIMS PYQs")
        answer = answer.replace("B. Quick Revision Notes", "B. QUICK REVISION NOTES")
        answer = answer.replace("C. Practice MCQs", "C. PRACTICE MCQs")
        # =======================================

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
