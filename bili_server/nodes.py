#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-15

from bili_server.generate_chain import create_generate_chain


class GraphNodes:
    def __init__(self, llm, retriever, retrieval_grader, hallucination_grader, code_evaluator, question_rewriter):
        self.llm = llm
        self.retriever = retriever
        self.retrieval_grader = retrieval_grader
        self.hallucination_grader = hallucination_grader
        self.code_evaluator = code_evaluator
        self.question_rewriter = question_rewriter
        self.generate_chain = create_generate_chain(llm)

    async def retrieve(self, state):
        """
        根据输入问题检索文档，并将它们添加到图状态中。
        Retrieve documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        print("---节点：开始检索---")
        question = state["input"]

        # 执行检索
        documents = await self.retriever.get_retriever(keywords=[question], page=1)
        print(f"这是检索到的Docs:{documents}")
        return {"documents": documents, "input": question}

    def generate(self, state):
        """
        使用输入问题和检索到的文档生成答案，并将生成添加到图形状态中。
        Generate answer

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("---节点：生成响应---")

        question = state["input"]
        documents = state["documents"]

        # 基于RAG生成
        generation = self.generate_chain.invoke({"context": documents, "input": question})
        print(f"生成的响应为:{generation}")
        return {"documents": documents, "input": question, "generation": generation}

    def grade_documents(self, state):
        """
        重新表述输入问题以提高其清晰度和相关性，并使用转换后的问题更新图状态。
        Determines whether the retrieved documents are relevant to the question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with only filtered relevant documents
        """
        print("---节点：检查检索到的文档是否与问题相关---")
        question = state["input"]
        documents = state["documents"]


        filtered_docs = []

        for d in documents:
            score = self.retrieval_grader.invoke({"input": question, "document": d.page_content})
            grade = score["score"]
            if grade == "yes":
                print("---评估结果: 检索文档与问题相关---")
                filtered_docs.append(d)
            else:
                print("---评估结果: 检索文档与问题不相关---")
                continue

        return {"documents": filtered_docs, "input": question}

    def transform_query(self, state):
        """
        Transform the query to produce a better question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a re-phrased question
        """
        print("---节点：重写用户输入的问题---")

        question = state["input"]
        documents = state["documents"]

        # 问题重写
        better_question = self.question_rewriter.invoke({"input": question})
        print(f"这是重写的问题:{better_question}")
        return {"documents": documents, "input": better_question}
