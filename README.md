# BiliAgent: BiliBili Hotspots & Public Opinion Real-Time Analysis Agent

![136439902d507ef41f9f746bddd47fc](https://muyu001.oss-cn-beijing.aliyuncs.com/img/20241018001.jpg)

<p align="center">
  <a href="README_zh.md"><strong>中文</strong></a> | 
  <a href="docs/wechat.png"><strong>WeChat</strong></a>
</p>

## Project Introduction
BiliAgent is a complex AI Agent application built on large models. This tool receives user input on the web front-end, and the back-end calls the Bilibili API in real time. Based on the user's input, it queries real-time data, autonomously conducts data analysis, and generates precise responses or data analysis reports, which are then returned to the user through the front-end. For example, users can request:
- I am learning about deploying the Chat GLM model. Please find the most positively reviewed relevant videos and return the links along with your recommendations.
- I am preparing to release a video about Swarm technology. Please generate a trending title based on current popular video titles and descriptions to help me gain more attention.

<div align="center">
<img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/image-20241018111329177.png" alt="image-20240713010710534" width="600"/>
</div>

## Core Technology

**In terms of project architecture**, BiliAgent is an end-to-end service using a front-end/back-end separation architecture. The backend combines LangServe and FastAPI technologies, utilizing the LangServe's `add_routes` interface to encapsulate chains and RAG services from LangChain into REST APIs. It supports high-concurrency requests, streaming, and asynchronous operations. The frontend is built with Streamlit, focusing on simple user interaction rather than complex visual presentation. **In terms of technology application**, the core AI Agent framework is provided by LangGraph, and the basic model invocation is done through LangChain, supporting the most popular GPT series (international) and GLM4 models (domestic).

- **Technology Stack**

  - **AI Agent Framework**: LangGraph

  - **Model Invocation**: Supports mainstream online & open-source models through LangChain

  - **Frontend Technology**: Streamlit

  - **Backend Technology**: LangServe + FastAPI

  - **Embedded Models**: OpenAI Embedding, GLM Embedding

  - **State Tracking**: LangSmith

- **Business Logic Flowchart**
<div align="center">
<img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/20241016001.png" width="700"/>
</div>

- **Complete Project Architecture**
<div align="center">
<img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/20241016002.png" width="700"/>
</div>

- **Core Function Development Flowchart**
<div align="center">
  <img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/20241018007.png" width="700"/>
</div>

## Installation Guide
```bash
# 克隆仓库
git clone https://github.com/fufankeji/BiliAgent.git

# 安装依赖
cd BiliAgent
pip install -r requirements.txt

# 修改.env.bak文件 为 .env

# 在.env文件中填写OpenAI API Key

# 运行服务端
python app/client

# 运行客户端
streamlit run app/client.py
```

## More Functionality Source Code

This version is the basic edition. For more refined implementations and details of BiliBili data & public opinion analysis, please join our technical exchange group. **<span style="color:red;">Scan to add our customer service agent Mudeng, and reply with “BiliAgent” for detailed inquiries 👇</span>**

<div align="center">
<img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20241016153337.jpg" width="200"/>
</div>

## How to Contribute

We welcome contributions via Pull Requests or Issues. All forms of contributions are greatly appreciated, including but not limited to new feature suggestions, code optimizations, and documentation improvements.


