import os

from dotenv import load_dotenv

from sheets_service import SheetsService
from reminder_engine import ReminderEngine
from twilio_service import TwilioService


load_dotenv()


WEB_APP_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbwRF24MtGZqsM7wVlwdNw92l9gUWXWYOYq4I2kOUCckF1S3M04PgSLyzh0DsIuHOMwH"
    "/exec?action=rides"
)


def main():
    print("Starting Driver Pickup Reminder Agent...\n")

    sheets = SheetsService(WEB_APP_URL)
    engine = ReminderEngine()
    twilio = TwilioService()

    # Temporary testing number.
    # This is the verified number on the Twilio trial account.
    test_phone = os.getenv("TEST_DRIVER_PHONE")

    if not test_phone:
        raise ValueError(
            "TEST_DRIVER_PHONE is missing from .env"
        )

    rides = sheets.get_rides()

    print(f"Found {len(rides)} rides\n")

    for index, ride in enumerate(rides):

        # First ride corresponds to spreadsheet row 2.
        row_number = index + 2

        minutes = engine.minutes_until_pickup(
            ride["pickup_time"]
        )

        print(
            f"{ride['driver_name']}: "
            f"{minutes:.1f} minutes until pickup"
        )

        # Check whether the reminder should be sent.
        if engine.should_remind(ride):

            print("  → Reminder needed")
            print("  → Initiating Twilio call...")

            print(
                f"  → Sheet phone: "
                f"{repr(ride['phone_number'])}"
            )

            print(
                f"  → Test phone: "
                f"{test_phone}"
            )

            # --------------------------------
            # STEP 1: Make the Twilio call
            # --------------------------------
            try:

                call = twilio.make_call(test_phone)

                print(
                    f"  → Call created: {call.sid}"
                )

            except Exception as error:

                print(
                    f"  → Twilio call failed: {error}"
                )

                continue

            # --------------------------------
            # STEP 2: Update Google Sheet
            # --------------------------------
            try:

                result = sheets.update_status(
                    row_number=row_number,
                    reminder_status="sent",
                    call_status="initiated"
                )

                print(
                    f"  → Sheet updated successfully: "
                    f"{result}"
                )

            except Exception as error:

                print(
                    f"  → WARNING: Call succeeded, "
                    f"but Sheet update failed: {error}"
                )

        else:

            reminder_status = str(
                ride.get("reminder_status", "")
            ).strip().lower()

            if reminder_status == "sent":

                print(
                    "  → Reminder already sent"
                )

            else:

                print(
                    "  → No reminder needed"
                )

        print()


if __name__ == "__main__":
    main()