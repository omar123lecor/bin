#!/usr/bin/env python3

import argparse
import os
from status import check_login_status
from datetime import datetime

LOG_PATH = os.path.join(os.path.expanduser("~"), "ID1FS/log")
LOG_FILE_NAME = "execution_log.txt"

def log_command(command, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Command: {command}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")  # Add a separator for better readability between log entries

def count_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return len(lines)

def main():
    # Check status before running the script
    if not check_login_status():
        print("Login status is disabled. Please enable the system.")
        return

    # Setup command line argument parser
    parser = argparse.ArgumentParser(description="Count the number of lines, characters, or words in a file.")
    parser.add_argument('file', metavar='FILE', type=str, help='The path to the file to analyze')
    parser.add_argument('-c', '--characters', action='store_true', help='Count the number of characters instead of lines')
    parser.add_argument('-w', '--words', action='store_true', help='Count the number of words instead of lines')
    parser.add_argument('-l', '--lines', action='store_true', help='Count the number of lines (default)')

    # Parse command line arguments
    args = parser.parse_args()

    # Construct the full path to the file in the '~/ID1FS/home' directory
    file_path = os.path.join(os.path.expanduser("~/ID1FS/home"), args.file)

    # Log the command
    log_command("count_lines", f"File: {file_path}, Characters: {args.characters}, Words: {args.words}, Lines: {args.lines}")

    if args.characters:
        with open(file_path, 'r') as file:
            content = file.read()
            count = len(content)
            print(f"Number of characters in {file_path}: {count}")
    elif args.words:
        with open(file_path, 'r') as file:
            content = file.read()
            words = content.split()
            count = len(words)
            print(f"Number of words in {file_path}: {count}")
    else:
        # Default, or if -l is specified, count the number of lines
        count = count_lines(file_path)
        print(f"Number of lines in {file_path}: {count}")

if __name__ == "__main__":
    main()

