import streamlit as st
from google import genai

st.title("Test Tutor 2026")

# Recupero chiave
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Manca la chiave nei Secrets!")
else:
    client = genai.Client(api_key=api_key)
    
    user_input = st.text_input("Scrivi 'Ciao' qui:")
    
    if user_input:
        try:
            # Usiamo il modello più stabile del 2026
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=user_input
            )
            st.write("Il Tutor risponde:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Errore: {e}")
