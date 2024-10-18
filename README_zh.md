# BiliAgent：BiliBili热点 & 舆情实时分析智能体

![136439902d507ef41f9f746bddd47fc](https://muyu001.oss-cn-beijing.aliyuncs.com/img/20241018001.jpg)

<p align="center">
  <a href="README.md"><strong>English</strong></a> | 
  <a href="docs/wechat.png"><strong>微信</strong></a>
</p>

## 项目简介
BiliAgent 是一个基于大模型构建的复杂 AI Agent 应用工具，该应用工具在网页端接收用户输入，后端实时调用 Bilibili API，可以依据用户的输入的问题需求去查询实时数据，得到结果后，自主执行数据分析过程，最终生成精准的回复或数据分析报告，通过前端返回给用户。例如，用户可以在该工具中提出以下需求：

- 我正在学习 Chat GLM 模型的部署，请查找当前哪些相关视频的好评最多，返回当前视频的链接及你推荐的理由
- 我准备发布一个 Swarm 技术相关的视频，请根据当前热门视频的标题和描述，生成一个热门标题，帮助我提升关注度

  

## 核心技术

**在项目架构方面**，BiliAgent是一个端到端的服务，采用前后端分离架构。后端结合 LangServe 和 FastAPI 技术，利用 LangServe 的 add_routes 接口，将 LangChain 应用中的链和 RAG服务 封装成 REST API，具备高并发请求、流式传输和异步操作的能力。前端界面由 Streamlit 构建，主要聚焦于简洁的用户交互而非复杂的视觉表现。**在技术应用方面**，核心的 AI Agent 框架由 LangGraph 提供支持，基础的模型调用则通过 LangChain 实现，支持目前国内外最热门的 GPT 系列（国外）和 GLM4 模型（国内）。

- **技术栈**
- **AI Agent 框架**: LangGraph
  
- **模型调用**: 基于LangChain支持主流的在线& 开源模型 
  
- **前端技术**: Streamlit
  
- **后端技术**: LangServe + FastAPI
  
- **嵌入模型**: OpenAI Embedding, GLM Embedding
  
- **状态追踪**: LangSmith
  <br>
  <br>
- **业务逻辑流程图**
<div align="center">
  <img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/20241016001.png" width="700"/>
  </div>
<br>
<br>


- **完整项目架构图**

<div align="center">
  <img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/20241016002.png" width="700"/>
  </div>
<br>
<br>


- **核心功能开发流程图**

<div align="center">
  <img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/202410180010.png" width="200"/>
  </div>
<br>
<br>


## 安装指南
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

## 更多功能源码

此版本为基础版，更精细化的BiliBili数据 & 舆情分析实现源码及细节，请加入技术交流群探讨。**<span style="color:red;">扫码添加客服小可爱木登，回复“BiliAgent”详询哦👇</span>**

<div align="center">
<img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20241016153337.jpg" width="200"/>
</div>

## 如何贡献

欢迎通过 Pull Requests 或 Issues 来提交你的贡献或反馈。我们非常欢迎各种形式的贡献，包括但不限于新功能的建议、代码优化、文档改进等。
