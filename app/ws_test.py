from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_test(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("CONNECTED FROM SERVER")

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"ECHO: {data}")
