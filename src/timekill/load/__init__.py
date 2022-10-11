from .reddit import load_reddit


def load_all():
    # TODO: Needs to be expanded and made configurable
    # TODO: Include timekill/ActivityWatch-related subreddits/search by default
    #       This as a way to get those who use it to stay up to date from within.
    return load_reddit("python")
