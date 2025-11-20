import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖", layout="wide")

# Title
st.title("🤖 Groq AI Chatbot")

# Sidebar for API key and settings
with st.sidebar:
    st.header("Settings")
    groq_api_key = st.text_input("Enter your Groq API Key:", type="password")
    
    model = st.selectbox(
        "Select Model:",
        ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"]
    )
    
    temperature = st.slider("Temperature:", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens:", 100, 4000, 1024, 100)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    if not groq_api_key:
        st.error("Please enter your Groq API key in the sidebar!")
        st.stop()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Initialize Groq client
            client = Groq(api_key=groq_api_key)
            
            # Create chat completion
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Stream the response
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            full_response = "Sorry, I encountered an error. Please check your API key and try again."
            message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Instructions in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("""
    ### How to use:
    1. Get your API key from [Groq Console](https://console.groq.com/)
    2. Enter your API key above
    3. Select your preferred model
    4. Start chatting!
    
    ### Features:
    - Real-time streaming responses
    - Multiple model options
    - Adjustable temperature & tokens
    - Chat history
    """)