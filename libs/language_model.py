from langchain_community.chat_models import ChatOllama
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain import hub
from langchain.agents import create_react_agent
from .rag import db
from .tool_def import get_metric_values, get_unique_dimension_values
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

# llm = ChatOllama(model='llama3', temperature=0)
# llm.base_url = 'http://localhost:11434'

model = ChatOllama(model="llama3-groq-tool-use")
model.base_url = 'http://localhost:11434'

# prompt = hub.pull('hwchase17/react')
prompt = PromptTemplate(template=f"""
Answer the following questions as best you can. You have access to the following tools:

{{tools}}

Use the following format:

Question: the input question you must answer

Thought: you should always think about what to do

Action: the action to take, should be one of [{{tool_names}}]

Action Input: the input to the action

Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer

Final Answer: the final answer to the original input question.

Begin!

Question:{{input}}.

Thought:{{agent_scratchpad}}.""",
input_variables=['input']
)

tools = [get_unique_dimension_values, get_metric_values]

agent_runnable = create_react_agent(model, tools, prompt)



from langchain_community.llms import Ollama

retriever_agent = Ollama(model='llama3', base_url='http://localhost:11434', callback_manager=CallbackManager([StreamingStdOutCallbackHandler]))

from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    retriever_agent,
    retriever=db.as_retriever(),
    chain_type_kwargs={"prompt": hub.pull("rlm/rag-prompt-llama")}
)
