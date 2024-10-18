#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-17
import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# LangChain Docs:https://python.langchain.com/docs/integrations/chat/openai/

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
)

messages = [
    (
        "system", "You are a helpful assistant that translates English to Chinese. Translate the user sentence.",
    ),
    (
        "human", "I love programming."
    ),
]

ai_msg = llm.invoke(messages)
print(ai_msg.content)
