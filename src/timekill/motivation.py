"""
Mechanisms for improving motivation.

Still a work in progress, but some ideas so far:

 - Randomly select a motivational quote from a list of quotes.
   - TODO: Select a quote intelligently, somehow.
 - Remind the user that even if they don't feel like it, they should do the bare minimum, even if only for 5min.
   - Aka "non-zero days"
"""

quotes = [
    # Fantastic mood
    (
        "Wow, you're really feeling great today! Try channeling that energy into something healthy or productive!",
        lambda mood: mood >= 8,
    ),
    # Good mood
    (
        "You're doing great! Keep it up! Just make sure you work on what's important and don't get stuck.",
        lambda mood: mood >= 6,
    ),
    (
        # TODO: this isn't really motivational, but is a good thing for the user to be mindful of
        "Let's go! Will you work on one big thing today, or a bunch of small things?",
        lambda mood: mood >= 6,
    ),
    "Being mindful of and completing the current priorities helps you feel satisfied at the end of the day.",
    # Bad mood
    (
        # TODO: stuff like this is a good idea, but it's not really motivational and needs more context to be accurate
        "If you're feeling overwhelmed, try to focus on the one single pressing or valuable task.",
        lambda mood: mood <= 5,
    ),
    (
        "Even if you don't feel like doing that thing today, do it for at least 5 minutes and see how it goes.",
        lambda mood: mood <= 4,
    ),
    (
        # cope
        "Not all days are perfect, but a bad day can still be okay. Try to do something, even if it's just a little bit. You'll feel better about it after.",
        lambda mood: mood <= 3,
    ),
]


def get_motivational_quote(mood: int):
    """
    Get a motivational quote.

    Mood is a scale 1-10, where 5 is neutral, 6+ is good, 8+ is great.
    """
    if mood < 5:
        return "You can do it!"
    elif mood < 6:
        return "You're doing great!"
    elif mood < 8:
        return "You're doing awesome!"
    else:
        return "You're doing amazing!"
