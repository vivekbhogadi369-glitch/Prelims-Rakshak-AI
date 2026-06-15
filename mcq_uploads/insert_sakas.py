from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 101

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the Sakas in ancient India, consider the following statements:

1. They were of Central Asian origin.
2. They established political power in parts of north-western and western India.
3. Their rule began before the Mauryan Empire.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Sakas were of Central Asian origin and entered India in the post-Mauryan period. They established power in regions such as north-western India, Malwa, Gujarat and western India. Their rule did not begin before the Mauryan Empire.",
        "elimination_logic": "Statement 3 is a chronological trap. The Sakas were post-Mauryan, not pre-Mauryan. Statements 1 and 2 correctly describe their origin and political spread."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following Saka rulers is best known for the Junagadh inscription?""",
        "options": ["a) Rudradaman I", "b) Kanishka", "c) Menander", "d) Pushyamitra Shunga"],
        "answer": "a) Rudradaman I",
        "explanation": "Rudradaman I, a Western Kshatrapa ruler, is associated with the Junagadh inscription. The inscription is important for its Sanskrit prose and for information on the repair of the Sudarshana lake.",
        "elimination_logic": "Kanishka was a Kushana ruler, Menander was Indo-Greek, and Pushyamitra was Shunga. The Junagadh inscription is specifically linked with Rudradaman I."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Ruler/Dynasty — Association

1. Rudradaman I — Western Kshatrapas
2. Menander — Indo-Greeks
3. Kanishka — Kushanas

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Rudradaman I belonged to the Western Kshatrapas, Menander was an Indo-Greek ruler, and Kanishka was a Kushana ruler. These three represent different post-Mauryan political powers in north-western and western India.",
        "elimination_logic": "All three pairs are correctly matched. The question tests whether the candidate can distinguish overlapping post-Mauryan powers rather than mixing all foreign-origin dynasties together."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to the Western Kshatrapas, consider the following statements:

1. They ruled parts of western India.
2. They came into conflict with the Satavahanas.
3. They were the immediate predecessors of the Mauryas.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Western Kshatrapas ruled regions such as Malwa, Gujarat and western India. They had prolonged conflicts with the Satavahanas. They were post-Mauryan rulers, not immediate predecessors of the Mauryas.",
        "elimination_logic": "Statement 3 is historically impossible. The Mauryas came earlier, while Western Kshatrapas were post-Mauryan. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): The Junagadh inscription of Rudradaman I is important for the history of early Sanskrit inscriptions.

Reason (R): It is one of the earliest long inscriptions composed in polished Sanskrit prose.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "The Junagadh inscription of Rudradaman I is historically significant because it is among the earliest major inscriptions in classical Sanskrit prose. It also records the repair of the Sudarshana lake and gives political information about Rudradaman.",
        "elimination_logic": "Both the assertion and reason are correct. The reason directly explains the importance of the inscription in epigraphic and linguistic history."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following statements regarding post-Mauryan foreign-origin powers in India is/are correct?

1. The Sakas, Parthians and Kushanas entered through north-western routes.
2. These groups remained completely outside Indian cultural traditions.
3. Their rule contributed to cultural and artistic interactions.

Select the correct answer using the code below.""",
        "options": ["a) 1 and 2 only", "b) 1 and 3 only", "c) 2 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 1 and 3 only",
        "explanation": "Sakas, Parthians and Kushanas entered through north-western routes and established power in different regions. Over time, they interacted with Indian religious, artistic and administrative traditions rather than remaining completely outside them.",
        "elimination_logic": "Statement 2 is an absolute and incorrect claim. These groups were gradually Indianised and contributed to cultural synthesis. Statements 1 and 3 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements about Saka political titles:

1. The title Kshatrapa was used by Saka rulers.
2. Mahakshatrapa indicated a higher political status than Kshatrapa.
3. The title Kshatrapa was first used only by Gupta emperors.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Saka rulers used titles such as Kshatrapa and Mahakshatrapa. Mahakshatrapa denoted a higher or superior status. These titles were not first used only by Gupta emperors.",
        "elimination_logic": "Statement 3 is incorrect because Kshatrapa is strongly associated with Saka/Western Kshatrapa political terminology. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following post-Mauryan powers broadly in the order of their prominence in north-western/western India:

1. Indo-Greeks
2. Sakas
3. Kushanas
4. Western Kshatrapas

Select the correct answer.""",
        "options": ["a) 1-2-3-4", "b) 2-1-4-3", "c) 1-3-2-4", "d) 3-1-2-4"],
        "answer": "a) 1-2-3-4",
        "explanation": "After the decline of Mauryan power, Indo-Greeks appeared in the north-west, followed by Sakas and then Kushanas. Western Kshatrapas continued as an important Saka line in western India.",
        "elimination_logic": "Indo-Greeks should precede Sakas in the broad sequence. Kushanas rose after Sakas in north-western India. Western Kshatrapas are later and regionally important in western India."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to Rudradaman I, consider the following statements:

1. He was associated with the Western Kshatrapas.
2. His inscription mentions the repair of the Sudarshana lake.
3. He was a Mauryan emperor who issued edicts on Dhamma.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Rudradaman I was a Western Kshatrapa ruler. His Junagadh inscription records the repair of the Sudarshana lake. He was not a Mauryan emperor and did not issue Ashokan-style Dhamma edicts.",
        "elimination_logic": "Statement 3 deliberately mixes Rudradaman with Ashoka. Rudradaman belongs to the post-Mauryan Saka/Western Kshatrapa context, while Dhamma edicts belong to Ashoka."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements about the historical significance of the Sakas:

1. They contributed to political changes in post-Mauryan western India.
2. Their coinage and inscriptions help reconstruct regional history.
3. Their arrival caused the immediate disappearance of all existing Indian polities.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Sakas played an important role in post-Mauryan western India. Their coins and inscriptions, especially those of the Western Kshatrapas, are important sources for political chronology and regional history. Existing Indian polities did not disappear immediately; there were conflicts, accommodations and cultural interactions.",
        "elimination_logic": "Statement 3 is an exaggerated and historically inaccurate claim. Political change was gradual and regionally varied, not an immediate total disappearance of all earlier polities."
    }
]

with app.app_context():
    MCQ.query.filter_by(subject_id=SUBJECT_ID, topic_id=TOPIC_ID).delete()

    for item in questions:
        db.session.add(MCQ(
            subject_id=SUBJECT_ID,
            topic_id=TOPIC_ID,
            difficulty=item["difficulty"],
            question=item["question"],
            options_json=json.dumps(item["options"]),
            answer=item["answer"],
            explanation=item["explanation"],
            elimination_logic=item["elimination_logic"]
        ))

    db.session.commit()
    print("Inserted Sakas MCQs:", len(questions))
