import streamlit as st
from google import genai

# Recupera la chiave dai Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Manca la chiave API nei Secrets di Streamlit!")
else:
    # Nuova configurazione 2026
    client = genai.Client(api_key=api_key)

    st.title("Tutor Personale - Free Teach")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Chiedimi pure..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Sintassi per la nuova libreria
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
