from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 2

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the Early Vedic period, consider the following statements:

1. The Rig Veda is the main source for understanding this phase.
2. Society was predominantly pastoral.
3. Iron was extensively used in agriculture.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Early Vedic period is mainly reconstructed from the Rig Veda. The economy was largely pastoral, though agriculture was known. Extensive use of iron belongs mainly to the Later Vedic phase.",
        "elimination_logic": "Statement 3 is the chronological trap. Iron use becomes significant in the Later Vedic period, not the Early Vedic phase. Therefore, only 1 and 2 are correct."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following assemblies is most closely associated with popular participation in the Early Vedic polity?""",
        "options": ["a) Sabha and Samiti", "b) Mantriparishad and Amatya", "c) Ur and Nadu", "d) Mahasabha and Nagaram"],
        "answer": "a) Sabha and Samiti",
        "explanation": "Sabha and Samiti were important assemblies in the Early Vedic polity. They reflected participatory elements in tribal political life.",
        "elimination_logic": "Mantriparishad and Amatya belong to later monarchical administration. Ur, Nadu, Mahasabha and Nagaram are associated with South Indian local institutions, not Early Vedic polity."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Term — Meaning/Association

1. Jana — Tribe or people
2. Vish — Clan or common people
3. Gopati — Protector of cattle

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Jana referred to the tribe or people, Vish to the clan/common people, and Gopati reflected the king’s role as protector of cattle in a pastoral society.",
        "elimination_logic": "All three terms fit the socio-political vocabulary of the Early Vedic period. There is no mismatch in the pairs."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to the transition from Early Vedic to Later Vedic society, consider the following statements:

1. Agriculture became more important in the Later Vedic period.
2. The political structure moved towards larger territorial kingdoms.
3. The position of tribal assemblies became stronger than before.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Later Vedic period saw greater agricultural expansion, especially with iron tools, and the emergence of larger territorial polities. Tribal assemblies declined in importance as kingship became stronger.",
        "elimination_logic": "Statement 3 is incorrect. UPSC often tests institutional change: assemblies did not become stronger; their influence declined with the rise of monarchy."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): The Later Vedic period witnessed increasing social differentiation.

Reason (R): Varna distinctions became more defined and ritual hierarchy gained importance.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "Later Vedic society shows clearer varna divisions and increased ritual hierarchy. Brahmanical rituals became more elaborate, contributing to social stratification.",
        "elimination_logic": "Both assertion and reason are historically correct. The reason directly explains the increasing social differentiation, so option (a) is correct."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following changes are associated with the Later Vedic period?

1. Expansion into the western Ganga plains
2. Greater importance of agriculture
3. Decline in ritual sacrifices
4. Emergence of stronger monarchy

Select the correct answer using the code below.""",
        "options": ["a) 1, 2 and 4 only", "b) 1 and 3 only", "c) 2, 3 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "a) 1, 2 and 4 only",
        "explanation": "The Later Vedic period saw eastward expansion, growing agriculture and stronger monarchy. Ritual sacrifices did not decline; rather, they became more elaborate and central to Brahmanical authority.",
        "elimination_logic": "Statement 3 is the trap. Later Vedic religion involved elaborate sacrifices like Rajasuya and Ashvamedha. Therefore, options containing 3 are eliminated."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Vedic text — Broad association

1. Rig Veda — Hymns to deities
2. Sama Veda — Melodies and chants
3. Yajur Veda — Sacrificial formulae
4. Atharva Veda — Spells and popular beliefs

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1, 2 and 3 only", "b) 2, 3 and 4 only", "c) 1 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "d) 1, 2, 3 and 4",
        "explanation": "Rig Veda consists mainly of hymns, Sama Veda is linked with chants, Yajur Veda with sacrificial formulae, and Atharva Veda with spells, healing practices and popular beliefs.",
        "elimination_logic": "All four pairs are standard and correctly matched. The question tests confusion between Sama and Yajur Veda; Sama is musical, Yajur is ritual formula-based."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to women in the Vedic period, consider the following statements:

1. Women participated in assemblies and religious rituals in the Early Vedic period.
2. Their position became relatively more restricted in the Later Vedic period.
3. The Upanayana ceremony for women became more prominent in the Later Vedic period.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Women enjoyed a comparatively better position in the Early Vedic period, with participation in rituals and assemblies. In the Later Vedic period, patriarchal control and ritual restrictions increased.",
        "elimination_logic": "Statement 3 is incorrect because women’s ritual and educational access became more restricted, not more prominent, in the Later Vedic phase."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following developments in broad chronological order:

1. Predominantly pastoral Rig Vedic society
2. Expansion of agriculture with increasing iron use
3. Emergence of large territorial mahajanapadas
4. Composition of early Vedic hymns

Select the correct answer.""",
        "options": ["a) 4-1-2-3", "b) 1-4-2-3", "c) 4-2-1-3", "d) 2-4-1-3"],
        "answer": "a) 4-1-2-3",
        "explanation": "Early Vedic hymns are associated with the Rig Vedic phase, which reflects a predominantly pastoral society. Later, agriculture expanded with iron use, eventually paving the way for large territorial states and mahajanapadas.",
        "elimination_logic": "Mahajanapadas must come last. Iron-supported agrarian expansion must come after the early pastoral Rig Vedic context. Therefore, 4-1-2-3 is the correct broad sequence."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements about Vedic polity:

1. In the Early Vedic period, the king was primarily a tribal chief rather than an absolute monarch.
2. In the Later Vedic period, kingship became more powerful and ritualised.
3. Taxes were collected through a highly centralised bureaucratic machinery comparable to the Mauryan state.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Early Vedic kingship was tribal and limited by assemblies. Later Vedic kingship became more territorial, hereditary and ritualised through sacrifices. However, it did not have a Mauryan-type centralised bureaucracy.",
        "elimination_logic": "Statement 3 is an anachronistic trap. Comparing Later Vedic polity to Mauryan bureaucracy is historically incorrect. Statements 1 and 2 correctly show political evolution."
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
    print("Inserted Vedic Age MCQs:", len(questions))
