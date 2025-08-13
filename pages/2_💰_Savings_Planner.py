"""
Savings Planner Page - AI-powered savings goal creation and tracking
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import time

# Configure page
st.set_page_config(
    page_title="Savings Planner - Taxora",
    page_icon="💰",
    layout="wide"
)

# Backend API configuration
API_BASE_URL = "http://127.0.0.1:8000"

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

def calculate_savings_projection(target_amount, monthly_saving, start_date, target_date):
    """Calculate savings projection and timeline."""
    months_to_target = (target_date.year - start_date.year) * 12 + (target_date.month - start_date.month)
    
    if months_to_target <= 0:
        return None
    
    total_saved = monthly_saving * months_to_target
    shortfall = max(0, target_amount - total_saved)
    required_monthly = target_amount / months_to_target if months_to_target > 0 else 0
    
    # Generate monthly projection
    projection = []
    current_amount = 0
    
    for month in range(months_to_target + 1):
        projection.append({
            'month': month,
            'amount': current_amount,
            'target_line': (target_amount / months_to_target) * month if months_to_target > 0 else 0
        })
        current_amount += monthly_saving
    
    return {
        'months_to_target': months_to_target,
        'total_saved': total_saved,
        'shortfall': shortfall,
        'required_monthly': required_monthly,
        'projection': projection,
        'success_rate': min(100, (total_saved / target_amount) * 100) if target_amount > 0 else 0
    }

def main():
    """Main savings planner interface."""
    st.title("💰 AI-Powered Savings Planner")
    st.markdown("Create smart savings goals with AI-driven insights and recommendations")
    
    # Sidebar for quick stats
    with st.sidebar:
        st.header("📊 Savings Overview")
        
        # Sample data - in real app, this would come from user data
        st.metric("💰 Total Savings", "₹1,25,000", "↗️ +15,000")
        st.metric("🎯 Active Goals", "3", "↗️ +1")
        st.metric("📈 Monthly Growth", "12.5%", "↗️ +2.1%")
        
        st.markdown("### 🏆 Recent Achievements")
        st.success("✅ Emergency Fund - Completed!")
        st.info("🎯 Vacation Fund - 75% complete")
        st.warning("⏰ House Down Payment - 45% complete")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Create Goal", "📊 Track Progress", "🤖 AI Insights"])
    
    with tab1:
        st.header("🎯 Create New Savings Goal")
        
        with st.form("savings_goal_form"):
            # Basic goal information
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Goal Details")
                goal_name = st.text_input(
                    "Goal Name:",
                    placeholder="e.g., Emergency Fund, Vacation, New Car",
                    help="Give your goal a memorable name"
                )
                
                target_amount = st.number_input(
                    "Target Amount (₹):",
                    min_value=1000,
                    value=100000,
                    step=1000,
                    help="How much do you want to save?"
                )
                
                target_date = st.date_input(
                    "Target Date:",
                    value=date(2025, 12, 31),
                    min_value=date.today(),
                    help="When do you want to achieve this goal?"
                )
                
                description = st.text_area(
                    "Description:",
                    placeholder="Describe your savings goal and why it's important to you",
                    help="This helps our AI provide better recommendations"
                )
            
            with col2:
                st.subheader("💼 Financial Details")
                monthly_salary = st.number_input(
                    "Monthly Salary (₹):",
                    min_value=1000,
                    value=50000,
                    step=1000,
                    help="Your current monthly income"
                )
                
                monthly_saving_target = st.number_input(
                    "Monthly Saving Target (₹):",
                    min_value=500,
                    value=10000,
                    step=500,
                    help="How much can you save each month?"
                )
                
                saving_method = st.selectbox(
                    "Preferred Saving Method:",
                    ["bank_account", "fixed_deposit", "mutual_fund", "stocks", "mixed"],
                    format_func=lambda x: {
                        "bank_account": "🏦 Bank Savings Account",
                        "fixed_deposit": "🔒 Fixed Deposit",
                        "mutual_fund": "📈 Mutual Funds",
                        "stocks": "📊 Stock Market",
                        "mixed": "🔄 Mixed Portfolio"
                    }[x],
                    help="Choose your preferred investment vehicle"
                )
                
                risk_tolerance = st.select_slider(
                    "Risk Tolerance:",
                    options=["Low", "Medium", "High"],
                    value="Medium",
                    help="How comfortable are you with investment risk?"
                )
            
            # Calculate projection
            if target_amount > 0 and monthly_saving_target > 0:
                projection = calculate_savings_projection(
                    target_amount, monthly_saving_target, date.today(), target_date
                )
                
                if projection:
                    st.subheader("📊 Savings Projection")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("⏱️ Months to Goal", f"{projection['months_to_target']}")
                    
                    with col2:
                        st.metric("💰 Total Saved", f"₹{projection['total_saved']:,}")
                    
                    with col3:
                        success_rate = projection['success_rate']
                        st.metric("🎯 Success Rate", f"{success_rate:.1f}%")
                    
                    with col4:
                        if projection['shortfall'] > 0:
                            st.metric("⚠️ Shortfall", f"₹{projection['shortfall']:,}")
                        else:
                            st.metric("✅ Surplus", f"₹{abs(projection['shortfall']):,}")
                    
                    # Projection chart
                    if projection['projection']:
                        df = pd.DataFrame(projection['projection'])
                        
                        fig = go.Figure()
                        
                        # Actual savings line
                        fig.add_trace(go.Scatter(
                            x=df['month'],
                            y=df['amount'],
                            mode='lines+markers',
                            name='Your Savings',
                            line=dict(color='#1f77b4', width=3)
                        ))
                        
                        # Target line
                        fig.add_trace(go.Scatter(
                            x=df['month'],
                            y=[target_amount] * len(df),
                            mode='lines',
                            name='Target Amount',
                            line=dict(color='#ff7f0e', width=2, dash='dash')
                        ))
                        
                        fig.update_layout(
                            title="Savings Projection Over Time",
                            xaxis_title="Months",
                            yaxis_title="Amount (₹)",
                            hovermode='x unified'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
            
            # Submit button
            if st.form_submit_button("🚀 Create Goal with AI Analysis", use_container_width=True):
                if not goal_name.strip():
                    st.error("❌ Please enter a goal name")
                elif target_amount <= 0:
                    st.error("❌ Please enter a valid target amount")
                elif monthly_saving_target <= 0:
                    st.error("❌ Please enter a valid monthly saving amount")
                else:
                    goal_data = {
                        "user_id": f"streamlit_user_{int(time.time())}",
                        "goal_data": {
                            "goal_name": goal_name,
                            "target_amount": target_amount,
                            "monthly_salary": monthly_salary,
                            "monthly_saving_target": monthly_saving_target,
                            "saving_method": saving_method,
                            "target_date": target_date.isoformat(),
                            "description": description,
                            "risk_tolerance": risk_tolerance
                        }
                    }
                    
                    with st.spinner("🤖 AI is analyzing your goal and creating personalized recommendations..."):
                        result = create_savings_goal(goal_data)
                        
                        if result and result.get('success'):
                            st.success("✅ Savings goal created successfully!")
                            
                            # Show AI suggestions
                            ai_suggestions = result.get('ai_suggestions', {})
                            if ai_suggestions:
                                st.subheader("🤖 AI Recommendations")
                                
                                # Personalized suggestions
                                suggestions = ai_suggestions.get('suggestions', [])
                                if suggestions:
                                    st.markdown("#### 💡 Personalized Strategies")
                                    for i, suggestion in enumerate(suggestions, 1):
                                        st.info(f"**{i}.** {suggestion}")
                                
                                # Areas to reduce expenses
                                reduce_areas = ai_suggestions.get('reduce_areas', [])
                                if reduce_areas:
                                    st.markdown("#### 📉 Expense Optimization")
                                    for area in reduce_areas:
                                        st.warning(f"💰 {area}")
                                
                                # Ways to increase income
                                increase_areas = ai_suggestions.get('increase_areas', [])
                                if increase_areas:
                                    st.markdown("#### 📈 Income Enhancement")
                                    for area in increase_areas:
                                        st.success(f"💼 {area}")
                                
                                # Investment recommendations
                                if saving_method in ['mutual_fund', 'stocks', 'mixed']:
                                    st.markdown("#### 📊 Investment Recommendations")
                                    if risk_tolerance == "Low":
                                        st.info("🔒 Consider debt funds and blue-chip stocks for stable returns")
                                    elif risk_tolerance == "Medium":
                                        st.info("⚖️ Mix of equity and debt funds for balanced growth")
                                    else:
                                        st.info("🚀 Growth-oriented equity funds for higher potential returns")
                        else:
                            st.error("❌ Failed to create savings goal. Please check your backend connection.")
    
    with tab2:
        st.header("📊 Track Your Progress")
        
        # Sample goals data - in real app, this would come from database
        sample_goals = [
            {"name": "Emergency Fund", "target": 150000, "current": 150000, "monthly": 15000, "status": "Completed"},
            {"name": "Vacation Fund", "target": 80000, "current": 60000, "monthly": 8000, "status": "In Progress"},
            {"name": "House Down Payment", "target": 500000, "current": 225000, "monthly": 25000, "status": "In Progress"},
            {"name": "New Car", "target": 300000, "current": 45000, "monthly": 12000, "status": "In Progress"}
        ]
        
        for goal in sample_goals:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    progress = goal["current"] / goal["target"] if goal["target"] > 0 else 0
                    st.subheader(f"🎯 {goal['name']}")
                    st.progress(progress)
                    st.caption(f"₹{goal['current']:,} / ₹{goal['target']:,} ({progress*100:.1f}%)")
                
                with col2:
                    st.metric("Monthly Saving", f"₹{goal['monthly']:,}")
                    remaining = goal['target'] - goal['current']
                    months_left = remaining / goal['monthly'] if goal['monthly'] > 0 and remaining > 0 else 0
                    st.caption(f"~{months_left:.1f} months left" if months_left > 0 else "Goal achieved!")
                
                with col3:
                    if goal['status'] == 'Completed':
                        st.success("✅ Completed")
                    else:
                        st.info("🔄 In Progress")
                    
                    if st.button(f"📝 Edit", key=f"edit_{goal['name']}"):
                        st.info("Edit functionality would open here")
                
                st.divider()
    
    with tab3:
        st.header("🤖 AI Financial Insights")
        
        # AI-generated insights
        insights = [
            {
                "title": "💡 Savings Rate Optimization",
                "content": "Your current savings rate of 20% is good, but increasing it to 25% could help you reach your goals 6 months earlier.",
                "type": "info"
            },
            {
                "title": "📈 Investment Opportunity",
                "content": "Consider moving your emergency fund excess (above 6 months expenses) to a balanced mutual fund for better returns.",
                "type": "success"
            },
            {
                "title": "⚠️ Goal Timeline Alert",
                "content": "Your house down payment goal may need adjustment. Consider increasing monthly savings by ₹5,000 or extending timeline by 8 months.",
                "type": "warning"
            },
            {
                "title": "🎯 Achievement Milestone",
                "content": "Congratulations! You've successfully built your emergency fund. This puts you ahead of 70% of people in your age group.",
                "type": "success"
            }
        ]
        
        for insight in insights:
            if insight["type"] == "info":
                st.info(f"**{insight['title']}**\n\n{insight['content']}")
            elif insight["type"] == "success":
                st.success(f"**{insight['title']}**\n\n{insight['content']}")
            elif insight["type"] == "warning":
                st.warning(f"**{insight['title']}**\n\n{insight['content']}")
        
        # Savings tips
        st.subheader("💰 Smart Savings Tips")
        
        tips = [
            "🔄 **Automate your savings**: Set up automatic transfers to make saving effortless",
            "📱 **Use the 50/30/20 rule**: 50% needs, 30% wants, 20% savings and debt repayment",
            "🛒 **Track your expenses**: Use apps to monitor where your money goes",
            "💳 **Reduce subscription services**: Cancel unused memberships and subscriptions",
            "🍽️ **Cook at home more**: Meal planning can save ₹5,000-10,000 per month",
            "🚗 **Optimize transportation**: Consider carpooling or public transport",
            "💡 **Energy efficiency**: LED bulbs and efficient appliances reduce utility bills",
            "🎁 **Cashback and rewards**: Use credit cards with good reward programs responsibly"
        ]
        
        for tip in tips:
            st.markdown(f"- {tip}")

if __name__ == "__main__":
    main()
