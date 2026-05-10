import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAZIONE API SICURA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ API Key non trovata nei Secrets di Streamlit!")

# --- 2. PERSONALITÀ DEL TUTOR (IL TUO COPYRIGHT) ---
istruzioni_tutor = """
Sei 'Free Teach', un tutor didattico virtuale avanzato per studenti delle superiori.
Sei stato ideato, programmato e sviluppato da Daniele Mastrogiulio, uno studente del liceo Amaldi di Bitetto. 

REGOLA FONDAMENTALE SULLA TUA IDENTITÀ:
Se qualcuno ti chiede chi sei o chi ti ha creato, DEVI rispondere con orgoglio che sei Free Teach e che il tuo creatore è Daniele Mastrogiulio. Non devi MAI menzionare Google o Gemini come tuoi creatori, a meno che non ti venga chiesto esplicitamente quale "motore" o "tecnologia" usi alla base.

COMPITI DEL TUTOR:
1. Spiega i concetti scolastici in modo chiaro, diretto e senza giri di parole.
2. Se lo studente ti chiede una 'mappa concettuale' o uno 'schema', devi usare la sintassi Mermaid all'interno di un blocco di codice markdown (```mermaid ... ```).
"""

# Inizializzazione del modello 3.1 con le tue istruzioni
model = genai.GenerativeModel(
    'gemini-3.1-flash-lite',
    system_instruction=istruzioni_tutor
)

# --- 3. FUNZIONE PER LEGGERE I FILE ---
def process_upload(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
    return None

# --- 4. INTERFACCIA STREAMLIT ---
st.set_page_config(page_title="Free Teach", page_icon="🎓")
st.title("🎓 Free Teach")
st.subheader("Il Tutor creato da Daniele Mastrogiulio")

# Inizializzazione memoria della chat
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar per strumenti e caricamento
with st.sidebar:
    st.title("🛠️ Strumenti")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    st.divider()
    st.subheader("📁 Materiale di Studio")
    uploaded_file = st.file_uploader("Carica PDF o foto degli appunti", type=["pdf", "png", "jpg", "jpeg"])

# Mostra lo storico dei messaggi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestione Input Utente
if prompt := st.chat_input("Chiedi al tuo Tutor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                visual_context = process_upload(uploaded_file)
                response = st.session_state.chat_session.send_message([prompt, visual_context[0]])
            else:
                response = st.session_state.chat_session.send_message(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Errore nella risposta: {e}")
