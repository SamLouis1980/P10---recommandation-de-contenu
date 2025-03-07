import streamlit as st
import requests

st.title("Système de Recommandation d'Articles")

user_id = st.text_input("Entrez un ID utilisateur:")

if st.button("Obtenir des recommandations"):
    api_url = "https://recom-contenu.azurewebsites.net/api/recommendation"
    response = requests.get(api_url, params={"userID": user_id})

    if response.status_code == 200:
        recommendations = response.json().get("recommendations", [])
        st.write("Articles recommandés :", recommendations)
    else:
        st.error("Erreur lors de la récupération des recommandations")
