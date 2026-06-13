from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 7

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the Indo-Greeks, consider the following statements:

1. They entered north-western India after the decline of Mauryan power.
2. Menander is one of the best-known Indo-Greek rulers.
3. Indo-Greek rule was centred mainly in the deep south of India.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Indo-Greeks emerged in north-western India after the weakening of Mauryan authority and the expansion of Greco-Bactrian power. Menander or Milinda is one of the most prominent Indo-Greek rulers.",
        "elimination_logic": "Statement 3 is geographically incorrect. Indo-Greek power was concentrated in north-western India and adjoining regions, not deep south India. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following texts records the dialogue between King Milinda and the Buddhist monk Nagasena?""",
        "options": ["a) Milindapanho", "b) Dipavamsa", "c) Arthashastra", "d) Rajatarangini"],
        "answer": "a) Milindapanho",
        "explanation": "Milindapanho records the philosophical dialogue between Indo-Greek ruler Menander, known as Milinda, and the Buddhist monk Nagasena.",
        "elimination_logic": "Dipavamsa is a Sri Lankan Buddhist chronicle. Arthashastra deals with polity and economy. Rajatarangini is a history of Kashmir. Milindapanho alone fits the context."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Indo-Greek feature — Historical significance

1. Bilingual coins — Interaction between Greek and Indian traditions
2. Portrait coins — Advancement in numismatic art
3. Milindapanho — Evidence of Buddhist intellectual engagement

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Indo-Greek coins often carried Greek and Prakrit/Kharosthi legends, reflecting cultural interaction. Their portrait coins show high numismatic skill. Milindapanho reflects Buddhist philosophical engagement with Menander.",
        "elimination_logic": "All three pairs are correctly matched. The question tests whether political, numismatic and religious evidence are understood together rather than in isolation."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to Indo-Greek coins, consider the following statements:

1. They often carried images of rulers.
2. They sometimes used Greek on one side and Prakrit in Kharosthi script on the other.
3. They provide no evidence for political authority or religious symbols.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Indo-Greek coins are valuable sources because they show ruler portraits, titles, bilingual legends and religious symbols. They help reconstruct political authority and cultural interaction.",
        "elimination_logic": "Statement 3 is incorrect because Indo-Greek coins are among the strongest sources for political, religious and cultural information. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): Indo-Greek rule contributed to cultural interaction in north-western India.

Reason (R): Their coinage, art forms and religious contacts show a blending of Hellenistic and Indian elements.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "Indo-Greek rule was important not merely politically but culturally. Their coins, artistic vocabulary and interaction with Buddhism indicate a fusion of Greek and Indian elements in the north-west.",
        "elimination_logic": "Both statements are correct. The reason directly explains the assertion by giving concrete evidence of cultural interaction."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following are associated with Indo-Greek influence in ancient India?

1. Development of high-quality portrait coinage
2. Interaction with Buddhism
3. Contribution to Gandhara artistic traditions
4. Introduction of Persian cuneiform inscriptions in India

Select the correct answer using the code below.""",
        "options": ["a) 1, 2 and 3 only", "b) 2 and 4 only", "c) 1 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "a) 1, 2 and 3 only",
        "explanation": "Indo-Greeks are associated with portrait coins, Buddhist interactions represented by Menander, and the broader Hellenistic influence that helped shape Gandhara art. Persian cuneiform inscriptions are not an Indo-Greek contribution.",
        "elimination_logic": "Statement 4 is the trap. Persian cuneiform belongs to Achaemenid traditions, not Indo-Greek cultural influence. Therefore options containing 4 are eliminated."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements regarding Menander:

1. He is identified with Milinda of Milindapanho.
2. He is associated with Buddhist philosophical discussions.
3. His rule was confined only to the Tamil region.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Menander is identified with Milinda and is associated with dialogue with Nagasena in Milindapanho. His sphere was in north-western India and adjoining regions, not the Tamil region.",
        "elimination_logic": "Statement 3 is geographically wrong and deliberately extreme. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to the political history of north-western India after the Mauryas, consider the following statements:

1. Indo-Greek power was linked to developments in Bactria.
2. North-western India became a zone of interaction among Greeks, Shakas, Parthians and Kushanas.
3. Indo-Greek rule produced a politically unified empire over the whole subcontinent.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Indo-Greek expansion was connected with Greco-Bactrian politics. After the Mauryas, north-western India saw overlapping and successive powers including Indo-Greeks, Shakas, Parthians and Kushanas. Indo-Greeks did not unify the whole subcontinent.",
        "elimination_logic": "Statement 3 is an exaggeration. Indo-Greek power was regional, not pan-Indian. Statements 1 and 2 correctly describe the geopolitical context."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following broad political developments in chronological order:

1. Mauryan decline
2. Indo-Greek penetration into north-western India
3. Rise of Kushana power
4. Prominence of Menander

Select the correct answer.""",
        "options": ["a) 1-2-4-3", "b) 2-1-4-3", "c) 1-3-2-4", "d) 4-1-2-3"],
        "answer": "a) 1-2-4-3",
        "explanation": "The weakening of Mauryan power created space in the north-west. Indo-Greek penetration followed, with Menander becoming one of the most prominent Indo-Greek rulers. Kushana power rose later.",
        "elimination_logic": "Mauryan decline must precede Indo-Greek expansion in India. Menander belongs within the Indo-Greek phase. Kushanas are later than Indo-Greek prominence."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements about Indo-Greek cultural impact:

1. Their coins help in reconstructing dynastic succession where literary evidence is limited.
2. Hellenistic artistic elements contributed to later Gandhara sculptural traditions.
3. Indo-Greek influence led to the immediate disappearance of all indigenous artistic traditions.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Indo-Greek coins are crucial for reconstructing rulers and chronology. Hellenistic features contributed to Gandhara art. However, Indo-Greek influence did not erase indigenous artistic traditions; cultural forms interacted and coexisted.",
        "elimination_logic": "Statement 3 is an absolute and historically wrong claim. Cultural contact led to fusion and adaptation, not complete disappearance of indigenous traditions. Statements 1 and 2 are correct."
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
    print("Inserted Indo-Greeks MCQs:", len(questions))
