from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import re
from difflib import SequenceMatcher

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")


def clean_display_topic(text):
    text = (text or "").strip()
    text = re.sub(r"^\s*subject\s*:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*topic\s*:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_topic(text):
    text = (text or "").lower().strip()

    text = re.sub(r"^\s*subject\s*:\s*", "", text)
    text = re.sub(r"^\s*topic\s*:\s*", "", text)

    # remove trailing subject markers only
    text = re.sub(r",?\s*indian history\s*$", "", text)
    text = re.sub(r",?\s*history\s*$", "", text)

    # normalize common variants
    text = text.replace("civilisation", "civilization")
    text = text.replace("centre", "center")
    text = text.replace("centres", "centers")

    # common exam synonym normalization
    text = re.sub(r"\bera\b", "age", text)
    text = re.sub(r"\bperiod\b", "age", text)

    # punctuation normalization
    text = text.replace("&", " and ")
    text = re.sub(r"[\[\]\(\)\{\}]", " ", text)
    text = re.sub(r"[-_/,:;]", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)

    # collapse spaces
    text = " ".join(text.split())

    return text.strip()


# ===== LOAD PYQ TXT =====
def load_pyq_text():
    try:
        with open("ancient_pyqs.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


PYQ_TEXT = load_pyq_text()


def extract_pyq_blocks(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Standard expected format:
    # [Heading]
    # content...
    # [Next Heading]
    pattern = re.compile(r"\[(.*?)\]\s*(.*?)(?=\n\s*\[.*?\]\s*|\Z)", re.DOTALL)
    matches = pattern.findall(text)

    blocks = []
    for raw_title, raw_content in matches:
        title = raw_title.strip()
        content = raw_content.strip()
        if title and content:
            blocks.append((title, content))

    return blocks


def score_topic_match(topic_norm, title_norm):
    if not topic_norm or not title_norm:
        return -1

    # 1. exact match
    if topic_norm == title_norm:
        return 1000

    # 2. containment match
    if topic_norm in title_norm or title_norm in topic_norm:
        return 900

    topic_words = set(topic_norm.split())
    title_words = set(title_norm.split())

    common = topic_words.intersection(title_words)

    # 3. strong word overlap
    if topic_words and title_words:
        overlap_score = len(common) * 100
    else:
        overlap_score = 0

    # 4. fuzzy backup
    fuzzy_score = int(SequenceMatcher(None, topic_norm, title_norm).ratio() * 100)

    return overlap_score + fuzzy_score


def get_pyqs_from_txt(topic):
    if not PYQ_TEXT.strip():
        return "No PYQs came from this subtopic so far."

    topic_norm = normalize_topic(topic)
    if not topic_norm:
        return "No PYQs came from this subtopic so far."

    blocks = extract_pyq_blocks(PYQ_TEXT)
    if not blocks:
        return "No PYQs came from this subtopic so far."

    best_title = ""
    best_content = None
    best_score = -1

    topic_words = set(topic_norm.split())

    for raw_title, raw_content in blocks:
        title_norm = normalize_topic(raw_title)
        score = score_topic_match(topic_norm, title_norm)

        if score > best_score:
            best_score = score
            best_title = title_norm
            best_content = raw_content

    if not best_content:
        return "No PYQs came from this subtopic so far."

    best_title_words = set(best_title.split())
    common_words = topic_words.intersection(best_title_words)
    fuzzy_ratio = SequenceMatcher(None, topic_norm, best_title).ratio()

    # Safe acceptance rules
    if best_score >= 900:
        return best_content

    if len(common_words) >= 2:
        return best_content

    if len(topic_words) == 1 and fuzzy_ratio >= 0.78:
        return best_content

    if len(topic_words) == 2 and len(common_words) >= 1 and fuzzy_ratio >= 0.72:
        return best_content

    return "No PYQs came from this subtopic so far."
# ========================


def force_exact_headings(answer):
    if not answer:
        return answer

    # normalize known heading variations
    replacements = {
        "A. UPSC PRElims PYQs (Past 10 Years)": "A. UPSC PRELIMS PYQs (Past 10 Years)",
        "A. UPSC PRElims PYQs": "A. UPSC PRELIMS PYQs (Past 10 Years)",
        "A. UPSC PRELims PYQs": "A. UPSC PRELIMS PYQs (Past 10 Years)",
        "A. UPSC Prelims PYQs": "A. UPSC PRELIMS PYQs (Past 10 Years)",
        "B. Quick Revision Notes": "B. QUICK REVISION NOTES",
        "B. Quick revision notes": "B. QUICK REVISION NOTES",
        "C. Practice MCQs": "C. PRACTICE MCQs",
        "C. Practice Mcqs": "C. PRACTICE MCQs",
    }

    for old, new in replacements.items():
        answer = answer.replace(old, new)

    # regex safety
    answer = re.sub(
        r"(?im)^a\.\s*upsc\s*prelims\s*pyqs(?:\s*\(past\s*10\s*years\))?\s*$",
        "A. UPSC PRELIMS PYQs (Past 10 Years)",
        answer,
    )
    answer = re.sub(
        r"(?im)^b\.\s*quick\s*revision\s*notes\s*$",
        "B. QUICK REVISION NOTES",
        answer,
    )
    answer = re.sub(
        r"(?im)^c\.\s*practice\s*mcqs\s*$",
        "C. PRACTICE MCQs",
        answer,
    )

    return answer


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

        display_topic = clean_display_topic(user_message)
        pyq_lookup_topic = normalize_topic(user_message)

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
{display_topic}

Answer strictly in this structure only:

A. UPSC PRELIMS PYQs (Past 10 Years)

Rules:
- This section will be replaced separately by the system
- Still keep the section heading in the answer
- If no PYQs are found, write exactly:
No PYQs came from this subtopic so far.

B. QUICK REVISION NOTES

At the beginning of this section, write exactly:
Here are your quick revision notes on {display_topic} for your exam.

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

        answer = force_exact_headings(answer)

        # ===== REPLACE PYQ SECTION FROM TXT =====
        pyq_content = get_pyqs_from_txt(pyq_lookup_topic)

        a_heading = "A. UPSC PRELIMS PYQs (Past 10 Years)"
        b_heading = "B. QUICK REVISION NOTES"

        if a_heading in answer and b_heading in answer:
            _, after_b = answer.split(b_heading, 1)
            answer = (
                f"{a_heading}\n\n"
                f"{pyq_content.strip()}\n\n"
                f"{b_heading}{after_b}"
            )

        answer = force_exact_headings(answer)
        # =======================================

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
