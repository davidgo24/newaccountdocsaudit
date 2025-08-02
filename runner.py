import subprocess
from datetime import datetime

# Set filename with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"compliance_log_{timestamp}.txt"

# Run main.py and capture output to file
with open(log_filename, "w") as f:
    subprocess.run(["python3", "main.py"], stdout=f)

# testing with terminal
with open(log_filename, "r") as f:
    print("\n📋 Compliance Check Output:\n")
    print(f.read())
