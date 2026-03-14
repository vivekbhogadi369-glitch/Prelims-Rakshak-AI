from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"answer": "Please enter topic, subject."})

        prompt = f"""
You are Prelims Rakshak AI created by Vivek Sir for UPSC aspirants.

SOURCE PRIORITY:

1️⃣ First priority → NCERT History textbooks (Class 6–12)
2️⃣ Second priority → Uploaded History Textbook
3️⃣ Third priority → Other uploaded history documents

Use the uploaded documents as the PRIMARY source.

Rules:
- Prefer NCERT explanations whenever available.
- Use the additional textbook to enrich explanations with diagrams, tables, and maps.
- Only use general model knowledge if documents lack information.
- Do NOT include references or citations.
- Do NOT add supplementary questions.
- Do NOT add extra sections beyond A, B and C.
- End the full answer with exactly this sentence:
All the best for your preparation.

Student query:
{user_message}

Answer strictly in this structure only:

A. UPSC PRELIMS PYQs (Past 15 years)

- List relevant PYQs if available.
- If exact PYQs are not available, include PYQs from closely related subtopics.
- Mention the year like:
2019 - UPSC Prelims
- Then write the question and answer.
- If none exist, write exactly:
No PYQs came from this subtopic so far.

B. QUICK REVISION NOTES (minimum 700 words)

Structure the notes like UPSC coaching revision sheets.

Include the following:

1. Title
2. 2–3 line introduction
3. Key headings with bullet points
4. Important concepts
5. Important factual points
6. Mini table wherever useful
7. Timeline / chronology
8. Map or location pointers
9. Diagram / hierarchy / flowchart in text form
10. UPSC trap areas
11. One-line revision takeaway

Make the notes visually rich using:
• tables
• bullet points
• simple diagrams
• map references

Avoid long paragraphs.

C. PRACTICE MCQs

Generate exactly 10 UPSC standard MCQs.

Pattern:
5 Statement based
3 Match the following
2 Factual

Difficulty distribution:
3 Easy
5 Moderate
2 Tough

For EACH MCQ include:
- Correct Answer
- Elimination Logic
- Why other options are wrong
- Trap Zone
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [VECTOR_STORE_ID],
                    "max_num_results": 10
                }
            ]
        )

        answer = "Error: No answer generated."

        for item in response.output:
            if getattr(item, "type", "") == "message":
                contents = getattr(item, "content", [])
                for content in contents:
                    if getattr(content, "type", "") in ["output_text", "text"]:
                        answer = getattr(content, "text", "Error: No answer generated.")
                        break
                if answer != "Error: No answer generated.":
                    break

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
