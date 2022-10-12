import pytest

from timekill.classify import classify_gpt3
from timekill.classify.example_content import content_aw, example_content
from timekill.load import load_reddit


@pytest.mark.openai
def test_classify():
    """Test the classify function."""
    classification = classify_gpt3(content_aw, example_content[1:])
    assert classification


@pytest.mark.openai
@pytest.mark.reddit
def test_classify_reddit():
    """Test the classify function with reddit data."""

    contents = load_reddit("python")
    for content in contents[:3]:
        classification = classify_gpt3(content, example_content[:2])
        classification.pretty()
