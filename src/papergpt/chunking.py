def chunk_pages(pages, chunk_size=900, overlap=150):
    chunks = []
    for page in pages:
        text = " ".join(page["text"].split())
        start = 0
        while start < len(text):
            chunk = text[start:start + chunk_size]
            if chunk.strip():
                chunks.append({"page": page["page"], "text": chunk})
            start += chunk_size - overlap
    return chunks
