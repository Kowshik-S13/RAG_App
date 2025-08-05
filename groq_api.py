
def get_reponse(prompt):
    from langchain_groq import ChatGroq


    llm = ChatGroq(api_key="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", model="llama-3.1-8b-instant")

    response = llm.invoke(prompt).content.strip()
    
    return response