from docx import Document
import pdfplumber

import tempfile

def load_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])

def load_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def load_txt(file):
    return file.read().decode("utf-8")

def load_file(uploaded_file):
    if not uploaded_file:
        return "-1"
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file.flush()
            file_path = tmp_file.name

    if uploaded_file.name.endswith(".docx"):
        text = load_docx(file_path)
    elif uploaded_file.name.endswith(".pdf"):
        text = load_pdf(file_path)
    elif uploaded_file.name.endswith(".txt"):
        with open(file_path, "rb") as f:
            text = load_txt(f)
    else:
        return "-1"
    return text, file_path