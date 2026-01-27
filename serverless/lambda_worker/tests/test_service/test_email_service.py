from unittest.mock import patch

from services.email_service import EmailService


@patch("services.email_service.ses")
def test_send_email_success(mock_ses):
    service = EmailService()

    to = ["user1@gmail.com", "user2@gmail.com"]
    from_email = "sender@gmail.com"
    subject = "Test Subject"
    body = "Test Body"

    service.send_email(
        to=to,
        from_email=from_email,
        subject=subject,
        body=body,
    )

    mock_ses.send_email.assert_called_once_with(
        Source=from_email,
        Destination={"ToAddresses": to},
        Message={
            "Subject": {"Data": subject},
            "Body": {
                "Text": {"Data": body}
            },
        },
    )
