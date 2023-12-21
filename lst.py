#!/usr/bin/env python3
import os
import argparse
from datetime import datetime
from status import check_login_status

ID1FS_PATH = os.path.expanduser("~/ID1FS")
LOG_PATH = os.path.join(ID1FS_PATH, "log")
LOG_FILE_NAME = "execution_log.txt"


def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")


def list_directory_content(path, include_subdirectories, include_files):
    for element in os.listdir(path):
        element_path = os.path.join(path, element)
        if os.path.isfile(element_path) and include_files:
            print(element)
            if include_subdirectories:
                with open(element_path, 'r') as file_content:
                    content = file_content.read()
                    print(f"    Contenu du fichier:\n{content}")
        elif os.path.isdir(element_path) and include_subdirectories:
            print(f"{element} (dossier)")
            if include_files:
                for sous_element in os.listdir(element_path):
                    print(f"  {sous_element}")


# Vérifiez le statut avant d'exécuter le script principal
if check_login_status():
    os.chdir(ID1FS_PATH)  # Changez le répertoire de travail vers ~/ID1FS

    # Configuration de l'analyseur d'arguments
    parser = argparse.ArgumentParser(description="Liste le contenu du répertoire courant avec différentes options.")
    parser.add_argument('path', nargs='?', default='home', help='Chemin du répertoire à lister (par défaut, ~/ID1FS/home)')
    parser.add_argument('-f', '--fichiers', action='store_true', help='Afficher uniquement les fichiers')
    parser.add_argument('-d', '--repertoires', action='store_true', help='Afficher uniquement les répertoires')
    parser.add_argument('-a', '--caches', action='store_true', help='Afficher les fichiers cachés')
    parser.add_argument('-l', '--long', action='store_true', help='Afficher les détails des fichiers')
    parser.add_argument('-n', '--nombre', action='store_true', help='Calculer le nombre de fichiers dans le répertoire')

    # Analyse des arguments de la ligne de commande
    args = parser.parse_args()

    # Vérifiez si le chemin spécifié existe, sinon utilisez le répertoire courant
    path = os.path.join(ID1FS_PATH, args.path) if args.path else ID1FS_PATH

    # Liste les fichiers dans le répertoire spécifié
    liste_fichiers_courant = os.listdir(path)

    # Filtrer les fichiers et répertoires selon les options
    if args.fichiers:
        liste_fichiers_courant = [fichier for fichier in liste_fichiers_courant if os.path.isfile(fichier)]
        print(f"Contenu du répertoire {args.path} (fichiers seulement):")
        log_execution("List Files", f"Listing files in the directory {args.path}.")
        for fichier in liste_fichiers_courant:
            print(fichier)
            if args.repertoires:
                with open(fichier, 'r') as file_content:
                    content = file_content.read()
                    print(f"    Contenu du fichier:\n{content}")
    elif args.repertoires:
        liste_fichiers_courant = [fichier for fichier in liste_fichiers_courant if os.path.isdir(fichier)]
        print(f"les répertoires existants dans le répertoire {args.path}:")
        log_execution("List Directories", f"Listing directories in the directory {args.path}.")
        for fichier in liste_fichiers_courant:
            print(fichier)
    elif args.caches:
        liste_fichiers_courant = [fichier for fichier in liste_fichiers_courant if fichier.startswith('.')]
        print(f"Contenu du répertoire {args.path} (fichiers cachés):")
        log_execution("List Hidden Files", f"Listing hidden files in the directory {args.path}.")
        for fichier in liste_fichiers_courant:
            print(fichier)
    elif args.long:
        print(f"Contenu du répertoire {args.path} (détails des fichiers):")
        log_execution("List File Details", f"Listing file details in the directory {args.path}.")
        for fichier in liste_fichiers_courant:
            stat_info = os.stat(fichier)
            date_modification = datetime.utcfromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            type_fichier = 'd' if os.path.isdir(fichier) else '-'
            print(f"{type_fichier}{os.stat(fichier).st_mode:04o} {stat_info.st_nlink} {stat_info.st_uid} {stat_info.st_gid} {stat_info.st_size} {date_modification} {fichier}")

    # Liste les fichiers et répertoires dans le répertoire spécifié
    print(f"\nContenu du répertoire {args.path}:")
    log_execution("List All in Directory", f"Listing all files and directories in the directory {args.path}.")
    list_directory_content(path, args.repertoires, args.fichiers)

else:
    print("Le statut de connexion est désactivé. Veuillez activer le système.")
    log_execution("Error", "Connection status is off. Please login first.")

