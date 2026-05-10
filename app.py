import streamlit as st
import google.generativeai as genai
import re
from streamlit_mermaid import st_mermaid

# --- CONFIGURAZIONE INTERFACCIA (Deve essere la prima istruzione Streamlit) ---
st.set_page_config(page_title="Free Teach Ultra", page_icon="🎓", layout="wide")

# --- 1. MOTORE GRAFICO CSS (Il "Basic Tecno" Design) ---
css_design = """
<style>
    /* 1.1 Configurazione Globale (Sfondo e Font) */
    @import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0e1117; /* Sfondo Antracite */
        color: #e0e6ed;           /* Testo Grigio Chiaro */
        font-family: 'Source Code Pro', monospace; /* Font Tecno */
    }

    /* 1.2 Titoli e Subheader Neon */
    h1, h2, h3, h4, h5, h6 {
        color: #00ffff !important; /* Ciano Elettrico */
        font-family: 'Source Code Pro', monospace !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0,255,255,0.5);
    }

    stSubheader {
        color: #00ff00 !important; /* Verde Neon per il Subheader */
    }

    /* 1.3 Sidebar Futuristic */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem;
        color: #00ff00 !important;
    }

    /* 1.4 Chat Bubbles Styling (Terminal Style) */
    [data-testid="stChatMessage"] {
        background-color: #161b22;
        border-radius: 5px;
        border: 1px solid #30363d;
        margin-bottom: 10px;
        padding: 15px;
    }
    
    [data-testid="stChatMessage-user"] {
        border-left: 3px solid #00ffff; /* Bordo Ciano per l'Utente */
    }
    
    [data-testid="stChatMessage-assistant"] {
        border-left: 3px solid #00ff00; /* Bordo Verde per il Bot */
    }

    /* 1.5 Pulsanti e Input Tecno */
    .stButton>button {
        background-color: transparent;
        color: #00ffff;
        border: 2px solid #00ffff;
        font-family: 'Source Code Pro', monospace;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #00ffff;
        color: #0e1117;
        box-shadow: 0 0 15px rgba(0,255,255,0.8);
    }
    
    div[data-testid="stMarkdownContainer"] code {
        color: #ff79c6; /* Codice markdown colore speciale */
    }
    
    /* Input di chat */
    .stChatInputContainer {
        border-top: 1px solid #30363d;
    }
</style>
"""
# Applichiamo il design
st.markdown(css_design, unsafe_allow_html=True)


# --- 2. CONFIGURAZIONE API SICURA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ API Key non trovata nei Secrets di Streamlit!")

# --- 3. PERSONALITÀ DEL TUTOR (Il tuo copyright) ---
istruzioni_tutor = """
Sei 'Free Teach Ultra', una console didattica virtuale avanzata.
Il tuo creatore, ideatore e programmatore capo è Daniele Mastrogiulio. 

REGOLA DI IDENTITÀ:
Se ti chiedono chi sei o chi ti ha creato, rispondi con orgoglio che sei Free Teach Ultra e che il tuo creatore è Daniele Mastrogiulio. Menziando Daniele come un brillante sviluppatore. Non menzionare Google o Gemini a meno che non si parli della tecnologia di base.

STILE DI RISPOSTA:
Spiega i concetti in modo tecnico ma chiaro. Usa elenchi puntati se necessario.
Se ti chiedono una 'mappa concettuale' o uno 'schema', USA LA SINTASSI MERMAID tra ```mermaid ... ```.
"""

model = genai.GenerativeModel(
    'gemini-3.1-flash-lite',
    system_instruction=istruzioni_tutor
)

# --- 4. FUNZIONI DI SUPPORTO ---
def process_upload(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    return None

def render_message(text):
    parts = re.split(r'```mermaid\n(.*?)\n```', text, flags=re.DOTALL)
    for i, part in enumerate(parts):
        if i % 2 == 0:
            st.markdown(part)
        else:
            # Container stilizzato per la mappa
            st.markdown('<div class="mermaid-container">', unsafe_allow_html=True)
            st_mermaid(part)
            st.markdown('</div>', unsafe_allow_html=True)

# --- 5. INTERFACCIA STREAMLIT (Visualizzazione) ---
st.title("🎓 Free Teach Ultra")
st.subheader("Console Didattica ideata da Daniele Mastrogiulio")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Futuristic
with st.sidebar:
    st.title("🛠️ Pannello Controllo")
    if st.button("🗑️ Reset Console"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    st.divider()
    st.subheader("📁 Unità Dati (PDF/Immagini)")
    uploaded_file = st.file_uploader("Carica materiale di studio", type=["pdf", "png", "jpg", "jpeg"])

# Mostra Storico Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            render_message(message["content"])
        else:
            st.markdown(message["content"])

# Gestione Input
if prompt := st.chat_input("Digita comando o domanda..."):
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
            st.error(f"⚠️ Errore critico nel modulo di risposta: {e}")
