# Utiliser une image officielle Python
FROM python:3.11

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du projet
COPY . .

# Exposer le port de l’API
EXPOSE 8000

# Commande de démarrage de l’API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
