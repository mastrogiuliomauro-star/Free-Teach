import streamlit as st
import google.generativeai as genai

# Configuration
genai.configure(api_key="AIzaSyALF4ut4nFZf8CUgRKQy1mkrCaP7sLJv8E")

# Auto-detect model to prevent 404 errors
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_to_use = next((m for m in available_models if 'flash' in m), available_models[0])
except Exception:
    model_to_use = "models/gemini-1.5-flash"

# Page setup for Google (SEO)
st.set_page_config(page_title="Free Teach - Your AI Study Buddy", page_icon="📖")

st.title("📖 Free Teach")
st.subheader("Your friendly AI tutor for stress-free homework!")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("### Let's get started!")
    subject = st.text_input("Subject", placeholder="e.g., History, Science, Math...")
    topic = st.text_input("Topic", placeholder="e.g., Ancient Rome, Photosynthesis...")
    
    if st.button("Start Lesson"):
        if subject and topic:
            st.session_state.started = True
            model = genai.GenerativeModel(model_to_use)
            st.session_state.chat = model.start_chat(history=[])
            
            # THE TUTOR PROMPT: Friendly, helpful, and multi-language
            tutor_prompt = (
                f"You are 'Free Teach', a friendly and encouraging after-school tutor. "
                f"Help the student with {subject} about '{topic}'. "
                "CRITICAL INSTRUCTION: Your default language is English, BUT if the user speaks to you in Italian "
                "or asks to speak Italian, switch to Italian immediately and continue the session in that language. "
                "Don't just give answers; explain the 'why' and ask helpful questions. Be a study buddy, not a scary professor."
            )
            
            with st.spinner("Calling your tutor..."):
                response = st.session_state.chat.send_message(tutor_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()

if st.session_state.started:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if user_input := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    if st.sidebar.button("Reset Session"):
        st.session_state.messages = []
        st.session_state.started = False
        st.rerun()