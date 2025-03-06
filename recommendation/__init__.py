import azure.functions as func
import logging
import json
import numpy as np
import pandas as pd
import pickle
from io import BytesIO
from azure.storage.blob import BlobServiceClient
import os

# modification pour forcer deploiement
# Récupérer la connexion Azure Blob Storage depuis les variables d'environnement
STORAGE_CONNECTION_STRING = os.getenv("AzureWebJobsStorage")
CONTAINER_NAME = "recom-storage"

# Initialisation du client Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Chargement des fichiers nécessaires avec gestion des erreurs
def load_blob(blob_name):
    try:
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob().readall()
        return blob_data
    except Exception as e:
        logging.error(f"Erreur lors du chargement du blob {blob_name}: {e}")
        return None

# Charger le modèle SVD
svd_model_data = load_blob("svd_best_model.pkl")
svd_model = pickle.loads(svd_model_data) if svd_model_data else None

# Charger les interactions utilisateur-article
interactions_data = load_blob("merged_interactions.csv")
interactions_df = pd.read_csv(BytesIO(interactions_data)) if interactions_data else pd.DataFrame()

# Charger les embeddings des articles
embeddings_data = load_blob("articles_embeddings_pca.npy")
articles_embeddings = np.load(BytesIO(embeddings_data)) if embeddings_data else None

# Charger les recommandations basées sur le contenu
recommendations_data = load_blob("top_n_recommendations_by_id.npy")
content_based_recommendations = np.load(BytesIO(recommendations_data)) if recommendations_data else None

# Fonction de recommandation hybride
def recommend_hybrid(user_id, top_n=5):
    if interactions_df.empty or not svd_model or not content_based_recommendations:
        return ["Erreur : données manquantes ou modèle indisponible"]

    user_id = int(user_id)
    user_articles = interactions_df[interactions_df['user_id'] == user_id]['article_id'].tolist()

    if user_articles:
        predictions = [svd_model.predict(user_id, article) for article in set(interactions_df['article_id'])]
        recommendations = sorted(predictions, key=lambda x: x.est, reverse=True)[:top_n]
        recommended_articles = [pred.iid for pred in recommendations]
    else:
        random_article = np.random.choice(interactions_df['article_id'].unique())
        recommended_articles = content_based_recommendations[random_article][:top_n]

    return recommended_articles

# Azure Function pour gérer les requêtes HTTP
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function - Recommandation déclenchée")

    user_id = req.params.get('userID')
    if not user_id:
        try:
            req_body = req.get_json()
            user_id = req_body.get('userID')
        except ValueError:
            pass

    if user_id:
        recommendations = recommend_hybrid(user_id)
        response = {"user_id": user_id, "recommendations": recommendations}
        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse("Merci de fournir un `userID` en paramètre.", status_code=400)
