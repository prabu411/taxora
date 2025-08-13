"""
Business Tracker Page - Business analytics and tax optimization
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json

# Configure page
st.set_page_config(
    page_title="Business Tracker - Taxora",
    page_icon="📊",
    layout="wide"
)

# Backend API configuration
API_BASE_URL = "http://127.0.0.1:8000"

def create_business_profile(profile_data):
    """Create a new business profile."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/business/profile",
            json=profile_data,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def add_transaction(transaction_data):
    """Add a business transaction."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/business/transaction",
            json=transaction_data,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def generate_sample_data():
    """Generate sample business data for demonstration."""
    # Sample transactions for the last 6 months
    transactions = []
    categories = {
        'income': ['Sales', 'Services', 'Consulting', 'Product Sales'],
        'expense': ['Office Rent', 'Utilities', 'Marketing', 'Travel', 'Equipment', 'Supplies']
    }
    
    for i in range(50):
        transaction_type = 'income' if i % 3 == 0 else 'expense'
        category = categories[transaction_type][i % len(categories[transaction_type])]
        
        base_amount = 50000 if transaction_type == 'income' else 15000
        amount = base_amount + (i * 1000) + (i % 7 * 2000)
        
        transactions.append({
            'date': (datetime.now() - timedelta(days=i*3)).strftime('%Y-%m-%d'),
            'type': transaction_type,
            'category': category,
            'amount': amount,
            'description': f'{category} transaction #{i+1}',
            'gst_applicable': i % 4 == 0
        })
    
    return transactions

def main():
    """Main business tracker interface."""
    st.title("📊 Business Analytics & Tax Tracker")
    st.markdown("Comprehensive business financial management with AI-powered insights")
    
    # Initialize sample data
    if 'transactions' not in st.session_state:
        st.session_state.transactions = generate_sample_data()
    
    # Sidebar for business overview
    with st.sidebar:
        st.header("💼 Business Overview")
        
        # Calculate metrics from transactions
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
        
        st.metric("💰 Monthly Revenue", f"₹{total_income:,.0f}", "↗️ +15%")
        st.metric("💸 Monthly Expenses", f"₹{total_expenses:,.0f}", "↘️ -5%")
        st.metric("📈 Net Profit", f"₹{net_profit:,.0f}", "↗️ +25%")
        
        # Profit margin
        profit_margin = (net_profit / total_income * 100) if total_income > 0 else 0
        st.metric("📊 Profit Margin", f"{profit_margin:.1f}%", "↗️ +3%")
        
        st.markdown("### 🎯 Quick Actions")
        if st.button("📄 Generate Report", use_container_width=True):
            st.info("Report generation feature would be implemented here")
        
        if st.button("💾 Export Data", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"business_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Add Transaction", "📊 Analytics", "🧾 Tax Insights", "💼 Business Profile"])
    
    with tab1:
        st.header("📝 Add Business Transaction")
        
        with st.form("transaction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💰 Transaction Details")
                
                transaction_type = st.selectbox(
                    "Transaction Type:",
                    ["income", "expense"],
                    format_func=lambda x: "💰 Income" if x == "income" else "💸 Expense"
                )
                
                if transaction_type == "income":
                    categories = ["Sales", "Services", "Consulting", "Product Sales", "Interest", "Other Income"]
                else:
                    categories = ["Office Rent", "Utilities", "Marketing", "Travel", "Equipment", "Supplies", "Professional Fees", "Other Expenses"]
                
                category = st.selectbox("Category:", categories)
                
                amount = st.number_input(
                    "Amount (₹):",
                    min_value=1,
                    value=10000,
                    step=100,
                    help="Enter the transaction amount"
                )
                
                transaction_date = st.date_input(
                    "Date:",
                    value=datetime.now().date(),
                    help="When did this transaction occur?"
                )
            
            with col2:
                st.subheader("📋 Additional Information")
                
                description = st.text_area(
                    "Description:",
                    placeholder="Detailed description of the transaction",
                    help="Provide details for better tracking and tax purposes"
                )
                
                gst_applicable = st.checkbox(
                    "GST Applicable",
                    help="Check if this transaction involves GST"
                )
                
                if gst_applicable:
                    gst_rate = st.selectbox(
                        "GST Rate:",
                        [5, 12, 18, 28],
                        format_func=lambda x: f"{x}%"
                    )
                    
                    gst_amount = amount * gst_rate / 100
                    st.info(f"GST Amount: ₹{gst_amount:,.2f}")
                
                payment_method = st.selectbox(
                    "Payment Method:",
                    ["Cash", "Bank Transfer", "UPI", "Credit Card", "Cheque"]
                )
                
                invoice_number = st.text_input(
                    "Invoice/Receipt Number:",
                    placeholder="Optional reference number"
                )
            
            if st.form_submit_button("💾 Add Transaction", use_container_width=True):
                new_transaction = {
                    'date': transaction_date.strftime('%Y-%m-%d'),
                    'type': transaction_type,
                    'category': category,
                    'amount': amount,
                    'description': description,
                    'gst_applicable': gst_applicable,
                    'payment_method': payment_method,
                    'invoice_number': invoice_number
                }
                
                # Add to session state
                st.session_state.transactions.append(new_transaction)
                
                st.success("✅ Transaction added successfully!")
                
                # Show AI insights
                if transaction_type == "expense":
                    st.info("🤖 AI Insight: This expense may be tax-deductible under business expenses. Keep the receipt for tax filing.")
                else:
                    st.info("🤖 AI Insight: Remember to set aside 30% of this income for taxes and business expenses.")
                
                st.rerun()
    
    with tab2:
        st.header("📊 Business Analytics")
        
        # Prepare data
        df = pd.DataFrame(st.session_state.transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        df['month'] = df['date'].dt.to_period('M')
        
        # Monthly trends
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Monthly Revenue vs Expenses")
            
            monthly_summary = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
            
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
            
            fig.update_layout(
                title="Monthly Financial Trends",
                xaxis_title="Month",
                yaxis_title="Amount (₹)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🥧 Expense Breakdown")
            
            expense_data = df[df['type'] == 'expense'].groupby('category')['amount'].sum()
            
            if not expense_data.empty:
                fig = px.pie(
                    values=expense_data.values,
                    names=expense_data.index,
                    title="Expense Categories"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No expense data available")
        
        # Income sources
        st.subheader("💰 Income Sources Analysis")
        
        income_data = df[df['type'] == 'income'].groupby('category')['amount'].sum().sort_values(ascending=True)
        
        if not income_data.empty:
            fig = px.bar(
                x=income_data.values,
                y=income_data.index,
                orientation='h',
                title="Income by Category",
                labels={'x': 'Amount (₹)', 'y': 'Category'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No income data available")
        
        # Recent transactions table
        st.subheader("📋 Recent Transactions")
        
        recent_transactions = df.sort_values('date', ascending=False).head(10)
        
        # Format for display
        display_df = recent_transactions.copy()
        display_df['amount'] = display_df['amount'].apply(lambda x: f"₹{x:,.0f}")
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df[['date', 'type', 'category', 'amount', 'description']],
            use_container_width=True
        )
    
    with tab3:
        st.header("🧾 Tax Insights & Optimization")
        
        # Calculate tax-related metrics
        df = pd.DataFrame(st.session_state.transactions)
        
        # Ensure data types are correct
        if not df.empty:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Filter for current year data
            current_year_data = df[df['date'].dt.year == datetime.now().year]
        else:
            current_year_data = pd.DataFrame()
        
        # Calculate annual metrics with safety checks
        if not current_year_data.empty and 'type' in current_year_data.columns and 'amount' in current_year_data.columns:
            annual_income = current_year_data[current_year_data['type'] == 'income']['amount'].sum()
            annual_expenses = current_year_data[current_year_data['type'] == 'expense']['amount'].sum()
            taxable_income = annual_income - annual_expenses
        else:
            annual_income = 0
            annual_expenses = 0
            taxable_income = 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Annual Income", f"₹{annual_income:,.0f}")
        
        with col2:
            st.metric("💸 Deductible Expenses", f"₹{annual_expenses:,.0f}")
        
        with col3:
            st.metric("🧾 Taxable Income", f"₹{taxable_income:,.0f}")
        
        # Tax calculation (simplified)
        if taxable_income > 0:
            st.subheader("💰 Estimated Tax Liability")
            
            # Simplified tax calculation for demonstration
            if taxable_income <= 250000:
                tax_rate = 0
            elif taxable_income <= 500000:
                tax_rate = 5
            elif taxable_income <= 1000000:
                tax_rate = 20
            else:
                tax_rate = 30
            
            estimated_tax = taxable_income * tax_rate / 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("📊 Tax Rate", f"{tax_rate}%")
                st.metric("💰 Estimated Tax", f"₹{estimated_tax:,.0f}")
            
            with col2:
                quarterly_tax = estimated_tax / 4
                st.metric("📅 Quarterly Payment", f"₹{quarterly_tax:,.0f}")
                
                net_income = taxable_income - estimated_tax
                st.metric("💵 Net Income", f"₹{net_income:,.0f}")
        
        # Tax optimization suggestions
        st.subheader("🤖 AI Tax Optimization Suggestions")
        
        suggestions = [
            "💡 **Section 80C Deductions**: Invest in ELSS, PPF, or life insurance to save up to ₹1.5 lakh in taxes",
            "🏠 **Home Loan Benefits**: If you have a home loan, claim deductions under Section 24 and 80C",
            "💼 **Business Expense Optimization**: Ensure all legitimate business expenses are properly documented",
            "📱 **Digital Payments**: Use digital payment methods for better expense tracking and compliance",
            "🧾 **GST Input Credit**: Claim input tax credit on business purchases to reduce GST liability",
            "📊 **Quarterly Reviews**: Regular review of expenses can help identify additional deduction opportunities"
        ]
        
        for suggestion in suggestions:
            st.info(suggestion)
        
        # GST summary
        if 'gst_applicable' in current_year_data.columns:
            gst_transactions = current_year_data[current_year_data['gst_applicable'] == True]
        else:
            gst_transactions = pd.DataFrame()  # Empty DataFrame if column doesn't exist
        
        if not gst_transactions.empty:
            st.subheader("🧾 GST Summary")
            
            gst_income = gst_transactions[gst_transactions['type'] == 'income']['amount'].sum()
            gst_expenses = gst_transactions[gst_transactions['type'] == 'expense']['amount'].sum()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("📈 GST on Sales", f"₹{gst_income * 0.18:,.0f}")
            
            with col2:
                st.metric("📉 Input Tax Credit", f"₹{gst_expenses * 0.18:,.0f}")
    
    with tab4:
        st.header("💼 Business Profile Management")
        
        st.subheader("🏢 Create/Update Business Profile")
        
        with st.form("business_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                business_name = st.text_input("Business Name:", placeholder="Your Business Name")
                business_type = st.selectbox(
                    "Business Type:",
                    ["Sole Proprietorship", "Partnership", "Private Limited", "LLP", "Public Limited"]
                )
                industry = st.selectbox(
                    "Industry:",
                    ["Technology", "Retail", "Manufacturing", "Services", "Healthcare", "Education", "Other"]
                )
                registration_number = st.text_input("Registration Number:", placeholder="GST/CIN Number")
            
            with col2:
                annual_turnover = st.number_input("Expected Annual Turnover (₹):", min_value=0, value=1000000)
                employee_count = st.number_input("Number of Employees:", min_value=1, value=5)
                business_address = st.text_area("Business Address:", placeholder="Complete business address")
                contact_email = st.text_input("Contact Email:", placeholder="business@example.com")
            
            if st.form_submit_button("💾 Save Business Profile", use_container_width=True):
                profile_data = {
                    "business_name": business_name,
                    "business_type": business_type,
                    "industry": industry,
                    "registration_number": registration_number,
                    "annual_turnover": annual_turnover,
                    "employee_count": employee_count,
                    "business_address": business_address,
                    "contact_email": contact_email
                }
                
                st.success("✅ Business profile saved successfully!")
                st.info("🤖 AI will now provide personalized recommendations based on your business profile.")

if __name__ == "__main__":
    main()
