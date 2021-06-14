# Projet 4 : Développez un programme logiciel en Python

Le Projet 4  est une application qui permet de gérer les tournois d'échecs 
(système suisse des tournois) à éxécuter localement
   
## Installation et exécution de l'application sans pipenv (avec venv et pip)

1. Cloner ce dépôt de code à l'aide de la commande `$ git clone clone https://github.com/ML-coder-60/projet4.git` 
2. Rendez-vous depuis un terminal à la racine du répertoire projet4 avec la commande `$ cd projet4`
3. Créer un environnement virtuel pour le projet avec 
            `$ python -m venv env` sous windows 
            `$ python3 -m venv env` sous macos ou linux.
4. Activez l'environnement virtuel avec `$ env\Scripts\activate` sous windows ou `$ source env/bin/activate` sous macos ou linux.
5. Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`
6. Démarrer l' application `$ python main.py`

## Utilisation 

Lorsque le programme est lancé . 
Utilisateur peut 

1. Modifier/Lister/Créer les joueurs à laide du menu player management
2. Lister/charger/Créer des tournois à laide du menu tournament management

## Créer un rapport Flake8 du code au format Html 

1. Rendez-vous depuis un terminal à la racine du répertoire projet4 avec la commande `$ cd projet4`
1. Installer les dépendances Flake avec la commande `$ pip install -r requirements-flake.txt`
3. Générer le rapport dans le répertoire flake8_report avec la commande  
    `$ flake8  --max-line-length 119  --exclude="./env/*"  --format=html --htmldir=flake8_report`
4. Ouvrir le fichier index.html situé dans le répertoire flake8_report pour visualiser le rapport


