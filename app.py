from flask import Flask, request, jsonify, render_template, send_from_directory
from openai import OpenAI
import os
import re
import json
from difflib import SequenceMatcher

# ✅ FIXED (static serving)
app = Flask(__name__, static_folder="static")


# ✅ FORCE STATIC ROUTE (important for Railway)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")


def load_pyqs_json():
    try:
        with open("pyqs.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


PYQS_DATA = load_pyqs_json()


def get_pyq_subjects():
    return list(PYQS_DATA.keys())


def get_pyq_topics(subject):
    if subject in PYQS_DATA and isinstance(PYQS_DATA[subject], dict):
        return list(PYQS_DATA[subject].keys())
    return []


def get_pyqs_by_subject_topic(subject, topic):
    if subject in PYQS_DATA:
        if topic in PYQS_DATA[subject]:
            return PYQS_DATA[subject][topic]
    return []


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

    text = re.sub(r",?\s*indian history\s*$", "", text)
    text = re.sub(r",?\s*history\s*$", "", text)

    text = text.replace("civilisation", "civilization")
    text = text.replace("centre", "center")
    text = text.replace("centres", "centers")

    text = re.sub(r"\bera\b", "age", text)
    text = re.sub(r"\bperiod\b", "age", text)

    text = text.replace("&", " and ")
    text = re.sub(r"[\[\]\(\)\{\}]", " ", text)
    text = re.sub(r"[-_/,:;]", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)

    text = " ".join(text.split())

    return text.strip()


def load_pyq_text():
    try:
        with open("ancient_pyqs.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


PYQ_TEXT = load_pyq_text()


def extract_pyq_blocks(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")

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

    if topic_norm == title_norm:
        return 1000

    if topic_norm in title_norm or title_norm in topic_norm:
        return 900

    topic_words = set(topic_norm.split())
    title_words = set(title_norm.split())

    common = topic_words.intersection(title_words)

    overlap_score = len(common) * 100 if topic_words and title_words else 0
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

    if best_score >= 900:
        return best_content

    if len(common_words) >= 2:
        return best_content

    if len(topic_words) == 1 and fuzzy_ratio >= 0.78:
        return best_content

    if len(topic_words) == 2 and len(common_words) >= 1 and fuzzy_ratio >= 0.72:
        return best_content

    return "No PYQs came from this subtopic so far."


def force_exact_headings(answer):
    if not answer:
        return answer

    replacements = {
        "A. UPSC Prelims PYQs": "A. UPSC PRELIMS PYQs (Past 10 Years)",
        "B. Quick Revision Notes": "B. QUICK REVISION NOTES",
        "C. Practice MCQs": "C. PRACTICE MCQs",
    }

    for old, new in replacements.items():
        answer = answer.replace(old, new)

    return answer


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pyq-subjects", methods=["GET"])
def pyq_subjects():
    try:
        return jsonify({"subjects": get_pyq_subjects()})
    except Exception as e:
        return jsonify({"subjects": [], "error": str(e)}), 500


@app.route("/pyq-topics", methods=["GET"])
def pyq_topics():
    try:
        subject = request.args.get("subject", "").strip()
        return jsonify({"topics": get_pyq_topics(subject)})
    except Exception as e:
        return jsonify({"topics": [], "error": str(e)}), 500


@app.route("/pyq-questions", methods=["GET"])
def pyq_questions():
    try:
        subject = request.args.get("subject", "").strip()
        topic = request.args.get("topic", "").strip()
        return jsonify({"questions": get_pyqs_by_subject_topic(subject, topic)})
    except Exception as e:
        return jsonify({"questions": [], "error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"answer": "Please enter topic, subject."})

        display_topic = clean_display_topic(user_message)
        pyq_lookup_topic = normalize_topic(user_message)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Topic: {display_topic}",
            tools=[{"type": "file_search", "vector_store_ids": [VECTOR_STORE_ID]}]
        )

        answer = "Error: No answer generated."

        for item in response.output:
            if getattr(item, "type", "") == "message":
                for content in getattr(item, "content", []):
                    if getattr(content, "type", "") in ["output_text", "text"]:
                        answer = getattr(content, "text", answer)

        answer = force_exact_headings(answer)

        pyq_content = get_pyqs_from_txt(pyq_lookup_topic)

        if "A. UPSC PRELIMS PYQs (Past 10 Years)" in answer:
            parts = answer.split("B. QUICK REVISION NOTES")
            if len(parts) == 2:
                answer = f"A. UPSC PRELIMS PYQs (Past 10 Years)\n\n{pyq_content}\n\nB. QUICK REVISION NOTES{parts[1]}"

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
