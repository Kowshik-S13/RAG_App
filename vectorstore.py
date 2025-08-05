
from langchain_community.vectorstores import Weaviate

def get_context(client, embedder, query, chunks):
    vectorstore = Weaviate(
            client=client,
            index_name="InsuranceChunk",
            embedding=embedder,
            text_key="text"
        )

    vectorstore.add_texts(chunks)
    query_emb = embedder.embed_query(query)
    docs = vectorstore.similarity_search_by_vector(query_emb, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    return context