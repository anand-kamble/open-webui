
import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

import aiohttp
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from open_webui.apps.ollama.main import (GenerateChatCompletionForm,
                                         get_ollama_url, post_streaming_url)
from open_webui.apps.webui.models.models import ModelModel, Models
from open_webui.config import (AIOHTTP_CLIENT_TIMEOUT, CORS_ALLOW_ORIGIN, ENABLE_MODEL_FILTER,
                               MODEL_FILTER_LIST, RAG_PAPERQA_TEMPERATURE,
                               UPLOAD_DIR, AppConfig)
from open_webui.env import SRC_LOG_LEVELS
from open_webui.utils.utils import get_verified_user
from paperqa import Docs, Settings, ask

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


def get_uploaded_files(directory: str) -> list[str]:
    try:
        files: list[str] = os.listdir(Path((directory)))
        return [file for file in files if os.path.isfile(os.path.join(directory, file))]
    except FileNotFoundError:
        return []


async def main(query: str) -> None:
    docs = Docs()
    uploaded_files: list[str] = get_uploaded_files("backend/data/uploads")

    valid_extensions: set[str] = {".pdf", ".txt", ".html"}
    uploaded_files = [file for file in uploaded_files if Path(
        file).suffix in valid_extensions]

    local_llm_config: dict[str, list[dict[str, str | dict[str, str]]]] = {
        "model_list": [
            {
                "model_name": "ollama/llama3.2",
                "litellm_params": {
                    "model": "ollama/llama3.2",
                    "api_base": "http://localhost:11434",
                },
            }
        ]
    }
    settings = Settings(
        llm="ollama/llama3.2",
        llm_config=local_llm_config,
        summary_llm="ollama/llama3.2",
        summary_llm_config=local_llm_config,
        temperature=0.2,
        embedding="ollama/llama3.2",
    )

    for doc in uploaded_files:
        print("Adding doc: ", Path("backend/data/uploads").joinpath(doc))
        await docs.aadd(Path("backend/data/uploads").joinpath(doc), settings=settings)
        print("Added doc successfully: ", doc)

    print("Default settings: ", settings)

    answer = await docs.aquery(
        query="Whos resume is this?",
        settings=settings
    )
    
async def cleanup_response(
    response: Optional[aiohttp.ClientResponse],
    session: Optional[aiohttp.ClientSession],
):
    if response:
        response.close()
    if session:
        await session.close()
        
async def query_and_stream_response(query: str, settings: Settings):
    docs = Docs()
    uploaded_files = get_uploaded_files("backend/data/uploads")
    
    valid_extensions = {".pdf", ".txt", ".html"}
    uploaded_files = [file for file in uploaded_files if Path(file).suffix in valid_extensions]

    # Add documents to the PaperQA Docs instance
    for doc in uploaded_files:
        docs.add(Path("backend/data/uploads").joinpath(doc), settings=settings)
    
    # Stream the response from the PaperQA query
    for partial_answer in docs.query(query=query, settings=settings):
        yield json.dumps({"message": {"content": partial_answer}}) + "\n"

async def json_streamer():
    # Yield parts of the JSON response iteratively
    yield json.dumps({"message": {"content": "Hello I am Anand"}, "done": False}) + "\n"
    # Simulate more data streaming
    yield json.dumps({"message": {"content": "This is the second part"}, "done": False}) + "\n"
    # Finalize the response
    yield json.dumps({"message": {"content": "Streaming complete"}, "done": True}) + "\n"


@app.post("/api/chat/")
async def generate_paperqa_chat_completion(
    form_data: GenerateChatCompletionForm,
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
) -> StreamingResponse:
    payload: dict[str, Any] = {**form_data.model_dump(exclude_none=True)}
    log.debug(f"{payload = }")

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

    local_llm_config: dict[str, list[dict[str, str | dict[str, str]]]] = {
        "model_list": [
            {
                "model_name": "ollama/llama3.2",
                "litellm_params": {
                    "model": "ollama/llama3.2",
                    "api_base": "http://localhost:11434",
                },
            }
        ]
    }
    settings = Settings(
        llm="ollama/llama3.2",
        llm_config=local_llm_config,
        summary_llm="ollama/llama3.2",
        summary_llm_config=local_llm_config,
        temperature=0.2,
        embedding="ollama/llama3.2",
    )
    return StreamingResponse(
        json_streamer(),
        media_type="application/json",
    )

