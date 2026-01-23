from core.aws_clients import ses


class EmailService:

    def send_email(
        self,
        to: list[str],
        from_rmail:str,
        subject: str,
        body: str,
        cc: list[str] | None = None,
    ):
        destination = {"ToAddresses": to}
        if cc:
            destination["CcAddresses"] = cc

        ses.send_email(
            Source=from_rmail,
            Destination=destination,
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {"Data": body}
                },
            },
        )
