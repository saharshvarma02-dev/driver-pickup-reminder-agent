# Driver Pickup Reminder Agent

An automated driver pickup reminder system that monitors scheduled rides, determines when a reminder is required, places a voice call through Twilio, and updates the ride status in Google Sheets.

The project is built as a lightweight Python automation agent with Google Apps Script acting as the bridge to Google Sheets.

---

## Overview

The Driver Pickup Reminder Agent is designed to reduce missed driver pickups by automatically identifying rides approaching their scheduled pickup time.

The agent:

1. Retrieves scheduled rides from Google Sheets.
2. Calculates the time remaining until each pickup.
3. Determines whether a reminder is required.
4. Places a voice call using Twilio.
5. Updates the corresponding ride in Google Sheets.
6. Prevents duplicate reminders using the ride's reminder status.

The system can be run repeatedly without repeatedly calling drivers who have already received their reminder.

---

## Architecture

```text
                 Google Sheets
                      │
                      ▼
              Google Apps Script
                      │
                      ▼
                Python Agent
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   Reminder Engine          Twilio Service
          │                       │
          │                       ▼
          │                  Voice Call
          │
          ▼
   Reminder Status
          │
          ▼
   Already Sent?
      │       │
     YES      NO
      │       │
      ▼       ▼
    Skip    Call Driver
              │
              ▼
       Update Google Sheet
         status = sent
