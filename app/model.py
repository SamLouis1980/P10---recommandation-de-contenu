import numpy as np
from scipy.spatial import distance
from surprise import AlgoBase
from app.data_loader import load_recommendations, load_svd_model, load_interactions, load_embeddings

# Chargement des données
recommendations = load_recommendations()
svd_model = load_svd_model()
interactions = load_interactions()
embeddings = load_embeddings()

def get_top_n_recommendations(user_id, n=5):
    """
    Récupère les recommandations pré-générées pour un utilisateur donné.

    Parameters:
    - user_id (int): ID de l'utilisateur
    - n (int): Nombre d'articles recommandés

    Returns:
    - list of dict: Liste des recommandations avec ID et score de popularité.
    """
    if user_id in recommendations:
        return [{"id": int(article_id), "score": float(score)} for article_id, score in recommendations[user_id][:n]]
    else:
        return []

def predict_with_svd(user_id, all_article_ids, n=5):
    """
    Prédit les articles les plus pertinents pour un utilisateur avec le modèle SVD.

    Parameters:
    - user_id (int): ID de l'utilisateur
    - all_article_ids (list): Liste des articles
    - n (int): Nombre de recommandations

    Returns:
    - list of dict: Liste des recommandations avec ID et score prédictif.
    """
    predictions = []
    for article_id in all_article_ids:
        prediction = svd_model.predict(uid=user_id, iid=article_id)
        predictions.append((article_id, prediction.est))
    
    # Trier par score décroissant et renvoyer les n meilleurs
    predictions.sort(key=lambda x: x[1], reverse=True)
    return [{"id": int(article_id), "score": float(score)} for article_id, score in predictions[:n]]

def recommend_hybrid(user_id, n=5, weight_cbf=0.5):
    """
    Recommandation hybride combinant Content-Based Filtering (CBF) et SVD.

    Parameters:
    - user_id (int): ID de l'utilisateur
    - n (int): Nombre de recommandations
    - weight_cbf (float): Poids de la méthode CBF (0.0 à 1.0)

    Returns:
    - list of dict: Liste des recommandations avec ID et score hybride.
    """
    # Obtenir les recommandations SVD et CBF
    svd_recommendations = predict_with_svd(user_id, list(range(len(embeddings))), n=10)
    cbf_recommendations = get_top_n_recommendations(user_id, n=10)

    # Fusionner les scores
    combined_scores = {}
    for rec in cbf_recommendations:
        combined_scores[rec["id"]] = weight_cbf * rec["score"]

    for rec in svd_recommendations:
        if rec["id"] in combined_scores:
            combined_scores[rec["id"]] += (1 - weight_cbf) * rec["score"]
        else:
            combined_scores[rec["id"]] = (1 - weight_cbf) * rec["score"]

    # Trier et renvoyer les n meilleurs articles
    sorted_recommendations = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    return [{"id": int(article_id), "score": float(score)} for article_id, score in sorted_recommendations[:n]]