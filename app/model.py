import numpy as np
import pandas as pd
import pickle

# Chargement du modèle SVD
def load_svd_model(model_path: str):
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    return model

# Chargement des embeddings des articles
def load_embeddings(embeddings_path: str):
    return np.load(embeddings_path)

# Chargement des interactions utilisateurs-articles
def load_interactions(interactions_path: str):
    return pd.read_csv(interactions_path)

# Recommandation basée sur SVD
def recommend_articles(user_id: int, model, interactions_df, top_n=5):
    """Retourne les `top_n` articles recommandés pour un utilisateur donné."""
    if user_id not in interactions_df["user_id"].values:
        return []

    all_article_ids = interactions_df["article_id"].unique()
    predictions = [(article_id, model.predict(user_id, article_id).est) for article_id in all_article_ids]
    
    # Trier par score de prédiction décroissant et prendre les `top_n`
    top_articles = sorted(predictions, key=lambda x: x[1], reverse=True)[:top_n]
    
    return [{"id": article[0], "score": article[1]} for article in top_articles]
