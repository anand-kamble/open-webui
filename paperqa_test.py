from pathlib import Path
import re
from paperqa import ask, Settings, Docs
from paperqa.agents.models import AnswerResponse
import asyncio
import os
from paperqa import Settings, agent_query, QueryRequest
from paperqa.llms import LLMModel, LiteLLMModel

os.environ["OPENAI_API_KEY"] = ""

local_llm_config = {
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

DEFAULT_SETTINGS = Settings(
    llm="ollama/llama3.2",
    llm_config=local_llm_config,
    summary_llm="ollama/llama3.2",
    summary_llm_config=local_llm_config,
    temperature=0.2,
    embedding="ollama/llama3.2",
)


def get_uploaded_files(directory):
    try:
        files = os.listdir(directory)
        return [file for file in files if os.path.isfile(os.path.join(directory, file))]
    except FileNotFoundError:
        return []


uploaded_files: list = get_uploaded_files("backend/data/uploads")

# ollamaLLMModel = LLMModel(config=local_llm_config["model_list"][0]["litellm_params"])

print("Uploaded files: ", uploaded_files)
async def main() -> None:
    docs = Docs()
    # valid extensions include .pdf, .txt, and .html
    for doc in uploaded_files:
        print("Adding doc: ", Path("backend/data/uploads").joinpath(doc))
        await docs.aadd(Path("backend/data/uploads").joinpath(doc),settings=DEFAULT_SETTINGS)
        print("Added doc successfully: ", doc)

    print("Default settings: ", DEFAULT_SETTINGS)
    
    answer = await docs.aquery(
        query="Whos resume is this?",
        settings=DEFAULT_SETTINGS
    )
    print("====================================")
    print(answer)


asyncio.run(main())

# async def get_answer():
#     answer = await agent_query(
#         QueryRequest(
#             query="What manufacturing challenges are unique to bispecific antibodies?",
#             settings=DEFAULT_SETTINGS,
#         ),
#     )
#     return answer

# ask(
#     "What manufacturing challenges are unique to bispecific antibodies?",
#     settings=DEFAULT_SETTINGS,
# )

# asyncio.run(get_answer())
