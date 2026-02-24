from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# 1. Load PDF
loader = PyPDFLoader("sample.pdf")
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs = text_splitter.split_documents(documents)

# 3. Create embeddings (local model)
embedding = HuggingFaceEmbeddings()

# 4. Store in Chroma DB
vectorstore = Chroma.from_documents(
    docs,
    embedding,
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever()

# 5. Use local Ollama model
llm = Ollama(model="llama3")

# 6. RAG chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)

while True:
    query = input("\nAsk a question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    result = qa.run(query)
    print("\nAnswer:", result)