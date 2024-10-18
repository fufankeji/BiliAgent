#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-15


from langchain_core.documents import Document
from bilibili_tools import get_bilibi
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentLoader:
    """
    This class uses the get_docs function to take a Keyword as input, and outputs a list of documents (including metadata).
    """

    async def get_docs(self, keywords: List[str], page: int) -> List[Document]:
        """
        Asynchronously retrieves documents based on specific keywords from the BiliBili API.
        This function utilizes a pipeline to fetch and format video data, returning it as Document objects.

        Args:
        keywords (List[str]): A list of keywords used to query the BiliBili API.
        page (int): The page number in the API request, used for pagination.

        Returns:
            List[Document]: A list of Document objects containing the retrieved content.
        """

        raw_docs = await get_bilibi.bilibili_detail_pipiline(keywords=keywords, page=page)

        docs = [Document(page_content=doc["real_data"]) for doc in raw_docs]

        return docs

    async def create_vector_store(self, docs, store_path: Optional[str] = None) -> 'FAISS':
        """
        Creates a FAISS vector store from a list of documents.

        Args:
            docs (List[Document]): A list of Document objects containing the content to be stored.
            store_path (Optional[str]): The path to store the vector store locally. If None, the vector store will not be stored.

        Returns:
            FAISS: The FAISS vector store containing the documents.
        """
        # 执行文本切分，并使用OpenAI Embedding模型生成向量表示
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
        texts = text_splitter.split_documents(docs)
        embedding_model = OpenAIEmbeddings()
        store = FAISS.from_documents(texts, embedding_model)

        if store_path:
            store.save_local(store_path)
        return store

    async def get_retriever(self, keywords: List[str], page: int):
        """
        Retrieves documents and returns a retriever based on the documents.

        Args:
            keywords (List[str]): Keywords to search documents.
            page (int): Page number for pagination of results.

        Returns:
            Retriever instance or FAISS vector store.
        """
        print(f"开始实时查询BiliBiliAPI获取数据")
        docs = await self.get_docs(keywords, page)
        print(f"接收到的BiliBili数据为：{docs}")
        print("-------------------------")
        print(f"开始进行向量数据库存储")
        vector_store = await self.create_vector_store(docs)
        print(f"成功完成向量数据库的存储")
        print("-------------------------")
        print(f"开始进行文本检索")
        retriever = vector_store.as_retriever(search_kwargs={"k": 10})
        retriever_result = retriever.invoke(str(keywords))
        print(f"检索到的数据为：{retriever_result}")
        return retriever_result


if __name__ == '__main__':
    import asyncio

    # 创建 DocumentLoader 实例并调用 get_docs
    async def main():
        loader = DocumentLoader()
        await loader.get_retriever(keywords=["ChatGLM3-6b"], page=1)

    asyncio.run(main())
