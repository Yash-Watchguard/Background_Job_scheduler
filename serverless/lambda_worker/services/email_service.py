from core.aws_clients import ses


class EmailService:

    def send_email(
        self,
        to: list[str],
        from_email: str,
        subject: str,
        body: str,
    ):
        destination = {"ToAddresses": to}
        ses.send_email(
            Source=from_email,
            Destination=destination,
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {"Data": body}
                },
            },
        )
