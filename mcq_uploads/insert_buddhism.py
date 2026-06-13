from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 3

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the basic teachings of Buddhism, consider the following statements:

1. Suffering is central to human existence.
2. Desire is identified as a cause of suffering.
3. Liberation is possible through the Eightfold Path.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "The Four Noble Truths explain suffering, its cause, its cessation and the path to cessation. Desire or craving is identified as the cause of suffering, and the Eightfold Path is prescribed as the way to liberation.",
        "elimination_logic": "All three statements are foundational Buddhist doctrines. There is no doctrinal mismatch. Hence all are correct."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following events is associated with Sarnath in the life of the Buddha?""",
        "options": ["a) Birth", "b) Enlightenment", "c) First sermon", "d) Mahaparinirvana"],
        "answer": "c) First sermon",
        "explanation": "After attaining enlightenment at Bodh Gaya, the Buddha delivered his first sermon at Sarnath. This event is known as Dharmachakra Pravartana.",
        "elimination_logic": "Birth is associated with Lumbini, enlightenment with Bodh Gaya, and Mahaparinirvana with Kushinagar. Sarnath is specifically linked with the first sermon."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Place — Association with Buddha

1. Lumbini — Birth
2. Bodh Gaya — Enlightenment
3. Kushinagar — Mahaparinirvana

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Lumbini is associated with the birth of Buddha, Bodh Gaya with enlightenment under the Bodhi tree, and Kushinagar with Mahaparinirvana.",
        "elimination_logic": "All three are standard life-event associations. No pair is incorrectly matched."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to Buddhist Councils, consider the following statements:

1. The First Buddhist Council was held at Rajagriha.
2. The Second Buddhist Council was held at Vaishali.
3. The Fourth Buddhist Council under Kanishka is associated with Kashmir.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "The First Council was held at Rajagriha after Buddha’s death. The Second was held at Vaishali. The Fourth Council under Kanishka is generally associated with Kashmir and the development of Sarvastivada scholastic traditions.",
        "elimination_logic": "The trap is confusion between council locations. Rajagriha, Vaishali and Kashmir are correctly matched with the First, Second and Fourth Councils respectively."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): Buddhism gained popularity among merchants and urban groups.

Reason (R): Buddhism did not strongly depend on costly sacrificial rituals and accepted donations from lay followers.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "Buddhism appealed to merchants, artisans and urban groups because it offered an ethical path without dependence on elaborate Vedic sacrifices. Monasteries also developed links with trade routes and received patronage from lay supporters.",
        "elimination_logic": "Both statements are historically valid. The reason directly explains Buddhist appeal among non-ritual and commercial groups. Hence option (a) is correct."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following features are associated with early Buddhism?

1. Rejection of the authority of the Vedas
2. Emphasis on ethical conduct
3. Acceptance of a permanent individual soul as central doctrine

Select the correct answer using the code below.""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Early Buddhism rejected Vedic ritual authority and emphasised ethical conduct, right action and mental discipline. It did not accept a permanent individual soul as a central doctrine; the doctrine of anatta or non-self is important.",
        "elimination_logic": "Statement 3 is the doctrinal trap. A permanent soul is more aligned with many Brahmanical traditions, whereas Buddhism stresses non-self. Therefore, only statements 1 and 2 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Buddhist term — Meaning

1. Sangha — Monastic community
2. Dhamma — Teaching or doctrine
3. Vinaya — Rules of monastic discipline

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Sangha refers to the Buddhist monastic community, Dhamma to the teaching or doctrine, and Vinaya to monastic discipline. These form core institutional and doctrinal elements of Buddhism.",
        "elimination_logic": "All three terms are correctly matched. The question tests basic but important Buddhist institutional vocabulary."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to the difference between Hinayana/Theravada and Mahayana traditions, consider the following statements:

1. Mahayana gave greater emphasis to the Bodhisattva ideal.
2. Image worship became more prominent under Mahayana.
3. Theravada completely rejected monastic discipline.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Mahayana Buddhism emphasised the Bodhisattva ideal and encouraged devotional practices, including image worship. Theravada did not reject monastic discipline; Vinaya remained central to monastic life.",
        "elimination_logic": "Statement 3 is an extreme and incorrect statement. No major Buddhist school rejected monastic discipline completely. Statements 1 and 2 correctly capture Mahayana features."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following events in the life of Buddha in chronological order:

1. Enlightenment at Bodh Gaya
2. First sermon at Sarnath
3. Birth at Lumbini
4. Mahaparinirvana at Kushinagar

Select the correct answer.""",
        "options": ["a) 3-1-2-4", "b) 1-3-2-4", "c) 3-2-1-4", "d) 2-1-3-4"],
        "answer": "a) 3-1-2-4",
        "explanation": "The sequence is birth at Lumbini, enlightenment at Bodh Gaya, first sermon at Sarnath and Mahaparinirvana at Kushinagar.",
        "elimination_logic": "Birth must come first and Mahaparinirvana last. Enlightenment precedes the first sermon. Therefore, the correct order is 3-1-2-4."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements regarding Buddhist monastic institutions:

1. Monasteries often emerged along trade routes.
2. Lay donations played an important role in sustaining the Sangha.
3. Buddhist monasteries remained completely isolated from economic life.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Buddhist monasteries frequently developed near trade routes and urban centres. Merchant donations and lay patronage were important for sustaining the Sangha. Monasteries were not completely isolated from economic activity.",
        "elimination_logic": "Statement 3 is incorrect due to the absolute phrase 'completely isolated'. Archaeological and textual evidence shows interaction between monasteries, merchants and lay donors. Statements 1 and 2 are correct."
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
    print("Inserted Buddhism MCQs:", len(questions))
