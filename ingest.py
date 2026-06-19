from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def ingest_pdf(pdf_path):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("Pages Loaded:", len(documents))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)
    
    print("Chunks Created:", len(docs))

    emb = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore=Chroma.from_documents(
        documents=docs,
        embedding=emb,
        persist_directory="agreements_db"
    )
    print(
    "Stored Documents:",
    vectorstore._collection.count()
)
    return "PDF Ingested Successfully"

if __name__ == "__main__":
    ingest_pdf(
        r"C:\Users\Rithish\Downloads\rag_project\AWS_RAG\AWS Customer Agreement.pdf"
    )