#!/usr/bin/env python3
import argparse
import os
import json
from status import check_login_status
from datetime import datetime

LOG_PATH = os.path.join(os.path.expanduser("~"), "ID1FS/log")
LOG_FILE_NAME = "execution_log.txt"
base_path = os.path.join(os.path.expanduser("~"), "ID1FS/home")
metadata_path = os.path.join(os.path.expanduser("~"), "ID1FS/metadata/metadata.json")

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def add_metadata(item_name, item_path):
    metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as metadata_file:
            try:
                metadata = json.load(metadata_file)
            except json.decoder.JSONDecodeError:
                print("Le fichier de métadonnées est vide ou mal formé. Il sera recréé.")

    full_path = os.path.join(base_path, item_path)

    stat_info = os.stat(full_path)

    metadata[item_name] = {
        'path': full_path,
        'created_at': format_timestamp(stat_info.st_ctime),
        'last_modified_at': format_timestamp(stat_info.st_mtime),
        'size': stat_info.st_size,
        'permissions': oct(stat_info.st_mode & 0o777),
        'owner': stat_info.st_uid,
        'group': stat_info.st_gid
    }

    with open(metadata_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=2)

    print(f"Metadata added for '{item_name}' at '{full_path}'.")
    log_execution("Metadata", f"Metadata added for '{item_name}' at '{full_path}'.")

def create_item(item_name, is_directory):
    full_path = os.path.join(base_path, item_name)

    try:
        if is_directory:
            os.makedirs(full_path, exist_ok=True)
            print(f"Répertoire '{item_name}' créé avec succès.")
            add_metadata(item_name, item_name)
            log_execution("Création de Répertoire", f"Répertoire créé : '{full_path}'")
        else:
            with open(full_path, 'w') as file:
                file.write(f"Contenu du fichier créé : {item_name}\n")
            print(f"Fichier '{item_name}' créé avec succès.")
            add_metadata(item_name, item_name)
            log_execution("Création de Fichier", f"Fichier créé : '{full_path}'")

    except Exception as e:
        print(f"Erreur lors de la création de '{item_name}': {e}")
        action_type = "Répertoire" if is_directory else "Fichier"
        log_execution(f"Erreur lors de la Création de {action_type}", f"Erreur lors de la création de '{item_name}': {str(e)}")

def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")

def main():
    if not check_login_status():
        print("Le statut de connexion est inactif. Veuillez activer le système.")
        log_execution("Erreur", "L'exécution du script a échoué : Le statut de connexion est inactif.")
        return

    parser = argparse.ArgumentParser(description="Commande pour créer des fichiers et des répertoires")

    parser.add_argument('-f', '--create-file', metavar='NOM_FICHIER', help='Créer un fichier')
    parser.add_argument('-d', '--create-dir', metavar='NOM_REPERTOIRE', help='Créer un répertoire')

    args = parser.parse_args()

    if args.create_file:
        create_item(args.create_file, False)
    elif args.create_dir:
        create_item(args.create_dir, True)
    else:
        parser.print_help()
        log_execution("Erreur", "Aucune opération spécifiée.")

if __name__ == "__main__":
    main()

