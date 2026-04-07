from flask import Flask, request, jsonify, render_template, send_from_directory
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

    return best_content


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pyqs")
def pyqs_page():
    return render_template("pyqs.html")


@app.route("/notes")
def notes_page():
    return render_template("notes.html")


@app.route("/pyq-subjects", methods=["GET"])
def pyq_subjects():
    return jsonify({"subjects": get_pyq_subjects()})


@app.route("/pyq-topics", methods=["GET"])
def pyq_topics():
    subject = request.args.get("subject", "").strip()
    return jsonify({"topics": get_pyq_topics(subject)})


@app.route("/pyq-questions", methods=["GET"])
def pyq_questions():
    subject = request.args.get("subject", "").strip()
    topic = request.args.get("topic", "").strip()
    return jsonify({"questions": get_pyqs_by_subject_topic(subject, topic)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
