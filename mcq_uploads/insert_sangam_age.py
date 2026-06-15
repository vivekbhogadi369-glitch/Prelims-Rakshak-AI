from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 9

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to Sangam literature, consider the following statements:

1. Ettuthokai and Pattuppattu are important collections of Sangam poetry.
2. Sangam texts provide information on polity, society, economy and culture of early historic Tamilakam.
3. Sangam literature was composed entirely in Sanskrit.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Ettuthokai and Pattuppattu are major Sangam literary collections. These texts are valuable for reconstructing early historic Tamil society, political formations, trade, warfare, patronage, social values and ecological classifications. Sangam literature was composed mainly in Tamil, not Sanskrit.",
        "elimination_logic": "Statement 3 is the language trap. Sangam literature belongs to the early Tamil literary tradition. Once statement 3 is eliminated, only option (a) remains."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following pairs is correctly matched?

Dynasty — Traditional capital""",
        "options": ["a) Chera — Vanji", "b) Chola — Madurai", "c) Pandya — Uraiyur", "d) Satavahana — Kaveripattinam"],
        "answer": "a) Chera — Vanji",
        "explanation": "The Cheras are traditionally associated with Vanji, the Cholas with Uraiyur and Kaveripattinam, and the Pandyas with Madurai. Correct identification of capitals is important for understanding early Tamil political geography.",
        "elimination_logic": "Madurai belongs to the Pandyas, not Cholas. Uraiyur belongs to Cholas, not Pandyas. Kaveripattinam is a Chola port, not Satavahana capital. Hence only Chera–Vanji is correct."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Tamil dynasty — Emblem

1. Chera — Bow
2. Chola — Tiger
3. Pandya — Fish

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "The traditional symbols of the three crowned kings were: bow for the Cheras, tiger for the Cholas and fish for the Pandyas. These symbols appear in literary and numismatic traditions and became important markers of dynastic identity.",
        "elimination_logic": "All three symbols are correctly matched. The common trap is to confuse Chola tiger with Pandya fish or Chera bow. No pair is incorrect."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to the concept of Tinai in Sangam literature, consider the following statements:

1. It connects landscapes with human emotions, occupations and cultural practices.
2. Kurinji is associated with mountainous regions.
3. Marutam is associated with pastoral and dry desert tracts.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Tinai is an important Sangam classification linking ecology, livelihood, emotions and social life. Kurinji refers to mountainous regions. Marutam refers to fertile agricultural plains, while Mullai is pastoral and Palai is arid/dry landscape.",
        "elimination_logic": "Statement 3 wrongly matches Marutam with pastoral and desert ecology. Marutam is agricultural/fertile plains. Therefore, only statements 1 and 2 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): Sangam literature is a major source for reconstructing early historic South India.

Reason (R): It contains references to kingship, warfare, gift-giving, social groups, trade, ports and ecological zones.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "Sangam literature is not merely poetic; it contains rich historical references to the three crowned kings, chiefs, bards, warriors, merchants, ports, overseas trade, social practices and ecological divisions. Hence it is indispensable for early South Indian history.",
        "elimination_logic": "The assertion is correct. The reason gives the exact range of historical information found in Sangam texts and therefore directly explains the assertion."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following are associated with the economy of the Sangam Age?

1. Overseas trade with the Roman world
2. Ports such as Kaveripattinam and Muchiri
3. Use of the term Yavana for foreign traders
4. Complete absence of internal exchange networks

Select the correct answer using the code below.""",
        "options": ["a) 1, 2 and 3 only", "b) 2 and 4 only", "c) 1 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "a) 1, 2 and 3 only",
        "explanation": "The Sangam Age witnessed active inland and overseas trade. Roman coins, literary references to Yavanas, and ports like Kaveripattinam and Muchiri indicate commercial networks. Internal exchange also existed along with maritime trade.",
        "elimination_logic": "Statement 4 is incorrect because Sangam economy had internal trade networks as well as overseas commerce. Options containing 4 must be eliminated."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Term — Association in Sangam context

1. Yavana — Foreign trader, often linked with Greeks/Romans
2. Velir — Minor chiefs
3. Nadu — Territorial unit or region

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Yavana is used in early Indian texts for foreign traders, often Greeks/Romans in the Sangam context. Velir were minor chiefs, while Nadu refers to a territorial unit or region. These terms help understand Sangam polity and society beyond the three crowned kings.",
        "elimination_logic": "All three are correctly matched. The trap is to restrict Sangam polity only to Chera-Chola-Pandya kings and ignore intermediate chiefs and regional units."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to social conditions in the Sangam Age, consider the following statements:

1. Society included kings, chiefs, warriors, bards, merchants, agriculturists and pastoral groups.
2. Poets and bards played a role in preserving political memory and praise traditions.
3. Sangam society was completely isolated from external commercial and cultural contacts.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Sangam society was socially diverse and included ruling elites, warriors, bards, merchants and productive groups. Poets and bards were important in courtly and martial culture. External trade with Yavanas and Roman contacts shows that society was not isolated.",
        "elimination_logic": "Statement 3 is the absolute trap. Sangam texts and archaeological evidence show external contacts. Statements 1 and 2 correctly describe the social and cultural structure."
    },
    {
        "difficulty": "Hard",
        "question": """Match the following:

Tinai — Associated landscape

1. Kurinji — Mountains
2. Mullai — Pastoral forests
3. Marutam — Agricultural plains
4. Neytal — Seashore

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1, 2 and 3 only", "b) 2, 3 and 4 only", "c) 1 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "d) 1, 2, 3 and 4",
        "explanation": "The Tinai classification links ecological zones with forms of life and poetic themes. Kurinji is mountainous, Mullai is pastoral/forest, Marutam is agricultural plain, Neytal is coastal, and Palai is arid landscape.",
        "elimination_logic": "All four pairs are correctly matched. The main trap is confusing Mullai with Marutam or Palai. Since each pair is correctly associated, option (d) is correct."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements regarding Sangam polity:

1. The Cheras, Cholas and Pandyas are referred to as the three crowned kings.
2. Political power was exercised only through a highly centralised bureaucratic state similar to the Mauryan Empire.
3. Chieftains and warrior elites played an important role in political society.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 1 and 3 only", "c) 2 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 1 and 3 only",
        "explanation": "Sangam polity was centred around the three crowned kings but also included several chiefs and warrior elites. It was not a Mauryan-style centralised bureaucratic empire; political authority was more segmentary and based on kinship, warfare, tribute and gift-giving.",
        "elimination_logic": "Statement 2 is an anachronistic trap. Applying a Mauryan administrative model to Sangam polity is incorrect. Statements 1 and 3 are correct."
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
    print("Inserted Sangam Age MCQs:", len(questions))
