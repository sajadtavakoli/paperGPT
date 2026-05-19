from transformers import pipeline

def build_context(retrieved):
    blocks = []
    for i, item in enumerate(retrieved, start=1):
        blocks.append(f"[{i}] Page {item['page']}: {item['text']}")
    return "\n\n".join(blocks)

def answer_with_context(question: str, retrieved, model_name: str = "google/flan-t5-base"):
    context = build_context(retrieved)
    prompt = f"""Answer the question using only the context below.
If the answer is not in the context, say that the paper context is insufficient.
Cite sources as [1], [2], etc.

Context:
{context}

Question: {question}
Answer:"""
    generator = pipeline("text2text-generation", model=model_name)
    return generator(prompt, max_new_tokens=256)[0]["generated_text"]
