from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import analyze_request, route_action


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CustomerRequest(BaseModel):
    message: str


@app.get("/")
def health_check():
    return {
        "status": "AI Support Router API running"
    }


@app.post("/analyze")
def analyze_support_request(request: CustomerRequest):

    decision = analyze_request(request.message)

    tool_result = route_action(decision)

    return {
        "decision": decision.model_dump(),
        "tool_result": tool_result
    }