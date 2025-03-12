import streamlit as st
import requests

# URL de la Cloud Function
CLOUD_FUNCTION_URL = "https://europe-west1-genial-venture-447118-b9.cloudfunctions.net/recommendation-function"

st.title("🔍 Recommandation d'Articles")

# Champ de sélection pour l'ID utilisateur
user_id = st.number_input("Entrez un ID utilisateur :", min_value=1, step=1)

if st.button("Obtenir les recommandations"):
    if user_id:
        with st.spinner("🔄 Chargement..."):
            response = requests.get(f"{CLOUD_FUNCTION_URL}?user_id={user_id}")
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("recommendations", [])
                
                if recommendations:
                    st.subheader("🎯 Articles recommandés :")
                    for rec in recommendations:
                        st.write(f"📖 **Article ID:** {rec['id']}")
                else:
                    st.warning("⚠️ Aucune recommandation trouvée.")
            else:
                st.error(f"🚨 Erreur : {response.status_code}")
    else:
        st.warning("⚠️ Veuillez entrer un ID utilisateur valide.")

