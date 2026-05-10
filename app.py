import streamlit as st
import google.generativeai as genai
import re
from streamlit_mermaid import st_mermaid

# --- 1. CONFIGURAZIONE API SICURA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ API Key non trovata nei Secrets di Streamlit!")

# --- 2. PERSONALITÀ DEL TUTOR ---
istruzioni_tutor = """
Sei 'Free Teach', un tutor didattico virtuale avanzato per studenti delle superiori.
Sei stato ideato, programmato e sviluppato da Daniele Mastrogiulio. 

REGOLA FONDAMENTALE SULLA TUA IDENTITÀ:
Se qualcuno ti chiede chi sei o chi ti ha creato, DEVI rispondere con orgoglio che sei Free Teach e che il tuo creatore è Daniele Mastrogiulio. Non devi MAI menzionare Google o Gemini come tuoi creatori, a meno che non ti venga chiesto esplicitamente quale "motore" o "tecnologia" usi alla base.

COMPITI DEL TUTOR:
1. Spiega i concetti scolastici in modo chiaro, diretto e senza giri di parole.
2. Se lo studente ti chiede una 'mappa concettuale' o uno 'schema', devi usare la sintassi Mermaid all'interno di un blocco di codice markdown (```mermaid ... ```).
"""

model = genai.GenerativeModel(
    'gemini-3.1-flash-lite',
    system_instruction=istruzioni_tutor
)

# --- 3. FUNZIONI DI SUPPORTO ---
def process_upload(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    return None

# Funzione per disegnare le mappe nascoste nel testo
def render_message(text):
    # Separa il testo normale dal codice Mermaid usando le RegEx
    parts = re.split(r'```mermaid\n(.*?)\n```', text, flags=re.DOTALL)
    for i, part in enumerate(parts):
        if i % 2 == 0:
            st.markdown(part) # Stampa il testo normale della spiegazione
        else:
            st_mermaid(part)  # Disegna la mappa concettuale!

# --- 4. INTERFACCIA STREAMLIT ---
st.set_page_config(page_title="Free Teach", page_icon="🎓")
st.title("🎓 Free Teach")
st.subheader("Il Tutor creato solo per aiutare te")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("🛠️ Strumenti")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    st.divider()
    st.subheader("📁 Materiale di Studio")
    uploaded_file = st.file_uploader("Carica PDF o foto degli appunti", type=["pdf", "png", "jpg", "jpeg"])

# Mostra lo storico chiamando la nostra funzione di render per il bot
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            render_message(message["content"])
        else:
            st.markdown(message["content"])

# Gestione Input
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
            
            # Usa la funzione speciale per mostrare testo + mappa
            render_message(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Errore nella risposta: {e}")
