"""
Taxora AI Finance Assistant - Streamlit Frontend
A comprehensive AI-powered financial management system
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Taxora AI Finance Assistant",
    page_icon="🤖💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Enhanced CSS with better alignment and hover effects
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Main Container - Centered */
    .main .block-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Header Styles - Centered */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .sub-header {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
    }

    .sub-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 2px;
    }

    /* Centered Content Boxes */
    .content-box {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 2rem auto;
        max-width: 1000px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }

    .content-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }

    /* Metric Cards with Hover Effects */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        border-color: #667eea;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    /* AI Response Styling - Centered */
    .ai-response {
        background: linear-gradient(145deg, #e8f4fd, #d1ecf1);
        padding: 2rem;
        border-radius: 20px;
        border-left: 5px solid #667eea;
        margin: 2rem auto;
        max-width: 900px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        text-align: center;
    }

    .ai-response:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
    }

    /* Provider Badge - Centered */
    .provider-badge {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: 500;
        margin: 1rem auto;
        box-shadow: 0 5px 20px rgba(40, 167, 69, 0.3);
        transition: all 0.3s ease;
        text-align: center;
    }

    .provider-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
    }

    /* Team Credit Card - Centered */
    .team-credit {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 3rem;
        border-radius: 25px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        margin: 3rem auto;
        max-width: 1000px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        text-align: center;
    }

    .team-credit:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        border-color: #667eea;
    }

    /* Button Enhancements - Centered */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        margin: 0 auto;
        display: block;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        background: linear-gradient(45deg, #764ba2, #667eea);
    }

    /* Centered Form Styling */
    .stForm {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 25px;
        padding: 3rem;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.1);
        margin: 2rem auto;
        max-width: 900px;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }

        .main .block-container {
            padding: 1rem;
            margin: 0.5rem;
        }

        .content-box, .team-credit, .ai-response {
            padding: 1.5rem;
            margin: 1rem auto;
        }
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_provider' not in st.session_state:
        st.session_state.current_provider = 'granite'

def get_api_status():
    """Check if the backend API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/status", timeout=5)
        return response.status_code == 200
    except:
        return False

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

def create_savings_goal(goal_data):
    """Create a new savings goal."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/savings/goal",
            json=goal_data,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖💰 Taxora AI Finance Assistant</h1>', unsafe_allow_html=True)
    
    # Check API status
    if not get_api_status():
        st.error("❌ Backend API is not running. Please start the FastAPI server first.")
        st.code("cd backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload")
        return
    
    # Sidebar for navigation and settings
    with st.sidebar:
        st.markdown("### 🎛️ Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Dashboard", "💬 AI Chat", "💰 Savings Planner", "📊 Business Tracker", "🔧 Settings"]
        )
        
        st.markdown("### 🤖 AI Provider")
        providers = get_available_providers()
        if providers:
            provider_options = {}
            for pid, pinfo in providers.items():
                if pinfo.get('status') == 'available':
                    provider_options[pinfo['name']] = pid
            
            if provider_options:
                selected_provider_name = st.selectbox(
                    "Select AI Provider:",
                    list(provider_options.keys())
                )
                selected_provider = provider_options[selected_provider_name]
                
                if selected_provider != st.session_state.current_provider:
                    if set_ai_provider(selected_provider):
                        st.session_state.current_provider = selected_provider
                        st.success(f"✅ Switched to {selected_provider_name}")
                    else:
                        st.error("❌ Failed to switch provider")
        
        st.markdown("### 👥 Development Team")
        st.markdown("""
        - **GaneshPrabu** - Lead Developer
        - **EswaraKumar** - Backend Developer  
        - **Akshya Nethra** - Frontend Developer
        """)
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "💬 AI Chat":
        show_ai_chat()
    elif page == "💰 Savings Planner":
        show_savings_planner()
    elif page == "📊 Business Tracker":
        show_business_tracker()
    elif page == "🔧 Settings":
        show_settings()

def show_dashboard():
    """Show the main dashboard."""
    st.markdown('<h2 class="sub-header">📊 Financial Dashboard</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Savings", "₹50,000", "↗️ +5,000")
    
    with col2:
        st.metric("📈 Monthly Income", "₹75,000", "↗️ +2,500")
    
    with col3:
        st.metric("💸 Monthly Expenses", "₹45,000", "↘️ -1,200")
    
    with col4:
        st.metric("🎯 Savings Rate", "40%", "↗️ +3%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Monthly Savings Trend")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        savings = [8000, 12000, 15000, 18000, 22000, 25000]
        
        fig = px.line(x=months, y=savings, title="Savings Growth")
        fig.update_layout(xaxis_title="Month", yaxis_title="Savings (₹)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Expense Breakdown")
        categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Others']
        amounts = [15000, 8000, 5000, 7000, 10000]
        
        fig = px.pie(values=amounts, names=categories, title="Monthly Expenses")
        st.plotly_chart(fig, use_container_width=True)
    
    # AI Insights
    st.subheader("🤖 AI Financial Insights")
    insights = [
        "💡 You're saving 40% of your income - excellent progress!",
        "📈 Consider investing in SIP for long-term wealth building",
        "🎯 You're on track to reach your emergency fund goal by December",
        "💰 Reduce entertainment expenses by 10% to boost savings"
    ]
    
    for insight in insights:
        st.info(insight)

def show_ai_chat():
    """Show the AI chat interface."""
    st.markdown('<h2 class="sub-header">💬 AI Financial Advisor</h2>', unsafe_allow_html=True)
    
    # Initialize session if needed
    if not st.session_state.session_id:
        with st.form("session_form"):
            st.write("👋 Welcome! Let's start your financial consultation.")
            name = st.text_input("Your Name:", value="User")
            role = st.selectbox("I'm here to help with:", 
                              ["general", "savings", "investment", "business", "tax"])
            
            if st.form_submit_button("🚀 Start Chat"):
                session_id = start_session(name, role)
                if session_id:
                    st.session_state.session_id = session_id
                    st.success(f"✅ Session started! Session ID: {session_id}")
                    st.rerun()
                else:
                    st.error("❌ Failed to start session")
    
    else:
        # Show current provider
        providers = get_available_providers()
        current_provider_name = "Unknown"
        for pid, pinfo in providers.items():
            if pid == st.session_state.current_provider:
                current_provider_name = pinfo.get('name', pid)
                break
        
        st.markdown(f'<div class="provider-badge">🤖 Current AI: {current_provider_name}</div>', 
                   unsafe_allow_html=True)
        
        # Chat history
        chat_container = st.container()
        
        with chat_container:
            for i, (user_msg, ai_msg, provider) in enumerate(st.session_state.chat_history):
                # User message
                st.markdown(f"**👤 You:** {user_msg}")
                
                # AI response
                st.markdown(f'<div class="ai-response"><strong>🤖 {provider}:</strong><br>{ai_msg}</div>', 
                           unsafe_allow_html=True)
                st.markdown("---")
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area("💬 Ask your financial question:", 
                                    placeholder="e.g., What are the best investment options for beginners?",
                                    height=100)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                send_button = st.form_submit_button("📤 Send", use_container_width=True)
            
            if send_button and user_input.strip():
                with st.spinner("🤖 AI is thinking..."):
                    response = send_chat_message(user_input, st.session_state.session_id)
                    
                    if response:
                        ai_reply = response.get('reply', 'No response received')
                        provider_used = response.get('provider', 'Unknown')
                        
                        # Add to chat history
                        st.session_state.chat_history.append((user_input, ai_reply, provider_used))
                        st.rerun()
                    else:
                        st.error("❌ Failed to get AI response")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.session_id = None
            st.rerun()

def show_savings_planner():
    """Show the savings planner interface."""
    st.markdown('<h2 class="sub-header">💰 AI-Powered Savings Planner</h2>', unsafe_allow_html=True)
    
    with st.form("savings_goal_form"):
        st.subheader("🎯 Create New Savings Goal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            goal_name = st.text_input("Goal Name:", placeholder="Emergency Fund")
            target_amount = st.number_input("Target Amount (₹):", min_value=1000, value=100000, step=1000)
            monthly_salary = st.number_input("Monthly Salary (₹):", min_value=1000, value=50000, step=1000)
        
        with col2:
            monthly_saving_target = st.number_input("Monthly Saving Target (₹):", min_value=500, value=10000, step=500)
            saving_method = st.selectbox("Saving Method:", 
                                       ["bank_account", "fixed_deposit", "mutual_fund", "stocks"])
            target_date = st.date_input("Target Date:", value=date(2025, 12, 31))
        
        description = st.text_area("Description:", placeholder="Building emergency fund for financial security")
        
        if st.form_submit_button("🚀 Create Goal with AI Insights"):
            goal_data = {
                "user_id": f"streamlit_user_{int(time.time())}",
                "goal_data": {
                    "goal_name": goal_name,
                    "target_amount": target_amount,
                    "monthly_salary": monthly_salary,
                    "monthly_saving_target": monthly_saving_target,
                    "saving_method": saving_method,
                    "target_date": target_date.isoformat(),
                    "description": description
                }
            }
            
            with st.spinner("🤖 AI is analyzing your goal..."):
                result = create_savings_goal(goal_data)
                
                if result and result.get('success'):
                    st.success("✅ Savings goal created successfully!")
                    
                    # Show AI suggestions
                    ai_suggestions = result.get('ai_suggestions', {})
                    if ai_suggestions:
                        st.subheader("🤖 AI Recommendations")
                        
                        suggestions = ai_suggestions.get('suggestions', [])
                        if suggestions:
                            st.write("💡 **Personalized Suggestions:**")
                            for suggestion in suggestions:
                                st.info(f"• {suggestion}")
                        
                        reduce_areas = ai_suggestions.get('reduce_areas', [])
                        if reduce_areas:
                            st.write("📉 **Areas to Reduce Expenses:**")
                            for area in reduce_areas:
                                st.warning(f"• {area}")
                        
                        increase_areas = ai_suggestions.get('increase_areas', [])
                        if increase_areas:
                            st.write("📈 **Ways to Increase Income:**")
                            for area in increase_areas:
                                st.success(f"• {area}")
                else:
                    st.error("❌ Failed to create savings goal")

def show_business_tracker():
    """Show the business tracker interface."""
    st.markdown('<h2 class="sub-header">📊 Business Analytics & Tax Tracker</h2>', unsafe_allow_html=True)
    
    # Business metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💼 Monthly Revenue", "₹2,50,000", "↗️ +15%")
    
    with col2:
        st.metric("💸 Monthly Expenses", "₹1,80,000", "↘️ -5%")
    
    with col3:
        st.metric("💰 Net Profit", "₹70,000", "↗️ +25%")
    
    # Transaction input
    st.subheader("📝 Add Business Transaction")
    
    with st.form("transaction_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            transaction_type = st.selectbox("Type:", ["Income", "Expense"])
            amount = st.number_input("Amount (₹):", min_value=1, value=1000)
        
        with col2:
            category = st.selectbox("Category:", 
                                  ["Sales", "Services", "Office Rent", "Utilities", "Marketing", "Travel", "Others"])
            date_input = st.date_input("Date:", value=datetime.now().date())
        
        with col3:
            description = st.text_input("Description:", placeholder="Client payment for services")
            gst_applicable = st.checkbox("GST Applicable")
        
        if st.form_submit_button("💾 Add Transaction"):
            st.success("✅ Transaction added successfully!")
            
            # Show AI tax insights
            st.info("🤖 AI Insight: This transaction may qualify for business expense deduction under Section 37(1)")

def show_settings():
    """Show the settings page."""
    st.markdown('<h2 class="sub-header">🔧 System Settings</h2>', unsafe_allow_html=True)
    
    # API Status
    st.subheader("🌐 API Status")
    if get_api_status():
        st.success("✅ Backend API is running")
    else:
        st.error("❌ Backend API is not accessible")
    
    # Provider Status
    st.subheader("🤖 AI Provider Status")
    providers = get_available_providers()
    
    if providers:
        for provider_id, provider_info in providers.items():
            status = provider_info.get('status', 'unknown')
            name = provider_info.get('name', provider_id)
            
            if status == 'available':
                st.success(f"✅ {name}: Available")
            else:
                st.warning(f"⚠️ {name}: {status}")
    else:
        st.error("❌ No providers available")
    
    # System Information
    st.subheader("ℹ️ System Information")
    st.info(f"**Backend URL:** {API_BASE_URL}")
    st.info(f"**Current Session:** {st.session_state.session_id or 'None'}")
    st.info(f"**Active Provider:** {st.session_state.current_provider}")

if __name__ == "__main__":
    main()
