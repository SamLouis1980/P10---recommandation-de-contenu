import azure.functions as func
import logging
import json
from .recommender import recommend_articles

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function - Recommandation déclenchée")

    try:
        user_id = req.params.get('userID')
        if not user_id:
            req_body = req.get_json()
            user_id = req_body.get('userID')

        if not user_id:
            return func.HttpResponse("Merci de fournir un `userID` en paramètre.", status_code=400)

        logging.info(f"User ID reçu : {user_id}")

        # Vérifier si recommend_articles est bien importé et fonctionne
        recommendations = recommend_articles(user_id)
        response = {"user_id": user_id, "recommendations": recommendations}

        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)

    except Exception as e:
        logging.error(f"Erreur interne : {str(e)}")
        return func.HttpResponse(f"Erreur interne : {str(e)}", status_code=500)
