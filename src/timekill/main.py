"""
Timekill: the better way to kill time.
"""

import os
from datetime import datetime, timedelta
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


@main.command("list")
def list_():
    """
    List content with recommendations.
    """
    for content in load_all():
        classification = classify_gpt3(content)
        print(classification.pretty())


def sleep_progress(seconds: int, label="Sleeping"):
    """
    Sleep with a progress bar.
    """
    import time

    with click.progressbar(range(seconds), label=label) as bar:
        for _ in bar:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break


@main.command()
def suggest():
    """
    Suggest activities to do.
    """
    from .suggest import suggest_activities, Context
    from .notify import notify

    context = Context.prompt()
    activities = suggest_activities(context)
    while len(activities) > 0:
        activity = activities.pop(0)
        print("\n" + activity.pretty())
        if not click.confirm("> Do you want to do this?"):
            print("Alright, let's try something else.")
            continue
        activity.do()
        if activity.duration:
            finished = sleep_progress(activity.duration, label=activity.title)
            if finished:
                notify(
                    activity.title,
                    f"Finished after {timedelta(seconds=activity.duration)}!",
                )

        # wait for user to request another suggestion
        click.prompt(
            "> Press enter to get another suggestion",
            default=True,
            show_default=False,
            prompt_suffix="",
        )

    if len(activities) == 0:
        print("Ran out of suggestions. Try again later.")


@app.get("/classify")
def classify(contents: list[Content]):
    """
    Classify endpoint. Takes a list of content items and returns a list of classifications.

    Uses GPT-3 using the OpenAI API.
    """
    return [classify_gpt3(content) for content in contents]


if __name__ == "__main__":
    main()
