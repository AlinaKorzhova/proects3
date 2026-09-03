import pytest
from unittest.mock import Mock, patch
from src.external_api import function


@patch("requests.get")
def test_function(mock_get):
    mock_get.return_value.json.return_value = {"result": 100}
    assert (function({"operationAmount": {"amount": 79114.93, "currency": {"code": "RUB"}}}) == 79114.93)
    assert (function({"operationAmount": {"amount": 79114.93, "currency": {"code": "USD"}}}) == 100)
