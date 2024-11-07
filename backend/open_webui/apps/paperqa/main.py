
import json
import logging
import os
from pathlib import Path
import time
from typing import Any, Optional, TypedDict, Union

import aiohttp
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import files
from open_webui.apps.ollama.main import ChatMessage, get_ollama_url
from open_webui.apps.webui.models.models import ModelModel, Models
from open_webui.config import (CORS_ALLOW_ORIGIN, ENABLE_MODEL_FILTER,
                               MODEL_FILTER_LIST, RAG_PAPERQA_TEMPERATURE,
                               UPLOAD_DIR, AppConfig)
from open_webui.env import SRC_LOG_LEVELS
from open_webui.utils.utils import get_verified_user
from paperqa import Answer, Docs, Settings, ask
from pydantic import HttpUrl, BaseModel

"""
class GenerateChatCompletionForm(BaseModel):
    model: str
    messages: list[ChatMessage]
    format: Optional[str] = None
    options: Optional[dict] = None
    template: Optional[str] = None
    stream: Optional[bool] = None
    keep_alive: Optional[Union[int, str]] = None
"""


class FileMeta(BaseModel):
    name: str
    content_type: str
    size: int
    path: str


class FileInfo(BaseModel):
    created_at: int
    filename: str
    id: str
    meta: FileMeta
    user_id: str


class FileResponse(BaseModel):
    collection_name: str
    error: str
    file: FileInfo
    id: str
    name: str
    size: int
    status: str
    type: str
    url: HttpUrl


class GenerateChatCompletionForm(BaseModel):
    model: str
    messages: list[ChatMessage]
    format: Optional[str] = None
    options: Optional[dict] = None
    template: Optional[str] = None
    stream: Optional[bool] = None
    keep_alive: Optional[Union[int, str]] = None
    files: Optional[list[FileResponse]] = None


log: logging.Logger = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["PAPERQA"])

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.config = AppConfig()

app.state.config.MODEL_FILTER_LIST = MODEL_FILTER_LIST
app.state.config.ENABLE_MODEL_FILTER = ENABLE_MODEL_FILTER
app.state.config.RAG_PAPERQA_TEMPERATURE = RAG_PAPERQA_TEMPERATURE


async def paperqa_inference(
    model: str, ollama_url: str, form_data: GenerateChatCompletionForm, temperature: Optional[float] = 0.2
):

    if not "ollama" in model:
        model = f"ollama/{model}"

    if form_data.files is not None:
        chat_documents: list[str] = [
            file.file.meta.path for file in form_data.files]
        local_llm_config: dict[str, list[dict[str, str | dict[str, str | list[ChatMessage]]]]] = {
            "model_list": [
                {
                    "model_name": model,
                    "litellm_params": {
                        "model": model,
                        "api_base": ollama_url,
                    },
                }
            ]
        }

        if form_data.messages:
            local_llm_config["model_list"][0]["litellm_params"]["messages"] = form_data.messages

        settings = Settings(
            llm=model,
            llm_config=local_llm_config,
            summary_llm=model,
            summary_llm_config=local_llm_config,
            temperature=temperature,
            embedding=model,
        )

        docs = Docs()
        log.info("Starting PaperQA inference with uploaded files")

        load_start_time = time.time()
        for doc in chat_documents:
            await docs.aadd(Path(doc), settings=settings)
        load_end_time = time.time()

        eval_start_time = time.time()
                
        current_query = form_data.messages[-1].content
        answer: Answer = await docs.aquery(
            query=current_query,
            settings=settings
        )
        eval_end_time = time.time()
        log.info("Completed PaperQA inference with uploaded files")

        answer_dict: dict[str, Any] = answer.model_dump()

        

        citations = {
            "document": [],
            "metadata": [{
                "file_id": str,
                "Name": str,
                "page": int,
                "source": str,
                "start_index": int
            }],
            "source": {
                "collection_name": str,
                "error": str,
                "file": FileInfo,
                "id": str,
                "name": str,
                "size": int,
                "status": str,
                "type": str,
                "url": HttpUrl
            }
        }

        contexts = answer_dict.get("contexts", [])
        if contexts:
            for context in contexts:
                citations["document"].append(context["text"]["text"])
                citations["metadata"].append({
                    "file_id": context["text"]["doc"]["dockey"],
                    "Name": context["text"]["doc"]["docname"],
                    "page": 1,
                    "source": context["text"]["doc"]["citation"],
                    "start_index": 0
                })

        info: dict[str, int | float] = {
            "eval_count": answer_dict["token_counts"][model][0],
            "eval_duration": eval_end_time - eval_start_time * 1000,
            "load_duration": load_end_time - load_start_time * 1000,
            "prompt_eval_count": answer_dict["token_counts"][model][1],
            "prompt_eval_duration": 0,
            "total_duration": eval_end_time - load_start_time * 1000,
        }
        
        
        yield json.dumps({"message": {"content": answer_dict["answer"]},"context": answer_dict["context"], "info": info, "done": False}) + "\n"
        
        docs.clear_docs()
        
        yield json.dumps({"message": {"content": ""}, "context": answer_dict["context"], "info": info, "done": True}) + "\n"


@app.post("/api/chat/")
@app.post("/api/chat/{url_idx}")
async def generate_paperqa_chat_completion(
    form_data: GenerateChatCompletionForm,
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
) -> StreamingResponse:
    payload: dict[str, Any] = {**form_data.model_dump(exclude_none=True)}
    log.debug(f"{payload = }")
    print("form_data: ", form_data)
    if "metadata" in payload:
        del payload["metadata"]

    model_id: str = form_data.model

    if app.state.config.ENABLE_MODEL_FILTER:
        if user.role == "user" and model_id not in app.state.config.MODEL_FILTER_LIST:
            raise HTTPException(
                status_code=403,
                detail="Model not found",
            )

    model_info: ModelModel | None = Models.get_model_by_id(model_id)

    if model_info:
        if model_info.base_model_id:
            payload["model"] = model_info.base_model_id

        params = model_info.params.model_dump()

        if params:
            if payload.get("options") is None:
                payload["options"] = {}

    if ":" not in payload["model"]:
        payload["model"] = f"{payload['model']}:latest"

    url = get_ollama_url(url_idx, payload["model"])

    log.info(f"url: {url}")
    log.debug(payload)

    return StreamingResponse(
        paperqa_inference(model=payload["model"],
                          ollama_url=url, form_data=form_data),
        media_type="application/json",
    )
