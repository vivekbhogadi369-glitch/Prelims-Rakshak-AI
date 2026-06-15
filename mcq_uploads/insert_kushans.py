from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 102

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the Kushans, consider the following statements:

1. They were connected with the Yuezhi tribal movement from Central Asia.
2. Kanishka was one of their most important rulers.
3. Their political influence was confined only to peninsular India.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Kushans emerged from the Yuezhi groups that moved from Central Asia. Kanishka was their most famous ruler. Their power extended across north-western India, the Gangetic region and Central Asian zones, not peninsular India alone.",
        "elimination_logic": "Statement 3 is geographically wrong and intentionally restrictive. Kushan power was trans-regional, linking Central Asia and northern India. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following rulers is most closely associated with the Fourth Buddhist Council held in Kashmir according to traditional accounts?""",
        "options": ["a) Menander", "b) Kanishka", "c) Rudradaman I", "d) Pushyamitra Shunga"],
        "answer": "b) Kanishka",
        "explanation": "Kanishka is traditionally associated with the Fourth Buddhist Council in Kashmir, which is linked with the development of Sarvastivada scholastic traditions and Mahayana Buddhism.",
        "elimination_logic": "Menander was Indo-Greek, Rudradaman was a Western Kshatrapa, and Pushyamitra was Shunga. Kanishka alone fits the Kushan-Buddhist Council context."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Kushan feature — Historical significance

1. Kanishka — Patronage of Buddhism
2. Gold coins — Evidence of flourishing trade
3. Gandhara art — Greco-Roman and Indian artistic interaction

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Kanishka is known for Buddhist patronage. Kushan gold coins indicate prosperity and long-distance trade. Gandhara art reflects interaction between Hellenistic, Roman, Iranian and Indian traditions.",
        "elimination_logic": "All three associations are correct. The question tests whether the candidate can link political patronage, economic prosperity and artistic synthesis under the Kushans."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to Kushan coinage, consider the following statements:

1. Kushan coins carried images of rulers and deities.
2. They included deities from different religious traditions.
3. They provide no evidence for cultural interaction.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Kushan coins carried royal portraits and deities from Greek, Iranian and Indian traditions. They are important evidence for religious pluralism, royal ideology and cultural interaction.",
        "elimination_logic": "Statement 3 is incorrect because Kushan coinage is one of the strongest sources for cultural interaction. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): The Kushan Empire played an important role in trans-regional trade.

Reason (R): It controlled regions linking Central Asia, north-western India and routes connected with the Silk Road.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "The Kushan Empire occupied a strategic position between Central Asia, the Indian subcontinent and long-distance trade routes. This helped the movement of goods, coins, ideas, religions and artistic styles.",
        "elimination_logic": "Both assertion and reason are correct. The reason explains why Kushans were important for long-distance trade and cultural transmission."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following are associated with the Kushan period?

1. Expansion of Gandhara and Mathura schools of art
2. Prominence of Mahayana Buddhism
3. Long-distance trade with Central Asia and Roman world
4. Complete disappearance of coinage-based economy

Select the correct answer using the code below.""",
        "options": ["a) 1, 2 and 3 only", "b) 2 and 4 only", "c) 1 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "a) 1, 2 and 3 only",
        "explanation": "The Kushan period saw the growth of Gandhara and Mathura art, Mahayana Buddhism, and flourishing trade links. Coinage was highly developed, especially gold coinage.",
        "elimination_logic": "Statement 4 is the opposite of historical evidence. Kushan coinage was extensive and sophisticated. Therefore options containing 4 are eliminated."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements regarding Kanishka:

1. He issued inscriptions and coins that help reconstruct Kushan history.
2. He patronised Buddhism but Kushan religious life was not exclusively Buddhist.
3. He ruled before Chandragupta Maurya.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Kanishka is known through inscriptions, coins and Buddhist traditions. He patronised Buddhism, but Kushan coinage shows religious plurality. He was a post-Mauryan ruler, not earlier than Chandragupta Maurya.",
        "elimination_logic": "Statement 3 is a chronological trap. Kanishka belongs to the early centuries CE, long after Chandragupta Maurya. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to Gandhara and Mathura schools during the Kushan period, consider the following statements:

1. Gandhara art shows strong Greco-Roman influence.
2. Mathura art developed mainly using indigenous artistic traditions.
3. Both schools contributed to the development of Buddha images.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Gandhara art reflected Greco-Roman influence in drapery, anatomy and style, while Mathura art developed from indigenous traditions using red sandstone. Both schools were important in the emergence and spread of anthropomorphic Buddha images.",
        "elimination_logic": "No statement is incorrect. The trap is to assume only Gandhara contributed to Buddha images; Mathura was equally important in early Buddha iconography."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following broad political developments in chronological order:

1. Mauryan decline
2. Indo-Greek presence in north-western India
3. Saka rule in western India
4. Kushan prominence under Kanishka

Select the correct answer.""",
        "options": ["a) 1-2-3-4", "b) 2-1-4-3", "c) 1-3-2-4", "d) 3-1-2-4"],
        "answer": "a) 1-2-3-4",
        "explanation": "After Mauryan decline, Indo-Greeks appeared in north-western India. Sakas followed as another important post-Mauryan power, and Kushan prominence under Kanishka came later.",
        "elimination_logic": "Mauryan decline must come first. Kushan prominence under Kanishka comes after Indo-Greeks and Sakas in the broad sequence. Hence 1-2-3-4 is correct."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements about the significance of the Kushans:

1. They facilitated movement of Buddhism towards Central Asia.
2. Their empire connected Indian, Iranian and Central Asian cultural zones.
3. Their rule caused the immediate decline of all urban trade networks.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Kushans helped connect the Indian subcontinent with Central Asia and facilitated the spread of Buddhism along trade routes. Their rule supported urban and commercial networks rather than causing their immediate decline.",
        "elimination_logic": "Statement 3 is historically incorrect. Kushan rule is linked with trade prosperity, not immediate collapse of urban trade. Statements 1 and 2 are correct."
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
    print("Inserted Kushans MCQs:", len(questions))
