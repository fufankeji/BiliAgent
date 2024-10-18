#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-16

# https://bigmodel.cn/

import os
from zhipuai import ZhipuAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# 在.env文件中填写自己的APIKey
client = ZhipuAI(api_key=os.getenv("GLM_API_KEY"))
response = client.chat.completions.create(
    model="glm-4-plus",  # 填写需要调用的模型编码
    messages=[
        {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
        {"role": "user", "content": "农夫需要把狼、羊和白菜都带过河，但每次只能带一样物品，而且狼和羊不能单独相处，羊和白菜也不能单独相处，问农夫该如何过河。"}
    ],
)
print(response.choices[0].message)