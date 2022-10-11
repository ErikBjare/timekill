"""
Timekill: the better way to kill time.
"""

import os
from dataclasses import dataclass

import click
import fastapi

from .models import Content
from .classify import classify_gpt3
from .load import load_all


app = fastapi.FastAPI()


@click.group()
def main():
    pass


@main.command()
def start():
    """
    Entrypoint for the timekill server
    """
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)


@main.command('list')
def list_():
    """
    List content with recommendations.
    """
    for content in load_all():
        classification = classify_gpt3(content)
        print(classification.pretty())


@app.get("/classify")
def classify(contents: list[Content]):
    """
    Classify endpoint. Takes a list of content items and returns a list of classifications.

    Uses GPT-3 using the OpenAI API.
    """
    return [classify_gpt3(content) for content in contents]


if __name__ == "__main__":
    main()
