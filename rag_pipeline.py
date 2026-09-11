from langchain_groq import ChatGroq
from config import GROQ_API_KEY


def create_llm():
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="openai/gpt-oss-20b",
        temperature=0
    )

    return llm


def generate_answer(llm, question, documents):
    context = "\n\n".join(
        document.page_content for document in documents
    )

    prompt = f"""
You are DocuMind, a document question-answering assistant.

Answer the user's question using ONLY the information provided
in the document context below.

IMPORTANT: Never use LaTeX. Never use \frac, \displaystyle, or any backslash notation. Write all math in plain text only (e.g. 1/f = 1/v - 1/u).
If the answer cannot be found in the context, say:
"I could not find the answer in the document."

Document context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content