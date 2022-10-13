from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from typing import Literal, get_args

import click
from pydantic import BaseModel

from .schedule import Schedule

# different types of activities, useful for filtering and satisfying needs
ActivityType = Literal[
    "any",
    "work",
    "leisure",
    "exercise",
    "relax",
    "social",
    "learn",
    "meditate",
    "other",
]
LocationType = Literal["home", "work", "outside"]


class Activity(BaseModel):
    """A suggested activity for the user."""

    title: str
    description: str = ""
    type: ActivityType | None = None

    # the priority of the activity, higher is better, 0 is default
    priority: int = 0

    # the condition under which the activity is suggested
    condition: Callable[["Context"], bool] = lambda _: True

    # TODO: redundant given flexibility of `condition`?
    schedule: Schedule | None = None

    # An estimation of the time it will take to complete the activity. In seconds.
    duration: int | None = None

    def __repr__(self) -> str:
        return f"Activity({self.title!r})"

    def do(self, context: "Context" = None) -> None:
        """Execute the activity."""
        print(f"Doing activity: {self.title}")
        if context:
            context.history.append(self)

    def pretty(self) -> str:
        duration = timedelta(seconds=self.duration) if self.duration else None
        duration_str = f" ({duration})" if duration else ""
        desc_str = f": {self.description}" if self.description else ""
        return f"[{self.title}{duration_str}{desc_str}]"


class Exercise(Activity):
    """An exercise to do."""

    type: ActivityType = "exercise"


@dataclass
class Context:
    activity: ActivityType
    location: LocationType
    timestamp: datetime = field(default_factory=datetime.now)
    history: list[Activity] = field(default_factory=list)

    @property
    def date(self) -> date:
        return self.timestamp.date()

    @property
    def time(self) -> time:
        return self.timestamp.time()

    @classmethod
    def prompt(cls) -> "Context":
        """Prompt the user for a context."""

        valid_activities = get_args(ActivityType)
        activity = click.prompt(
            "What are you doing?",
            type=click.Choice(valid_activities),
            default=valid_activities[0],
            show_choices=False,
            show_default=True,
        )

        valid_locations = get_args(LocationType)
        location = click.prompt(
            "Where are you?",
            type=click.Choice(valid_locations),
            default=valid_locations[0],
            show_choices=False,
            show_default=True,
        )

        return cls(activity, location)
