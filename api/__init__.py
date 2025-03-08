import azure.functions as func
import logging
import json
from .recommender import recommend_articles

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function - Recommandation déclenchée")

    try:
        logging.info("Lecture des paramètres...")
        user_id = req.params.get('userID')
        if not user_id:
            req_body = req.get_json()
            user_id = req_body.get('userID')

        if not user_id:
            logging.warning("Aucun userID fourni")
            return func.HttpResponse("Merci de fournir un `userID` en paramètre.", status_code=400)

        logging.info(f"User ID reçu : {user_id}")

        # Vérification de la fonction recommend_articles
        try:
            logging.info("Appel de recommend_articles...")
            recommendations = recommend_articles(user_id)
            logging.info(f"Recommandations obtenues : {recommendations}")
        except Exception as e:
            logging.error(f"Erreur dans recommend_articles : {str(e)}", exc_info=True)
            return func.HttpResponse(f"Erreur interne (recommend_articles) : {str(e)}", status_code=500)

        response = {"user_id": user_id, "recommendations": recommendations}
        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)

    except Exception as e:
        logging.error(f"Erreur critique : {str(e)}", exc_info=True)  # Affichage détaillé de l'erreur
        return func.HttpResponse(f"Erreur interne (générale) : {str(e)}", status_code=500)
