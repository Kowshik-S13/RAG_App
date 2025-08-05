import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_core.documents import Document
#UnboundLocalError: cannot access local variable 'all_docs' where it is not associated with a value

def load_file(uploaded_files):
    all_docs = ""
    filepaths = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_path = tmp_file.name
                if uploaded_file.name.endswith(".pdf"):
                    loader = PyPDFLoader(temp_path)
                    docs = loader.load()
                elif uploaded_file.name.endswith(".txt"):
                    loader = TextLoader(temp_path)
                    docs = loader.load()
                elif uploaded_file.name.endswith(".docx"):
                    loader = Docx2txtLoader(temp_path)
                    docs = loader.load()
                else:
                    docs = []
            all_docs += "\n\n".join([doc.page_content for doc in docs])
            filepaths.append(uploaded_file.name)
    return all_docs, filepaths