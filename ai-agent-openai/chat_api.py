import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel  # noqa: E402

from agent_def import todo_agent  # noqa: E402
from agents import Runner, RunState  # noqa: E402

app = FastAPI(title="Todo Agent Chat")

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


class ApprovelRequest(BaseModel):
    state: dict | None = None
    is_approved: bool
    


class ChatResponse(BaseModel):
    status: str
    approval: dict | None = None
    response: str | None = None
    state: dict | None = None


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    result = await Runner.run(todo_agent, req.message)

    if result.interruptions:
        state = result.to_state()
        interruption = result.interruptions[0]

        return ChatResponse(
            status="approval_required",
            approval={
                "tool": interruption.name,
                "arguments": interruption.arguments,
            },
            state=state.to_json(),
        )

    return ChatResponse(
        status="completed",
        response=result.final_output,
    )
    


@app.post("/approve", response_model=ChatResponse)
async def approve(req: ApprovelRequest):

    state = await RunState.from_json(
        todo_agent,
        req.state,
    )

    interruptions = state.get_interruptions()

    if not interruptions:
        return ChatResponse(
            status="completed",
            response="No approval required.",
        )

    interruption = interruptions[0]

    if req.is_approved:
        state.approve(interruption)
    else:
        state.reject(
            interruption,
            rejection_message="Action was rejected.",
        )

    result = await Runner.run(
        todo_agent,
        state,
    )

    return ChatResponse(
        status="completed",
        response=result.final_output,
    )
    
        
    


@app.get("/")
async def root():
    return {"message": "Todo agent chat. POST a message to /chat"}