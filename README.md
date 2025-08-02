# Missing Docs Alert – Internal Ops Prototype

This is a working prototype simulating a tool that tracks missing document uploads for new member accounts. It’s based on a real operational issue I observed while working at a credit union.

When new accounts are opened, documents like IDs, Membership Applications, and Agreements are expected to be uploaded to Synergy. If they’re not, Symitar profiles remain incomplete. This can cause downstream issues during verification or service interactions.

---

## What This Prototype Does

1. Tracks which members are still missing required documentation
2. Identifies the employee who opened the account
3. Simulates two scheduled emails:
   - Morning reminder (9:00 AM) to the employee
   - Afternoon escalation (2:30 PM) to employee + manager + new accounts team

All logic is handled on the frontend using Alpine.js. Data is mocked via local JSON files, and the app simulates real-time checks by running on load. This mimics an automated system polling Synergy every x minutes.

---


## Compliance Logic

- Members with all required docs uploaded within the last 72 hours are marked **in compliance**
- Older compliant entries fade out visually
- Members with incomplete documentation after 24 hours from account opening are flagged **out of compliance**

Each entry displays:
- Member name and ID
- Missing documents (if any)
- Employee who opened the account
- Scheduled email preview for accountability

