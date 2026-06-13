from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 6

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the Mauryan Empire, consider the following statements:

1. Chandragupta Maurya founded the Mauryan Empire.
2. Kautilya’s Arthashastra provides information on statecraft and administration.
3. Ashoka was the immediate successor of Chandragupta Maurya.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Chandragupta Maurya founded the Mauryan Empire after overthrowing the Nandas. The Arthashastra, attributed to Kautilya, is an important source for Mauryan statecraft, economy and administration. Ashoka was not the immediate successor of Chandragupta; Bindusara came between them.",
        "elimination_logic": "Statement 3 is the chronological trap. The correct succession was Chandragupta Maurya → Bindusara → Ashoka. Therefore, options containing statement 3 are eliminated."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following events is most closely associated with Ashoka’s change in state policy?""",
        "options": ["a) Battle of Hydaspes", "b) Kalinga War", "c) Battle of Tarain", "d) Battle of Talikota"],
        "answer": "b) Kalinga War",
        "explanation": "The Kalinga War had a deep impact on Ashoka. His inscriptions describe the suffering caused by the war and his subsequent emphasis on Dhamma, welfare and moral governance.",
        "elimination_logic": "Hydaspes is associated with Alexander and Porus. Tarain belongs to the Ghurid-Rajput conflict. Talikota belongs to the Vijayanagara period. Kalinga alone belongs to Ashoka’s reign."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Mauryan source — Nature of information

1. Arthashastra — Administrative and economic policy
2. Indica — Account by Megasthenes
3. Ashokan inscriptions — Royal orders and Dhamma policy

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "The Arthashastra gives information on statecraft, administration, taxation and economy. Indica was written by Megasthenes, the Greek ambassador at Chandragupta’s court. Ashokan inscriptions are primary sources for Ashoka’s Dhamma and administrative communication.",
        "elimination_logic": "All three are correctly matched. The question tests whether the candidate can distinguish textual, foreign and epigraphic sources of Mauryan history."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to Ashoka’s Dhamma, consider the following statements:

1. It was identical to Buddhism as a monastic religion.
2. It emphasised ethical conduct, compassion and respect for elders.
3. It promoted tolerance towards different sects.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 2 and 3 only",
        "explanation": "Ashoka personally supported Buddhism, but his Dhamma was not identical to Buddhist monastic doctrine. It was a broad moral-ethical code emphasising non-violence, compassion, respect for parents and teachers, welfare, restraint and tolerance among sects.",
        "elimination_logic": "Statement 1 is the conceptual trap. Ashoka’s Dhamma was not a sectarian Buddhist creed imposed on all subjects. Statements 2 and 3 correctly capture its ethical and inclusive character."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): The Mauryan Empire required an elaborate administrative machinery.

Reason (R): It covered a large territory and involved taxation, law enforcement, military organisation and provincial administration.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "The Mauryan Empire was one of the earliest large territorial empires in the subcontinent. Its size required an organised bureaucracy, revenue system, provincial administration, espionage, military control and public works.",
        "elimination_logic": "Both the assertion and reason are historically correct. The reason directly explains why an elaborate administrative system was necessary for Mauryan imperial control."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements regarding Mauryan provincial administration:

1. Important provinces were often governed by royal princes or members of the royal family.
2. Taxila and Ujjain were important provincial centres.
3. The Mauryan state had no system of officials below the provincial level.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Mauryan Empire had important provincial centres such as Taxila and Ujjain. Royal princes or kumaras were often associated with provincial administration. The state also had several lower-level officials for revenue, policing, records and local administration.",
        "elimination_logic": "Statement 3 is incorrect because Mauryan administration extended below the provincial level through multiple categories of officials. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following features are associated with Mauryan art and architecture?

1. Polished stone pillars
2. Animal capitals
3. Rock-cut caves at Barabar
4. Extensive use of true arches in monumental buildings

Select the correct answer using the code below.""",
        "options": ["a) 1, 2 and 3 only", "b) 1 and 4 only", "c) 2, 3 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "a) 1, 2 and 3 only",
        "explanation": "Mauryan art is known for polished sandstone pillars, animal capitals such as the lion capital, and rock-cut caves like the Barabar caves. True arches as a major architectural feature are associated with much later architectural traditions.",
        "elimination_logic": "Statement 4 is an anachronistic architectural trap. Mauryan monuments did not characteristically use true arches in the way later Indo-Islamic architecture did. Hence 1, 2 and 3 are correct."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to Ashokan inscriptions, consider the following statements:

1. They are among the earliest deciphered written records of the Indian subcontinent.
2. Most major inscriptions were composed in Sanskrit.
3. They were used to communicate royal policy to a wide public.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 1 and 3 only", "c) 2 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 1 and 3 only",
        "explanation": "Ashokan inscriptions are among the earliest deciphered written records in Indian history. They were mostly in Prakrit written in Brahmi script, with some inscriptions in Kharosthi, Greek and Aramaic in the north-west. They communicated royal policy, moral instructions and administrative concerns.",
        "elimination_logic": "Statement 2 is incorrect because most Ashokan inscriptions were not in Sanskrit. Once statement 2 is eliminated, only option (b) remains."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following in chronological order:

1. Kalinga War
2. Accession of Chandragupta Maurya
3. Reign of Bindusara
4. Ashoka’s Dhamma policy after remorse

Select the correct answer.""",
        "options": ["a) 2-3-1-4", "b) 3-2-1-4", "c) 2-1-3-4", "d) 1-2-3-4"],
        "answer": "a) 2-3-1-4",
        "explanation": "Chandragupta founded the Mauryan Empire, followed by Bindusara. Ashoka later came to power, fought the Kalinga War, and thereafter gave greater emphasis to Dhamma and moral governance.",
        "elimination_logic": "Chandragupta must precede Bindusara and Ashoka. The Dhamma policy linked with remorse must follow the Kalinga War. Hence the correct order is 2-3-1-4."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements regarding the decline of the Mauryan Empire:

1. It can be explained solely by Ashoka’s policy of non-violence.
2. Fiscal stress, administrative overcentralisation and weak successors are among the explanations suggested by historians.
3. Regional political forces gained importance after the weakening of Mauryan control.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 2 and 3 only",
        "explanation": "The decline of the Mauryan Empire was a complex process. Historians point to factors such as administrative overcentralisation, pressure on resources, succession problems, provincial assertion and changing political conditions. It cannot be reduced solely to Ashoka’s non-violence.",
        "elimination_logic": "Statement 1 is a monocausal explanation and is therefore incorrect. UPSC often rejects simplistic single-cause explanations for complex imperial decline. Statements 2 and 3 provide a more historically balanced explanation."
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
    print("Inserted Mauryan Empire MCQs:", len(questions))
