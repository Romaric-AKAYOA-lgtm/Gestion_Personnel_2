import os
import webbrowser
import subprocess
import time
import sys

def start_server():
    try:
        # Lancer le serveur Django dans un sous-processus
        process = subprocess.Popen([sys.executable, "manage.py", "runserver"])

        # Attendre un peu pour que le serveur démarre
        time.sleep(2)

        # Ouvrir automatiquement le navigateur par défaut
        webbrowser.open("http://127.0.0.1:8000")

        # Attendre que le processus serveur se termine
        process.wait()

    except KeyboardInterrupt:
        print("Arrêt manuel détecté.")

    finally:
        # Fermer proprement le processus
        try:
            process.terminate()
        except Exception:
            pass
        os._exit(0)

# Ne pas lancer automatiquement si ce fichier est importé ailleurs
if __name__ == "__main__":
    start_server()
