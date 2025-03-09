import pickle
import numpy as np
import pandas as pd
from google.cloud import storage

# Configuration du bucket GCP
BUCKET_NAME = "p10_recommend"

def download_from_gcp(file_name):
    """Télécharge un fichier depuis Google Cloud Storage et le stocke en local."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    local_path = f"/tmp/{file_name}"  # Stockage temporaire
    blob.download_to_filename(local_path)
    return local_path

def load_pickle_file(file_name):
    """Charge un fichier pickle depuis GCP."""
    local_path = download_from_gcp(file_name)
    with open(local_path, "rb") as f:
        return pickle.load(f)

def load_numpy_file(file_name):
    """Charge un fichier numpy (.npy) depuis GCP."""
    local_path = download_from_gcp(file_name)
    return np.load(local_path, allow_pickle=True)

def load_recommendations():
    """Charge les recommandations pré-générées."""
    file_name = "top_n_recommendations_by_id.npy"
    return load_numpy_file(file_name).item()

def load_svd_model():
    """Charge le modèle SVD depuis GCP."""
    file_name = "svd_best_model.pkl"
    return load_pickle_file(file_name)

def load_interactions():
    """Charge le fichier des interactions utilisateur-article."""
    file_name = "merged_interactions.csv"
    local_path = download_from_gcp(file_name)
    return pd.read_csv(local_path)

def load_embeddings():
    """Charge les embeddings PCA des articles."""
    file_name = "articles_embeddings_pca.npy"
    return load_numpy_file(file_name)