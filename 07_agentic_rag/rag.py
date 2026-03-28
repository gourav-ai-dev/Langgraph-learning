from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

def create_retriever():
    loader = TextLoader("data/sample.txt")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )

    docs = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore.as_retriever()