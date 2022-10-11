from datetime import datetime, time, date
from typing import Literal, get_args
from dataclasses import dataclass


Activity = Literal["work", "leisure", "exercise", "relax", "socialize", "learn"]
Location = Literal["home", "work", "outside"]
TimeOfDay = Literal["morning", "afternoon", "evening", "night"]


@dataclass
class Context:
    activity: Activity
    location: Location

    @property
    def date(self) -> date:
        return datetime.now().date()

    @property
    def time(self) -> time:
        return datetime.now().time()

    @classmethod
    def prompt(cls) -> "Context":
        """Prompt the user for a context."""
        import click

        valid_activities = get_args(Activity)
        activity = click.prompt(
            "What are you doing? ",
            type=click.Choice(valid_activities),
        )

        valid_locations = get_args(Location)
        location = click.prompt(
            "Where are you?",
            type=click.Choice(valid_locations),
        )

        return cls(activity, location)
