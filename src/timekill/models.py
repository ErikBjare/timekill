from pydantic import BaseModel

from .emoji import emoji_check, emoji_fail


class Content(BaseModel):
    """
    A piece of content to classify/recommend.
    """

    title: str
    description: str
    url: str
    source_url: str

    def to_text(self) -> str:
        """
        Convert the content to a string that can be parsed by GPT-3.
        """
        # use max description length of 30 tokens, or 500 characters
        max_tokens = 30
        max_chars = 500
        description = (" ".join(self.description.split(" ")[:max_tokens]))[:max_chars]
        return f"Title: {self.title}\nDescription: {description}\nURL: {self.url}\nSource URL: {self.source_url}"


class Classification(BaseModel):
    """A classification of a piece of content."""

    content: Content
    recommended: bool
    reason: str

    def pretty(self) -> str:
        emoji = emoji_check if self.recommended else emoji_fail
        return f"{emoji}: {self.content.title} ({self.content.url})"
