import requests


class SheetsService:

    def __init__(self, web_app_url):
        self.web_app_url = web_app_url

    def get_rides(self):

        response = requests.get(
            self.web_app_url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def update_status(
        self,
        row_number,
        reminder_status=None,
        call_status=None
    ):

        payload = {
            "action": "update_status",
            "row_number": int(row_number)
        }

        if reminder_status is not None:
            payload["reminder_status"] = reminder_status

        if call_status is not None:
            payload["call_status"] = call_status

        response = requests.post(
            self.web_app_url,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        print(
            f"  → Apps Script HTTP status: "
            f"{response.status_code}"
        )

        print(
            f"  → Apps Script response: "
            f"{repr(response.text)}"
        )

        # Don't blindly assume the response is JSON.
        if not response.text.strip():
            return {
                "success": True,
                "message": "Empty response from Apps Script"
            }

        try:
            return response.json()

        except ValueError:
            return {
                "success": False,
                "message": "Apps Script returned non-JSON response",
                "response": response.text
            }