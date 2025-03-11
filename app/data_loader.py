import pickle
import os
import numpy as np
import pandas as pd
from google.cloud import storage
from surprise import dump

# Configuration du bucket GCP
BUCKET_NAME = "p10_recommend"

def download_from_gcp(file_name):
    """Télécharge un fichier depuis Google Cloud Storage et le stocke en local."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    local_path = os.path.join(os.getcwd(), file_name)
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
    return load_numpy_file(file_name)

def load_svd_model():
    """Télécharge le modèle SVD depuis GCS et le charge en mémoire."""
    file_name = "svd_best_model2.pkl"
    local_path = os.path.join(os.getcwd(), file_name)  # On stocke dans le répertoire courant

    print(f"Téléchargement du modèle depuis GCS: gs://{BUCKET_NAME}/{file_name} -> {local_path}")
    download_from_gcp(file_name)  # Télécharge dans le dossier actuel

    # Chargement du modèle Surprise
    loaded_model, details = dump.load(local_path)

    # Correction : récupérer le vrai modèle s'il est stocké dans `details`
    if loaded_model is None and isinstance(details, object):
        loaded_model = details

    print(f"Modèle chargé correctement : {type(loaded_model)}")
    return loaded_model

def load_interactions():
    """Charge le fichier des interactions utilisateur-article."""
    file_name = "merged_interactions.csv"
    local_path = download_from_gcp(file_name)
    return pd.read_csv(local_path)

def load_embeddings():
    """Charge les embeddings PCA des articles."""
    file_name = "articles_embeddings_pca.npy"
    return load_numpy_file(file_name)
