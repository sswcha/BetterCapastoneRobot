# Set-ExecutionPolicy Unrestricted -Scope Process

import logging

import asyncio
import uvicorn

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from modules.models import Todo
from modules.ConnectionManager import ConnectionManager



app = FastAPI()
manager = ConnectionManager()

app.mount("/templates", StaticFiles(directory="templates"))
templates = Jinja2Templates(directory="templates")



@app.get('/')
async def name(request: Request):
    template_content = {
        "title": "My Page"
    }
    return templates.TemplateResponse("index.html", {"request": request, **template_content})



@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_direct_message(f"Received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_direct_message("Disconnected from socket", websocket)