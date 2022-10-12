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
from copy import copy
from datetime import datetime, time, timedelta

from ..emoji import emoji_check, emoji_fail
from .activities import ACTIVITIES
from .models import Activity, Context


def suggest_activities(context: Context, skip: list[Activity] = None) -> list[Activity]:
    """
    Suggest an activity based on the context.

    Rank by priority.
    """
    # TODO: Try and plan a hypothetical day, and suggest activities based on that

    debug = False
    if debug:
        print(context)
        print(
            "\n".join(
                [
                    f" - {emoji_check if a.condition(context) else emoji_fail} {a.title}"
                    for a in ACTIVITIES
                ]
            )
        )

    # Filter by condition
    # Skip already performed activities
    candidates = list(
        filter(
            lambda a: a.condition(context)
            and a not in context.history
            and (skip is None or a not in skip),
            ACTIVITIES,
        )
    )
    candidates.sort(key=lambda a: a.priority, reverse=True)
    return candidates


def plan_day(
    context: Context, stop: time = time(23, 59)
) -> list[tuple[time, Activity]]:
    """
    Plan a day based on the context.
    """
    # Take a copy to avoid mutating the original
    context = copy(context)

    plan = []
    while context.time < stop:
        activities = suggest_activities(context)
        for activity in activities:
            plan.append((context.time, activity))
            # TODO: Activities should prob have a fallback if duration not set
            context.timestamp += timedelta(seconds=activity.duration or 0)
            context.history.append(activity)
            break
        else:
            # No suitable activities found, step forward in time
            context.timestamp += timedelta(minutes=1)

    return plan


def print_plan(context: Context, plan: list[tuple[time, Activity]]):
    """Print a plan to the console."""
    # Take a copy to avoid mutating the original
    context = copy(context)

    for t, activity in plan:
        context.timestamp = datetime.combine(context.timestamp, t)
        print(
            f"{t.hour}:{str(t.minute).zfill(2)} | {activity.title}"
            + (
                f" ({timedelta(seconds=activity.duration)})"
                if activity.duration
                else ""
            )
        )
        if activity.description:
            print(f"           - {activity.description}")
