import json
from datetime import datetime

#loading jsons - json used for quick prototype - ideally we'd try to get new acct reports data access

with open("mock_data/member_apps.json", "r") as f:
    member_apps = json.load(f)

with open("mock_data/upload_logs.json", "r") as f:
    upload_logs = json.load(f)

OPS_EMAIL = "ops@creditunion.com"
NOW = datetime.now()
ALERT_9AM = NOW.replace(hour=9, minute=0, second=0, microsecond=0)
ALERT_230PM = NOW.replace(hour=14, minute=30, second=0, microsecond=0)

#getter to retrieve uploaded docs for a member
def get_uploaded_docs_for_member(member_id):
    for log in upload_logs:
        if log["member_id"] == member_id:
            return log["uploaded_docs"]
    return []

#helper to send email - creating local logs for prototype 
def send_email_alert(member, missing_docs, escalation=False):
    print("\n📩 EMAIL SENT")
    print(f"To: {member['employee_email']}")
    if escalation:
        print(f"CC: {member['manager_email']}, {OPS_EMAIL}")
    print(f"Subject: {'URGENT' if escalation else 'Reminder'} – Missing Documents for Member #{member['member_id']}")
    print(f"Missing Docs: {', '.join(missing_docs)}")
    print("Deadline: End of Day Today")
    print("-" * 50)

#results tracker - for compliance logging
compliant_members = []
noncompliant_members = []

#main loop
for member in member_apps:
    opened_date = datetime.fromisoformat(member["opened_date"])
    hours_since_open = (NOW - opened_date).total_seconds() / 3600

    if hours_since_open < 24:
        continue  # Give employee a full 24hr window before checking

    uploaded_docs = get_uploaded_docs_for_member(member["member_id"])
    missing_docs = [doc for doc in member["required_docs"] if doc not in uploaded_docs]

    if not missing_docs:
        compliant_members.append(member)
        continue  

    noncompliant_members.append((member, missing_docs))

    if NOW >= ALERT_230PM:
        send_email_alert(member, missing_docs, escalation=True)
    elif NOW >= ALERT_9AM:
        send_email_alert(member, missing_docs, escalation=False)

#print report - always useful for daily ops
print("\n DAILY COMPLIANCE CHECK –", NOW.strftime("%B %d, %Y"))

print("\n In Compliance:")
for m in compliant_members:
    print(f"- {m['member_name']} (#{m['member_id']})")

print("\n Still Missing Docs:")
for m, missing in noncompliant_members:
    print(f"- {m['member_name']} (#{m['member_id']}): {', '.join(missing)}")

print(f"\nChecked {len(compliant_members) + len(noncompliant_members)} member(s)")
