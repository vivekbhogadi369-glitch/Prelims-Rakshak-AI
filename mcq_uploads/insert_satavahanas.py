from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 8

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the Satavahanas, consider the following statements:

1. They emerged as an important power in the Deccan after the decline of Mauryan authority.
2. Their rule was confined only to the Gangetic plains.
3. They issued coins which help in reconstructing their political history.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 1 and 3 only", "c) 2 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 1 and 3 only",
        "explanation": "The Satavahanas rose as a major Deccan power in the post-Mauryan period. Their coins, inscriptions and donations are important sources for reconstructing their chronology, political authority and economic networks.",
        "elimination_logic": "Statement 2 is geographically incorrect. The Satavahanas were primarily associated with the Deccan, not only the Gangetic plains. Statements 1 and 3 are correct."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following rulers is most closely associated with the restoration of Satavahana power after conflicts with the Western Kshatrapas?""",
        "options": ["a) Gautamiputra Satakarni", "b) Pushyamitra Shunga", "c) Menander", "d) Kanishka"],
        "answer": "a) Gautamiputra Satakarni",
        "explanation": "Gautamiputra Satakarni is regarded as one of the greatest Satavahana rulers. He is credited with defeating the Shakas, Yavanas and Pahlavas and restoring Satavahana prestige.",
        "elimination_logic": "Pushyamitra was a Shunga ruler, Menander was Indo-Greek, and Kanishka was Kushan. Gautamiputra Satakarni alone fits the Satavahana-Western Kshatrapa context."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Satavahana source/feature — Historical significance

1. Nasik inscription of Gautami Balashri — Information on Gautamiputra Satakarni
2. Lead coins — Important Satavahana coinage feature
3. Prakrit inscriptions — Evidence of administrative and religious patronage

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "The Nasik inscription of Gautami Balashri gives valuable information about Gautamiputra Satakarni. Satavahana coinage includes lead coins, especially in the Deccan. Their Prakrit inscriptions record donations, political claims and religious patronage.",
        "elimination_logic": "All three pairs are correct. The question tests whether the candidate can connect epigraphy, numismatics and political history rather than treating Satavahana sources separately."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to Satavahana polity, consider the following statements:

1. Matronymics were used by several Satavahana rulers.
2. The use of titles and inscriptions helped project royal authority.
3. Satavahana rulers completely rejected Brahmanical social ideals.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Several Satavahana rulers used matronymics, such as Gautamiputra and Vasisthiputra. Inscriptions and royal titles projected political legitimacy. Satavahanas supported Brahmanical ideals while also patronising Buddhist establishments.",
        "elimination_logic": "Statement 3 is too absolute and incorrect. Satavahana rulers did not completely reject Brahmanical ideals; they participated in Brahmanical social and ritual frameworks while also extending religious patronage more broadly."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): The Satavahanas played an important role in Deccan trade networks.

Reason (R): Their territories connected inland production zones with western coastal ports involved in long-distance trade.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "Satavahana territories linked the Deccan plateau with western coastal ports. This helped movement of goods such as textiles, beads, metals and agricultural products in both inland and overseas trade.",
        "elimination_logic": "Both statements are correct. The reason directly explains Satavahana economic significance by connecting geography, inland routes and maritime trade."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following are associated with the Satavahana period?

1. Patronage to Buddhist caves and monasteries
2. Use of Prakrit in inscriptions
3. Conflicts with Western Kshatrapas
4. Complete absence of coinage

Select the correct answer using the code below.""",
        "options": ["a) 1, 2 and 3 only", "b) 2 and 4 only", "c) 1 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "a) 1, 2 and 3 only",
        "explanation": "The Satavahana period saw patronage to Buddhist establishments such as caves and monasteries, extensive Prakrit inscriptions, and conflicts with Western Kshatrapas. Coinage was present and is an important historical source.",
        "elimination_logic": "Statement 4 is directly opposite to evidence. Satavahana coins are important for reconstructing political and economic history. Therefore, options containing 4 are eliminated."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements regarding Satavahana society and religion:

1. Satavahana rulers claimed Brahmanical affiliations.
2. Buddhist institutions received donations during the Satavahana period.
3. Religious patronage was completely limited to one sect.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Satavahana rulers often claimed Brahmanical status and supported Brahmanical rituals. At the same time, Buddhist caves and monasteries received donations from rulers, officials, merchants and lay donors.",
        "elimination_logic": "Statement 3 is incorrect because religious patronage was not confined to a single sect. Satavahana society shows overlapping Brahmanical and Buddhist patronage networks."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to the Satavahana-Western Kshatrapa conflict, consider the following statements:

1. Control over western India and trade routes was an important factor.
2. Gautamiputra Satakarni claimed victory over Shakas, Yavanas and Pahlavas.
3. These conflicts had no economic significance and were purely ritual contests.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Satavahana-Western Kshatrapa conflict was linked to control over western India, trade routes and political prestige. Gautamiputra Satakarni’s claims against Shakas, Yavanas and Pahlavas are known from inscriptions.",
        "elimination_logic": "Statement 3 is wrong because the conflict had clear territorial and economic dimensions. Statements 1 and 2 correctly explain the political economy of the conflict."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following broad developments in chronological order:

1. Decline of Mauryan authority
2. Rise of Satavahanas in the Deccan
3. Prominence of Gautamiputra Satakarni
4. Later conflicts and interactions with Western Kshatrapas

Select the correct answer.""",
        "options": ["a) 1-2-3-4", "b) 2-1-4-3", "c) 1-3-2-4", "d) 3-1-2-4"],
        "answer": "a) 1-2-3-4",
        "explanation": "After Mauryan decline, regional powers such as the Satavahanas emerged. Gautamiputra Satakarni marks a major phase of Satavahana power. Later political interaction and conflict with Western Kshatrapas continued in western India and the Deccan.",
        "elimination_logic": "Mauryan decline must come first. Gautamiputra cannot precede the rise of Satavahana power. Hence 1-2-3-4 is the correct broad sequence."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements about the historical importance of Satavahana inscriptions:

1. They help reconstruct genealogy and political claims.
2. They provide evidence of donations to religious establishments.
3. They are irrelevant for understanding social identities such as matronymics.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Satavahana inscriptions provide genealogical information, political titles, claims of conquest and evidence of donations. They also reveal social features such as matronymics and patterns of patronage.",
        "elimination_logic": "Statement 3 is incorrect because inscriptions are crucial for understanding matronymics and social identity. Statements 1 and 2 are correct."
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
    print("Inserted Satavahanas MCQs:", len(questions))
