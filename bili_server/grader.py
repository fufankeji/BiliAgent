#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-15

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class GraderUtils:
    def __init__(self, model):
        self.model = model

    def create_retrieval_grader(self):
        """
        Creates a retrieval grader that assesses the relevance of a retrieved document to a user question.

        Returns:
            A callable function that takes a document and a question as input and returns a JSON object with a binary score indicating whether the document is relevant to the question.
        """

        # 使用的特殊标记是为了指定不同部分的开始和结束，以及明确不同类型的文本块。
        # 这些标记可以帮助大模型更好地理解和区分输入数据的不同部分，从而更精确地执行特定的任务。
        # 您是一名评分员，负责评估检索到的文档与用户问题的相关性。如果文档包含与用户问题相关的关键词，请将其评为相关。这不需要非常严格的测试。目标是过滤掉错误的检索结果。
        grade_prompt = PromptTemplate(
            template="""
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are a grader assessing relevance of a retrieved document to a user question. If the document contains keywords related to the user question, grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals.
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
            Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>

            Here is the retrieved document: \n\n {document} \n\n
            Here is the user question: {input} \n
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>
            """,
            input_variables=["document", "input"],
        )

        # 创建一个 检索 的链
        retriever_grader = grade_prompt | self.model | JsonOutputParser()

        return retriever_grader

    # 您是一名评分员，负责评估答案是否基于/得到一组事实的支持。请给出“是”或“否”的二元评分，以表明答案是否基于/得到事实的支持。提供一个只有一个键“score”的JSON，不需要前言或解释。
    def create_hallucination_grader(self):
        """
        Creates a hallucination grader that assesses whether an answer is grounded in/supported by a set of facts.

        Returns:
            A callable function that takes a generation (answer) and a list of documents (facts) as input and returns a JSON object with a binary score indicating whether the answer is grounded in/supported by the facts.
        """
        hallucination_prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are a grader assessing whether an answer is grounded in / supported by a set of facts. Give a binary score 'yes' or 'no' score to indicate whether the answer is grounded in / supported by a set of facts. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>
            Here are the facts:
            \n ------- \n
            {documents}
            \n ------- \n
            Here is the answer: {generation}
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "documents"],
        )

        hallucination_grader = hallucination_prompt | self.model | JsonOutputParser()

        return hallucination_grader

    def create_code_evaluator(self):
        """
        Creates a code evaluator that assesses whether the generated code is correct and relevant to the given question.

        Returns:
            A callable function that takes a generation (code), a question, and a list of documents as input and returns a JSON object with a binary score and feedback.
        """
        eval_template = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a code evaluator assessing whether the generated code is correct and relevant to the given question.
            Provide a JSON response with the following keys:

            'score': A binary score 'yes' or 'no' indicating whether the code is correct and relevant.
            'feedback': A brief explanation of your evaluation, including any issues or improvements needed.

            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Here is the generated code:
            \n ------- \n
            {generation}
            \n ------- \n
            Here is the question: {input}
            \n ------- \n
            Here are the relevant documents: {documents}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "input", "documents"],
        )

        code_evaluator = eval_template | self.model | JsonOutputParser()

        return code_evaluator

    # 您是一个问题重写器，将输入的问题转换成更好的版本，优化以适应向量存储检索。请查看输入并尝试理解其潜在的语义意图/含义。
    def create_question_rewriter(self):
        """
        Creates a question rewriter chain that rewrites a given question to improve its clarity and relevance.

        Returns:
            A callable function that takes a question as input and returns the rewritten question as a string.
        """
        re_write_prompt = PromptTemplate(
            template="""
            You a question re-writer that converts an input question to a better version that is optimized for vectorstore retrieval. Look at the input and try to reason about the underlying sematic intent / meaning.

            Here is the initial question: {input}

            Formulate an improved question.""",

            input_variables=["input"],
        )

        question_rewriter = re_write_prompt | self.model | StrOutputParser()

        return question_rewriter


if __name__ == '__main__':
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("model"),
    )

    # 创建一个评分器类的实例
    grader = GraderUtils(llm)

    # # 创建一个检索的评估器
    # retrieval_grader = grader.create_retrieval_grader()
    #
    # # 这是不相关的
    # retrieval_grader_results = retrieval_grader.invoke({
    #     "document": "哈哈哈",
    #     "input": "请问关于ChatGLM3-6B热门视频的描述有哪些？"
    # })
    #
    # # 这是相关的
    # # retrieval_grader_results = retrieval_grader.invoke({
    # #     "document": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
    # #     "input": "请问关于ChatGLM3-6B热门视频的描述有哪些？"
    # # })
    #
    # print(f"retrieval_grader_results: {retrieval_grader_results}")

    # # 创建一个检测大模型幻觉的生成器
    # hallucination_grader = grader.create_hallucination_grader()
    #
    # # 这是出现幻觉的回答
    # # hallucination_grader_results = hallucination_grader.invoke({
    # #     "documents": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
    # #     "generation": "你好"
    # # })
    #
    # # 这是基于检索内容生成的回答
    # hallucination_grader_results = hallucination_grader.invoke({
    #     "documents": "这是我查询到的热门视频的描述：ChatGLM3-6B的安装部署、微调、训练智能客服。文档、数据集、微调脚本获取方式：麻烦一键三连，评论后，我会找到评论私发源码，谢谢大家。",
    #     "generation": "一般对于ChatGLM3-6B模型的热门视频，可以从安装部署、微调、训练等方向来思考"
    # })
    #
    # print(f"hallucination_grader_results:{hallucination_grader_results}")
    #
    # # Get the code evaluator
    # code_evaluator = grader.create_code_evaluator()

    # 对输入的问题进行重写
    question_rewriter = grader.create_question_rewriter()
    question_rewriter_results = question_rewriter.invoke({
        "input": "对于ChatGLM3-6B模型，应该如何写热门标题的描述,请你用中文回复"
    })
    print(f"question_rewriter_results: {question_rewriter_results}")
