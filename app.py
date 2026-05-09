import streamlit as st
from google import genai
import time

st.set_page_config(page_title="Free Teach - Tutor AI", layout="centered")
st.title("🤖 Il tuo Tutor Personale")

api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Manca la chiave API nei Secrets!")
else:
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Chiedimi pure..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # PROVIAMO I MODELLI UNO DOPO L'ALTRO SE C'È TRAFFICO
        successo = False
        # Usiamo versioni "Lite" o "Latest" che sono meno congestionate
        modelli_da_provare = ["gemini-2.0-flash-lite", "gemini-flash-latest", "gemini-2.0-flash"]
        
        with st.spinner("Il Tutor sta riflettendo..."):
            for modello in modelli_da_provare:
                try:
                    response = client.models.generate_content(
                        model=modello,
                        contents=prompt
                    )
                    risposta = response.text
                    with st.chat_message("assistant"):
                        st.markdown(risposta)
                    st.session_state.messages.append({"role": "assistant", "content": risposta})
                    successo = True
                    break # Se funziona, esce dal ciclo
                except Exception as e:
                    if "429" in str(e):
                        continue # Se c'è traffico, prova il prossimo modello
                    else:
                        st.error(f"Errore: {e}")
                        break
            
            if not successo:
                st.warning("I server di Google sono molto carichi. Aspetta 30 secondi e riprova a inviare il messaggio.")
