import streamlit as st
import google.generativeai as genai

# Configurazione della pagina
st.set_page_config(page_title="Free Teach", page_icon="📖")
st.title("📖 Free Teach")
st.caption("Il tuo tutor personale AI - Creato da Daniele")

# Caricamento della chiave segreta dai Secrets di Streamlit
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("ERRORE: Manca la chiave API nei Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Inizializzazione del modello (usiamo 1.5-flash che è veloce e gratuito)
model = genai.GenerativeModel('gemini-1.5-flash')

# Gestione della memoria della chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra i messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dell'utente
if prompt := st.chat_input("Chiedimi qualsiasi cosa..."):
    # Aggiungi messaggio utente alla storia
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generazione risposta
    with st.chat_message("assistant"):
        try:
            # Istruzioni per il tutor
            full_prompt = f"Sei Free Teach, un tutor scolastico amichevole. Spiega le cose in modo semplice. Domanda: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Si è verificato un errore: {e}")
