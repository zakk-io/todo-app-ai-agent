from fastapi import FastAPI
from pydantic import BaseModel
from agent import todo_agent
from fastapi.middleware.cors import CORSMiddleware 
import os
from agent import AgentResponse
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000"
    ).split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: AgentResponse


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    result = todo_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": request.message
            }
        ]
    })


    return ChatResponse(
        response=result["structured_response"]
    )