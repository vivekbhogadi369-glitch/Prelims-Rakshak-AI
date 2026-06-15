from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 7

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the Shunga dynasty, consider the following statements:

1. Pushyamitra Shunga founded the dynasty after the decline of Mauryan power.
2. The Shungas ruled immediately before the Mauryas.
3. Their political base was mainly in north India.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 1 and 3 only", "c) 2 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 1 and 3 only",
        "explanation": "Pushyamitra Shunga, a Mauryan general, founded the Shunga dynasty after the decline of Mauryan authority. The Shungas were a post-Mauryan power with their base in north India, especially around Magadha and central Gangetic regions.",
        "elimination_logic": "Statement 2 is the chronological trap. Shungas came after the Mauryas, not before them. Once statement 2 is eliminated, only option (b) remains."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following rulers is associated with the foundation of the Shunga dynasty?""",
        "options": ["a) Agnimitra", "b) Pushyamitra Shunga", "c) Vasudeva Kanva", "d) Kharavela"],
        "answer": "b) Pushyamitra Shunga",
        "explanation": "Pushyamitra Shunga founded the Shunga dynasty after overthrowing the last Mauryan ruler, Brihadratha. His reign marks the beginning of post-Mauryan political reorganisation in the Gangetic region.",
        "elimination_logic": "Agnimitra was a later Shunga ruler. Vasudeva Kanva founded the Kanva dynasty. Kharavela was associated with Kalinga. Hence Pushyamitra Shunga is correct."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Person/Dynasty — Association

1. Pushyamitra Shunga — Post-Mauryan ruler
2. Agnimitra — Malavikagnimitram
3. Vasudeva Kanva — Kanva dynasty

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Pushyamitra Shunga was a post-Mauryan ruler. Agnimitra is known from Kalidasa’s Malavikagnimitram. Vasudeva Kanva is associated with the foundation of the Kanva dynasty after the Shungas.",
        "elimination_logic": "All three pairs are correct. The trap is to confuse Vasudeva Kanva with a Shunga ruler or to ignore literary evidence related to Agnimitra."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to the Shunga period, consider the following statements:

1. It witnessed continuation and development of art at sites such as Bharhut and Sanchi.
2. All Buddhist monuments were destroyed during Shunga rule.
3. The period followed the decline of Mauryan imperial unity.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 1 and 3 only", "c) 2 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 1 and 3 only",
        "explanation": "The Shunga period saw important artistic activity at Bharhut and Sanchi. Although Pushyamitra is sometimes represented in Buddhist texts as hostile to Buddhism, archaeological evidence shows continued Buddhist artistic patronage and monument development.",
        "elimination_logic": "Statement 2 is an extreme statement. The word 'all' makes it historically unsafe. Buddhist monuments did not disappear; Bharhut and Sanchi developed significantly. Statements 1 and 3 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): The Shunga period should not be understood simply as a complete break from Mauryan traditions.

Reason (R): Some administrative, artistic and regional political continuities survived even after the decline of Mauryan central authority.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "The Shunga period represents both political change and continuity. Mauryan imperial unity declined, but regional administration, artistic traditions and older cultural networks did not vanish suddenly.",
        "elimination_logic": "Both assertion and reason are historically sound. The reason directly explains why the Shunga period should be viewed as transition rather than total rupture."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following statements regarding Pushyamitra Shunga is/are correct?

1. He performed Ashvamedha sacrifices.
2. He was associated with revival of Brahmanical ritual authority.
3. He issued Ashokan-style Dhamma edicts across the empire.

Select the correct answer using the code below.""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Pushyamitra Shunga is traditionally associated with the performance of Ashvamedha sacrifices and a revival of Brahmanical ritual practices. However, Ashokan-style Dhamma edicts belong to Ashoka, not Pushyamitra.",
        "elimination_logic": "Statement 3 is a direct ruler-period mismatch. Dhamma edicts are Mauryan-Ashokan, not Shunga. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements about Bharhut and Sanchi during the post-Mauryan period:

1. They show development of Buddhist narrative art.
2. They indicate that Buddhist artistic activity continued after the Mauryas.
3. They were exclusively royal projects of Ashoka and saw no later additions.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Bharhut and Sanchi are important for Buddhist narrative reliefs and artistic developments. Their continued development in the post-Mauryan period shows that Buddhist patronage was not limited to Ashoka alone.",
        "elimination_logic": "Statement 3 is incorrect because these monuments saw later additions and patronage. The trap is to assume Buddhist monuments are only Ashokan in origin and development."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to the political context of the Shungas and Kanvas, consider the following statements:

1. The Shungas emerged after the weakening of Mauryan central power.
2. The Kanvas succeeded the Shungas.
3. The Kanvas created a pan-Indian empire larger than the Mauryan Empire.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Shungas emerged in the post-Mauryan context, and the Kanvas succeeded them. The Kanvas were a relatively short-lived dynasty and did not create a pan-Indian empire larger than the Mauryas.",
        "elimination_logic": "Statement 3 is historically exaggerated. The Kanvas were not imperial on a Mauryan scale. Statements 1 and 2 correctly establish the political sequence."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following in correct chronological order:

1. Rule of the Kanvas
2. Decline of Mauryan Empire
3. Rule of Pushyamitra Shunga
4. Rise of Satavahanas as an important Deccan power

Select the correct answer.""",
        "options": ["a) 2-3-1-4", "b) 3-2-1-4", "c) 2-1-3-4", "d) 1-2-3-4"],
        "answer": "a) 2-3-1-4",
        "explanation": "The Mauryan Empire declined first, followed by the rise of Pushyamitra Shunga. The Kanvas succeeded the Shungas. The Satavahanas became an important Deccan power in the broader post-Mauryan political landscape.",
        "elimination_logic": "Mauryan decline must come before Shunga rule. Kanvas must come after Shungas. Therefore, 2-3-1-4 is the only correct sequence."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements regarding the historical interpretation of the Shunga period:

1. It is often associated with Brahmanical revival.
2. Archaeological evidence suggests continued Buddhist artistic activity.
3. The period witnessed the complete disappearance of regional political powers.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Shunga period is associated with Brahmanical ritual revival, but this did not mean the disappearance of Buddhist art. Bharhut and Sanchi show continued Buddhist activity. The period also saw regional powers emerging rather than disappearing.",
        "elimination_logic": "Statement 3 is the overstatement. Post-Mauryan India saw regionalisation of power, not disappearance of regional polities. Statements 1 and 2 capture the balanced historical interpretation."
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
    print("Inserted Shungas and Kanwas MCQs:", len(questions))
