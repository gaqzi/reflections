from . import create_index as main
import pytest


def test_seen_headers():
    """Test the 'seen_headers' set."""
    # Arrange.
    seen_headers = main.seen_headers()

    # Act.
    seen_headers.add('a')
    seen_headers.add({'b','c'})

    # Assert.
    assert isinstance(seen_headers, set)
    assert isinstance(seen_headers[0], str)
