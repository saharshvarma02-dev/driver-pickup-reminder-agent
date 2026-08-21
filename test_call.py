import os

from dotenv import load_dotenv
from twilio.rest import Client  # type: ignore[import-unresolved]

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
driver_number = os.getenv("TEST_DRIVER_PHONE")

client = Client(account_sid, auth_token)

call = client.calls.create(
    url="https://webhooks.twilio.com/v1/Voice/Template/voice_text_to_speech",
    to=driver_number,
    from_=twilio_number,
)

print("Call initiated!")
print("Call SID:", call.sid)