"""
The example from the README
"""

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi_sio import FastAPISIO


class PurrModel(BaseModel):
    detail: str
    loudness: int


class BellyRubModel(BaseModel):
    where_exactly: str
    scratches_num: int


fastapi = FastAPI()
sio = FastAPISIO(app=fastapi)

# Mount this ASGI app. The FastAPI app is passed as the other_asgi_app
# so you'll have access to the FastAPI routes as well.
app = sio.asgi_app

# Run with `uvicorn examples.from_readme:app`


@fastapi.get("/")
async def example_fastapi_route():
    return {"message": "Welcome to the FastAPI-SIO example!"}


purr_channel = sio.create_emitter(
    "purrs",
    model=PurrModel,
    summary="Channel for purrs",
    description="Receive any purrs here!",
)


@sio.on(
    "rubs",
    model=BellyRubModel,
    summary="Channel for belly rubs",
    description="Send your belly rubs through here!",
)
async def handle_rub(sid, data):
    await purr_channel.emit(PurrModel(loudness=2, detail="Purr for all listeners"))
    return "Ack to the one who rubbed"
