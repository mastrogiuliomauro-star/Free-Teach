import streamlit as st
from google import genai

# Configurazione Pagina (SEO friendly)
st.set_page_config(page_title="Free Teach - Il tuo Tutor AI", page_icon="🎓")
st.title("🎓 Free Teach")
st.subheader("L'intelligenza artificiale al servizio del tuo studio")

api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Manca la chiave API!")
else:
    # Qui diamo la "Personalità" al Tutor
    istruzioni_tutor = """
    Tu sei il Tutor ufficiale di 'Free Teach', una piattaforma creata da Daniele per aiutare gli studenti.
    Il tuo tono deve essere:
    1. Incoraggiante e amichevole (usa pure qualche emoji 🚀, ✨, 📖).
    2. Chiaro e semplice: spiega i concetti difficili come se avessi davanti un amico.
    3. Mai dare solo la soluzione: se ti chiedono un esercizio, spiega il ragionamento passo dopo passo.
    4. Motivatore: se l'utente dice che non capisce, incoraggialo e prova un altro esempio.
    5. Identità: se ti chiedono chi sei, rispondi che sei il Tutor di Free Teach.
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
                # Applichiamo la personalità qui
                response = client.models.generate_content(
                    model="gemini-1.5-flash"
                    config={'system_instruction': istruzioni_tutor},
                    contents=prompt
                )
                
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Ouch! Qualcosa è andato storto: {e}")
