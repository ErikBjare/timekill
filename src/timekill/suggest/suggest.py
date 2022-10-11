"""
Suggest an activity for the user based on their current time of day and context.

For example:
 - Could fetch items from your TODO list, or suggest non-content activities (like exercise, take notes, Duolingo, etc.)
 - Suggestions could be based on:
   - Time of day, so it won't suggest a workout late at night, or doing unfocused work in the morning.
   - Location, so it won't suggest a workout if you're at work.
   - Previous activities, so it won't suggest a workout if you're already working out.

Once-a-day things:
 - exercise (at least every third day, alternating between cardio and strength, suggesting whichever you haven't done in the last three days)
 - write daily notes
 - Duolingo
 - Do Brilliant.org problems
 - Upcoming calendar events
 - Finish items on TODO list

Once-a-week things:
 - Plan next week (on Fridays-Sundays)

Once-a-month things:
 - Review stats (on the first 3 days of the month)
"""


from datetime import time
from typing import Literal, get_args
from dataclasses import dataclass

from .models import Activity, Exercise
from .context import Context


activities = [
    Activity(
        title="Write daily notes",
        duration=5 * 60,
        priority=5,
    ),
    Activity(
        title="Do Brilliant",
        duration=20 * 60,
        condition=lambda c: c.activity in ("learn"),
        priority=3,
    ),
    Activity(
        title="Do Duolingo",
        duration=5 * 60,
        condition=lambda c: c.activity in ("relax", "learn"),
        priority=1,
    ),
    # Work
    Activity(
        title="Check GitHub notifications",
        duration=10 * 60,
        condition=lambda c: c.activity == "work",
        priority=1,
    ),
    Activity(
        title="Review today's ActivityWatch stats",
        duration=3 * 60,
        # TODO: Don't suggest if already done today (check using AW data)
        condition=lambda c: c.activity == "work" and 16 < c.time.hour < 22,
        priority=2,
    ),
    # Exercise
    Exercise(
        title="Lift weights",
        duration=45 * 60,
        condition=lambda c: c.location == "home" and c.time.hour < 17,
        priority=4,
    ),
    Exercise(
        title="Go for a run",
        description="choose your own pace",
        duration=45 * 60,
        # TODO: Don't suggest if already worked out today, or if cardio was done yesterday
        condition=lambda c: c.location == "home" and c.time.hour < 18,
        priority=4,
    ),
    Exercise(
        title="Go for a walk",
        duration=30 * 60,
        # Only suggest if sun is out (overkill: and maybe that it's not raining?)
        condition=lambda c: c.activity != "work" and c.time.hour < 20,
    ),
    # Social
    Activity(
        title="Check in with friends",  # TODO: Who? How can I figure out who to check in with? Split into multiple activities?
        duration=20 * 60,
        condition=lambda c: c.activity not in ("work", "learn") and c.time.hour < 20,
        priority=1,
    ),
    Activity(
        title="Call parents/grandparents",
        duration=30 * 60,
        # TODO: Don't suggest if done recently
        condition=lambda c: c.activity not in ("work", "learn") and c.time.hour < 20,
        priority=1,
    ),
    # Recurring reviews
    Activity(
        title="Monthly review",
        description="Review ActivityWatch, Whoop, quantifiedme stats",
        duration=10 * 60,
        condition=lambda c: c.date.day <= 3,
        priority=4,
    ),
    Activity(
        title="Weekly review",
        description="Review ActivityWatch, Whoop, quantifiedme stats",
        duration=10 * 60,
        condition=lambda c: c.date.weekday() in (0, 5, 6),
        priority=4,
    ),
    # Leisure
    Activity(
        # TODO: Read what? (maybe based on what I've been reading lately)
        title="Read",
        duration=30 * 60,
        priority=4,
        condition=lambda c: c.activity in ("relax", "learn", "leisure"),
    ),
    Activity(
        title="Watch a movie",
        duration=90 * 60,
        condition=lambda c: c.activity in ("relax", "leisure") and 18 < c.time.hour,
    ),
    Activity(
        title="Go to the sauna",
        duration=60 * 60,
        condition=lambda c: c.location == "home"
        and c.activity in ("relax")
        and 16 < c.time.hour < 20,
    ),
    # Behavioral queues
    Activity(
        title="Brush teeth",
        duration=5 * 60,
        condition=lambda c: c.time.hour < 10 or 21 < c.time.hour,
    ),
    Activity(
        title="Eat dinner",
        duration=30 * 60,
        condition=lambda c: 17 < c.time.hour < 21,
    ),
    Activity(
        title="Go to bed",
        duration=8 * 60 * 60,
        condition=lambda c: c.time.hour > 22,
    ),
]
activities.sort(key=lambda a: a.priority, reverse=True)


def suggest_activities(context: Context) -> list[Activity]:
    """
    Suggest an activity based on the context.

    Use some form of priority-ranking.
    """
    # TODO: Try and plan a hypothetical day, and suggest activities based on that

    print(
        " - "
        + "\n - ".join([repr((a.title, a.condition(context))) for a in activities])
    )
    candidates = list(filter(lambda a: a.condition(context), activities))
    candidates.sort(key=lambda a: a.priority, reverse=True)
    return candidates
