
from langchain_community.embeddings import SentenceTransformerEmbeddings
import torch

def get_embedding_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return SentenceTransformerEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={"device": device}
    )