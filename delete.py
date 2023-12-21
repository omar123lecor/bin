#!/usr/bin/env python3
import argparse
import os
import shutil
import json
import sys
from status import check_login_status
from datetime import datetime

BASE_PATH = os.path.expanduser("~/ID1FS/home")
METADATA_PATH = os.path.expanduser("~/ID1FS/metadata/metadata.json")
BACKUP_PATH = os.path.expanduser("~/ID1FS/backup")
LOG_PATH = os.path.expanduser("~/ID1FS/log")
LOG_FILE_NAME = "execution_log.txt"

def get_full_path(name):
    return os.path.join(BASE_PATH, name)

def create_backup(name):
    if not os.path.exists(BACKUP_PATH):
        os.makedirs(BACKUP_PATH)

    source_path = get_full_path(name)
    backup_path = os.path.join(BACKUP_PATH, f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    shutil.copy2(source_path, backup_path)
    log_execution("Backup", f"Item '{name}' backed up to '{backup_path}'.")

def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")

def create_metadata(name, is_directory):
    metadata = {}

    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r') as metadata_file:
            metadata = json.load(metadata_file)

    full_path = get_full_path(name)
    stat_info = os.stat(full_path)

    metadata[name] = {
        'path': full_path,
        'created_at': format_timestamp(stat_info.st_ctime),
        'last_modified_at': format_timestamp(stat_info.st_mtime),
        'size': stat_info.st_size,
        'permissions': oct(stat_info.st_mode & 0o777),  # Convert to octal
        'owner': stat_info.st_uid,
        'group': stat_info.st_gid,
        'is_directory': is_directory
    }

    with open(METADATA_PATH, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=2)
        print(f"Metadata added for '{name}'.")
        log_execution("Metadata Creation", f"Metadata added for '{name}'.")

def delete_item(name, is_directory):
    full_path = get_full_path(name)

    try:
        create_backup(name)

        if is_directory:
            try:
                # Supprimez le dossier et ses sous-dossiers
                shutil.rmtree(full_path)
                print(f"Le dossier {full_path} et ses sous-dossiers ont été supprimés avec succès.")
                log_execution("Directory Deletion", f"Directory '{full_path}' deleted successfully.")
            except Exception as e:
                print(f"Erreur lors de la suppression du dossier {full_path}: {e}")
                log_execution("Directory Deletion Error", f"Error deleting directory '{full_path}': {str(e)}")
        else:
            os.remove(full_path)
            print(f"File '{full_path}' deleted successfully.")
            log_execution("File Deletion", f"File '{full_path}' deleted successfully.")

        remove_metadata(name)

    except Exception as e:
        item_type = "Directory" if is_directory else "File"
        log_execution(f"{item_type} Deletion Error", f"Error deleting {item_type.lower()} '{full_path}': {str(e)}")
        print(f"Error deleting {item_type.lower()} '{full_path}': {str(e)}")

def remove_metadata(name):
    metadata = {}

    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r') as metadata_file:
            metadata = json.load(metadata_file)

    if name in metadata:
        del metadata[name]

        with open(METADATA_PATH, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=2)
            print(f"Metadata removed for '{name}'.")
            log_execution("Metadata Removal", f"Metadata removed for '{name}'.")

def delete_directory(directory_name):
    base_path = os.path.expanduser("~/ID1FS/home")
    target_directory = os.path.join(base_path, directory_name)

    if os.path.exists(target_directory) and os.path.isdir(target_directory):
        try:
            shutil.rmtree(target_directory)
            print(f"Le dossier {target_directory} et ses sous-dossiers ont été supprimés avec succès.")
        except Exception as e:
            print(f"Erreur lors de la suppression du dossier {target_directory}: {e}")
    else:
        print(f"Le dossier {target_directory} n'existe pas ou n'est pas un répertoire.")

def main():
    if not check_login_status():
        log_execution("Error", "Script execution failed: Login status is inactive.")
        return

    parser = argparse.ArgumentParser(description="Command for deleting files and directories")

    parser.add_argument('-f', '--delete-file', metavar='FILENAME', help='Delete a file')
    parser.add_argument('-d', '--delete-dir', metavar='DIRNAME', help='Delete a directory')

    args = parser.parse_args()

    if args.delete_file:
        delete_item(args.delete_file, False)
    elif args.delete_dir:
        delete_item(args.delete_dir, True)
    else:
        log_execution("Error", "Script execution failed: Missing options or filename.")
        parser.print_help()

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "-d":
        directory_name = sys.argv[2]
        delete_directory(directory_name)
    else:
        main()

