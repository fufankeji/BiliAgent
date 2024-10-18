#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-17
import os

from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# LangChain Docs:https://python.langchain.com/docs/integrations/chat/zhipuai/

# pip install --upgrade httpx httpx-sse PyJWT

chat = ChatZhipuAI(
    api_key=os.getenv("GLM_API_KEY"),
    model="glm-4",
)

messages = [
    AIMessage(content="Hi."),
    SystemMessage(content="Your role is a poet."),
    HumanMessage(content="Write a short poem about AI in four lines."),
]

response = chat.invoke(messages)
print(response.content)