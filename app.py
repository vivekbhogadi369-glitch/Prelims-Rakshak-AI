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
1. First priority -> NCERT History textbooks (Class 6 to 12)
2. Second priority -> Uploaded History textbook
3. Third priority -> Other uploaded history documents

Use the uploaded documents as the PRIMARY source.

General Rules:
- Prefer NCERT explanations whenever available.
- Use the additional textbook to enrich explanation and presentation.
- Only use general model knowledge if documents lack information.
- Do NOT include references.
- Do NOT include citations.
- Do NOT include source names.
- Do NOT include supplementary questions.
- Do NOT include follow-up questions.
- Do NOT include "Would you like..." style endings.
- Do NOT add any extra section beyond A, B and C.
- End the full answer with exactly this sentence:
All the best for your preparation.

Student query:
{user_message}

Answer strictly in this structure only:

A. UPSC PRELIMS PYQs (Past 15 years)

- List relevant PYQs if available.
- If exact PYQs are not available, include PYQs from closely related subtopics.
- For every PYQ mention the year like:
2019 - UPSC Prelims
- Then write the question and answer.
- If none exist, write exactly:
No PYQs came from this subtopic so far.

B. QUICK REVISION NOTES (minimum 700 words)

Make this section look like a polished UPSC coaching handout, not like generic AI output.

Required format for Quick Revision Notes:
1. Topic Title in clean revision style
2. Brief Introduction (2-3 lines only)
3. Core headings with concise bullet points
4. Sub-points where required
5. Important concepts
6. Important factual points
7. One mini table wherever useful
8. One timeline / chronology block wherever relevant
9. One map / site / location block wherever relevant
10. One mini flowchart / hierarchy / mindmap in text format
11. UPSC Trap Zone
12. One-line Revision Takeaway

Strict formatting rules for Quick Revision Notes:
- Do NOT use ugly labels such as:
  "Map/Location Pointers"
  "Diagram / Hierarchy in Text Form"
  "Mini Mindmap Summary"
- Instead use polished coaching-note headings such as:
  "Important Sites"
  "Administrative Structure"
  "Chronology"
  "Exam Focus"
  "Quick Revision Flow"
  "UPSC Trap Zone"
- Avoid long paragraphs.
- Prefer crisp bullets and short blocks.
- Make headings short, natural, and classroom-style.
- Tables must look clean and useful.
- Flowcharts should look neat in plain text.
- The whole section must feel like Vajiram/Drishti style revision notes.
- Keep the tone academic, exam-focused, and attractive.

C. PRACTICE MCQs

Generate exactly 10 UPSC standard MCQs.

Pattern:
- 5 Statement based
- 3 Match the following
- 2 Factual

Difficulty:
- 3 Easy
- 5 Moderate
- 2 Tough

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
