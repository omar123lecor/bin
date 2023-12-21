#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime

# Use os.path.expanduser("~") to dynamically obtain the home directory

LOG_PATH = os.path.join(os.path.expanduser("~"), "ID1FS/log")
LOG_FILE_NAME = "execution_log.txt"
LOGIN_STATUS_PATH = os.path.join(os.path.expanduser("~"), "ID1FS/metadata/login_status.json")
TARGET_DIRECTORY = os.path.join(os.path.expanduser("~"), "ID1FS/home")

def check_login_status():
    try:
        with open(LOGIN_STATUS_PATH, "r") as status_file:
            status_data = json.load(status_file)
            return status_data["status"]
    except FileNotFoundError:
        return False

def display_file_content(filename, options):
    if check_login_status():
        # Prepend the default directory if no path is specified
        if not os.path.isabs(filename):
            filename = os.path.join(TARGET_DIRECTORY, filename)

        # Check if the file is in the target directory
        if os.path.abspath(filename).startswith(os.path.abspath(TARGET_DIRECTORY)):
            try:
                with open(filename, "r") as file:
                    content = file.read()

                    if options.a:
                        # Display numbered lines
                        content = [f"{i+1}: {line}" for i, line in enumerate(content.splitlines())]
                        content = "\n".join(content)
                        print(f"File content:\n{content}")
                    elif options.b:
                        # Display the number of lines
                        line_count = len(content.splitlines())
                        print(f"Number of lines in '{filename}': {line_count}")
                    elif options.r:
                        # Display the number of characters
                        char_count = len(content)
                        print(f"Number of characters in '{filename}': {char_count}")
                    else:
                        print(f"File content:\n{content}")

                    # Log the display content action
                    log_execution("Display Content", f"Content of file '{filename}' displayed.")
            except FileNotFoundError:
                # Log the file not found error
                log_execution("Error", f"File '{filename}' not found.")
                print(f"Error: File '{filename}' not found.")
        else:
            # Log the unauthorized file error
            log_execution("Error", f"File '{filename}' is not allowed. It must be in the directory '{TARGET_DIRECTORY}'.")
            print(f"Error: File '{filename}' is not allowed. It must be in the directory '{TARGET_DIRECTORY}'.")
    else:
        # Log the connection status off error
        log_execution("Error", "Connection status is off. Please login first.")
        print("Error: Connection status is off. Please login first.")

def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")  # Add a separator for better readability between log entries

def main():
    parser = argparse.ArgumentParser(description="Display file content with specific options if connection status is on")
    parser.add_argument("filename", help="Name of the file to display")
    parser.add_argument("-a", action="store_true", help="Display lines with line numbers")
    parser.add_argument("-b", action="store_true", help="Display the number of lines in the file")
    parser.add_argument("-r", action="store_true", help="Display the number of characters in the file")

    args = parser.parse_args()
    display_file_content(args.filename, args)

if __name__ == "__main__":
    main()

