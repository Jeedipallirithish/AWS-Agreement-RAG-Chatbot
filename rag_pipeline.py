from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

# loading existing one 

emb = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="agreements_db",
    embedding_function=emb
)

print(
    "Documents in DB:",
    vectorstore._collection.count()
)
print("Documents in DB:", vectorstore._collection.count())

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)


# prompt 

prompt = PromptTemplate(
    template="""
Answer only from the context.

Context:
{context}

Question:
{question}
"""
)


# setting up llm 
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)


# chains connecting the all as rag_chain
rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)



# creating a function for asking 
#def ask_question(question):

    ##docs = retriever.invoke(question)

    #print("Retrieved Docs:", len(docs))

    #for doc in docs:
       # print(doc.page_content[:200])
       # print("-"*50)

    #answer = rag_chain.invoke(question)

    #return answer, docs


def ask_question(question):

    docs = retriever.invoke(question)

    print("="*50)
    print("Retrieved Docs:", len(docs))
    print("="*50)

    for doc in docs:
        print(doc.page_content[:500])
        print("-"*50)

    answer = rag_chain.invoke(question)

    return answer, docs