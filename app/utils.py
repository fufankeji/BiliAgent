#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-15

from langchain_openai import ChatOpenAI
from bili_server.document_loader import DocumentLoader
from bili_server.edges import EdgeGraph
from bili_server.generate_chain import create_generate_chain
from bili_server.graph import GraphState
from bili_server.grader import GraderUtils
from bili_server.nodes import GraphNodes

from langgraph.graph import END, StateGraph


def create_parser_components(api_key: str, model: str):
    """
    创建并初始化解析器组件和评分器实例。

    Args:
    api_key (str): 用于访问OpenAI服务的API密钥。

    Returns:
    dict: 包含所有创建的组件实例的字典。
    """

    # 创建 retriever 实例，用于文档检索
    retriever = DocumentLoader()

    # 创建 LLM model 实例，配置为使用 GPT-4o 模型和指定的温度参数
    llm = ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=0
    )

    # 创建生成链，用于基于语言模型的生成任务
    generate_chain = create_generate_chain(llm)

    # 初始化评分器实例，用于创建和管理多种评分工具
    grader = GraderUtils(llm)

    # 创建评估检索文档与用户问题相关性的评分器
    retrieval_grader = grader.create_retrieval_grader()

    # 创建评估模型的回答是否出现幻觉的评分器
    hallucination_grader = grader.create_hallucination_grader()

    # 创建代码评估器，用于评估代码执行结果的正确性
    code_evaluator = grader.create_code_evaluator()

    # 创建问题重写器，用于优化用户问题，使其更适合模型理解和回答
    question_rewriter = grader.create_question_rewriter()

    # 返回包含所有组件的字典，以便在其他部分的代码中使用
    return {
        "llm": llm,
        "retriever": retriever,
        "generate_chain": generate_chain,
        "retrieval_grader": retrieval_grader,
        "hallucination_grader": hallucination_grader,
        "code_evaluator": code_evaluator,
        "question_rewriter": question_rewriter
    }


def create_workflow(api_key: str, model: str):
    """
    创建并初始化工作流以及其组成的节点和边。

    Returns:
    StateGraph: 完全初始化和编译好的工作流对象。
    """

    # 调用函数并直接解构字典以获取所有实例
    (llm, retriever, generate_chain,
     retrieval_grader, hallucination_grader,
     code_evaluator, question_rewriter) = create_parser_components(api_key, model).values()

    # 初始化图结构
    workflow = StateGraph(GraphState)

    # 创建图节点的实例
    graph_nodes = GraphNodes(llm, retriever, retrieval_grader, hallucination_grader, code_evaluator, question_rewriter)

    # 创建边节点的实例
    edge_graph = EdgeGraph(hallucination_grader, code_evaluator)

    # 定义节点
    workflow.add_node("retrieve", graph_nodes.retrieve)  # retrieve documents
    workflow.add_node("grade_documents", graph_nodes.grade_documents)  # grade documents
    workflow.add_node("generate", graph_nodes.generate)  # generate answers
    workflow.add_node("transform_query", graph_nodes.transform_query)  # transform query

    # 创建图
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        edge_graph.decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        }
    )
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_conditional_edges(
        "generate",
        edge_graph.grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": END,
            "not useful": "transform_query",
        }
    )

    # 编译图
    chain = workflow.compile()
    return chain


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())

    create_workflow(os.getenv('OPENAI_API_KEY'),
                    os.getenv('model'),
                    )
