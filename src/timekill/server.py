import click
import fastapi
import uvicorn

from .classify import classify_gpt3
from .models import Content

app = fastapi.FastAPI()


@click.group()
def server():
    """Subcommands for running a server (WIP)"""
    pass


@server.command("start")
def start():
    """
    Entrypoint for the timekill server
    """
    uvicorn.run(app, host="127.0.0.1", port=8000)


@app.get("/classify")
def classify(contents: list[Content]):
    """
    Classify endpoint. Takes a list of content items and returns a list of classifications.

    Uses GPT-3 using the OpenAI API.
    """
    return [classify_gpt3(content) for content in contents]
