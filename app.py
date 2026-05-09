import streamlit as st
from google import genai

# Configurazione con la NUOVA libreria Google GenAI
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Tutor Personale - Free Teach")

# Inizializza la cronologia se non esiste
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra i messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dell'utente
if prompt := st.chat_input("Come posso aiutarti?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Nuova sintassi per generare la risposta
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Ops! Qualcosa è andato storto: {e}")
