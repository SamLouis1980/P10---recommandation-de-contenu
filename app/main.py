from fastapi import FastAPI, HTTPException
from app.data_loader import load_recommendations

# Initialisation de l'API
app = FastAPI(title="API de Recommandation", version="1.0")

# Chargement des recommandations depuis GCP
try:
    recommendations = load_recommendations()
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement des recommandations : {e}")

@app.get("/")
def home():
    return {"message": "API de recommandation en ligne !"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int):
    """Renvoie les recommandations d'articles pour un utilisateur donné."""
    if user_id not in recommendations:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    return {"user_id": user_id, "recommendations": recommendations[user_id]}
