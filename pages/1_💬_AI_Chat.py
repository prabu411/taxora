"""
AI Chat Page - Advanced chat interface with multiple AI providers
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="AI Chat - Taxora",
    page_icon="💬",
    layout="wide"
)

# Backend API configuration
API_BASE_URL = "http://127.0.0.1:8000"

def initialize_session_state():
    """Initialize session state variables."""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_provider' not in st.session_state:
        st.session_state.current_provider = 'granite'

def get_available_providers():
    """Get available AI providers from the backend."""
    try:
        response = requests.get(f"{API_BASE_URL}/ai/providers", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('available_providers', {})
        return {}
    except:
        return {}

def start_session(name, role):
    """Start a new chat session."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/start",
            json={"name": name, "role": role},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('session_id')
        return None
    except:
        return None

def send_chat_message(message, session_id):
    """Send a chat message to the AI."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message, "session_id": session_id},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def set_ai_provider(provider):
    """Set the active AI provider."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/ai/provider",
            json={"provider": provider},
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def main():
    """Main chat interface."""
    initialize_session_state()
    
    st.title("💬 AI Financial Advisor Chat")
    st.markdown("Get personalized financial advice from our AI experts")
    
    # Sidebar for provider selection
    with st.sidebar:
        st.header("🤖 AI Provider Settings")
        
        providers = get_available_providers()
        if providers:
            provider_options = {}
            for pid, pinfo in providers.items():
                if pinfo.get('status') == 'available':
                    provider_options[pinfo['name']] = pid
            
            if provider_options:
                selected_provider_name = st.selectbox(
                    "Select AI Provider:",
                    list(provider_options.keys()),
                    help="Choose which AI model to use for your consultation"
                )
                selected_provider = provider_options[selected_provider_name]
                
                if selected_provider != st.session_state.current_provider:
                    if set_ai_provider(selected_provider):
                        st.session_state.current_provider = selected_provider
                        st.success(f"✅ Switched to {selected_provider_name}")
                    else:
                        st.error("❌ Failed to switch provider")
        
        # Provider information
        st.markdown("### 🔍 Provider Info")
        if st.session_state.current_provider == 'granite':
            st.info("🧠 **IBM Granite**: Fast, local AI model. Best for quick responses and general advice.")
        elif st.session_state.current_provider == 'gemini':
            st.info("🎯 **Google Gemini**: Advanced AI with deep reasoning. Best for complex analysis.")
        elif st.session_state.current_provider == 'huggingface':
            st.info("🤗 **Hugging Face**: Open source AI models. Best for diverse perspectives.")
        
        # Chat statistics
        if st.session_state.chat_history:
            st.markdown("### 📊 Chat Stats")
            st.metric("Messages", len(st.session_state.chat_history))
            
            # Word count
            total_words = sum(len(msg[0].split()) + len(msg[1].split()) 
                            for msg in st.session_state.chat_history)
            st.metric("Total Words", total_words)
    
    # Main chat interface
    if not st.session_state.session_id:
        # Session setup
        st.markdown("### 👋 Welcome to Taxora AI Chat")
        st.markdown("Let's start your personalized financial consultation")
        
        with st.form("session_setup"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name:", value="User", help="Enter your name for personalized advice")
            
            with col2:
                role = st.selectbox(
                    "What brings you here today?",
                    ["general", "savings", "investment", "business", "tax"],
                    format_func=lambda x: {
                        "general": "💬 General Financial Advice",
                        "savings": "💰 Savings Planning", 
                        "investment": "📈 Investment Guidance",
                        "business": "💼 Business Finance",
                        "tax": "🧾 Tax Planning"
                    }[x],
                    help="Choose your primary area of interest"
                )
            
            if st.form_submit_button("🚀 Start Chat Session", use_container_width=True):
                session_id = start_session(name, role)
                if session_id:
                    st.session_state.session_id = session_id
                    st.success(f"✅ Chat session started! Welcome, {name}!")
                    st.rerun()
                else:
                    st.error("❌ Failed to start session. Please check if the backend is running.")
    
    else:
        # Active chat interface
        # Show current provider
        providers = get_available_providers()
        current_provider_name = "Unknown"
        for pid, pinfo in providers.items():
            if pid == st.session_state.current_provider:
                current_provider_name = pinfo.get('name', pid)
                break
        
        st.info(f"🤖 Currently chatting with: **{current_provider_name}**")
        
        # Chat history container
        chat_container = st.container()
        
        with chat_container:
            if st.session_state.chat_history:
                for i, (user_msg, ai_msg, provider) in enumerate(st.session_state.chat_history):
                    # User message
                    with st.chat_message("user"):
                        st.write(user_msg)
                    
                    # AI response
                    with st.chat_message("assistant"):
                        st.write(f"**{provider}**: {ai_msg}")
            else:
                st.info("💡 Start the conversation by asking a financial question below!")
        
        # Chat input
        user_input = st.chat_input("Ask your financial question here...")
        
        if user_input:
            # Add user message to chat
            with st.chat_message("user"):
                st.write(user_input)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("🤖 AI is thinking..."):
                    response = send_chat_message(user_input, st.session_state.session_id)
                    
                    if response:
                        ai_reply = response.get('reply', 'No response received')
                        provider_used = response.get('provider', 'Unknown')
                        
                        st.write(f"**{provider_used}**: {ai_reply}")
                        
                        # Add to chat history
                        st.session_state.chat_history.append((user_input, ai_reply, provider_used))
                    else:
                        st.error("❌ Failed to get AI response. Please try again.")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        with col2:
            if st.button("🔄 New Session", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.session_id = None
                st.rerun()
        
        with col3:
            if st.button("💾 Export Chat", use_container_width=True):
                # Create export data
                export_data = {
                    "session_id": st.session_state.session_id,
                    "provider": st.session_state.current_provider,
                    "timestamp": datetime.now().isoformat(),
                    "chat_history": st.session_state.chat_history
                }
                
                st.download_button(
                    label="📥 Download Chat History",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"taxora_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main()
