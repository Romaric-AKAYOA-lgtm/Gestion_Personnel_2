from setuptools import setup, find_packages
import os

# Lire et traiter le fichier requirements.txt si disponible
requirements_file = "requirements.txt"
if os.path.exists(requirements_file):
    with open(requirements_file, encoding="utf-8") as f:
        required = [
            line.strip() for line in f.readlines() 
            if line.strip() and not line.startswith("#")  # Ignore les lignes vides et les commentaires
        ]
else:
    required = []

setup(
    name="Gestion_Personnel_2",  # ✅ Nom du package modifié
    version="1.0",  # Version du package
    description="Application de gestion du personnel",  # ✅ Description modifiée
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Ton Nom",  # À personnaliser
    author_email="ton.email@example.com",  # À personnaliser
    license="MIT",
    url="https://github.com/ton-projet/Gestion_Personnel_2",  # ✅ URL modifiée
    packages=find_packages(),
    install_requires=required,
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "start-django=Gestion_Personnel_2.start_server:start_server",  # ✅ Entrée modifiée
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://github.com/ton-projet/Gestion_Personnel_2/wiki",  # ✅ Lien doc modifié
        "Code Source": "https://github.com/ton-projet/Gestion_Personnel_2",  # ✅ Code source modifié
        "Issues": "https://github.com/ton-projet/Gestion_Personnel_2/issues",  # ✅ Issues modifié
    },
)
