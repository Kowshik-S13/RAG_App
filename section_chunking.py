import nltk
nltk.download('punkt')


def section_chunking(text, max_chunk_size=800, overlap=0):
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 > max_chunk_size:
            if len(para) > max_chunk_size:
                sentences = nltk.sent_tokenize(para)
                temp_chunk = ""
                for sentence in sentences:
                    if len(temp_chunk) + len(sentence) + 1 <= max_chunk_size:
                        temp_chunk += sentence + " "
                    else:
                        chunks.append(temp_chunk.strip())
                        temp_chunk = sentence + " "
                if temp_chunk:
                    chunks.append(temp_chunk.strip())
                current_chunk = ""
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        else:
            current_chunk += para + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    if overlap > 0 and len(chunks) > 1:
        overlapped_chunks = []
        for i in range(len(chunks)):
            chunk = chunks[i]
            if i > 0:
                overlap_text = chunks[i-1][-overlap:]
                chunk = overlap_text + " " + chunk
            overlapped_chunks.append(chunk.strip())
        chunks = overlapped_chunks

    return chunks