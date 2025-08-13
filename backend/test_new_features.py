#!/usr/bin/env python3
"""
Test New Financial Features
Tests Savings Planner and Business Tracker functionality
"""

import requests
import json
import time
from datetime import datetime, timedelta

def test_savings_planner():
    """Test savings planner functionality."""
    print("💰 Testing Savings Planner")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test creating a savings goal
        goal_data = {
            "user_id": "test_user",
            "goal_data": {
                "goal_name": "Emergency Fund",
                "target_amount": 100000,
                "monthly_salary": 50000,
                "monthly_saving_target": 10000,
                "saving_method": "bank_account",
                "target_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                "description": "Building an emergency fund for financial security"
            }
        }
        
        response = requests.post(f"{base_url}/savings/goal", json=goal_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                goal_id = result["goal_id"]
                print(f"✅ Savings goal created: {goal_id}")
                print(f"💡 AI Suggestions: {len(result.get('ai_suggestions', {}).get('suggestions', []))} provided")
                
                # Test adding a savings entry
                entry_data = {
                    "goal_id": goal_id,
                    "entry_data": {
                        "amount": 5000,
                        "saving_method": "bank_account",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "description": "First savings entry"
                    }
                }
                
                entry_response = requests.post(f"{base_url}/savings/entry", json=entry_data, timeout=30)
                
                if entry_response.status_code == 200:
                    entry_result = entry_response.json()
                    if entry_result["success"]:
                        print(f"✅ Savings entry added: ₹{entry_data['entry_data']['amount']:,}")
                        
                        # Test getting analysis
                        analysis_response = requests.get(f"{base_url}/savings/analysis/{goal_id}", timeout=30)
                        
                        if analysis_response.status_code == 200:
                            analysis_result = analysis_response.json()
                            if analysis_result["success"]:
                                analysis = analysis_result["analysis"]
                                print(f"✅ Analysis generated:")
                                print(f"   • Progress: ₹{analysis['current_progress']:,} ({analysis['percentage_complete']:.1f}%)")
                                print(f"   • On track: {analysis['on_track']}")
                                print(f"   • Days remaining: {analysis['days_remaining']}")
                                
                                # Test 30-day plan
                                plan_response = requests.get(f"{base_url}/savings/plan/{goal_id}", timeout=30)
                                
                                if plan_response.status_code == 200:
                                    plan_result = plan_response.json()
                                    if plan_result["success"]:
                                        print(f"✅ 30-day plan generated")
                                        return True
                                    else:
                                        print(f"❌ 30-day plan failed: {plan_result.get('error')}")
                                else:
                                    print(f"❌ 30-day plan request failed: {plan_response.status_code}")
                            else:
                                print(f"❌ Analysis failed: {analysis_result.get('error')}")
                        else:
                            print(f"❌ Analysis request failed: {analysis_response.status_code}")
                    else:
                        print(f"❌ Savings entry failed: {entry_result.get('error')}")
                else:
                    print(f"❌ Savings entry request failed: {entry_response.status_code}")
            else:
                print(f"❌ Goal creation failed: {result.get('error')}")
        else:
            print(f"❌ Goal creation request failed: {response.status_code}")
            
        return False
        
    except Exception as e:
        print(f"❌ Savings planner test error: {e}")
        return False

def test_business_tracker():
    """Test business tracker functionality."""
    print("\n🏢 Testing Business Tracker")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test creating a business profile
        profile_data = {
            "business_name": "Test Business Pvt Ltd",
            "owner_name": "Test Owner",
            "gst_number": "22AAAAA0000A1Z5",
            "business_type": "private_limited",
            "sector": "goods_18",
            "registration_date": "2024-01-01"
        }
        
        response = requests.post(f"{base_url}/business/profile", json=profile_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                business_id = result["business_id"]
                print(f"✅ Business profile created: {business_id}")
                print(f"🏢 Business: {result['profile']['business_name']}")
                
                # Test adding a transaction
                transaction_data = {
                    "business_id": business_id,
                    "transaction_data": {
                        "transaction_type": "credit",
                        "amount": 50000,
                        "category": "Sales",
                        "party_name": "Customer ABC",
                        "party_gst_number": "22BBBBB0000B1Z5",
                        "invoice_number": "INV-001",
                        "gst_applicable": True,
                        "gst_sector": "goods_18",
                        "description": "Product sales with 18% GST"
                    }
                }
                
                txn_response = requests.post(f"{base_url}/business/transaction", json=transaction_data, timeout=30)
                
                if txn_response.status_code == 200:
                    txn_result = txn_response.json()
                    if txn_result["success"]:
                        print(f"✅ Transaction added: ₹{transaction_data['transaction_data']['amount']:,}")
                        print(f"💰 GST Amount: ₹{txn_result['transaction']['gst_amount']:,}")
                        
                        # Test GST summary
                        current_month = datetime.now().month
                        current_year = datetime.now().year
                        
                        gst_response = requests.get(f"{base_url}/business/gst/{business_id}/{current_month}/{current_year}", timeout=30)
                        
                        if gst_response.status_code == 200:
                            gst_result = gst_response.json()
                            if gst_result["success"]:
                                summary = gst_result["summary"]
                                print(f"✅ GST summary generated:")
                                print(f"   • Taxable amount: ₹{summary['total_taxable_amount']:,}")
                                print(f"   • GST collected: ₹{summary['total_gst_collected']:,}")
                                print(f"   • Net liability: ₹{summary['net_gst_liability']:,}")
                                
                                # Test GST return calculation
                                return_response = requests.get(f"{base_url}/business/gst-return/{business_id}/{current_month}/{current_year}", timeout=30)
                                
                                if return_response.status_code == 200:
                                    return_result = return_response.json()
                                    if return_result["success"]:
                                        print(f"✅ GST return calculated:")
                                        print(f"   • Return amount: ₹{return_result['gst_return_amount']:,}")
                                        print(f"   • Due date: {return_result['due_date']}")
                                        
                                        # Test business analytics
                                        analytics_response = requests.get(f"{base_url}/business/analytics/{business_id}?period=month", timeout=30)
                                        
                                        if analytics_response.status_code == 200:
                                            analytics_result = analytics_response.json()
                                            if analytics_result["success"]:
                                                analytics = analytics_result["analytics"]
                                                print(f"✅ Business analytics generated:")
                                                print(f"   • Total credits: ₹{analytics['total_credits']:,}")
                                                print(f"   • Total debits: ₹{analytics['total_debits']:,}")
                                                print(f"   • Net profit: ₹{analytics['net_profit']:,}")
                                                
                                                # Test monthly reminder
                                                reminder_response = requests.get(f"{base_url}/business/reminder/{business_id}", timeout=30)
                                                
                                                if reminder_response.status_code == 200:
                                                    reminder_result = reminder_response.json()
                                                    if reminder_result["success"]:
                                                        print(f"✅ Monthly reminder generated")
                                                        print(f"   • For month: {reminder_result['for_month']}")
                                                        print(f"   • Action required: {reminder_result['action_required']}")
                                                        return True
                                                    else:
                                                        print(f"❌ Reminder failed: {reminder_result.get('error')}")
                                                else:
                                                    print(f"❌ Reminder request failed: {reminder_response.status_code}")
                                            else:
                                                print(f"❌ Analytics failed: {analytics_result.get('error')}")
                                        else:
                                            print(f"❌ Analytics request failed: {analytics_response.status_code}")
                                    else:
                                        print(f"❌ GST return failed: {return_result.get('error')}")
                                else:
                                    print(f"❌ GST return request failed: {return_response.status_code}")
                            else:
                                print(f"❌ GST summary failed: {gst_result.get('error')}")
                        else:
                            print(f"❌ GST summary request failed: {gst_response.status_code}")
                    else:
                        print(f"❌ Transaction failed: {txn_result.get('error')}")
                else:
                    print(f"❌ Transaction request failed: {txn_response.status_code}")
            else:
                print(f"❌ Business profile failed: {result.get('error')}")
        else:
            print(f"❌ Business profile request failed: {response.status_code}")
            
        return False
        
    except Exception as e:
        print(f"❌ Business tracker test error: {e}")
        return False

def test_frontend_pages():
    """Test that frontend pages are accessible."""
    print("\n🎨 Testing Frontend Pages")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    pages = [
        ("/static/index.html", "Main Page"),
        ("/static/savings.html", "Savings Planner"),
        ("/static/business.html", "Business Tracker"),
        ("/static/chat.html", "Chat Interface")
    ]
    
    results = {}
    
    for url, name in pages:
        try:
            response = requests.get(f"{base_url}{url}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Accessible")
                results[name] = True
            else:
                print(f"❌ {name}: Status {response.status_code}")
                results[name] = False
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            results[name] = False
    
    return all(results.values())

def main():
    """Run comprehensive test of new features."""
    print("🚀 NEW FINANCIAL FEATURES TEST")
    print("=" * 70)
    
    start_time = time.time()
    
    # Test all features
    savings_success = test_savings_planner()
    business_success = test_business_tracker()
    frontend_success = test_frontend_pages()
    
    # Summary
    print("\n🎉 NEW FEATURES TEST SUMMARY")
    print("=" * 70)
    
    print(f"\n💰 Savings Planner: {'✅ PASS' if savings_success else '❌ FAIL'}")
    print(f"🏢 Business Tracker: {'✅ PASS' if business_success else '❌ FAIL'}")
    print(f"🎨 Frontend Pages: {'✅ PASS' if frontend_success else '❌ FAIL'}")
    
    overall_success = savings_success and business_success and frontend_success
    
    print(f"\n🏆 OVERALL RESULT: {'✅ ALL TESTS PASSED' if overall_success else '⚠️ SOME ISSUES FOUND'}")
    
    elapsed_time = time.time() - start_time
    print(f"⏱️ Test Duration: {elapsed_time:.2f} seconds")
    
    if overall_success:
        print("\n🎉 CONGRATULATIONS!")
        print("Your new financial features are fully functional!")
        print("\n🌟 Available Features:")
        print("   ✅ AI-Powered Savings Planner")
        print("   ✅ Business Credit/Debit Tracker")
        print("   ✅ GST Management & Returns")
        print("   ✅ Monthly Tax Reminders")
        print("   ✅ AI Financial Insights")
        print("   ✅ 30-Day Savings Plans")
        print("   ✅ Business Analytics")
        
        print("\n🎯 Access Your Features:")
        print("   • Savings Planner: http://127.0.0.1:8000/static/savings.html")
        print("   • Business Tracker: http://127.0.0.1:8000/static/business.html")
        print("   • Main Dashboard: http://127.0.0.1:8000/static/index.html")
        
    else:
        print("\n⚠️ Some features need attention")
        print("Check the details above for specific issues")
    
    return overall_success

if __name__ == "__main__":
    main()
