#!/usr/bin/python3
import json
import os
import argparse
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

def est_executable(chemin_fichier):
    return os.access(chemin_fichier, os.X_OK)

def chercher_fichier(chemin, nom_fichier, afficher_type, afficher_executable):
    if not nom_fichier:
        print("Erreur : Veuillez fournir un nom de fichier.")
        log_execution("Error", "No file name provided")
        return None

    if not afficher_type and not afficher_executable:
        print("Erreur : Veuillez spécifier au moins l'une des options -type ou -x.")
        log_execution("Error", "Missing -type or -x option")
        return None

    chemin = os.path.expanduser(chemin)

    for dossier_actuel, sous_dossiers, fichiers in os.walk(chemin):
        if nom_fichier in fichiers or nom_fichier in sous_dossiers:
            chemin_fichier_trouve = os.path.join(dossier_actuel, nom_fichier)

            if afficher_type:
                est_repertoire = os.path.isdir(chemin_fichier_trouve)
                est_fichier = os.path.isfile(chemin_fichier_trouve)

                if est_fichier:
                    print(f"Le chemin '{chemin_fichier_trouve}' est un fichier.")
                    log_execution("Search", f"Found file: {chemin_fichier_trouve} (File)")
                elif est_repertoire:
                    print(f"Le chemin '{chemin_fichier_trouve}' est un répertoire.")
                    log_execution("Search", f"Found file: {chemin_fichier_trouve} (Directory)")

            if afficher_executable:
                if os.path.isfile(chemin_fichier_trouve):
                    est_script_executable = est_executable(chemin_fichier_trouve)

                    if est_script_executable:
                        print(f"Le fichier '{nom_fichier}' est un script exécutable.")
                        log_execution("Search", f"Found file: {chemin_fichier_trouve} (Executable Script)")
                    else:
                        print(f"Le fichier '{nom_fichier}' est un fichier texte.")
                        log_execution("Search", f"Found file: {chemin_fichier_trouve} (Text File)")
                else:
                    print(f"Le chemin '{chemin_fichier_trouve}' est un répertoire.")
                    log_execution("Search", f"Found file: {chemin_fichier_trouve} (Directory)")

            return chemin_fichier_trouve

    print(f"Le fichier '{nom_fichier}' n'a pas été trouvé dans le chemin spécifié.")
    log_execution("Search", f"File not found: {nom_fichier}")
    return None

def log_execution(action, details):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Details: {details}\n")
        log_file.write("\n")  # Add a separator for better readability between log entries

def main():
    parser = argparse.ArgumentParser(description="Trouver un fichier dans les sous-dossiers du répertoire pré-défini.")
    parser.add_argument("nom_fichier", nargs="?", help="Le nom du fichier ou du répertoire à rechercher.")
    parser.add_argument("-type", "--type", action="store_true", help="Afficher le type du chemin (fichier ou répertoire).")
    parser.add_argument("-x", "--executable", action="store_true", help="Vérifier si le fichier est un script exécutable.")

    args = parser.parse_args()
    nom_fichier_recherche = args.nom_fichier

    if check_login_status():
        # Remplacez cela par le répertoire que vous souhaitez explorer
        chemin_recherche = "~/ID1FS/home"

        # Utilisation de la fonction chercher_fichier avec les options
        resultat = chercher_fichier(
            chemin_recherche, nom_fichier_recherche,
            args.type, args.executable
        )
    else:
        print("Le statut de connexion est désactivé. Veuillez activer le système.")

if __name__ == "__main__":
    main()
