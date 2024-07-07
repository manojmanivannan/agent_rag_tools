from langchain_community.chat_models import ChatOllama
from langchain_experimental.llms.ollama_functions import OllamaFunctions

# llm = ChatOllama(model='llama3', temperature=0)
# llm.base_url = 'http://localhost:11434'

llm = OllamaFunctions(model="llama3", format='json')
llm.base_url = 'http://localhost:11434'