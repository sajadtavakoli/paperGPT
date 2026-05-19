from papergpt.chunking import chunk_pages

def test_chunk_pages():
    pages = [{"page": 1, "text": "a " * 1000}]
    chunks = chunk_pages(pages, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert chunks[0]["page"] == 1
