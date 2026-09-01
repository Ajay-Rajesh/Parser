from transformers import pipeline

# Load once when the app starts
llm = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-3B-Instruct",
    device_map="auto"
)

SYSTEM_PROMPT = """
You are an AI document assistant.

Rules:
- Answer ONLY from the provided context.
- If the answer is not in the context, reply: "Not found in the documents."
- Be concise.
- Reply in the same language as the user's question.
"""

def generate_answer(question, chunks):
    context = "\n\n".join(
        f"[Document {i+1}]\n{c['text']}"
        for i, c in enumerate(chunks[:3])
    )

    prompt = f"""{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:"""

    result = llm(
        prompt,
        max_new_tokens=180,
        do_sample=False,
        return_full_text=False
    )

    return result[0]["generated_text"].split("Answer:")[-1].strip()