
import logging
import os
from pathlib import Path
from typing import Any, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from open_webui.apps.ollama.main import (GenerateChatCompletionForm,
                                         get_ollama_url)
from open_webui.apps.webui.models.models import ModelModel, Models
from open_webui.config import (CORS_ALLOW_ORIGIN, MODEL_FILTER_LIST,
                               RAG_PAPERQA_TEMPERATURE, UPLOAD_DIR, AppConfig)
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


def get_uploaded_files(directory: str) -> list[str]:
    try:
        files: list[str] = os.listdir(Path((directory)))
        return [file for file in files if os.path.isfile(os.path.join(directory, file))]
    except FileNotFoundError:
        return []


async def main(query:str) -> None:
    docs = Docs()
    uploaded_files: list[str] = get_uploaded_files("backend/data/uploads")
    
    valid_extensions: set[str] = {".pdf", ".txt", ".html"}
    uploaded_files = [file for file in uploaded_files if Path(file).suffix in valid_extensions]

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


@app.post("/chat/completion")
def generate_paperqa_chat_completion(
    form_data: GenerateChatCompletionForm,
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
) -> dict[str, Any]:
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

            # payload["options"] = apply_model_params_to_body_ollama(
            #     params, payload["options"]
            # )
            # payload = apply_model_system_prompt_to_body(params, payload, user)

    if ":" not in payload["model"]:
        payload["model"] = f"{payload['model']}:latest"

    url = get_ollama_url(url_idx, payload["model"])
    log.info(f"url: {url}")
    log.debug(payload)

    # return await post_streaming_url(
#         f"{url}/api/chat",
#         json.dumps(payload),
#         stream=form_data.stream,
#         content_type="application/x-ndjson",
#     )

    docs = Docs()

    # return {"response": answer, "payload": payload}

    return {"response": "Hello I am anand", "payload": payload}
