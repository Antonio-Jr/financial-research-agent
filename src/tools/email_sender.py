"""Email sending tool wrapper using SendGrid.

This module exposes `send_email` decorated as a `function_tool` so it
can be invoked by agents. The implementation uses the SendGrid SDK
with configuration taken from the project's settings.
"""

import logging

import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To

from agents import function_tool
from src.config import settings

logger = logging.getLogger(__name__)


@function_tool
def send_email(email_to: str, subject: str, html_body: str):
    """Send an HTML email via SendGrid.

    Args:
        email_to: Recipient email address.
        subject: Email subject line.
        html_body: HTML body content for the email.

    Returns:
        A dict summarizing the send result with `status` and HTTP `code`.

    Raises:
        ValueError: If `email_to` is not a valid email address.
    """
    if not email_to or "@" not in email_to:
        raise ValueError("You need to inform a valid email to perform this operation")

    logger.info("🚀 Sending email to %s with subject: %s", email_to, subject)
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    from_email = Email(settings.SENDER_EMAIL_ADDRESS)
    to_email = To(email_to)
    subject = subject
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content)

    try:
        logger.debug("Email payload size: %d", len(html_body) if html_body else 0)
        response = sg.client.mail.send.post(request_body=mail.get())
        logger.info("Status Code: %s", response.status_code)
        logger.debug("Response Body: %s", getattr(response, "body", None))
        logger.debug("Response Headers: %s", getattr(response, "headers", None))

        if response.status_code in [200, 201, 202]:
            logger.info("SUCCESS: Email sent to %s (status: %s)", email_to, response.status_code)
            return {"status": "Success", "code": response.status_code, "to": email_to}
        else:
            logger.warning("FAILURE: Email to %s returned unexpected status %s", email_to, response.status_code)
            return {"status": "Failure", "code": response.status_code, "to": email_to}

    except Exception as e:
        logger.exception("ERROR: Could not send email to %s: %s", email_to, e)
        return {"status": "Failure", "code": 500, "to": email_to, "message": str(e)}
