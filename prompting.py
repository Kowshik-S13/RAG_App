
from langchain_core.prompts import PromptTemplate
def zero_shot_template():
    return PromptTemplate.from_template("Answer the following question about the insurance policy report:\n{query}")

def context_injection_template():
    return PromptTemplate.from_template("Context:\n{context}\n\nQuestion: {query}\nAnswer:")