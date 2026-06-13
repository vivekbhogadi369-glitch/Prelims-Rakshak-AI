from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 5

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the Mahajanapadas, consider the following statements:

1. They represented a transition from tribal chiefdoms to territorial states.
2. Some Mahajanapadas were monarchies while some were gana-sanghas.
3. All Mahajanapadas were located only in the Ganga valley.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The Mahajanapadas mark the emergence of territorial states from earlier lineage-based polities. They included both monarchies such as Magadha and Kosala and gana-sanghas such as Vajji and Malla. They were not confined only to the Ganga valley; some were located in north-western and central Indian regions.",
        "elimination_logic": "Statement 3 is an overgeneralisation. While the middle Ganga valley became politically important, all Mahajanapadas were not located only there. Statements 1 and 2 correctly reflect the political transition and diversity of political forms."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following Mahajanapadas was associated with the city of Rajagriha in its early phase?""",
        "options": ["a) Kosala", "b) Magadha", "c) Avanti", "d) Vatsa"],
        "answer": "b) Magadha",
        "explanation": "Rajagriha or Rajgir was an early capital of Magadha before Pataliputra rose to prominence. Magadha later became the nucleus of imperial expansion in northern India.",
        "elimination_logic": "Kosala is associated with Shravasti, Avanti with Ujjain/Mahishmati, and Vatsa with Kaushambi. Rajagriha is specifically linked with Magadha."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Mahajanapada — Capital/Important centre

1. Vatsa — Kaushambi
2. Avanti — Ujjain
3. Kosala — Shravasti

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Vatsa was associated with Kaushambi, Avanti with Ujjain and Mahishmati, and Kosala with Shravasti. These centres were important in the political geography of the Mahajanapada period.",
        "elimination_logic": "All three are correctly matched. The trap is usually confusion between Vatsa-Kaushambi and Avanti-Ujjain, but both associations are correct."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to the rise of Magadha, consider the following factors:

1. Fertile alluvial soil of the middle Ganga valley
2. Access to iron ore resources
3. Strategic location of Rajagriha and later Pataliputra
4. Complete absence of rival powers in north India

Which of the above contributed to the rise of Magadha?""",
        "options": ["a) 1, 2 and 3 only", "b) 1 and 4 only", "c) 2, 3 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "a) 1, 2 and 3 only",
        "explanation": "Magadha benefited from fertile agricultural zones, access to iron resources, forest and elephant wealth, and strategic capitals such as Rajagriha and Pataliputra. It did not rise because rival powers were absent; it defeated or absorbed rivals such as Anga, Kosala, Vajji and Avanti over time.",
        "elimination_logic": "Statement 4 is historically incorrect. The rise of Magadha occurred in a competitive political environment, not in the absence of rivals. Eliminating 4 leaves option (a)."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): The Mahajanapada period witnessed the growth of urban centres and monetised exchange.

Reason (R): Agricultural surplus, craft specialisation and trade networks expanded during this period.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "The sixth century BCE period is associated with the second urbanisation in the Ganga valley. Agricultural surplus, iron technology, craft production, trade, punch-marked coins and urban centres contributed to the changing economic landscape.",
        "elimination_logic": "Both assertion and reason are correct. The reason directly explains why urban centres and monetised exchange expanded. Hence option (a) is correct."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements regarding gana-sanghas during the Mahajanapada period:

1. They were non-monarchical political formations.
2. Political power was usually exercised by assemblies of clan elites.
3. They were completely egalitarian democracies based on universal adult participation.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Gana-sanghas were non-monarchical republic-like polities where political authority was exercised by assemblies of ruling lineages or clan elites. They should not be equated with modern democracies based on universal adult franchise.",
        "elimination_logic": "Statement 3 is the conceptual trap. UPSC often tests modern projection onto ancient institutions. Gana-sanghas were oligarchic or clan-based, not fully egalitarian democracies."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following developments are associated with the period of the Mahajanapadas?

1. Use of punch-marked coins
2. Growth of towns such as Kaushambi and Rajagriha
3. Emergence of new religious movements like Buddhism and Jainism
4. Decline of agriculture as an economic base

Select the correct answer using the code below.""",
        "options": ["a) 1, 2 and 3 only", "b) 2 and 4 only", "c) 1 and 4 only", "d) 1, 2, 3 and 4"],
        "answer": "a) 1, 2 and 3 only",
        "explanation": "The Mahajanapada period saw monetised exchange through punch-marked coins, urban growth and the rise of heterodox religious movements. Agriculture expanded rather than declined, forming the economic base for state formation and urbanisation.",
        "elimination_logic": "Statement 4 is opposite to historical evidence. Agriculture did not decline; surplus agriculture supported urbanisation and state expansion. Therefore, options containing 4 are eliminated."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following political centres from west to east:

1. Ujjain
2. Kaushambi
3. Rajagriha
4. Shravasti

Select the correct answer.""",
        "options": ["a) 1-2-4-3", "b) 2-1-4-3", "c) 1-4-2-3", "d) 4-1-2-3"],
        "answer": "a) 1-2-4-3",
        "explanation": "Ujjain in Avanti lies towards the west, Kaushambi in Vatsa lies further east in the Ganga-Yamuna region, Shravasti in Kosala lies to the north-east, and Rajagriha in Magadha lies further east in Bihar.",
        "elimination_logic": "This tests spatial political geography. Ujjain must appear first among the given centres. Rajagriha must appear after Kaushambi and Shravasti in an eastward sequence. Hence 1-2-4-3 is the correct broad order."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to Magadha’s expansion before the Mauryas, consider the following statements:

1. Bimbisara strengthened Magadha through matrimonial alliances and conquest.
2. Ajatashatru is associated with conflict against the Vajji confederacy.
3. Magadha’s rise was completed only after the decline of all urban centres.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Bimbisara expanded Magadha through conquest and alliances. Ajatashatru fought the Vajji confederacy and further consolidated Magadhan power. Magadha’s rise was closely linked with urbanisation, not the decline of urban centres.",
        "elimination_logic": "Statement 3 reverses the historical relationship. Magadha grew in the context of urban and agrarian expansion. Statements 1 and 2 correctly identify major rulers and political developments."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements:

1. The Mahajanapada period reflects a shift from lineage-based identity to territorial identity.
2. The emergence of taxation was connected with the maintenance of armies and administration.
3. The political economy of the period was entirely independent of trade routes.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "The term janapada itself suggests territory associated with a people, and mahajanapadas represent larger territorial states. Taxation, surplus extraction and administration were linked with standing armies and political consolidation. Trade routes remained important to the political economy of the period.",
        "elimination_logic": "Statement 3 is incorrect because trade routes, towns and monetised exchange were integral to the period. Statements 1 and 2 correctly describe the structural changes in polity and economy."
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
    print("Inserted Mahajanapadas MCQs:", len(questions))
