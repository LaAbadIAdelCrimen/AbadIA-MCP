import pytest
from unittest.mock import patch, MagicMock
from server.common import sendCmd
import requests

@patch("server.common.requests.get")
def test_send_cmd_get_json(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    mock_get.return_value = mock_response
    res = sendCmd("http://test", "action")
    assert res == {"key": "value"}

@patch("server.common.requests.post")
def test_send_cmd_post_text(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "raw text"
    mock_post.return_value = mock_response
    res = sendCmd("http://test", "action", type="text", mode="POST")
    assert res == "raw text"

def test_send_cmd_failures():
    # JSON error
    with patch("server.common.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError()
        mock_get.return_value = mock_response
        assert sendCmd("http://test", "action") is None
    
    # Request exception (using side_effect on the mock directly)
    with patch("server.common.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("fail")
        assert sendCmd("http://test", "action") is None

def test_session_handling():
    from server import common
    common.session_id = "123"
    with patch("server.common.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        sendCmd("http://test", "action")
        # Verify header was sent
        args, kwargs = mock_get.call_args
        assert kwargs["headers"]["X-Session-Id"] == "123"
    common.session_id = None

@patch("server.common.requests.get")
def test_status_599(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 599
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response
    res = sendCmd("http://test", "action")
    assert res["haFracasado"] == True
