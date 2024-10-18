#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-15

import os
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def create_generate_chain(llm):
    """
    Creates a generate chain for answering bilibili-related questions.

    Args:
        llm (LLM): The language model to use for generating responses.

    Returns:
        A callable function that takes a context and a question as input and returns a string response.
    """
    generate_template = """
    You are an AI personal assistant named FuFan. Users will pose questions related to BiliBili website data, which are presented in the parts enclosed by <context></context> tags.
    
    Use this information to formulate your answers.
    
    When a user's question requires fetching data using the BiliBili API, you may proceed accordingly.
    If you cannot find an answer, please respond honestly that you do not know. Do not attempt to fabricate an answer.  
    If the question is unrelated to the context, politely respond that you can only answer questions related to the context provided.
    
    For questions involving data analysis, please write the code in Python and provide a detailed analysis of the results to offer as comprehensive an answer as possible.
    
    <context>
    {context}
    </context>
    
    <question>
    {input}
    </question>
    """

    generate_prompt = PromptTemplate(template=generate_template, input_variables=["context", "input"])

    # 没有StrOutputParser() 输出可能如下所示：
    # {
    #     "content": "This is the response from the LLM.",
    #     "metadata": {
    #         "confidence": 0.8,
    #         "response_time": 0.5
    #     }
    # }

    # 使用StrOutputParser() ，它看起来像这样：
    # This is the response from the LLM.

    # Create the generate chain
    generate_chain = generate_prompt | llm | StrOutputParser()

    return generate_chain


if __name__ == '__main__':
    # https://python.langchain.com/docs/integrations/chat/openai/
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'),
                     model=os.getenv('model'),
                     )

    # 创建一个生成链
    generate_chain = create_generate_chain(llm)
    final_answer = generate_chain.invoke({
        "context": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
        "input": "请帮我梳理一下热门视频的描述信息"
    })
    print(final_answer)
