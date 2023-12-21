#!/usr/bin/python3
import os
import json
from datetime import datetime
import subprocess
import argparse
from status import check_login_status

# Chemin de base
base_path = os.path.expanduser('~/ID1FS/home')
# Chemin du fichier JSON de métadonnées
metadata_path = os.path.expanduser('~/ID1FS/metadata/metadata.json')

LOG_PATH = os.path.expanduser("~/ID1FS/log")
LOG_FILE_NAME = "execution_log.txt"

def format_timestamp(timestamp):
    # Formater le timestamp en une chaîne de date lisible
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def update_metadata(filename):
    # Charger les métadonnées existantes depuis le fichier JSON
    metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as metadata_file:
            metadata = json.load(metadata_file)

    # Chemin complet du fichier
    full_path = os.path.join(base_path, filename)

    # Vérifier si le fichier est dans les métadonnées
    if filename in metadata:
        # Mettre à jour la date de dernière modification
        stat_info = os.stat(full_path)
        metadata[filename]['last_modified_at'] = format_timestamp(stat_info.st_mtime)

        # Enregistrer les métadonnées mises à jour dans le fichier JSON
        with open(metadata_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=2)

        print(f"Métadonnées mises à jour pour '{full_path}'.")

def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")  # Add a separator for better readability between log entries

def edit_file_with_nano(filename):
    # Chemin complet du fichier à éditer
    full_path = os.path.join(base_path, filename)

    # Vérifier si le fichier existe
    if os.path.exists(full_path):
        # Ouvrir le fichier avec Nano pour modification
        subprocess.run(['nano', full_path])

        # Mettre à jour les métadonnées après modification
        update_metadata(filename)

        # Ajouter une entrée de journal pour l'édition du fichier
        log_execution("File Edit", f"File '{full_path}' edited with Nano.")
    else:
        log_execution("Error", f"File '{full_path}' not found. Edit operation aborted.")
        print(f"Le fichier '{full_path}' n'existe pas.")

if __name__ == "__main__":
    # Vérifier le statut avant d'exécuter le script
    if not check_login_status():
        log_execution("Error", "Script execution failed: Login status is inactive.")
        print("Le statut de connexion est désactivé. Veuillez activer le système.")
    else:
        parser = argparse.ArgumentParser(description="Modifier un fichier avec Nano et mettre à jour les métadonnées.")
        parser.add_argument('fichier', metavar='FICHIER', type=str, help='Le nom du fichier à modifier')
        args = parser.parse_args()

        edit_file_with_nano(args.fichier)
