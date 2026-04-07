
def split_text_chunk(text, chunk_size=300, overlap=30):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]      
        # avoid too short segments
        if len(chunk) > 30:
            chunks.append(" ".join(chunk))

        start += chunk_size - overlap

    return chunks
