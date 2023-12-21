#!/usr/bin/env python3
import json
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.expanduser("~"), "ID1FS/log")
LOG_FILE_NAME = "execution_log.txt"

def check_login_status():
    file_path = os.path.join(os.path.expanduser("~"), "ID1FS/metadata/login_status.json")
    try:
        with open(file_path, "r") as status_file:
            status_data = json.load(status_file)
            return status_data["status"]
    except FileNotFoundError:
        return False

def log_execution(action, success):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Success: {success}\n")
        log_file.write("\n")  # Add a separator for better readability between log entries

def main():
    if check_login_status():
        print("Status: ON")
        log_execution("Check Status", True)
    else:
        print("Status: OFF")
        log_execution("Check Status", False)

if __name__ == "__main__":
    main()

