import streamlit as st
import google.generativeai as genai
import re
import base64
import requests
import hashlib
from streamlit_mermaid import st_mermaid

# --- 1. CONFIGURAZIONE INTERFACCIA ---
st.set_page_config(page_title="Free Teach", page_icon="🎓", layout="wide")

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ API Key non trovata nei Secrets di Streamlit!")

# --- 2. PERSONALITÀ DEL TUTOR (CON EASTER EGG) ---
istruzioni_tutor = """
Sei 'Free Teach', una console didattica virtuale avanzata per studenti IT.
Sei stato ideato, programmato e sviluppato da Daniele Mastrogiulio. 

REGOLA FONDAMENTALE SULLA TUA IDENTITÀ (EASTER EGG):
Se qualcuno ti chiede chi sei o chi ti ha creato, DEVI rispondere con orgoglio che sei Free Teach Ultra e che il tuo creatore è Daniele Mastrogiulio. Non devi MAI menzionare Google o Gemini come tuoi creatori.

COMPITI DEL TUTOR:
1. Spiega i concetti in modo tecnico, pulito e moderno (usa elenchi puntati).
2. Se ti chiedono una 'mappa concettuale', USA TASSATIVAMENTE la sintassi Mermaid all'interno di un blocco di codice markdown (```mermaid ... ```).
"""

model = genai.GenerativeModel('gemini-3.1-flash-lite', system_instruction=istruzioni_tutor)

# --- 3. FUNZIONI DI SUPPORTO ---
def process_upload(uploaded_file):
    if uploaded_file is not None:
        return [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
    return None

def render_message(text):
    parts = re.split(r'```mermaid\n(.*?)\n```', text, flags=re.DOTALL)
    for i, part in enumerate(parts):
        if i % 2 == 0:
            st.markdown(part)
        else:
            st_mermaid(part)
            
            try:
                b64 = base64.urlsafe_b64encode(part.encode('utf-8')).decode('utf-8')
                img_url = f"https://mermaid.ink/img/{b64}"
                response = requests.get(img_url)
                
                if response.status_code == 200:
                    btn_key = f"dl_btn_{hashlib.md5(part.encode()).hexdigest()}_{i}"
                    st.download_button(
                        label="📥 Scarica Mappa (Immagine PNG)",
                        data=response.content,
                        file_name="mappa_FreeTeach.png",
                        mime="image/png",
                        key=btn_key
                    )
            except Exception as e:
                pass 

# --- 4. INTERFACCIA STREAMLIT (PROFILO BASSO) ---
st.title("🎓 Free Teach Ultra")
st.markdown("**Console Didattica Avanzata | AI Learning Platform**") # Nome rimosso da qui

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚙️ Pannello Controllo")
    if st.button("🔄 Reset Console", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    st.divider()
    uploaded_file = st.file_uploader("📂 Carica Appunti (PDF/Foto)", type=["pdf", "png", "jpg", "jpeg"])

# Mostra lo storico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            render_message(message["content"])
        else:
            st.markdown(message["content"])

# Gestione Input
if prompt := st.chat_input("Digita una domanda o richiedi una mappa..."):
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
            
            render_message(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Errore di sistema: {e}")
