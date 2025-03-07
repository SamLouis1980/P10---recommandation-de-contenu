import azure.functions as func
import logging
import json
from .recommender import recommend_articles

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
        recommendations = recommend_articles(user_id)
        response = {"user_id": user_id, "recommendations": recommendations}
        return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse("Merci de fournir un `userID` en paramètre.", status_code=400)
