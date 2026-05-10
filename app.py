import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAZIONE API SICURA ---
# Questa riga cerca la chiave nei "Secrets" di Streamlit, non nel codice pubblico
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ API Key non trovata nei Secrets di Streamlit!")

model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. FUNZIONE PER LEGGERE I FILE ---
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

# --- 3. INTESTAZIONE APP ---
st.title("🎓 Free Teach")
st.subheader("L'intelligenza artificiale al servizio dello studio")

# --- 4. INIZIALIZZAZIONE MEMORIA ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🛠️ Pannello Strumenti")
    
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    st.divider()
    
    st.subheader("📁 Carica Documenti")
    uploaded_file = st.file_uploader("Carica un PDF o una foto", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file:
        st.success("File caricato!")

# --- 6. VISUALIZZAZIONE CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. LOGICA DI RISPOSTA ---
if prompt := st.chat_input("Chiedi al Tutor..."):
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
            st.error(f"Errore: {e}")
