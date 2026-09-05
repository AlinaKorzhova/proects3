import pytest
from unittest.mock import Mock, patch, mock_open
from src.utils import read_json_file


def test_read_json_file():
    with patch("builtins.open", mock_open(read_data='[{"id": 344}]')):
        assert read_json_file() == [{"id": 344}]
    with patch("builtins.open", mock_open(read_data='{"id": 344}]')):
        assert read_json_file() == []

    assert read_json_file("") == []




