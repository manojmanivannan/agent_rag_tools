from langchain import hub
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader

import os
# from .language_model import retriever_agent

persist_directory = './chromadb'
embeddings = OllamaEmbeddings(base_url='http://localhost:11434', model='llama3')




if os.path.exists(persist_directory):

    print('Loading from disk')
    db = Chroma(embedding_function=embeddings,collection_name='tools-knowledge', persist_directory=persist_directory)

else:

    raw_documents = DirectoryLoader('./docs/', glob="**/*.txt", show_progress=True).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
    documents = text_splitter.split_documents(raw_documents)

    print('Writing to disk')
    db = Chroma.from_documents(documents=documents, embedding=embeddings, collection_name='tools-knowledge', persist_directory=persist_directory)



