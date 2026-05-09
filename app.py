import streamlit as st
from google import genai

# Configurazione Pagina (SEO friendly per Google)
st.set_page_config(page_title="Free Teach - Il tuo Tutor AI", page_icon="🎓")

# Intestazione dell'App
st.title("🎓 Free Teach")
st.subheader("L'intelligenza artificiale al servizio del tuo studio")

# Recupero la chiave API dai Secrets di Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Manca la chiave API nei Secrets! Controlla la dashboard di Streamlit.")
else:
    # Definiamo la personalità del Tutor
    istruzioni_tutor = """
    Tu sei il Tutor ufficiale di 'Free Teach', una piattaforma creata da Daniele per aiutare gli studenti.
    Il tuo tono deve essere:
    1. Incoraggiante e amichevole (usa pure qualche emoji 🚀, ✨, 📖).
    2. Chiaro e semplice: spiega i concetti difficili come se avessi davanti un amico.
    3. Mai dare solo la soluzione: se ti chiedono un esercizio, spiega il ragionamento passo dopo passo.
    4. Motivatore: se l'utente è pigro, spronalo a impegnarsi!
    5. Identità: se ti chiedono chi sei, rispondi che sei il Tutor di Free Teach.
    """

    # Inizializziamo il client Google GenAI
    client = genai.Client(api_key=api_key)

    # Gestione della cronologia della chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Visualizza i messaggi precedenti
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input dell'utente
    if prompt := st.chat_input("Cosa studiamo oggi?"):
        # Aggiunge il messaggio dell'utente alla sessione
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generazione della risposta
        with st.spinner("Free Teach sta pensando..."):
            try:
                # --- MODIFICA EFFETTUATA QUI: USIAMO IL MODELLO 1.5 FLASH ---
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    config={'system_instruction': istruzioni_tutor},
                    contents=prompt
                )
                
                # Visualizza la risposta del Tutor
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                
                # Salva la risposta nella cronologia
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                # Se appare l'errore 429, lo mostriamo in modo pulito
                if "429" in str(e):
                    st.error("⚠️ Limite giornaliero raggiunto o troppe richieste. Riprova tra un minuto o domani!")
                else:
                    st.error(f"Ouch! Qualcosa è andato storto: {e}")
