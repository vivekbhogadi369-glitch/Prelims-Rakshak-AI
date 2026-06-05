import os
import json
from app import db, app, Subject, Topic, PYQ


def load_pyqs():
    with open("pyqs.json", "r", encoding="utf-8") as f:
        return json.load(f)


def migrate_pyqs():
    data = load_pyqs()
    imported = 0
    skipped = 0

    with app.app_context():
        for subject_name, topics in data.items():

            subject = Subject.query.filter_by(name=subject_name).first()
            if not subject:
                subject = Subject(name=subject_name)
                db.session.add(subject)
                db.session.commit()

            for topic_name, questions in topics.items():

                topic = Topic.query.filter_by(
                    subject_id=subject.id,
                    name=topic_name
                ).first()

                if not topic:
                    topic = Topic(
                        subject_id=subject.id,
                        name=topic_name
                    )
                    db.session.add(topic)
                    db.session.commit()

                for q in questions:
                    question_text = q.get("question", "").strip()

                    if not question_text:
                        skipped += 1
                        continue

                    existing = PYQ.query.filter_by(
                        subject_id=subject.id,
                        topic_id=topic.id,
                        year=q.get("year"),
                        question=question_text
                    ).first()

                    if existing:
                        skipped += 1
                        continue

                    pyq = PYQ(
                        subject_id=subject.id,
                        topic_id=topic.id,
                        year=q.get("year"),
                        question=question_text,
                        options_json=json.dumps(q.get("options", []), ensure_ascii=False),
                        answer=q.get("correct_answer"),
                        explanation=q.get("explanation"),
                        elimination_logic=q.get("elimination_logic")
                    )

                    db.session.add(pyq)
                    imported += 1

                    if imported % 50 == 0:
                        db.session.commit()
                        print(f"Imported {imported} PYQs...")

        db.session.commit()

    print("Migration completed")
    print(f"Imported: {imported}")
    print(f"Skipped: {skipped}")


if __name__ == "__main__":
    migrate_pyqs()
