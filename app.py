import streamlit as st
from google import genai

def process_upload(uploaded_file):
    if uploaded_file is not None:
        # Legge i byte del file
        bytes_data = uploaded_file.getvalue()
        # Crea l'oggetto che Gemini può capire
        return [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
    return None

# Configurazione Pagina
st.set_page_config(page_title="Free Teach - Il tuo Tutor AI", page_icon="🎓")
st.title("🎓 Free Teach")
st.subheader("L'intelligenza artificiale al servizio dello studio")

api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Manca la chiave API!")
else:
    # Personalità del Tutor
    istruzioni_tutor = """
    Tu sei il Tutor ufficiale di 'Free Teach', una piattaforma creata da Daniele per aiutare gli studenti.
    Il tuo tono deve essere incoraggiante, chiaro e semplice.
    Se ti chiedono chi sei, rispondi che sei il Tutor di Free Teach creato da Daniele.
    """

    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Chiedi al Tutor..."):
    # Mostra il messaggio dell'utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Risposta del Tutor
    with st.chat_message("assistant"):
        # Se c'è un file caricato, lo "impacchettiamo"
        if uploaded_file:
            visual_context = process_upload(uploaded_file)
            # Inviamo sia il testo che il file
            response = st.session_state.chat_session.send_message([prompt, visual_context[0]])
        else:
            # Inviamo solo il testo
            response = st.session_state.chat_session.send_message(prompt)
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
