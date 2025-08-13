import streamlit as st
import requests
import time
import json
from typing import Dict, Any

# =========================
# Configuration
# =========================
BACKEND_BASE = "http://127.0.0.1:8000"
START_URL = f"{BACKEND_BASE}/start"
CHAT_URL = f"{BACKEND_BASE}/chat"
STATUS_URL = f"{BACKEND_BASE}/status"

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Taxora - AI Finance Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Classic Professional Styling
# =========================
st.markdown("""
<style>
/* Global Styling - Classic Professional Theme */
.stApp {
    background: radial-gradient(1200px 600px at 50% 0%, #1b1f3a 0%, #0f1226 40%, #0b0e1f 100%);
    font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Arial;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Ubuntu', 'Arial', sans-serif;
}

/* Header Styling */
.main-header {
    background: linear-gradient(135deg, #5B8DEF 0%, #9C6ADE 100%);
    color: #fff;
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    border: none;
}

.main-header h1 {
    margin: 0 0 0.5rem 0;
    font-size: 2.2rem;
        .metric-card {
            background: rgba(255,255,255,0.10);
            border: 1px solid #5B8DEF;
            border-radius: 18px;
            padding: 1.5rem 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 16px rgba(91,141,239,0.10);
            font-family: 'Inter', 'Segoe UI', 'Roboto', 'Ubuntu', 'Arial', sans-serif;
        }
        .metric-card h3 {
            margin: 0;
            color: #667eea;
            font-size: 1.1rem;
            font-family: 'Inter', 'Segoe UI', 'Roboto', 'Ubuntu', 'Arial', sans-serif;
            font-weight: 700;
        }
        .metric-card p {
            margin: 0.5rem 0 0 0;
            font-family: 'Inter', 'Segoe UI', 'Roboto', 'Ubuntu', 'Arial', sans-serif;
        }
        .metric-card .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2c3e50;
        }
        .metric-card .metric-label {
            font-size: 0.9rem;
            color: #C5C8D3;
            margin-top: 0.25rem;
        }
        .metric-card .metric-positive {
            color: #28a745;
            font-weight: 500;
        }
        .metric-card .metric-negative {
            color: #dc3545;
            font-weight: 500;
        }
        .metric-card .metric-icon {
            font-size: 3rem;
            opacity: 0.3;
        }
}

/* Professional Card Styling */
.professional-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 16px 16px;
    margin: 1rem 0;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
}

.professional-card:hover {
    box-shadow: 0 10px 30px rgba(91,141,239,0.35);
    border-color: #5B8DEF;
}

/* Chat Message Styling */
.user-message {
    background: linear-gradient(135deg, rgba(91,141,239,0.25), rgba(156,106,222,0.25));
    color: #EAF0FF;
    padding: 12px 14px;
    border-radius: 14px;
    margin: 6px 0;
    border-left: 4px solid #5B8DEF;
    box-shadow: 0 2px 6px rgba(91,141,239,0.2);
}

.assistant-message {
    background: rgba(255,255,255,0.05);
    color: #E6E8F0;
    padding: 12px 14px;
    border-radius: 14px;
    margin: 6px 0;
    border-left: 4px solid #10B981;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    border: 1px solid rgba(255,255,255,0.08);
}

.message-header {
    font-weight: 600;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.message-content {
    line-height: 1.6;
    font-size: 1rem;
}

.message-meta {
    font-size: 0.8rem;
    opacity: 0.7;
    margin-top: 0.5rem;
    font-style: italic;
}

/* Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #5B8DEF 0%, #9C6ADE 100%);
    color: #fff;
    border: 0;
    border-radius: 12px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(91,141,239,0.2);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #9C6ADE 0%, #5B8DEF 100%);
    box-shadow: 0 4px 18px rgba(156,106,222,0.35);
    transform: translateY(-2px) scale(1.03);
}

/* Input Styling */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    color: #E6E8F0 !important;
    font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Arial !important;
    font-size: 1rem !important;
    padding: 0.75rem !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus {
    border-color: #5B8DEF !important;
    box-shadow: 0 0 0 3px rgba(91,141,239,0.1) !important;
}

/* Sidebar Styling */
.css-1d391kg {
    background: #181c2b;
    border-right: 2px solid #5B8DEF;
}

/* Status Indicators */
.status-indicator {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0.25rem;
}

.status-connected {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.status-disconnected {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.status-warning {
    background: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

/* Insights Panel */
.insights-panel {
    background: linear-gradient(135deg, #23264a 0%, #181c2b 100%);
    border: 1px solid #5B8DEF;
    border-radius: 14px;
    padding: 1.25rem;
    margin: 1rem 0;
}

.insights-title {
    font-weight: 600;
    color: #E6E8F0;
    margin-bottom: 0.75rem;
    font-size: 1.1rem;
}

/* Professional Typography */
h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    font-family: 'Georgia', 'Times New Roman', serif;
}

.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
    margin: 0.5rem 0;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: #5B8DEF;
}

.metric-label {
    font-size: 0.9rem;
    color: #C5C8D3;
    margin-top: 0.25rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Session State Management
# =========================
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = "professional"
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

# =========================
# Helper Functions
# =========================
def check_backend_status():
    """Check if backend services are operational."""
    try:
        response = requests.get(STATUS_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def start_conversation(name: str, role: str):
    """Initialize a new conversation session."""
    try:
        payload = {"name": name, "role": role}
        response = requests.post(START_URL, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            st.session_state.session_id = data["session_id"]
            st.session_state.user_name = name
            st.session_state.user_role = role
            st.session_state.conversation_started = True
            
            # Add welcome message
            welcome_msg = {
                "role": "assistant",
                "content": data["message"],
                "timestamp": time.time(),
                "insights": {
                    "persona": role,
                    "capabilities": data.get("capabilities", [])
                }
            }
            st.session_state.messages.append(welcome_msg)
            return True
        return False
    except Exception as e:
        st.error(f"Failed to start conversation: {e}")
        return False

def send_message(message: str):
    """Send a message and get response."""
    try:
        payload = {
            "session_id": st.session_state.session_id,
            "message": message
        }
        
        # Add user message to history
        user_msg = {
            "role": "user",
            "content": message,
            "timestamp": time.time()
        }
        st.session_state.messages.append(user_msg)
        
        # Send to backend
        response = requests.post(CHAT_URL, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            # Add assistant response
            assistant_msg = {
                "role": "assistant",
                "content": data["reply"],
                "timestamp": time.time(),
                "processing_time": data.get("processing_time", 0),
                "insights": data.get("conversation_insights", {}),
                "nlu_data": data.get("nlu", {})
            }
            st.session_state.messages.append(assistant_msg)
            return True
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Failed to send message: {e}")
        return False

# =========================
# Main Application Header
# =========================
st.markdown("""
<div class="main-header">
    <h1>💼 Taxora - AI-Powered Finance Assistant</h1>
    <p>Conversational NLP Experience powered by IBM's generative AI and Watson NLP capabilities</p>
</div>
""", unsafe_allow_html=True)

# =========================
# Sidebar - System Status & Controls
# =========================
with st.sidebar:
    st.markdown("### 🔧 System Status")
    
    # Check backend status
    status_data = check_backend_status()
    if status_data:
        st.markdown(f"""
        <div class="professional-card">
            <div class="insights-title">Service Status</div>
            <div class="status-indicator status-connected">System Operational</div><br>
            <small>Active Sessions: {status_data.get('active_sessions', 0)}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Watson Services Status
        services = status_data.get('services', {})
        st.markdown("**IBM Watson Services:**")
        for service, status in services.items():
            status_class = "status-connected" if "✅" in status else "status-disconnected"
            st.markdown(f'<span class="status-indicator {status_class}">{service.replace("_", " ").title()}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-disconnected">Backend Unavailable</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Conversation Controls
    st.markdown("### 👤 Conversation Setup")
    
    if not st.session_state.conversation_started:
        with st.form("setup_form"):
            name = st.text_input("Your Name", placeholder="Enter your full name")
            role = st.selectbox(
                "Your Role",
                ["professional", "student", "general"],
                help="This helps me tailor my communication style and advice"
            )
            
            role_descriptions = {
                "professional": "🏢 Concise, data-driven advice with strategic frameworks",
                "student": "🎓 Friendly, educational guidance with step-by-step explanations", 
                "general": "⚖️ Balanced, accessible financial advice for everyone"
            }
            
            st.info(role_descriptions[role])
            
            if st.form_submit_button("Start Conversation", type="primary"):
                if name.strip():
                    if start_conversation(name.strip(), role):
                        st.success("Conversation started successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to start conversation. Please try again.")
                else:
                    st.warning("Please enter your name to continue.")
    else:
        st.markdown(f"""
        <div class="professional-card">
            <div class="insights-title">Current Session</div>
            <strong>Name:</strong> {st.session_state.user_name}<br>
            <strong>Role:</strong> {st.session_state.user_role.title()}<br>
            <strong>Messages:</strong> {len(st.session_state.messages)}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 New Conversation", type="secondary"):
            # Reset session
            for key in ["session_id", "messages", "user_name", "user_role", "conversation_started"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    st.markdown("---")
    
    # Quick Tips
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    <div class="professional-card">
        <div class="insights-title">How to Get the Best Advice</div>
        • Be specific about your financial situation<br>
        • Mention your goals and timeframe<br>
        • Ask follow-up questions for clarity<br>
        • Share relevant context (income, expenses, etc.)
    </div>
    """, unsafe_allow_html=True)

# =========================
# Main Chat Interface
# =========================
if st.session_state.conversation_started:
    # Chat History
    st.markdown("### 💬 Conversation")
    
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            timestamp = time.strftime("%H:%M:%S", time.localtime(message["timestamp"]))
            
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <div class="message-header">👤 You</div>
                    <div class="message-content">{message["content"]}</div>
                    <div class="message-meta">{timestamp}</div>
                </div>
                """, unsafe_allow_html=True)
            
            else:  # assistant
                insights = message.get("insights", {})
                processing_time = message.get("processing_time", 0)
                
                st.markdown(f"""
                <div class="assistant-message">
                    <div class="message-header">🤖 Taxora</div>
                    <div class="message-content">{message["content"]}</div>
                    <div class="message-meta">
                        {timestamp} • Response time: {processing_time}s
                        {f" • Sentiment: {insights.get('sentiment', 'neutral').title()}" if insights.get('sentiment') else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show conversation insights if available
                if insights and any(insights.values()):
                    with st.expander("🔍 Conversation Insights", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if insights.get("sentiment"):
                                st.metric("Sentiment", insights["sentiment"].title(), 
                                         f"{insights.get('confidence', 0):.0%} confidence")
                        
                        with col2:
                            if insights.get("key_topics"):
                                st.write("**Key Topics:**")
                                for topic in insights["key_topics"][:3]:
                                    if topic:
                                        st.write(f"• {topic}")
    
    # Message Input
    st.markdown("---")
    with st.form("message_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_area(
                "Your Message",
                placeholder="Ask me about savings, taxes, investments, budgeting, or any financial topic...",
                height=100,
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            send_button = st.form_submit_button("Send 📤", type="primary")
        
        if send_button and user_input.strip():
            with st.spinner("Taxora is thinking..."):
                if send_message(user_input.strip()):
                    st.rerun()

else:
    # Welcome Screen
    st.markdown("""
    <div class="professional-card">
        <div class="insights-title">Welcome to Taxora</div>
        <p>I'm your AI-powered conversational finance assistant, built with IBM's cutting-edge generative AI and Watson NLP technologies. I provide:</p>
        
        <div style="margin: 1.5rem 0;">
            <strong>🎯 Personalized Financial Guidance</strong><br>
            <small>Tailored advice based on your role and financial situation</small><br><br>
            
            <strong>🧠 Context-Aware Conversations</strong><br>
            <small>I remember our discussion and adapt my responses accordingly</small><br><br>
            
            <strong>📊 Sentiment-Based Adaptation</strong><br>
            <small>I adjust my tone and approach based on your emotional state</small><br><br>
            
            <strong>💼 Professional Expertise</strong><br>
            <small>Comprehensive knowledge in savings, taxes, investments, and budgeting</small>
        </div>
        
        <p><strong>To get started:</strong> Please enter your name and select your role in the sidebar, then click "Start Conversation".</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">💡</div>
            <div class="metric-label">Smart Insights</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">🔄</div>
            <div class="metric-label">Adaptive Learning</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">🛡️</div>
            <div class="metric-label">Enterprise Security</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 2rem;">
    <span style="font-family: 'Inter', 'Segoe UI', 'Roboto', 'Ubuntu', 'Arial', sans-serif; color: #5B8DEF; font-size: 1.2rem; font-weight: 700; letter-spacing: 1px;">Taxora v2.0</span> • Powered by IBM watsonx.ai & Watson NLP • 
    <em style="color: #9C6ADE;">Professional AI Finance Assistant</em>
</div>
""", unsafe_allow_html=True)
