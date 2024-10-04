
from typing import Optional
from open_webui.apps.ollama.main import GenerateChatCompletionForm
from open_webui.utils.utils import get_verified_user
from paperqa import ask, Settings, Docs
from fastapi import Depends

from open_webui.config import UPLOAD_DIR, RAG_PAPERQA_TEMPERATURE

# answer = ask(
#     "What manufacturing challenges are unique to bispecific antibodies?",
#     settings=Settings(temperature=RAG_PAPERQA_TEMPERATURE, paper_directory=UPLOAD_DIR),
# )

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

def generate_paperqa_chat_completion(
    form_data: GenerateChatCompletionForm,
    url_idx: Optional[int] = None,
    user=Depends(get_verified_user),
):
    payload = {**form_data.model_dump(exclude_none=True)}
    
    print(payload)
    docs = Docs()
    
    return {"response": answer, "payload": payload}