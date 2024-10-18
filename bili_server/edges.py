class EdgeGraph:
    def __init__(self, hallucination_grader, code_evaluator):
        self.hallucination_grader = hallucination_grader
        self.code_evaluator = code_evaluator

    def decide_to_generate(self, state):
        """
        根据过滤后的文档与输入问题的相关性确定是生成答案还是重新生成问题。如果所有文档都不相关，则决定转换查询；否则，它决定生成答案。
        Determines whether to generate an answer, or re-generate a question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Binary decision for next node to call
        """
        print("---进入检索文档与问题相关性判断---")

        filtered_documents = state["documents"]

        if not filtered_documents:
            print("---决策：所有检索到的文档均与问题无关，转换查询---")
            return "transform_query"
        else:

            print("---决策：生成最终响应---")
            return "generate"

    def grade_generation_v_documents_and_question(self, state):
        """
        根据文档的基础及其解决问题的能力来评估生成的答案。如果基于既定事实解决了问题，那么它被认为是有用的；否则，它不受支持或无用。
        Determines whether the generation is grounded in the document and answers question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Decision for next node to call
        """
        print("---检查是否输入模型幻觉输出---")
        question = state["input"]
        documents = state["documents"]
        generation = state["generation"]

        score = self.hallucination_grader.invoke({"documents": documents, "generation": generation})
        grade = score["score"]

        if grade == "yes":
            print("---决策: 生成内容是基于检索到的文档的既定事实---")

            print("---检查最终响应是否与输入的问题相关---")
            score = self.code_evaluator.invoke({"input": question, "generation": generation, "documents": documents})
            grade = score["score"]
            if grade == "yes":
                print("---判定: 生成响应与输入问题相关---")
                return "useful"
            else:
                print("---判定: 生成响应与输入问题不相关---")
                return "not useful"
        else:
            print("---判定：生成响应与检索文档不相关，模型进入幻觉状态---")
            return "not supported"
