import streamlit as st
from google import genai

st.title("Tutor Personale - Free Teach")

# 1. Recupero Chiave
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Inserisci la GOOGLE_API_KEY nei Secrets di Streamlit!")
else:
    # 2. Inizializzazione Client 2026
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Chiedimi quello che vuoi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # PROVA IL MODELLO PIÙ RECENTE DEL 2026
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Se il 2.0 fallisce, prova l'1.5 come ultima spiaggia
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e2:
                st.error(f"Errore persistente: {e2}")
