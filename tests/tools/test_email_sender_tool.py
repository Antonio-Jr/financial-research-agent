import pytest
import sys
import importlib
from unittest.mock import patch, MagicMock

# Patch function_tool before importing the tool
with patch("agents.function_tool", lambda x: x):
    # Force reload to apply the patch to the decorator
    import src.tools.email_sender
    importlib.reload(src.tools.email_sender)
    from src.tools.email_sender import send_email

def test_send_email_invalid_address():
    with pytest.raises(ValueError, match="inform a valid email"):
        send_email(email_to="invalid-email", subject="S", html_body="B")

@patch("src.tools.email_sender.sendgrid.SendGridAPIClient")
def test_send_email_success(mock_sg_client):
    # Setup mock
    mock_response = MagicMock()
    mock_response.status_code = 202
    mock_sg_client.return_value.client.mail.send.post.return_value = mock_response
    
    result = send_email(email_to="test@example.com", subject="S", html_body="B")
    
    assert result["status"] == "Success"
    assert result["code"] == 202
    assert result["to"] == "test@example.com"

@patch("src.tools.email_sender.sendgrid.SendGridAPIClient")
def test_send_email_api_failure(mock_sg_client):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_sg_client.return_value.client.mail.send.post.return_value = mock_response
    
    result = send_email(email_to="test@example.com", subject="S", html_body="B")
    
    assert result["status"] == "Failure"
    assert result["code"] == 401

@patch("src.tools.email_sender.sendgrid.SendGridAPIClient")
def test_send_email_exception(mock_sg_client):
    mock_sg_client.return_value.client.mail.send.post.side_effect = Exception("Connection Error")
    
    result = send_email(email_to="test@example.com", subject="S", html_body="B")
    
    assert result["status"] == "Failure"
    assert result["code"] == 500
    assert "Connection Error" in result["message"]
