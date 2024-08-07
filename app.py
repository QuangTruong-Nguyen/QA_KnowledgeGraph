import chainlit as cl
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from react_agent_v2 import get_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory



@cl.on_chat_start
async def on_chat_start():
    message_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key = "chat_history",
        output_key = "output",
        chat_memory = message_history,
        return_message = True
    )
    
    agent_executor = get_react_agent(memory)
    cl.user_session.set("runnable", agent_executor)

    
@cl.on_message
async def on_message(message: cl.Message):


    llm_chain = cl.user_session.get("runnable")

    response = llm_chain.invoke(
        {"input": message.content}, callbacks = [cl.LangchainCallbackHandler()]
    )

    await cl.Message(response["output"].replace("`", "")).send()