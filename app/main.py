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
logging.info(f"Type de svd_model: {type(svd_model)}")
interactions = load_interactions()
articles_embeddings = load_embeddings()
logging.info("Chargement terminé !")


@app.get("/")
def home():
    """
    Vérification du bon fonctionnement de l'API.
    """
    return {"message": "API de recommandation en ligne !"}


@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int, top_n: int = 5):
    logging.info(f"Requête reçue pour l'utilisateur {user_id}, top {top_n}")

    if user_id not in interactions['user_id'].values:
        return {"message": "Utilisateur inconnu"}

    user_rated_articles = interactions[interactions["user_id"] == user_id]["article_id"].tolist()

    predictions = []
    for article_id in range(articles_embeddings.shape[0]):
        if article_id not in user_rated_articles:
            pred = svd_model.predict(user_id, article_id)
            predictions.append((article_id, pred.est))

    predictions.sort(key=lambda x: x[1], reverse=True)
    recommended_articles = [{"id": article[0], "score": article[1]} for article in predictions[:top_n]]

    return {"user_id": user_id, "recommendations": recommended_articles}
