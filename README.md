# Projet 10 - Recommandation de Contenu

### Description du projet
Ce projet consiste à développer un système de recommandation de contenu pour la startup My Content. L’objectif est de proposer à chaque utilisateur 5 articles personnalisés en combinant deux approches :

Filtrage collaboratif (SVD) basé sur les interactions passées des utilisateurs.
Filtrage basé sur le contenu (similarité cosinus sur les embeddings).
L’ensemble est déployé sur Google Cloud en utilisant une architecture serverless avec Cloud Run, Cloud Functions, Cloud Storage et Docker.

### Installation et exécution locale

##### Prérequis
Python 3.11
Google Cloud SDK installé et configuré
Docker installé (optionnel pour exécuter l’API en conteneur)
Clé API Google Cloud configurée

##### Cloner le projet
git clone https://github.com/SamLouis1980/P10---Recommandation-de-Contenu.git

cd P10---Recommandation-de-Contenu

##### Lancer l’interface Streamlit (locale)
streamlit run app.py

### Description des fichiers et dossiers

.gitignore → Liste des fichiers à ignorer

Dockerfile → Fichier pour créer l’image Docker de l’API

docker-compose.yml → Configuration pour exécuter le projet en local

requirements.txt → Dépendances nécessaires pour l'API

app.py → Interface utilisateur (Streamlit)

##### cloud_function/
Contient le code de la Google Cloud Function, qui sert d’intermédiaire entre l’interface et l’API.

main.py → Code de la Cloud Function.

requirements.txt → Liste des dépendances nécessaires.

##### app/
main.py → Contient les endpoints de l’API

model.py → Implémente le système de recommandation

data_loader.py → Chargement des modèles et des fichiers

utils.py → Fonctions utilitaires diverses

