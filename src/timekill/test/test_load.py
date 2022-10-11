import pytest

from timekill.load import load_reddit


@pytest.mark.reddit
def test_load_reddit_json():
    """Test load_reddit function."""
    # Load data
    data = load_reddit("python")
    assert len(data) > 0
