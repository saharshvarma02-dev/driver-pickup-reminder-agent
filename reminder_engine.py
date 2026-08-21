from datetime import datetime, timezone


class ReminderEngine:

    def minutes_until_pickup(self, pickup_time):

        pickup = datetime.fromisoformat(
            pickup_time.replace("Z", "+00:00")
        )

        now = datetime.now(timezone.utc)

        return (
            pickup - now
        ).total_seconds() / 60

    def should_remind(self, ride):

        # Never send a duplicate reminder.
        reminder_status = str(
            ride.get("reminder_status", "")
        ).strip().lower()

        if reminder_status == "sent":
            return False

        minutes = self.minutes_until_pickup(
            ride["pickup_time"]
        )

        # Reminder window: 0–30 minutes before pickup.
        return 0 <= minutes <= 30