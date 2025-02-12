import pytest
from app import search_interface

def test_empty_query():
    # Test that an empty query returns the correct message, no results, and a None transcribed query.
    status, images, transcribed = search_interface("", 5)
    assert status == "No query provided. Please type your query."
    assert images == []
    assert transcribed is None
