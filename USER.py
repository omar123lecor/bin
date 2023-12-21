#!/usr/bin/env python3
import argparse
import getpass
import crypt
import json
import os
import subprocess
from datetime import datetime

LOG_PATH = os.path.join(os.path.expanduser("~"), "ID1FS/log")
LOG_FILE_NAME = "execution_log.txt"
USERS_FILE = "/ID1FS/bin/users.json"
LOGIN_STATUS_FILE = os.path.join(os.path.expanduser("~"), "ID1FS/metadata/login_status.json")

def crypter_mot_de_passe(mot_de_passe):
    # Utilisation de la méthode SHA-512 pour le cryptage du mot de passe
    return crypt.crypt(mot_de_passe, crypt.mksalt(crypt.METHOD_SHA512))

def ajouter_utilisateur_systeme(nom_utilisateur):
    log_execution("add")
    # Vérifier si l'utilisateur existe déjà
    try:
        subprocess.run(["id", nom_utilisateur], check=True)
        print(f"L'utilisateur {nom_utilisateur} existe déjà.")
        return
    except subprocess.CalledProcessError:
        pass

    # Ajouter l'utilisateur en utilisant la commande adduser
    subprocess.run(["sudo", "adduser", "--disabled-password", "--gecos", "", nom_utilisateur])

    # Enregistrez le nom d'utilisateur dans le fichier users.json
    enregistrer_utilisateur(nom_utilisateur)

    print(f"L'utilisateur {nom_utilisateur} a été ajouté avec succès.")
    # Set the user password using passwd
    subprocess.run(["sudo", "passwd", nom_utilisateur])

def enregistrer_utilisateur(nom_utilisateur):
    # Charger les utilisateurs existants depuis le fichier users.json s'il existe
    utilisateurs = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            utilisateurs = json.load(file)

    # Enregistrer le nouvel utilisateur
    utilisateurs[nom_utilisateur] = crypter_mot_de_passe("")  # empty password as a placeholder

    # Écrire la liste mise à jour dans le fichier users.json
    with open(USERS_FILE, "w") as file:
        json.dump(utilisateurs, file)

def supprimer_utilisateur(nom_utilisateur):
    log_execution("delete")
    try:
        subprocess.run(["sudo", "deluser", nom_utilisateur], check=True)
        print(f"L'utilisateur {nom_utilisateur} a été supprimé avec succès.")

        # Supprimer l'utilisateur du fichier users.json s'il existe
        supprimer_utilisateur_fichier(nom_utilisateur)
    except subprocess.CalledProcessError:
        print(f"L'utilisateur {nom_utilisateur} n'existe pas.")

def supprimer_utilisateur_fichier(nom_utilisateur):
    # Charger les utilisateurs existants depuis le fichier users.json s'il existe
    utilisateurs = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            utilisateurs = json.load(file)

        # Supprimer l'utilisateur du fichier users.json
        if nom_utilisateur in utilisateurs:
            del utilisateurs[nom_utilisateur]

            # Écrire la liste mise à jour dans le fichier users.json
            with open(USERS_FILE, "w") as file:
                json.dump(utilisateurs, file)

def changer_utilisateur(nom_utilisateur):
    log_execution("switch")
    try:
        subprocess.run(["sudo", "su", "-", nom_utilisateur], check=True)
    except subprocess.CalledProcessError:
        print(f"L'utilisateur {nom_utilisateur} n'existe pas.")

def check_login_status():
    # Check the login status from the login_status.json file
    if os.path.exists(LOGIN_STATUS_FILE):
        with open(LOGIN_STATUS_FILE, "r") as status_file:
            login_status = json.load(status_file)
            return login_status.get("status", False)
    return False

def login():
    if check_user_credentials():
        print("Login successful!")
        save_login_status(True)
        log_execution("Login", True)
    else:
        print("Login failed. Exiting.")
        save_login_status(False)
        log_execution("Login", False)

def check_user_credentials():
    # Simulate successful credential verification
    return True

def logout():
    print("Logout successful.")
    save_login_status(False)
    log_execution("Logout", True)

def save_login_status(status):
    # Save the login status to the login_status.json file
    with open(LOGIN_STATUS_FILE, "w") as status_file:
        json.dump({"status": status}, status_file)

def log_execution(action, success=None):
    log_file_path = os.path.join(LOG_PATH, LOG_FILE_NAME)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if success is not None:
            log_file.write(f"Success: {success}\n")
        log_file.write("\n")

def main():
    parser = argparse.ArgumentParser(description="Gérer les utilisateurs.")
    parser.add_argument("action", choices=["add", "delete", "switch"], help="Action à effectuer (add, delete, switch).")
    parser.add_argument("nom_utilisateur", help="Nom de l'utilisateur.")

    args = parser.parse_args()

    if args.action == "switch":
        changer_utilisateur(args.nom_utilisateur)
    else:
        # Check login status before allowing user management actions
        if not check_login_status():
            print("You need to login first.")
            return

        if args.action == "add":
            ajouter_utilisateur_systeme(args.nom_utilisateur)

        elif args.action == "delete":
            supprimer_utilisateur(args.nom_utilisateur)

if __name__ == "__main__":
    main()

