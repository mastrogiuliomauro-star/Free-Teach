import streamlit as st
import google.generativeai as genai

# Configurazione Pagina
st.set_page_config(page_title="Free Teach", page_icon="📖")
st.title("📖 Free Teach")
st.subheader("Il tuo tutor personale gratuito")

# Recupero della chiave dai Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Manca la chiave API! Vai nei Secrets di Streamlit e aggiungila.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Inizializzazione del modello
# Usiamo il nome standard che funziona con le librerie aggiornate
model = genai.GenerativeModel('gemini-1.5-flash')

# Memoria della chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dell'utente
if prompt := st.chat_input("In cosa posso aiutarti?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Qui il tutor riceve le sue istruzioni
            full_prompt = f"Sei Free Teach, un tutor scolastico amichevole. Aiuta lo studente: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Errore di connessione: {e}")
