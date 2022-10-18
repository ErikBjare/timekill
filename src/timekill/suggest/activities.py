from datetime import timedelta

from .models import Activity, Context, Exercise


def condition_work(c: Context) -> bool:
    return c.activity in ("any", "work")


def condition_focus(c: Context) -> bool:
    """
    Something that requires sustained focus.
    Alternate name: "deepwork" or "busy"
    """
    return c.activity in ("any", "work", "learn")


def condition_meditation(c: Context) -> bool:
    return c.activity in ("any", "meditation") and not [
        a for a in c.history if a.type == "meditate"
    ]


def condition_social(c: Context) -> bool:
    return (
        (c.activity == "any" or not condition_focus(c))
        and not condition_office_hours(c)
        and c.time.hour < 20
    )


def condition_learn(c: Context) -> bool:
    return c.activity in ("any", "learn") and c.location == "home"


def condition_bedtime(c: Context) -> bool:
    return c.time.hour >= 22 or c.time.hour < 4


def condition_exercise(c: Context) -> bool:
    return (
        not condition_focus(c)
        and c.location == "home"
        and 4 <= c.time.hour < 18
        and not [a for a in c.history if a.type == "exercise"]
    )


def condition_dinnertime(c: Context) -> bool:
    return 18 <= c.time.hour < 21


def condition_weekend(c: Context) -> bool:
    return c.date.weekday() in (5, 6)


def condition_new_month(c: Context) -> bool:
    return c.date.day <= 3


def condition_office_hours(c: Context) -> bool:
    """9-5 on weekdays"""
    return 9 <= c.time.hour < 17 and c.date.weekday() < 5


def condition_aw_time(c: Context, pattern: str, since=timedelta(hours=18)) -> bool:
    """condition for checking if time has been spent on a device activity (using ActivityWatch)"""
    raise NotImplementedError


ACTIVITIES = [
    Activity(
        title="Write daily notes",
        duration=5 * 60,
        condition=lambda c: 4 < c.time.hour < 21 and c.activity != "leisure",
        priority=5,
    ),
    # Work
    Activity(
        title="Check GitHub notifications",
        duration=10 * 60,
        condition=condition_work,
        priority=2,
    ),
    Activity(
        title="Review today's ActivityWatch stats",
        duration=3 * 60,
        # TODO: Don't suggest if already done today (check using AW data)
        condition=lambda c: condition_work(c) and 16 < c.time.hour < 22,
        priority=3,
    ),
    # Learn
    Activity(
        title="Do Brilliant",
        duration=20 * 60,
        condition=lambda c: condition_learn(c),
    ),
    Activity(
        title="Do Duolingo",
        duration=5 * 60,
        condition=lambda c: condition_learn(c) or c.activity == "relax",
    ),
    Activity(
        title="Do Anki",
        duration=5 * 60,
        condition=lambda c: condition_learn(c) or c.activity == "relax",
    ),
    # Exercise
    Exercise(
        title="Lift weights",
        duration=45 * 60,
        condition=condition_exercise,
        priority=4,
    ),
    Exercise(
        title="Go for a run",
        description="choose your own pace",
        duration=45 * 60,
        # TODO: Don't suggest if already worked out today, or if cardio was done yesterday
        condition=condition_exercise,
        priority=4,
    ),
    Exercise(
        title="Go for a walk",
        duration=30 * 60,
        # Only suggest if sun is out (overkill: and maybe that it's not raining?)
        condition=lambda c: (c.activity == "any" or not condition_focus(c))
        and c.time.hour < 20,
    ),
    # Social
    Activity(
        title="Check in with friends",  # TODO: Who? How can I figure out who to check in with? Split into multiple activities?
        duration=20 * 60,
        condition=condition_social,
        priority=1,
    ),
    Activity(
        title="Call parents/grandparents",
        duration=30 * 60,
        # TODO: Don't suggest if done recently
        condition=condition_social,
        priority=1,
    ),
    # Recurring reviews
    Activity(
        title="Monthly review",
        description="Review ActivityWatch, Whoop, quantifiedme stats",
        duration=10 * 60,
        condition=condition_new_month,
        priority=4,
    ),
    Activity(
        title="Weekly review",
        description="Review ActivityWatch, Whoop, quantifiedme stats",
        duration=10 * 60,
        condition=condition_weekend,
        priority=4,
    ),
    # Leisure
    Activity(
        # TODO: Read what? (maybe based on what I've been reading lately)
        title="Read",
        duration=30 * 60,
        priority=3,
        condition=lambda c: c.activity in ("any", "relax", "learn", "leisure"),
    ),
    Activity(
        title="Watch a movie",
        duration=90 * 60,
        condition=lambda c: c.activity in ("any", "relax", "leisure")
        and 18 < c.time.hour,
    ),
    Activity(
        title="Go to the sauna",
        duration=60 * 60,
        condition=lambda c: c.location == "home"
        and c.activity in ("relax")
        and 16 <= c.time.hour < 20,
    ),
    # Behavioral queues
    Activity(
        title="Meditate",
        duration=10 * 60,
        type="meditate",
        condition=condition_meditation,
    ),
    Activity(
        title="Practice Mendi",
        duration=5 * 60,
        type="meditate",
        condition=condition_meditation,
        # NOTE: This will always suggest Mendi, and never meditate
        priority=1,
    ),
    Activity(
        title="Brush teeth",
        duration=5 * 60,
        condition=condition_bedtime,
        priority=6,
    ),
    Activity(
        title="Eat dinner",
        duration=30 * 60,
        condition=condition_dinnertime,
    ),
    Activity(
        title="Go to bed",
        duration=8 * 60 * 60,
        condition=condition_bedtime,
        priority=5,
    ),
]
ACTIVITIES.sort(key=lambda a: a.priority, reverse=True)
