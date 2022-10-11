from pydantic import BaseModel


emoji_check = "✅"
emoji_fail = "❌"


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

        return f"Title: {self.title}\nDescription: {self.description}\nURL: {self.url}\nSource URL: {self.source_url}"


class Classification(BaseModel):
    """
    A classification of a piece of content.
    """

    content: Content
    recommended: bool
    reason: str

    def pretty(self) -> str:
        emoji = emoji_check if self.recommended else emoji_fail
        return f"{emoji}: {self.content.title} ({self.content.url})"
