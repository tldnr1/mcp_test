# api/server.py
from fastapi import FastAPI
from pydantic import BaseModel
from agents.graph import make_graph

app = FastAPI()

class MessageRequest(BaseModel):
    messages: str

@app.post("/chat")
async def chat(request: MessageRequest):
    async with make_graph() as agent:
        result = await agent.ainvoke({"messages": request.messages})
        return {"response": result}

# run by 'python -m api.server' at root(fastapi_with_mcp)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.server:app", host="0.0.0.0", port=8008, reload=True)
