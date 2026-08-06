from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
import requests
import logging
import time
import uuid
import os
import psutil
from dotenv import load_dotenv

from app.agents.agent_manager import AgentManager
from app.logger import logger
from app.security import verify_api_key
from app.router import choose_model
from app.webhook import router as webhook_router

load_dotenv()


class ClineOrchestrationRequest(BaseModel):
    task_description: str
    team: List[str] = []


app = FastAPI(
    title="OmniForces AI Gateway",
    version="1.4"
)


app.include_router(webhook_router)


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)


agent_manager = AgentManager()
agent_manager.register_cline_agent(agent_id="cline", name="Cline")


logging.basicConfig(
    filename="logs/requests.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


request_count = 0


@app.get("/")
def home():

    return {
        "status": "online",
        "service": "OmniForces AI Gateway",
        "ollama": "connected"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "requests_processed": request_count
    }


@app.get("/models")
def models():

    return {
        "models": [
            "deepseek-r1:7b",
            "llama3.2:latest"
        ]
    }


@app.post("/ask")
def ask_ai(
    prompt: str,
    authenticated: bool = Depends(verify_api_key)
):

    global request_count

    request_count += 1

    request_id = str(uuid.uuid4())

    model = choose_model(prompt)


    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }


    start = time.time()


    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )


    response.raise_for_status()


    duration = round(
        time.time() - start,
        2
    )


    logger.info(
        f"SUCCESS | id={request_id} | model={model} | {duration}s"
    )

    result = response.json()

    result["omniforces"] = {
        "request_id": request_id,
        "selected_model": model,
        "response_time": duration
    }

    return result


@app.post("/cline/orchestrate")
def cline_orchestrate(
    request: ClineOrchestrationRequest,
    authenticated: bool = Depends(verify_api_key),
):
    plan = agent_manager.perform_cline_orchestration(
        request.task_description,
        request.team,
    )

    return {
        "status": "ok",
        "task_description": request.task_description,
        "team": request.team,
        "plan": plan,
    }