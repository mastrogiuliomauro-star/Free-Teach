import streamlit as st
from google import genai

st.title("Tutor AI - Ultimo Tentativo")

# Recupero chiave
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Manca la chiave nei Secrets!")
else:
    # Inizializzazione Client
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Scrivi qui..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # USIAMO IL NOME "LATEST" PER AGGIRARE IL BUG DEL 404
            response = client.models.generate_content(
                model="gemini-1.5-flash-latest", 
                contents=prompt
            )
            
            res_text = response.text
            with st.chat_message("assistant"):
                st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            st.error(f"Ancora errore: {e}")
            # Se fallisce, stampiamo la lista dei modelli per capire cosa vede il tuo PC
            st.write("Modelli disponibili per la tua chiave:")
            try:
                for m in client.models.list():
                    st.write(f"- {m.name}")
            except:
                st.write("Impossibile recuperare la lista modelli.")
