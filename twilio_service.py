import os
import time

from twilio.rest import Client  # type: ignore[reportMissingImports]
from dotenv import load_dotenv

load_dotenv()


class TwilioService:

    def __init__(self):
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

        if not account_sid or not auth_token:
            raise ValueError(
                "Twilio credentials are missing from .env"
            )

        self.client = Client(
            account_sid,
            auth_token
        )

    def make_call(self, phone_number):

        phone_number = (
            str(phone_number)
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        print(
            f"Calling normalized number: {phone_number}"
        )

        call = self.client.calls.create(
            url="https://webhooks.twilio.com/v1/Voice/Template/voice_text_to_speech",
            to=phone_number,
            from_=self.twilio_number,
        )

        return call

    def get_call_status(self, call_sid):

        # Give Twilio a moment to update the call resource.
        time.sleep(2)

        call = self.client.calls(call_sid).fetch()

        return {
            "status": call.status,
            "duration": call.duration
        }