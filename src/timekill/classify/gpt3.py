import os
from dataclasses import dataclass

import joblib

from ..models import Content, Classification

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

memory = joblib.Memory("cache", verbose=0)


# Settings
context = "working"
interests = [
    "novel ideas",
    "show-and-tell",
    "open-source",
    "quantified self",
    "artificial intelligence",
    "machine learning",
    "brain-computer interfaces",
    "algorithmic trading",
]
disinterests = [
    "politics",
    "support questions",
    "spam",
    "clickbait",
    "marketing",
    "war",
]


def _gen_content_prompt(content: Content) -> str:
    """
    Generate a prompt for a piece of content.
    """
    return f"""---\nClassify this content:\n\n{content.to_text()}"""


def _gen_content_reply(content: Content, rec: bool, why: str) -> str:
    """
    Generate a (mock) reply/classification for a piece of content.
    """
    return f"""Recommended? {'Yes' if rec else 'No'}\nWhy? {why}"""


import pickle


class Cache:
    """A simple cache for classifications."""

    def __init__(self):
        self.cache = {}
        self.path = "cache/classify_cache.pkl"
        if os.path.exists(self.path):
            with open(self.path, "rb") as f:
                self.cache = pickle.load(f)

    def get(self, url: str) -> Classification | None:
        return self.cache.get(url, None)

    def put(self, url: str, classification: Classification) -> None:
        self.cache[url] = classification
        self.save()

    def save(self) -> None:
        with open(self.path, "wb") as f:
            pickle.dump(self.cache, f)


_cache = Cache()


def classify(
    content: Content,
    examples: list[tuple[Content, bool, str]] = [],
    cache=True,
) -> Classification:
    if cache:
        if classification := _cache.get(content.url):
            print("Cache hit for:", content.url)
            return classification

    import openai

    openai.api_key = OPENAI_API_KEY

    prompt = "This is a conversation between a human who wants to know if a piece of online content is relevant to him/her and their current context."
    prompt += " They will specify their preferences, and a helpful and knowledgeable AI will reply wether the content is relevant, and a step-by-step motivation of why.\n\n"
    prompt += f"I like: {', '.join(interests)}.\n"
    prompt += f"I dislike: {', '.join(disinterests)}.\n"
    prompt += f"I am currently: {context}.\n\n"

    for ex_content, ex_rec, ex_reason in examples:
        prompt += _gen_content_prompt(ex_content) + "\n\n"
        prompt += _gen_content_reply(ex_content, ex_rec, ex_reason).strip()
        prompt += "\n\n"

    prompt += _gen_content_prompt(content) + "\n\n"
    prompt += "Recommended?"

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0,
        top_p=1,
        max_tokens=64,
        frequency_penalty=0.1,
        presence_penalty=0.1,
        stop=["\n\n", "---"],
    )
    choice = response["choices"][0]["text"]
    classification = _parse_response(content, prompt + choice)
    if cache:
        _cache.put(content.url, classification)
    return classification


def _parse_response(content, response: str) -> Classification:
    """Takes the full prompt + response and parses out the classification."""
    lines = response.strip().split("\n")
    rec = lines[-2].strip().endswith("Yes")
    reason = lines[-1].split("Why?")[1].strip()
    return Classification(content=content, recommended=rec, reason=reason)
