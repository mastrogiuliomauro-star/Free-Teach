import streamlit as st
from google import genai

st.set_page_config(page_title="Free Teach - Tutor AI", layout="centered")
st.title("🤖 Il tuo Tutor Personale")

# Recupero chiave dai Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Manca la chiave API! Incollala nei Secrets di Streamlit.")
else:
    # Configurazione Client 2026
    client = genai.Client(api_key=api_key)

    # Inizializzazione chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Visualizzazione messaggi
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input utente
    if prompt := st.chat_input("Chiedimi qualsiasi cosa..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Usiamo 1.5-flash che è il più stabile per il piano gratuito
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Errore di comunicazione: {e}")
