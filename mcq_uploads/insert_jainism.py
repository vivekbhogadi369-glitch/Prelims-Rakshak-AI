from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 4

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to Jainism, consider the following statements:

1. Rishabhanatha is regarded as the first Tirthankara.
2. Mahavira is regarded as the twenty-fourth Tirthankara.
3. Jainism completely rejected the idea of karma.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Jain tradition regards Rishabhanatha as the first Tirthankara and Mahavira as the twenty-fourth. Jainism strongly accepts the doctrine of karma, but interprets karma as a subtle material substance binding the soul.",
        "elimination_logic": "Statement 3 is the trap. Jainism does not reject karma; rather, liberation requires freeing the soul from karmic bondage. Hence only statements 1 and 2 are correct."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following principles is most closely associated with the doctrine of Anekantavada in Jainism?""",
        "options": ["a) Absolute monotheism", "b) Many-sided nature of reality", "c) Ritual sacrifice as path to liberation", "d) Complete denial of the soul"],
        "answer": "b) Many-sided nature of reality",
        "explanation": "Anekantavada refers to the Jain doctrine that reality is complex and can be understood from multiple perspectives. It discourages one-sided absolutist claims.",
        "elimination_logic": "Jainism does not advocate absolute monotheism or Vedic ritual sacrifice. It accepts the existence of jiva or soul. Therefore, the many-sided nature of reality is the correct association."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Jain concept — Meaning

1. Ahimsa — Non-violence
2. Aparigraha — Non-possession
3. Syadvada — Conditional or relative predication

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Ahimsa is non-violence, Aparigraha is non-possession or non-attachment, and Syadvada expresses the conditional nature of statements from different standpoints.",
        "elimination_logic": "All three are core Jain philosophical-ethical ideas. The trap is usually between Anekantavada and Syadvada; Anekantavada is the many-sidedness of reality, while Syadvada is its logical expression."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to Mahavira, consider the following statements:

1. He belonged to the Kshatriya clan of the Jnatrikas.
2. He attained kaivalya after prolonged austerities.
3. He accepted the authority of the Vedas as final.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Mahavira belonged to the Jnatrika clan and attained kaivalya after intense austerities. Jainism, like Buddhism, did not accept Vedic authority as final.",
        "elimination_logic": "Statement 3 is incorrect because Jainism emerged as a shramana tradition outside Vedic orthodoxy. Statements 1 and 2 are correct."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): Jainism placed exceptional emphasis on Ahimsa.

Reason (R): Jainism believed that not only humans and animals but even plants and minute life-forms possess life.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "Jainism’s strict doctrine of Ahimsa is rooted in its belief that life exists in many forms, including tiny organisms. This explains the rigorous ethical discipline imposed on Jain monks.",
        "elimination_logic": "Both assertion and reason are correct. The reason directly explains why Jainism developed a stricter version of non-violence than many other traditions."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following were causes for the growth of Jainism in ancient India?

1. Reaction against elaborate Vedic rituals
2. Use of Prakrit and regional languages for communication
3. Support from merchant communities
4. Complete dependence on royal patronage alone

Select the correct answer using the code below.""",
        "options": ["a) 1, 2 and 3 only", "b) 2 and 4 only", "c) 1 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "a) 1, 2 and 3 only",
        "explanation": "Jainism grew partly as a response to ritual orthodoxy. Its use of accessible languages and support from urban and merchant communities helped its spread. It was not dependent only on royal patronage.",
        "elimination_logic": "Statement 4 is an absolute and incorrect statement. Jainism received some royal support but also depended heavily on lay and merchant patronage. Therefore, options containing 4 are eliminated."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements regarding Jain sects:

1. Digambaras believe that complete non-possession requires renunciation of clothing by monks.
2. Svetambaras allow white clothing for monks.
3. Both sects deny the importance of ascetic discipline.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Digambaras emphasise complete nudity for monks as a form of absolute non-possession, while Svetambaras permit white garments. Both traditions value ascetic discipline deeply.",
        "elimination_logic": "Statement 3 is incorrect because ascetic discipline is central to Jain practice in both sects. Statements 1 and 2 correctly capture sectarian differences."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to Jain metaphysics, consider the following statements:

1. Jiva refers to conscious soul.
2. Ajiva refers to non-living substance.
3. Liberation involves complete destruction of the soul.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Jainism distinguishes between jiva, the conscious soul, and ajiva, non-living substance. Liberation does not destroy the soul; it frees the soul from karmic bondage.",
        "elimination_logic": "Statement 3 is the philosophical trap. Jainism does not advocate annihilation of the soul. It believes in the purification and liberation of the soul. Hence only statements 1 and 2 are correct."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following in the correct sequence in the Jain path of spiritual progress:

1. Right knowledge
2. Right faith
3. Right conduct

Select the correct answer.""",
        "options": ["a) 2-1-3", "b) 1-2-3", "c) 3-2-1", "d) 2-3-1"],
        "answer": "a) 2-1-3",
        "explanation": "The Three Jewels of Jainism are Right Faith, Right Knowledge and Right Conduct. These together form the path towards liberation.",
        "elimination_logic": "Right conduct must follow faith and knowledge. The standard order is Samyak Darshana, Samyak Jnana and Samyak Charitra, corresponding to 2-1-3."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements about Jainism and Buddhism:

1. Both emerged in the context of the shramana tradition.
2. Both rejected the authority of Vedic sacrifices as essential to liberation.
3. Both accepted a permanent soul as a central doctrine.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Both Jainism and Buddhism emerged from the shramana milieu and challenged ritual orthodoxy. However, Jainism accepts jiva or soul, while Buddhism denies a permanent self through the doctrine of anatta.",
        "elimination_logic": "Statement 3 creates a common trap by treating Jainism and Buddhism as identical. Jainism accepts a soul; Buddhism does not accept a permanent individual self. Therefore, only 1 and 2 are correct."
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
    print("Inserted Jainism MCQs:", len(questions))
