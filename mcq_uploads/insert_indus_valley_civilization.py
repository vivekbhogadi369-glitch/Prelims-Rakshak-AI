from app import app, db, MCQ
import json

SUBJECT_ID = 1
TOPIC_ID = 1

questions = [
    {
        "difficulty": "Easy",
        "question": """With reference to the urban planning of the Indus Valley Civilization, consider the following statements:

1. Many cities followed a grid-pattern layout.
2. Drainage systems were mostly absent in residential areas.
3. Burnt bricks were widely used in several urban centres.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 1 and 3 only", "c) 2 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 1 and 3 only",
        "explanation": "Harappan urbanism is marked by planned streets, grid-like layouts in major cities, standardized baked bricks, and an advanced drainage network. Drains were not absent; they were among the most distinctive civic features.",
        "elimination_logic": "Statement 2 is the trap. UPSC often tests Harappan drainage as a marker of civic planning. Since 2 is incorrect, options containing 2 are eliminated. Statements 1 and 3 correctly reflect Harappan urban planning."
    },
    {
        "difficulty": "Easy",
        "question": """Which one of the following Harappan sites is best known for its dockyard-like structure?""",
        "options": ["a) Kalibangan", "b) Lothal", "c) Banawali", "d) Rakhigarhi"],
        "answer": "b) Lothal",
        "explanation": "Lothal in Gujarat is associated with a dockyard-like structure, indicating maritime trade and interaction with coastal networks.",
        "elimination_logic": "Kalibangan is important for fire altars and ploughed field evidence. Banawali is associated with town planning and fortification. Rakhigarhi is a major Harappan urban centre, but the dockyard association is specifically linked with Lothal."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following pairs:

Harappan site — Important evidence

1. Kalibangan — Ploughed field
2. Dholavira — Water management system
3. Chanhudaro — Bead-making and craft activities

Which of the pairs given above are correctly matched?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Kalibangan has evidence of a ploughed field. Dholavira is famous for its sophisticated water conservation system. Chanhudaro is known as an important craft-production centre, especially bead-making.",
        "elimination_logic": "All three are standard site-evidence associations. The question tests whether the candidate confuses economic/craft sites with urban planning sites. No pair is incorrectly matched."
    },
    {
        "difficulty": "Medium",
        "question": """With reference to Harappan economy, consider the following statements:

1. Agriculture was supported by crops such as wheat and barley.
2. Cotton was known to the Harappans.
3. Coinage was the principal medium of exchange.

Which of the statements given above is/are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "a) 1 and 2 only",
        "explanation": "Harappan economy was based on agriculture, craft production and trade. Wheat, barley and cotton were known. However, coinage was not used; exchange likely operated through barter and standardized weights.",
        "elimination_logic": "Statement 3 is an anachronistic trap. Coinage belongs to later historical phases, not Harappan civilisation. Once statement 3 is eliminated, only option (a) remains."
    },
    {
        "difficulty": "Medium",
        "question": """Assertion (A): Standardized weights and measures were important features of Harappan urban economy.

Reason (R): They helped regulate craft production, trade and exchange across widely separated urban centres.

Select the correct answer.""",
        "options": [
            "a) Both A and R are correct and R is the correct explanation of A",
            "b) Both A and R are correct but R is not the correct explanation of A",
            "c) A is correct but R is incorrect",
            "d) A is incorrect but R is correct"
        ],
        "answer": "a) Both A and R are correct and R is the correct explanation of A",
        "explanation": "Standardized weights indicate regulated economic transactions and integration across Harappan centres. Their uniformity suggests a shared commercial culture and administrative control over exchange.",
        "elimination_logic": "The assertion is correct because standardized weights are archaeologically attested. The reason is also correct because such standardization would be meaningful only in the context of trade, craft specialization and inter-regional exchange."
    },
    {
        "difficulty": "Medium",
        "question": """Consider the following statements regarding Harappan seals:

1. They commonly contain animal motifs and short inscriptions.
2. They provide evidence that the Harappan script has been fully deciphered.
3. They may have been used in trade, administration or identity marking.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 1 and 3 only", "c) 2 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 1 and 3 only",
        "explanation": "Harappan seals often carry animal motifs such as the unicorn and short inscriptions. Their exact function is debated, but they are linked with trade, administration and ownership/identity. The Harappan script remains undeciphered.",
        "elimination_logic": "Statement 2 is the key trap. Whenever a statement claims that Harappan script is fully deciphered, it is incorrect. Statements 1 and 3 are consistent with archaeological interpretation."
    },
    {
        "difficulty": "Medium",
        "question": """Which of the following features best distinguish Dholavira from many other Harappan sites?

1. Sophisticated water reservoirs
2. Three-fold division of settlement
3. Evidence of large signboard inscription

Select the correct answer using the code below.""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "d) 1, 2 and 3",
        "explanation": "Dholavira is notable for its elaborate water management, distinctive three-part settlement division, and a large inscription/signboard-like find. These make it one of the most distinctive Harappan urban centres.",
        "elimination_logic": "The trap is to associate only water management with Dholavira. UPSC may combine multiple unique features of a site. All three are valid associations."
    },
    {
        "difficulty": "Hard",
        "question": """With reference to regional variations within the Indus Valley Civilization, consider the following statements:

1. All Harappan settlements followed the same citadel-lower town pattern.
2. Coastal sites indicate participation in maritime trade networks.
3. Harappan cultural influence extended beyond present-day Punjab and Sindh.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 2 and 3 only",
        "explanation": "Harappan civilisation had regional diversity. Not all settlements followed the same layout. Coastal sites such as Lothal indicate maritime interaction. Harappan influence extended across Gujarat, Rajasthan, Haryana, Punjab, Sindh, Baluchistan and beyond.",
        "elimination_logic": "Statement 1 uses the absolute word 'all', making it suspect. Harappan urban forms varied across regions. Statements 2 and 3 correctly capture coastal trade and geographical spread."
    },
    {
        "difficulty": "Hard",
        "question": """Arrange the following Harappan sites approximately from west/north-west to east/south-east:

1. Mohenjo-daro
2. Kalibangan
3. Lothal
4. Dholavira

Select the correct answer.""",
        "options": ["a) 1-2-4-3", "b) 2-1-3-4", "c) 1-4-2-3", "d) 4-1-2-3"],
        "answer": "a) 1-2-4-3",
        "explanation": "Mohenjo-daro lies in Sindh, Kalibangan in Rajasthan, Dholavira in Kutch, and Lothal in Gujarat near the Gulf of Khambhat. The broad west/north-west to east/south-east ordering is Mohenjo-daro, Kalibangan, Dholavira and Lothal.",
        "elimination_logic": "This tests spatial understanding, not rote site features. Mohenjo-daro must come before Indian sites in a west/north-west sequence. Dholavira lies in Kutch, while Lothal lies further south-east in Gujarat."
    },
    {
        "difficulty": "Hard",
        "question": """Consider the following statements about the decline of the Harappan Civilization:

1. It was most likely caused by a single sudden invasion across all regions.
2. Environmental changes and shifts in river systems may have contributed to urban decline.
3. Harappan cultural elements continued in some post-urban regional cultures.

Which of the statements given above are correct?""",
        "options": ["a) 1 and 2 only", "b) 2 and 3 only", "c) 1 and 3 only", "d) 1, 2 and 3"],
        "answer": "b) 2 and 3 only",
        "explanation": "The decline of Harappan urbanism was a complex and regionally varied process. Environmental stress, river shifts, reduced trade and deurbanisation are considered important factors. Some Harappan cultural elements continued in later regional cultures.",
        "elimination_logic": "Statement 1 is too simplistic and uses the trap of a single-cause explanation. UPSC generally avoids monocausal explanations for complex civilisational decline. Statements 2 and 3 reflect current historical understanding."
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
    print("Inserted Indus Valley Civilization MCQs:", len(questions))
