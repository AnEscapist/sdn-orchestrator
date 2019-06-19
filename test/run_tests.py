import subprocess

subprocess.run(["python", "-m", "pytest", "-s"])
subprocess.run(["notify-send", "tests finished"])

