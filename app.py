import streamlit as st
from google import genai

# Configurazione Pagina
st.set_page_config(page_title="Free Teach - Tutor AI", layout="centered")
st.title("🤖 Il tuo Tutor Personale 2026")

# Recupero chiave dai Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Manca la chiave API nei Secrets!")
else:
    # Inizializzazione Client
    client = genai.Client(api_key=api_key)

    # Inizializzazione chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Visualizzazione cronologia
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input utente
    if prompt := st.chat_input("Chiedimi pure..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # USIAMO IL MODELLO CHE ABBIAMO TROVATO NELLA TUA LISTA!
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
