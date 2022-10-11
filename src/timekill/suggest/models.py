from datetime import timedelta
from typing import Literal, Callable
from pydantic import BaseModel

from . import Schedule
from . import Context


# different types of activities, useful for filtering and satisfying needs
ActivityType = Literal[
    "exercise",
    "reading",
    "writing",
    "learning",
    "work",
    "other",
    "meditation",
]


class Activity(BaseModel):
    """A suggested activity for the user."""

    title: str
    description: str = ""
    type: ActivityType | None = None

    # the priority of the activity, higher is better, 0 is default
    priority: int = 0

    # the condition under which the activity is suggested
    condition: Callable[[Context], bool] = lambda _: True

    # TODO: redundant given flexibility of `condition`?
    schedule: Schedule | None = None

    # An estimation of the time it will take to complete the activity. In seconds.
    duration: int | None = None

    def do(self) -> None:
        """Execute the activity."""
        print(f"Doing activity: {self.title}")

    def pretty(self) -> str:
        duration = timedelta(seconds=self.duration) if self.duration else None
        duration_str = f" ({duration})" if duration else ""
        desc_str = f": {self.description}" if self.description else ""
        return f"[{self.title}{duration_str}{desc_str}]"


class Exercise(Activity):
    """An exercise to do."""

    type: ActivityType = "exercise"
