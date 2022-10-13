"""
Timekill: the better way to kill time.
"""
from datetime import datetime, time, timedelta
from time import sleep

import click

from .classify import classify_gpt3
from .load import load_all
from .notify import notify
from .server import server
from .suggest import (
    Activity,
    Context,
    plan_day,
    print_plan,
    suggest_activities,
)


@click.group()
def main():
    """
    A better way to kill time, a tool for planning your day and finding things to do.

    NOTE: still in early development
    """
    pass


# Subgroups
main.add_command(server)


@main.command("list")
def list_():
    """
    List content with recommendations.
    """
    # TODO: figure out a way to score content such that it can be ranked
    for content in load_all():
        classification = classify_gpt3(content)
        print(classification.pretty())


def sleep_progress(seconds: int, label="Sleeping"):
    """
    Sleep with a progress bar.
    """

    with click.progressbar(range(seconds), label=label) as bar:
        for _ in bar:
            try:
                sleep(1)
            except KeyboardInterrupt:
                return False
    return True


@main.command()
def suggest():
    """
    Suggest activities to do.
    """

    context = Context.prompt()
    skipped: list[Activity] = []
    while True:
        activities = suggest_activities(context, skip=skipped)
        if len(activities) == 0:
            break
        activity = activities[0]
        print("\n" + activity.pretty())
        if not click.confirm("> Do you want to do this?"):
            skipped.append(activity)
            print("Alright, let's try something else.")
            continue
        activity.do(context)
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
        print("\nRan out of suggestions. Try again later.")


@main.command()
@click.option("--until", type=lambda s: time(*map(int, s.split(":"))))  # type: ignore
def plan(until: time):
    """
    Plan a day of activity.
    """

    context = Context.prompt()

    # set time for context, round start to 5-min interval
    start = datetime.now()
    start = start.replace(minute=start.minute // 5 * 5, second=0, microsecond=0)
    context.timestamp = start

    activities = plan_day(context, stop=until or time(23, 59))
    print("")
    print_plan(context, activities)


if __name__ == "__main__":
    main()
