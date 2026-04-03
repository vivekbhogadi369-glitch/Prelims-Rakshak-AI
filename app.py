from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import re
from difflib import SequenceMatcher

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

    # normalize common history-equivalent words
    text = text.replace("civilisation", "civilization")
    text = text.replace("centre", "center")
    text = text.replace("centres", "centers")

    # normalize separators/punctuation
    text = text.replace("&", " and ")
    text = re.sub(r"[\[\]\(\)\{\}]", " ", text)
    text = re.sub(r"[-_/,:;]", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)

    # normalize common interchangeable exam words
    text = re.sub(r"\bera\b", "age", text)
    text = re.sub(r"\bperiod\b", "age", text)

    # collapse spaces
    text = " ".join(text.split())

    # very light singularization for common plural endings
    words = []
    for w in text.split():
        if len(w) > 4 and w.endswith("ies"):
            w = w[:-3] + "y"
        elif len(w) > 4 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        words.append(w)

    return " ".join(words).strip()


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


def score_topic_match(topic_norm, title_norm):
    if not topic_norm or not title_norm:
        return 0.0

    # 1. exact match
    if topic_norm == title_norm:
        return 1000.0

    # 2. one contains the other
    if topic_norm in title_norm or title_norm in topic_norm:
        return 900.0

    topic_words = set(topic_norm.split())
    title_words = set(title_norm.split())

    if not topic_words or not title_words:
        return 0.0

    common = topic_words.intersection(title_words)

    # 3. word overlap
    overlap_count = len(common)
    overlap_ratio = overlap_count / max(len(topic_words), len(title_words))

    # 4. fuzzy similarity
    fuzzy = SequenceMatcher(None, topic_norm, title_norm).ratio()

    # combined score
    return (overlap_count * 100.0) + (overlap_ratio * 100.0) + (fuzzy * 10.0)


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
    # until next [Heading]
    pattern = re.compile(r"\[(.*?)\]\s*(.*?)(?=\n\s*\[.*?\]\s*|\Z)", re.DOTALL)
    matches = pattern.findall(text)

    if not matches:
        return "No PYQs came from this subtopic so far."

    best_score = -1.0
    best_content = None
    best_title = ""

    for raw_title, raw_content in matches:
        title_norm = normalize_topic(raw_title)
        content = raw_content.strip()

        if not title_norm or not content:
            continue

        score = score_topic_match(topic_norm, title_norm)

        if score > best_score:
            best_score = score
            best_content = content
            best_title = title_norm

    if not best_content:
        return "No PYQs came from this subtopic so far."

    # safety checks so wrong topics are not picked
    topic_words = set(topic_norm.split())
    best_title_words = set(best_title.split())
    common_words = topic_words.intersection(best_title_words)

    # accept if:
    # exact/containment score already hit, or
    # at least 2 common words, or
    # single-word topic with strong fuzzy similarity
    if best_score >= 900:
        return best_content

    if len(common_words) >= 2:
        return best_content

    if len(topic_words) == 1:
        fuzzy = SequenceMatcher(None, topic_norm, best_title).ratio()
        if fuzzy >= 0.72:
            return best_content

    # extra fallback:
    # for two-word topics, accept one strong matching keyword + decent fuzzy similarity
    if len(topic_words) == 2:
        fuzzy = SequenceMatcher(None, topic_norm, best_title).ratio()
        if len(common_words) >= 1 and fuzzy >= 0.68:
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
