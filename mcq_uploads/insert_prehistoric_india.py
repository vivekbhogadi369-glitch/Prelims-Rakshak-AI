from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 99

questions = [
    {
        "difficulty": "Easy",
        "question": """Consider the following statements regarding the Palaeolithic phase in India:

1. It was primarily associated with hunting and food-gathering.
2. Stone tools were generally made by flaking and chipping.
3. Agriculture was the dominant economic activity.

Which of the statements given above is/are correct?""",
        "options": [
            "a) 1 and 2 only",
            "b) 2 and 3 only",
            "c) 1 and 3 only",
            "d) 1, 2 and 3"
        ],
        "answer": "a) 1 and 2 only",
        "explanation": "The Palaeolithic phase was marked by hunting-gathering communities using chipped stone tools. Agriculture had not yet become the dominant mode of subsistence; it is associated with the Neolithic phase.",
        "elimination_logic": "Statement 3 is the trap. Agriculture belongs to the Neolithic period, not the Palaeolithic. Once statement 3 is eliminated, options (b), (c) and (d) are ruled out. Statements 1 and 2 correctly describe the Palaeolithic phase."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following is the most characteristic technological feature of the Mesolithic phase?""",
        "options": [
            "a) Use of iron tools",
            "b) Use of microliths",
            "c) Use of copper coins",
            "d) Use of burnt bricks"
        ],
        "answer": "b) Use of microliths",
        "explanation": "Microliths, or small stone tools, are the most distinctive technological feature of the Mesolithic period. They were often hafted into wooden or bone handles and used as composite tools.",
        "elimination_logic": "Iron tools belong to the Iron Age. Copper coins are much later. Burnt bricks are associated with early urban cultures such as the Harappan civilisation. Microliths are the correct Mesolithic marker."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to prehistoric cultural development, consider the following sequence:

1. Hunting-gathering economy
2. Microlithic tool tradition
3. Food production and domestication
4. Use of iron implements

Which one of the following represents the correct broad chronological sequence?""",
        "options": [
            "a) 1-2-3-4",
            "b) 2-1-3-4",
            "c) 1-3-2-4",
            "d) 3-1-2-4"
        ],
        "answer": "a) 1-2-3-4",
        "explanation": "The broad sequence is Palaeolithic hunting-gathering, followed by Mesolithic microlithic traditions, then Neolithic food production and domestication, and finally the wider use of iron in later periods.",
        "elimination_logic": "Food production cannot precede the hunting-gathering phase in prehistoric chronology. Microliths are later than early Palaeolithic hunting-gathering but earlier than settled Neolithic food production. Iron is the latest among the given developments."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Prehistoric site — Important feature

1. Burzahom — Pit dwellings
2. Koldihwa — Early rice evidence
3. Mehrgarh — Early farming and pastoralism

Which of the pairs given above are correctly matched?""",
        "options": [
            "a) 1 and 2 only",
            "b) 2 and 3 only",
            "c) 1 and 3 only",
            "d) 1, 2 and 3"
        ],
        "answer": "d) 1, 2 and 3",
        "explanation": "Burzahom is known for pit dwellings in Kashmir. Koldihwa is associated with early evidence of rice cultivation. Mehrgarh provides evidence of early farming and pastoralism in the north-western subcontinent.",
        "elimination_logic": "All three are standard site-feature associations. None of the pairs involves a period mismatch or site mismatch. Therefore, all three pairs are correctly matched."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): The Neolithic phase is considered a major turning point in human history.

Reason (R): It witnessed the beginning of food production, domestication of animals and more settled life.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "The Neolithic phase transformed human life by shifting communities from dependence on hunting-gathering towards food production, domestication and settled habitation. These changes later enabled surplus production and complex social life.",
        "elimination_logic": "The assertion is correct because the Neolithic phase changed the economic base of society. The reason is also correct and directly explains why this phase was transformative. Hence option (a) is correct."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to prehistoric rock art in India, consider the following statements:

1. Bhimbetka contains paintings from different cultural phases.
2. Rock art depicts only animals and not human activities.
3. Superimposition of paintings suggests repeated use of shelters over time.

Which of the statements given above is/are correct?""",
        "options": [
            "a) 1 and 2 only",
            "b) 1 and 3 only",
            "c) 2 and 3 only",
            "d) 1, 2 and 3"
        ],
        "answer": "b) 1 and 3 only",
        "explanation": "Bhimbetka rock shelters show paintings from multiple periods. These paintings depict animals, hunting, dancing and social activities. Superimposition of paintings indicates repeated artistic activity and prolonged use of the shelters.",
        "elimination_logic": "Statement 2 is incorrect because it uses the restrictive word 'only'. Prehistoric paintings include both animal figures and human/social activities. Statements 1 and 3 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements regarding the Mesolithic-Neolithic transition:

1. It occurred uniformly across the Indian subcontinent.
2. Older hunting-gathering practices continued alongside early cultivation in some regions.
3. The transition involved changes in tools, subsistence and settlement patterns.

Which of the statements given above are correct?""",
        "options": [
            "a) 1 and 2 only",
            "b) 2 and 3 only",
            "c) 1 and 3 only",
            "d) 1, 2 and 3"
        ],
        "answer": "b) 2 and 3 only",
        "explanation": "The transition from Mesolithic to Neolithic was gradual and regionally varied. In several regions, older practices such as hunting, gathering and fishing continued alongside early cultivation and domestication. Tool types, subsistence methods and settlement patterns changed over time.",
        "elimination_logic": "Statement 1 is incorrect because the transition was not uniform. UPSC often tests such overgeneralised statements. Statements 2 and 3 correctly reflect the gradual and regionally varied nature of cultural change."
    },
    {
        "difficulty": "Hard",
        "question": """Match the following:

Site — Region/Association

1. Daojali Hading — North-East India
2. Chirand — Middle Gangetic Valley
3. Hallur — South Indian Neolithic

Which of the pairs given above are correctly matched?""",
        "options": [
            "a) 1 and 2 only",
            "b) 2 and 3 only",
            "c) 1 and 3 only",
            "d) 1, 2 and 3"
        ],
        "answer": "d) 1, 2 and 3",
        "explanation": "Daojali Hading is an important Neolithic site in North-East India. Chirand is associated with the Middle Gangetic Valley region. Hallur is an important site of the South Indian Neolithic tradition.",
        "elimination_logic": "The question tests regional associations. None of the given pairs is misplaced. Daojali Hading, Chirand and Hallur represent different regional Neolithic traditions, making all three pairs correct."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements:

1. Mehrgarh provides evidence of early farming before the mature Harappan phase.
2. All Neolithic cultures in India followed the same settlement pattern.
3. Bone tools are known from some Neolithic sites.

Which of the statements given above is/are correct?""",
        "options": [
            "a) 1 and 2 only",
            "b) 1 and 3 only",
            "c) 2 and 3 only",
            "d) 1, 2 and 3"
        ],
        "answer": "b) 1 and 3 only",
        "explanation": "Mehrgarh shows early farming and pastoral activity before the mature Harappan phase. Indian Neolithic cultures were regionally diverse and did not follow a uniform settlement pattern. Bone tools are known from sites such as Burzahom and Chirand.",
        "elimination_logic": "Statement 2 is incorrect because it wrongly assumes uniformity across regions. Statements 1 and 3 are correct. The correct option must therefore include 1 and 3 but exclude 2."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to prehistoric India, consider the following:

1. Microliths
2. Pit dwellings
3. Ash mounds
4. Urban drainage system

Which of the above are associated with prehistoric or protohistoric cultural phases before mature urban Harappan civilisation?""",
        "options": [
            "a) 1, 2 and 3 only",
            "b) 2 and 4 only",
            "c) 1 and 4 only",
            "d) 1, 2, 3 and 4"
        ],
        "answer": "a) 1, 2 and 3 only",
        "explanation": "Microliths are associated with the Mesolithic phase. Pit dwellings are known from Neolithic Burzahom. Ash mounds are associated with South Indian Neolithic pastoral communities. Urban drainage is a mature Harappan urban feature, not a prehistoric feature before mature urbanism.",
        "elimination_logic": "Statement 4 is the trap. Urban drainage belongs to the mature Harappan urban phase. Once 4 is eliminated, options (b), (c) and (d) are ruled out. Statements 1, 2 and 3 fit prehistoric/protohistoric contexts before mature Harappan urbanism."
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

    print("Inserted Prehistoric India MCQs:", len(questions))
