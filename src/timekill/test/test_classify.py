import pytest

from timekill.load import load_reddit
from timekill.classify import classify_gpt3
from timekill.classify.example_content import example_content, content_aw


@pytest.mark.openai
def test_classify():
    """Test the classify function."""
    classification = classify_gpt3(content_aw, example_content[1:])


@pytest.mark.openai
@pytest.mark.reddit
def test_classify_reddit():
    """Test the classify function with reddit data."""

    contents = load_reddit("python")
    for content in contents[:3]:
        classification = classify_gpt3(content, example_content[:2])
        classification.pretty()
