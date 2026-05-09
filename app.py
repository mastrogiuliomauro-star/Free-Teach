import streamlit as st
from google import genai

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

    if prompt := st.chat_input("Cosa studiamo oggi?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Free Teach sta elaborando..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-lite", 
                    config={'system_instruction': istruzioni_tutor},
                    contents=prompt
                )
                
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Ouch! Qualcosa è andato storto: {e}")
