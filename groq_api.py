
def get_reponse(prompt):
    from langchain_groq import ChatGroq


    llm = ChatGroq(api_key="<API_KEY>", model="llama-3.1-8b-instant")

    response = llm.invoke(prompt).content.strip()
    
    return response