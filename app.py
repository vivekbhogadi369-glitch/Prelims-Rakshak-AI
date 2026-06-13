from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import re
import json
import base64
import requests
from difflib import SequenceMatcher
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash

app = Flask(__name__, static_folder="static")

database_url = os.environ.get("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Institute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(500))
    theme_color = db.Column(db.String(20), default="#6d28d9")
    status = db.Column(db.String(50), default="active")
    subscription_start = db.Column(db.Date)
    subscription_end = db.Column(db.Date)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institute_id = db.Column(db.Integer, db.ForeignKey("institute.id"), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)


class InstituteAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    institute_id = db.Column(
        db.Integer,
        db.ForeignKey("institute.id"),
        nullable=False
    )

    full_name = db.Column(
        db.String(200),
        nullable=False
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(300),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    name = db.Column(db.String(300), nullable=False)


class PYQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=True)
    year = db.Column(db.Integer)
    question = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text)
    answer = db.Column(db.Text)
    explanation = db.Column(db.Text)
    elimination_logic = db.Column(db.Text)


class MCQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=True)
    question = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text)
    answer = db.Column(db.Text)
    explanation = db.Column(db.Text)
    elimination_logic = db.Column(db.Text)
    difficulty = db.Column(db.String(50))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), default="english")


class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=True)
    language = db.Column(db.String(50), nullable=False)
    audio_url = db.Column(db.String(1000), nullable=False)


class CurrentAffair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    source_url = db.Column(db.String(1000))
    date = db.Column(db.Date)
    content = db.Column(db.Text)


class MonthlyMagazine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    file_url = db.Column(db.String(1000))


class JobAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    source_url = db.Column(db.String(1000))
    date = db.Column(db.Date)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)


class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(50))
    content_id = db.Column(db.Integer)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institute_id = db.Column(db.Integer, db.ForeignKey("institute.id"), nullable=True)
    title = db.Column(db.String(300), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_global = db.Column(db.Boolean, default=True)


@app.route("/db-check")
def db_check():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"database": "connected"}), 200
    except Exception as e:
        return jsonify({"database": "error", "details": str(e)}), 500


@app.route("/init-db")
def init_db():
    try:
        with app.app_context():
            db.create_all()
        return jsonify({"database": "tables created"}), 200
    except Exception as e:
        return jsonify({"database": "error", "details": str(e)}), 500


@app.route("/create-super-admin")
def create_super_admin():
    username = "vivek"
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "Super admin already exists"}), 200

    admin = User(
        institute_id=None,
        name="Vivek",
        username=username,
        password_hash=generate_password_hash("vivek@123"),
        role="super_admin",
        is_active=True
    )

    db.session.add(admin)
    db.session.commit()

    return jsonify({
        "message": "Super admin created",
        "username": "vivek",
        "password": "vivek@123",
        "role": "super_admin"
    }), 201


@app.route("/create-demo-institute")
def create_demo_institute():
    institute = Institute.query.filter_by(name="Demo Institute").first()

    if institute:
        return jsonify({
            "message": "Demo Institute already exists",
            "id": institute.id
        }), 200

    institute = Institute(
        name="Demo Institute",
        logo_url="",
        theme_color="#6d28d9",
        status="active"
    )

    db.session.add(institute)
    db.session.commit()

    return jsonify({
        "message": "Demo Institute created",
        "id": institute.id
    }), 201


@app.route("/create-demo-institute-admin")
def create_demo_institute_admin():

    institute = Institute.query.filter_by(
        name="Demo Institute"
    ).first()

    if not institute:
        return jsonify({
            "error": "Create Demo Institute first"
        }), 400

    existing = InstituteAdmin.query.filter_by(
        username="demo_admin"
    ).first()

    if existing:
        return jsonify({
            "message": "Institute admin already exists"
        }), 200

    admin = InstituteAdmin(
        institute_id=institute.id,
        full_name="Demo Institute Admin",
        username="demo_admin",
        password_hash=generate_password_hash("demo@123"),
        is_active=True
    )

    db.session.add(admin)
    db.session.commit()

    return jsonify({
        "message": "Institute admin created",
        "username": "demo_admin",
        "password": "demo@123",
        "institute_id": institute.id
    }), 201


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_pyqs_json():
    try:
        with open("pyqs.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


PYQS_DATA = load_pyqs_json()


# MCQs are now stored in PostgreSQL MCQ table.
# Old JSON-based MCQ loading has been disabled.


def get_pyq_subjects():
    subjects = Subject.query.order_by(Subject.name).all()
    return [s.name for s in subjects]


def get_pyq_topics(subject):

    subject_obj = Subject.query.filter_by(
        name=subject
    ).first()

    if not subject_obj:
        return []

    topics = Topic.query.filter_by(
        subject_id=subject_obj.id
    ).order_by(Topic.name).all()

    return [t.name for t in topics]


def get_pyqs_by_subject_topic(subject, topic):

    subject_obj = Subject.query.filter_by(
        name=subject
    ).first()

    if not subject_obj:
        return []

    topic_obj = Topic.query.filter_by(
        subject_id=subject_obj.id,
        name=topic
    ).first()

    if not topic_obj:
        return []

    pyqs = PYQ.query.filter_by(
        topic_id=topic_obj.id
    ).order_by(PYQ.year).all()

    result = []

    for q in pyqs:
        result.append({
            "year": q.year,
            "question": q.question,
            "options": json.loads(q.options_json or "[]"),
            "correct_answer": q.answer,
            "explanation": q.explanation,
            "elimination_logic": q.elimination_logic
        })

    return result


def get_mcq_subjects():
    subject_ids = db.session.query(MCQ.subject_id).distinct().all()
    ids = [row[0] for row in subject_ids]

    if not ids:
        return []

    subjects = Subject.query.filter(
        Subject.id.in_(ids)
    ).order_by(Subject.name).all()

    return [s.name for s in subjects]


def get_mcq_topics(subject):

    subject_obj = Subject.query.filter_by(
        name=subject
    ).first()

    if not subject_obj:
        return []

    topic_ids = db.session.query(MCQ.topic_id).filter(
        MCQ.subject_id == subject_obj.id,
        MCQ.topic_id.isnot(None)
    ).distinct().all()

    ids = [row[0] for row in topic_ids]

    if not ids:
        return []

    topics = Topic.query.filter(
        Topic.id.in_(ids)
    ).order_by(Topic.name).all()

    return [t.name for t in topics]


def get_mcqs_by_subject_topic(subject, topic):

    subject_obj = Subject.query.filter_by(
        name=subject
    ).first()

    if not subject_obj:
        return []

    topic_obj = Topic.query.filter_by(
        subject_id=subject_obj.id,
        name=topic
    ).first()

    if not topic_obj:
        return []

    mcqs = MCQ.query.filter_by(
        subject_id=subject_obj.id,
        topic_id=topic_obj.id
    ).order_by(MCQ.id).all()

    result = []

    for q in mcqs:
        result.append({
            "difficulty": q.difficulty or "MCQ",
            "question": q.question,
            "options": json.loads(q.options_json or "[]"),
            "correct_answer": q.answer,
            "explanation": q.explanation,
            "elimination_logic": q.elimination_logic
        })

    return result


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

    best_content = None
    best_score = -1

    for raw_title, raw_content in blocks:
        title_norm = normalize_topic(raw_title)
        score = score_topic_match(topic_norm, title_norm)

        if score > best_score:
            best_score = score
            best_content = raw_content

    if not best_content:
        return "No PYQs came from this subtopic so far."

    return best_content


def trim_text_for_tts(text, max_chars=2400):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:max_chars]


def get_language_code(language):
    language = (language or "").lower()

    if language == "telugu":
        return "te-IN"

    if language == "hindi":
        return "hi-IN"

    return "en-IN"


def get_speaker(language):
    language = (language or "").lower()

    if language == "telugu":
        return "neha"

    if language == "hindi":
        return "shubh"

    return "shubh"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pyqs")
def pyqs_page():
    return render_template("pyqs.html")


@app.route("/notes")
def notes_page():
    return render_template("notes.html")


@app.route("/daily-news")
def daily_news_page():
    return render_template("dailynews.html")


@app.route("/job-alerts")
def job_alerts_page():
    return render_template("jobalerts.html")


@app.route("/monthly-magazine")
def monthly_magazine_page():
    return render_template("monthlymagazine.html")


@app.route("/mcq")
def mcq_page():
    return render_template("mcq.html")


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

    return jsonify({
        "questions": get_pyqs_by_subject_topic(subject, topic)
    })


@app.route("/mcq-subjects", methods=["GET"])
def mcq_subjects():
    return jsonify({"subjects": get_mcq_subjects()})


@app.route("/mcq-topics", methods=["GET"])
def mcq_topics():
    subject = request.args.get("subject", "").strip()
    return jsonify({"topics": get_mcq_topics(subject)})


@app.route("/mcq-questions", methods=["GET"])
def mcq_questions():
    subject = request.args.get("subject", "").strip()
    topic = request.args.get("topic", "").strip()

    return jsonify({
        "questions": get_mcqs_by_subject_topic(subject, topic)
    })

# Old JSON MCQ data route disabled.

@app.route("/fix-mcq-schema")
def fix_mcq_schema():
    try:
        db.session.execute(text("""
            ALTER TABLE mcq
            ALTER COLUMN answer TYPE TEXT
        """))
        db.session.commit()

        return jsonify({
            "message": "MCQ schema fixed"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    try:
        api_key = os.environ.get("SARVAM_API_KEY", "").strip()

        if not api_key:
            return jsonify({"error": "Sarvam API key missing"}), 500

        data = request.get_json() or {}
        text = trim_text_for_tts(data.get("text", ""))
        language = data.get("language", "english")

        if not text:
            return jsonify({"error": "No text received"}), 400

        payload = {
            "text": text,
            "target_language_code": get_language_code(language),
            "speaker": get_speaker(language),
            "model": "bulbul:v3",
            "pace": 0.9,
            "speech_sample_rate": 24000
        }

        response = requests.post(
            "https://api.sarvam.ai/text-to-speech",
            headers={
                "api-subscription-key": api_key,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Sarvam API error",
                "status": response.status_code,
                "details": response.text
            }), 500

        result = response.json()
        audios = result.get("audios", [])

        if not audios:
            return jsonify({"error": "No audio returned"}), 500

        audio_base64 = audios[0]

        return jsonify({
            "audio_url": "data:audio/wav;base64," + audio_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
