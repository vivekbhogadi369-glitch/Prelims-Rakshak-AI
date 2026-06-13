from app import app, db, MCQ
import json

with app.app_context():

    questions = [
        {
            "question": "Which one of the following characteristics is most closely associated with the Mesolithic phase in the Indian subcontinent?",
            "options": [
                "a) Extensive use of polished stone axes",
                "b) Emergence of microlithic tools and semi-sedentary life",
                "c) Widespread use of iron implements",
                "d) Construction of planned urban settlements"
            ],
            "answer": "b",
            "explanation": "Microlithic tools and gradual transition towards semi-sedentary life are important features of the Mesolithic phase.",
            "elimination_logic": "Polished stone axes belong to the Neolithic period, iron implements to the Iron Age, and planned urban settlements to the Harappan civilisation."
        },

        {
            "question": "Which of the following sites is best known for pit dwellings during the Neolithic phase?",
            "options": [
                "a) Burzahom",
                "b) Hallur",
                "c) Chirand",
                "d) Daojali Hading"
            ],
            "answer": "a",
            "explanation": "Burzahom in Kashmir is famous for its pit dwellings.",
            "elimination_logic": "Hallur is associated with South Indian Neolithic culture, Chirand with Bihar Neolithic, and Daojali Hading with Northeast India."
        },

        {
            "question": "Consider the following statements regarding prehistoric rock art: 1. Bhimbetka contains evidence of prehistoric paintings. 2. Most paintings depict hunting scenes. Which of the statements given above is/are correct?",
            "options": [
                "a) 1 only",
                "b) 2 only",
                "c) Both 1 and 2",
                "d) Neither 1 nor 2"
            ],
            "answer": "c",
            "explanation": "Bhimbetka contains rich rock art traditions, many depicting hunting and daily life.",
            "elimination_logic": "Both statements are factually correct."
        },

        {
            "question": "Match the following: Site — Associated feature: 1. Mehrgarh — Early farming 2. Burzahom — Pit dwellings 3. Hallur — South Indian Neolithic. Which of the pairs given above are correctly matched?",
            "options": [
                "a) 1 and 2 only",
                "b) 2 and 3 only",
                "c) 1 and 3 only",
                "d) 1, 2 and 3"
            ],
            "answer": "d",
            "explanation": "All three site-feature associations are correct.",
            "elimination_logic": "These are standard prehistoric site associations asked repeatedly in UPSC."
        },

        {
            "question": "Assertion (A): The Neolithic phase represents a major turning point in human history. Reason (R): It witnessed the beginnings of food production and settled life.",
            "options": [
                "a) Both A and R are true and R is the correct explanation",
                "b) Both A and R are true but R is not the correct explanation",
                "c) A is true but R is false",
                "d) A is false but R is true"
            ],
            "answer": "a",
            "explanation": "Food production and settled life fundamentally transformed human societies.",
            "elimination_logic": "The reason directly explains why the Neolithic Revolution is considered a turning point."
        },

        {
            "question": "Which one of the following prehistoric sites is associated with the earliest evidence of rice cultivation in the Indian subcontinent?",
            "options": [
                "a) Mehrgarh",
                "b) Koldihwa",
                "c) Burzahom",
                "d) Hallur"
            ],
            "answer": "b",
            "explanation": "Koldihwa in Uttar Pradesh has yielded evidence of early rice cultivation.",
            "elimination_logic": "Mehrgarh is associated with early farming in Baluchistan, Burzahom with pit dwellings, and Hallur with South Indian Neolithic culture."
        }
    ]

    for item in questions:
        db.session.add(
            MCQ(
                subject_id=1,
                topic_id=99,
                difficulty="Medium",
                question=item["question"],
                options_json=json.dumps(item["options"]),
                answer=item["answer"],
                explanation=item["explanation"],
                elimination_logic=item["elimination_logic"]
            )
        )

    db.session.commit()

    print("Inserted:", len(questions))
