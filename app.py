"""
Taxora AI Finance Assistant - Streamlit Cloud Version
A comprehensive AI-powered financial management system for Streamlit Community Cloud
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json
import time
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Taxora AI Finance Assistant",
    page_icon="🤖💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with hover effects and centered layout
st.markdown("""
<style>
    /* Import Google Fonts and Custom Taxora Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
    
    /* Custom Taxora Font Definition */
    @font-face {
        font-family: 'Taxora';
        src: url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap');
        font-weight: normal;
        font-style: normal;
    }

    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Taxora', 'Orbitron', 'Poppins', sans-serif;
    }

    /* Main Container */
    .main .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Header Styles */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        font-family: 'Taxora', 'Orbitron', sans-serif;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        letter-spacing: 2px;
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

    /* Card Styles with Hover Effects */
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
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        border-color: #667eea;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    /* AI Response Styling */
    .ai-response {
        background: linear-gradient(145deg, #e8f4fd, #d1ecf1);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        margin: 1.5rem 0;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }

    .ai-response:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }

    /* Provider Badge */
    .provider-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        transition: all 0.3s ease;
    }

    .provider-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
    }

    /* Team Credit Card */
    .team-credit {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 2rem auto;
        max-width: 800px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        text-align: center;
    }

    .team-credit:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }

    .team-member {
        display: inline-block;
        margin: 0.5rem 1rem;
        padding: 1rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .team-member:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }

    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(45deg, #764ba2, #667eea);
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    .css-1d391kg .css-1v0mbdj {
        color: white;
    }

    /* Metric Value Styling */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
        border-color: #667eea;
    }

    /* Chat Message Styling */
    .stChatMessage {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .stChatMessage:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }

    /* Form Styling */
    .stForm {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin: 2rem 0;
    }

    /* Input Field Styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Progress Bar Styling */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 10px;
    }

    /* Selectbox Styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.2);
    }

    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }

    .loading {
        animation: pulse 2s infinite;
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

        .team-credit {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_provider' not in st.session_state:
        st.session_state.current_provider = 'demo'
    if 'savings_goals' not in st.session_state:
        st.session_state.savings_goals = []
    if 'transactions' not in st.session_state:
        st.session_state.transactions = generate_sample_transactions()

def generate_sample_transactions():
    """Generate sample transaction data for demonstration."""
    transactions = []
    categories = {
        'income': ['Salary', 'Freelance', 'Investment Returns', 'Business Income'],
        'expense': ['Rent', 'Groceries', 'Transportation', 'Entertainment', 'Utilities']
    }
    
    for i in range(30):
        transaction_type = 'income' if i % 4 == 0 else 'expense'
        category = categories[transaction_type][i % len(categories[transaction_type])]
        
        base_amount = 50000 if transaction_type == 'income' else 5000
        amount = base_amount + (i * 500) + (i % 5 * 1000)
        
        transactions.append({
            'date': (datetime.now() - timedelta(days=i*2)).strftime('%Y-%m-%d'),
            'type': transaction_type,
            'category': category,
            'amount': amount,
            'description': f'{category} - Transaction #{i+1}'
        })
    
    return transactions

def simulate_ai_response(message, provider):
    """Simulate AI response for demo purposes."""
    responses = {
        'demo': {
            'investment': "Based on your profile, I recommend a diversified portfolio with 60% equity and 40% debt. Consider SIP investments in large-cap mutual funds for steady growth. Start with ₹10,000 monthly SIP.",
            'savings': "To reach your savings goal, I suggest the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings. You can save an additional ₹5,000 monthly by optimizing your expenses.",
            'tax': "For tax optimization, maximize your 80C deductions up to ₹1.5 lakh. Consider ELSS mutual funds, PPF, and life insurance. Also explore 80D for health insurance deductions.",
            'budget': "Your current spending pattern shows room for improvement. Reduce dining out by 30% and entertainment expenses by 20%. This can free up ₹8,000 monthly for investments.",
            'default': "I'm here to help with your financial planning! I can assist with investments, savings strategies, tax planning, budgeting, and more. What specific area would you like to explore?"
        }
    }
    
    # Simple keyword matching for demo
    message_lower = message.lower()
    if any(word in message_lower for word in ['invest', 'investment', 'mutual fund', 'stock']):
        return responses[provider]['investment']
    elif any(word in message_lower for word in ['save', 'saving', 'goal']):
        return responses[provider]['savings']
    elif any(word in message_lower for word in ['tax', 'deduction', '80c']):
        return responses[provider]['tax']
    elif any(word in message_lower for word in ['budget', 'expense', 'spend']):
        return responses[provider]['budget']
    else:
        return responses[provider]['default']

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖💰 Taxora AI Finance Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; font-family: \'Taxora\', \'Orbitron\', sans-serif; font-weight: 500;">Your Personal AI-Powered Financial Advisor</p>', unsafe_allow_html=True)
    
    # Team Credits with enhanced styling
    st.markdown("""
    <div class="team-credit">
        <h2 style="color: #667eea; margin-bottom: 1.5rem; font-weight: 600;">👥 Meet Our Development Team</h2>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 1rem; margin: 2rem 0;">
            <div class="team-member">
                <h4 style="margin: 0; color: white;">🚀 GaneshPrabu</h4>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Lead Developer & AI Integration Specialist</p>
            </div>
            <div class="team-member">
                <h4 style="margin: 0; color: white;">⚡ EswaraKumar</h4>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Backend Development & API Architecture</p>
            </div>
            <div class="team-member">
                <h4 style="margin: 0; color: white;">🎨 Akshya Nethra</h4>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Frontend Development & UI/UX Design</p>
            </div>
        </div>
        <div style="margin-top: 2rem; padding: 1rem; background: linear-gradient(45deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); border-radius: 10px;">
            <p style="margin: 0; font-style: italic; font-size: 1.1rem; color: #667eea; font-weight: 500;">
                "Empowering financial decisions with cutting-edge AI technology"
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("### 🎛️ Navigation")
        page = st.selectbox(
            "Choose a feature:",
            ["🏠 Dashboard", "💬 AI Chat", "💰 Savings Planner", "📊 Business Tracker"]
        )
        
        st.markdown("### 🤖 AI Provider")
        st.info("🎯 **Demo Mode**: Simulated AI responses for demonstration")
        
        st.markdown("### 📊 Quick Stats")
        st.metric("💰 Total Savings", "₹1,25,000", "↗️ +15%")
        st.metric("📈 Monthly Income", "₹75,000", "↗️ +5%")
        st.metric("🎯 Savings Rate", "35%", "↗️ +3%")
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "💬 AI Chat":
        show_ai_chat()
    elif page == "💰 Savings Planner":
        show_savings_planner()
    elif page == "📊 Business Tracker":
        show_business_tracker()

def show_dashboard():
    """Show the main dashboard."""
    st.markdown('<h2 class="sub-header">📊 Financial Dashboard</h2>', unsafe_allow_html=True)

    # Enhanced Key metrics with custom cards - Single Total Savings card
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 2rem 0;">
        <div class="metric-card" style="max-width: 400px; width: 100%;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h3 style="margin: 0; color: #ff6b6b; font-size: 1.2rem; font-family: 'Taxora', 'Orbitron', sans-serif; font-weight: 600;">💰 Total Savings</h3>
                    <p style="margin: 0.5rem 0 0 0; font-size: 2.2rem; font-weight: 800; color: #2c3e50; font-family: 'Taxora', 'Orbitron', sans-serif;">₹1,25,000</p>
                    <p style="margin: 0.5rem 0 0 0; color: #00d4aa; font-weight: 600; font-family: 'Taxora', 'Orbitron', sans-serif;">↗️ +15,000 (13.6%)</p>
                </div>
                <div style="font-size: 3rem; opacity: 0.4; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));">💰</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Monthly Savings Trend")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        savings = [15000, 18000, 22000, 25000, 28000, 32000]
        
        fig = px.line(x=months, y=savings, title="Savings Growth Over Time")
        fig.update_layout(xaxis_title="Month", yaxis_title="Savings (₹)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Expense Breakdown")
        categories = ['Housing', 'Food', 'Transport', 'Entertainment', 'Utilities', 'Others']
        amounts = [20000, 12000, 8000, 5000, 3000, 2750]
        
        fig = px.pie(values=amounts, names=categories, title="Monthly Expenses")
        st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced AI Insights
    st.markdown('<h3 style="text-align: center; color: #667eea; margin: 3rem 0 2rem 0; font-size: 1.8rem;">🤖 AI Financial Insights</h3>', unsafe_allow_html=True)

    insights = [
        {
            "icon": "💡",
            "title": "Excellent Savings Performance",
            "content": "Your savings rate of 35% is excellent! You're ahead of 80% of people in your age group.",
            "type": "success"
        },
        {
            "icon": "📈",
            "title": "Investment Opportunity",
            "content": "Consider increasing your SIP investments by ₹5,000 to accelerate wealth building.",
            "type": "info"
        },
        {
            "icon": "🎯",
            "title": "Goal Achievement",
            "content": "You're on track to reach your emergency fund goal 2 months ahead of schedule.",
            "type": "success"
        },
        {
            "icon": "💰",
            "title": "Expense Optimization",
            "content": "Optimize your food expenses by 15% to boost savings by an additional ₹1,800 monthly.",
            "type": "warning"
        }
    ]

    # Create insight cards in a grid
    cols = st.columns(2)
    for i, insight in enumerate(insights):
        with cols[i % 2]:
            color_map = {
                "success": "#28a745",
                "info": "#17a2b8",
                "warning": "#ffc107"
            }
            bg_color = color_map.get(insight["type"], "#17a2b8")

            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #ffffff, #f8f9fa);
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                border-left: 4px solid {bg_color};
                transition: all 0.3s ease;
                cursor: pointer;
            " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 15px 35px rgba(0, 0, 0, 0.15)'"
               onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 8px 25px rgba(0, 0, 0, 0.1)'">
                <div style="display: flex; align-items: flex-start; gap: 1rem;">
                    <div style="font-size: 2rem; margin-top: 0.2rem;">{insight["icon"]}</div>
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0; color: {bg_color}; font-weight: 600;">{insight["title"]}</h4>
                        <p style="margin: 0; color: #2c3e50; line-height: 1.5;">{insight["content"]}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_ai_chat():
    """Show the AI chat interface."""
    st.markdown('<h2 class="sub-header">💬 AI Financial Advisor</h2>', unsafe_allow_html=True)

    # Enhanced demo mode notice
    st.markdown("""
    <div style="
        background: linear-gradient(45deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
    ">
        <h3 style="margin: 0 0 1rem 0; color: #667eea;">🎯 Demo Mode Active</h3>
        <p style="margin: 0; color: #2c3e50; font-size: 1.1rem;">
            Experience our AI-powered financial advisor with simulated responses.<br>
            Ask about <strong>investments</strong>, <strong>savings</strong>, <strong>taxes</strong>, or <strong>budgeting</strong>!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat history
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for i, (user_msg, ai_msg) in enumerate(st.session_state.chat_history):
                # User message
                with st.chat_message("user"):
                    st.write(user_msg)
                
                # AI response
                with st.chat_message("assistant"):
                    st.write(f"**Taxora AI**: {ai_msg}")
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
                time.sleep(1)  # Simulate processing time
                ai_reply = simulate_ai_response(user_input, st.session_state.current_provider)
                st.write(f"**Taxora AI**: {ai_reply}")
                
                # Add to chat history
                st.session_state.chat_history.append((user_input, ai_reply))
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("💾 Export Chat", use_container_width=True):
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "chat_history": st.session_state.chat_history
            }
            
            st.download_button(
                label="📥 Download Chat History",
                data=json.dumps(export_data, indent=2),
                file_name=f"taxora_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def show_savings_planner():
    """Show the savings planner interface."""
    st.markdown('<h2 class="sub-header">💰 AI-Powered Savings Planner</h2>', unsafe_allow_html=True)
    
    # Create new goal
    with st.form("savings_goal_form"):
        st.subheader("🎯 Create New Savings Goal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            goal_name = st.text_input("Goal Name:", placeholder="Emergency Fund")
            target_amount = st.number_input("Target Amount (₹):", min_value=1000, value=100000, step=1000)
            monthly_saving = st.number_input("Monthly Saving (₹):", min_value=500, value=10000, step=500)
        
        with col2:
            target_date = st.date_input("Target Date:", value=date(2025, 12, 31))
            category = st.selectbox("Category:", ["Emergency Fund", "Vacation", "House Down Payment", "Car Purchase", "Education", "Other"])
            description = st.text_area("Description:", placeholder="Why is this goal important to you?")
        
        if st.form_submit_button("🚀 Create Goal", use_container_width=True):
            # Calculate timeline
            months_to_target = ((target_date.year - date.today().year) * 12 + 
                              (target_date.month - date.today().month))
            
            if months_to_target > 0:
                total_saved = monthly_saving * months_to_target
                success_rate = min(100, (total_saved / target_amount) * 100)
                
                new_goal = {
                    "name": goal_name,
                    "target": target_amount,
                    "monthly": monthly_saving,
                    "target_date": target_date.isoformat(),
                    "category": category,
                    "description": description,
                    "created": datetime.now().isoformat(),
                    "success_rate": success_rate
                }
                
                st.session_state.savings_goals.append(new_goal)
                st.success("✅ Savings goal created successfully!")
                
                # Show AI recommendations
                st.subheader("🤖 AI Recommendations")
                if success_rate >= 100:
                    st.success(f"🎉 Excellent! You'll reach your goal with ₹{total_saved - target_amount:,.0f} to spare!")
                elif success_rate >= 80:
                    st.info(f"👍 Good plan! You'll achieve {success_rate:.1f}% of your goal. Consider increasing monthly savings by ₹{(target_amount - total_saved) / months_to_target:.0f}")
                else:
                    st.warning(f"⚠️ You'll only reach {success_rate:.1f}% of your goal. Increase monthly savings to ₹{target_amount / months_to_target:.0f} to meet your target.")
                
                st.rerun()
    
    # Display existing goals
    if st.session_state.savings_goals:
        st.subheader("📊 Your Savings Goals")
        
        for i, goal in enumerate(st.session_state.savings_goals):
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.subheader(f"🎯 {goal['name']}")
                    progress = min(1.0, goal['success_rate'] / 100)
                    st.progress(progress)
                    st.caption(f"Target: ₹{goal['target']:,} | Monthly: ₹{goal['monthly']:,}")
                
                with col2:
                    st.metric("Success Rate", f"{goal['success_rate']:.1f}%")
                
                with col3:
                    if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                        st.session_state.savings_goals.pop(i)
                        st.rerun()
                
                st.divider()

def show_business_tracker():
    """Show the business tracker interface."""
    st.markdown('<h2 class="sub-header">📊 Business Analytics & Tax Tracker</h2>', unsafe_allow_html=True)
    
    # Business metrics
    df = pd.DataFrame(st.session_state.transactions)
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_data = df[
        (df['date'].dt.month == current_month) & 
        (df['date'].dt.year == current_year)
    ]
    
    total_income = monthly_data[monthly_data['type'] == 'income']['amount'].sum()
    total_expenses = monthly_data[monthly_data['type'] == 'expense']['amount'].sum()
    net_profit = total_income - total_expenses
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💼 Monthly Revenue", f"₹{total_income:,.0f}", "↗️ +15%")
    
    with col2:
        st.metric("💸 Monthly Expenses", f"₹{total_expenses:,.0f}", "↘️ -5%")
    
    with col3:
        st.metric("💰 Net Profit", f"₹{net_profit:,.0f}", "↗️ +25%")
    
    # Add transaction
    with st.form("transaction_form"):
        st.subheader("📝 Add Transaction")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            transaction_type = st.selectbox("Type:", ["income", "expense"])
            amount = st.number_input("Amount (₹):", min_value=1, value=1000)
        
        with col2:
            if transaction_type == "income":
                categories = ["Salary", "Freelance", "Investment Returns", "Business Income"]
            else:
                categories = ["Rent", "Groceries", "Transportation", "Entertainment", "Utilities"]
            
            category = st.selectbox("Category:", categories)
            transaction_date = st.date_input("Date:", value=datetime.now().date())
        
        with col3:
            description = st.text_input("Description:", placeholder="Transaction details")
        
        if st.form_submit_button("💾 Add Transaction", use_container_width=True):
            new_transaction = {
                'date': transaction_date.strftime('%Y-%m-%d'),
                'type': transaction_type,
                'category': category,
                'amount': amount,
                'description': description
            }
            
            st.session_state.transactions.append(new_transaction)
            st.success("✅ Transaction added successfully!")
            st.rerun()
    
    # Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Income vs Expenses")
        
        monthly_summary = df.groupby([df['date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)
        
        if not monthly_summary.empty:
            fig = go.Figure()
            
            if 'income' in monthly_summary.columns:
                fig.add_trace(go.Scatter(
                    x=monthly_summary.index.astype(str),
                    y=monthly_summary['income'],
                    mode='lines+markers',
                    name='Income',
                    line=dict(color='#28a745', width=3)
                ))
            
            if 'expense' in monthly_summary.columns:
                fig.add_trace(go.Scatter(
                    x=monthly_summary.index.astype(str),
                    y=monthly_summary['expense'],
                    mode='lines+markers',
                    name='Expenses',
                    line=dict(color='#dc3545', width=3)
                ))
            
            fig.update_layout(title="Monthly Trends", xaxis_title="Month", yaxis_title="Amount (₹)")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Expense Categories")
        
        expense_data = df[df['type'] == 'expense'].groupby('category')['amount'].sum()
        
        if not expense_data.empty:
            fig = px.pie(values=expense_data.values, names=expense_data.index, title="Expense Breakdown")
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent transactions
    st.subheader("📋 Recent Transactions")
    recent_transactions = df.sort_values('date', ascending=False).head(10)
    
    if not recent_transactions.empty:
        display_df = recent_transactions.copy()
        display_df['amount'] = display_df['amount'].apply(lambda x: f"₹{x:,.0f}")
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df[['date', 'type', 'category', 'amount', 'description']],
            use_container_width=True
        )

if __name__ == "__main__":
    main()
