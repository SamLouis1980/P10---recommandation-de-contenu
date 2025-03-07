import numpy as np
import pandas as pd
import pickle
from io import BytesIO
from azure.storage.blob import BlobServiceClient

# Configuration Azure Blob Storage / penser a la clef
STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=recomcontenugroup8ae8;AccountKey=TON_CLEF;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "recom-storage"

# Initialisation du client Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def load_blob(blob_name):
    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob().readall()
    return blob_data

# Charger les modèles et données stockées sur Azure
svd_model = pickle.loads(load_blob("svd_best_model.pkl"))
interactions_df = pd.read_csv(BytesIO(load_blob("merged_interactions.csv")))
articles_embeddings = np.load(BytesIO(load_blob("articles_embeddings_pca.npy")))
content_based_recommendations = np.load(BytesIO(load_blob("top_n_recommendations_by_id.npy")))

def recommend_articles(user_id, top_n=5):
    user_id = int(user_id)
    user_articles = interactions_df[interactions_df['user_id'] == user_id]['article_id'].tolist()

    if user_articles:
        # Utilisateur connu → Recommandation avec SVD
        predictions = [svd_model.predict(user_id, article) for article in set(interactions_df['article_id'])]
        recommendations = sorted(predictions, key=lambda x: x.est, reverse=True)[:top_n]
        recommended_articles = [pred.iid for pred in recommendations]
    else:
        # Utilisateur inconnu → Recommandation basée contenu
        random_article = np.random.choice(interactions_df['article_id'].unique())
        recommended_articles = content_based_recommendations[random_article][:top_n]

    return recommended_articles
