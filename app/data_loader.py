from google.cloud import storage
import pickle
import numpy as np
import pandas as pd
import os

# Nom du bucket GCS
BUCKET_NAME = "p10_recommend"

def download_blob(blob_name, destination_file):
    """Télécharge un fichier depuis Google Cloud Storage vers le répertoire local temporaire"""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)

    os.makedirs(os.path.dirname(destination_file), exist_ok=True)
    blob.download_to_filename(destination_file)
    return destination_file

def load_recommendations():
    """Charge le fichier contenant les recommandations"""
    local_path = download_blob("top_n_recommendations_by_id.npy", "/tmp/top_n_recommendations_by_id.npy")
    return np.load(local_path, allow_pickle=True).item()

def load_svd_model():
    """Charge le modèle SVD enregistré"""
    local_path = download_blob("svd_best_model.pkl", "/tmp/svd_best_model.pkl")
    with open(local_path, "rb") as f:
        return pickle.load(f)

def load_interactions():
    """Charge le fichier des interactions utilisateur-article"""
    local_path = download_blob("merged_interactions.csv", "/tmp/merged_interactions.csv")
    return pd.read_csv(local_path)

def load_embeddings():
    """Charge le fichier contenant les embeddings des articles"""
    local_path = download_blob("articles_embeddings_pca.npy", "/tmp/articles_embeddings_pca.npy")
    return np.load(local_path, allow_pickle=True)