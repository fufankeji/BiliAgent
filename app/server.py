#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: MuyuCheney
# Date: 2024-10-15

import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from pydantic import BaseModel
from utils import create_workflow

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# 初始化图节点的工作流
chain = create_workflow(os.getenv('OPENAI_API_KEY'),
                        os.getenv('model'),
                        )


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: dict


app = FastAPI(
    title="BiliAgent Server",
    version="1.0",
    description="An API named bili_server designed specifically for real-time retrieval of live data from BiliBili."
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# 添加路由
add_routes(
    app,
    chain.with_types(input_type=Input, output_type=Output),
    path="/biliagent_chat",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
