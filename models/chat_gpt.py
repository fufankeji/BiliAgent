#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-16

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# https://platform.openai.com/docs/api-reference/chat?lang=python
from openai import OpenAI

# 在.env文件中填写自己的APIKey
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

completion = client.chat.completions.create(
    model=os.getenv("model"),
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(completion.choices[0].message.content)
