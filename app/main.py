from fastapi import FastAPI
from app.data_loader import load_recommendations, load_svd_model, load_interactions, load_embeddings
import logging
import numpy as np
import pandas as pd
from app.utils import setup_logging

# Configuration des logs
setup_logging()

# Initialisation de l'application FastAPI
app = FastAPI(title="Content Recommendation API")

# Chargement des données au démarrage de l'API
logging.info("Chargement des modèles et des données...")
recommendations = load_recommendations()
svd_model = load_svd_model()
interactions = load_interactions()
embeddings = load_embeddings()
logging.info("Chargement terminé !")


@app.get("/")
def home():
    """
    Vérification du bon fonctionnement de l'API.
    """
    return {"message": "API de recommandation en ligne !"}


@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int, top_n: int = 5):
    """
    Génère des recommandations pour un utilisateur donné.
    
    Args:
    - user_id (int): L'ID de l'utilisateur pour lequel générer des recommandations.
    - top_n (int): Nombre de recommandations à retourner (par défaut: 5).

    Returns:
    - dict: Liste des articles recommandés avec leurs scores.
    """
    logging.info(f"Requête reçue pour l'utilisateur {user_id}, top {top_n}")

    if user_id not in interactions["user_id"].values:
        return {"message": "Utilisateur inconnu ou aucune interaction enregistrée."}

    # Prédictions avec SVD
    predictions = []
    all_article_ids = interactions["article_id"].unique()

    for article_id in all_article_ids:
        pred = svd_model.predict(user_id, article_id)
        predictions.append((article_id, pred.est))

    # Trier les prédictions par score décroissant
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    # Sélectionner les N meilleurs articles recommandés
    top_recommendations = predictions[:top_n]

    # Transformer en format JSON
    response = {
        "user_id": user_id,
        "recommendations": [
            {"article_id": article_id, "score": round(score, 4)}
            for article_id, score in top_recommendations
        ]
    }

    logging.info(f"Recommandations générées pour {user_id}: {response}")

    return response