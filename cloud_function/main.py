import functions_framework
import requests

# Remplace ici par ton URL Cloud Run
CLOUD_RUN_URL = "https://recommendation-api-481199201103.europe-west1.run.app"

@functions_framework.http
def recommend(request):
    """
    Cloud Function qui relaie la requête vers Cloud Run.
    """
    request_json = request.get_json(silent=True)
    user_id = request_json.get("user_id") if request_json else request.args.get("user_id")
    
    if user_id is None:
        return {"error": "user_id is required"}, 400

    response = requests.get(f"{CLOUD_RUN_URL}/recommend/{user_id}")

    return response.json(), response.status_code