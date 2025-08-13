#!/usr/bin/env python3
"""
Test Enhanced Business Tracker
Tests comprehensive tax management and enhanced business profile features
"""

import requests
import json
import time
from datetime import datetime, timedelta

def test_enhanced_business_profile():
    """Test enhanced business profile creation."""
    print("🏢 Testing Enhanced Business Profile")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test creating enhanced business profile
        profile_data = {
            "business_name": "Enhanced Test Business Pvt Ltd",
            "owner_name": "Test Owner Enhanced",
            "gst_number": "22AAAAA0000A1Z5",
            "business_type": "private_limited",
            "sector": "goods_18",
            "registration_date": "2024-01-01",
            # Enhanced fields
            "pan_number": "AAAAA0000A",
            "tan_number": "AAAA00000A",
            "cin_number": "U12345AB2020PTC123456",
            "address": "123 Business Street, Commercial Area",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400001",
            "phone": "+91 9876543210",
            "email": "business@enhanced.com",
            "bank_account": "1234567890",
            "bank_ifsc": "SBIN0001234",
            # Tax registration details
            "professional_tax_number": "PT123456",
            "esi_number": "12345678901234567",
            "pf_number": "AB/DEL/12345",
            "trade_license_number": "TL123456"
        }
        
        response = requests.post(f"{base_url}/business/profile", json=profile_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                business_id = result["business_id"]
                print(f"✅ Enhanced business profile created: {business_id}")
                print(f"🏢 Business: {result['profile']['business_name']}")
                print(f"📧 Email: {result['profile']['email']}")
                print(f"🏦 Bank: {result['profile']['bank_account']}")
                
                # Check AI recommendations
                if "ai_recommendations" in result:
                    ai_recs = result["ai_recommendations"]
                    print(f"🤖 AI Recommendations provided:")
                    print(f"   • Required registrations: {len(ai_recs.get('required_registrations', []))}")
                    print(f"   • Applicable taxes: {len(ai_recs.get('applicable_taxes', []))}")
                
                return business_id
            else:
                print(f"❌ Enhanced profile creation failed: {result.get('error')}")
        else:
            print(f"❌ Enhanced profile request failed: {response.status_code}")
            
        return None
        
    except Exception as e:
        print(f"❌ Enhanced business profile test error: {e}")
        return None

def test_comprehensive_tax_management(business_id):
    """Test comprehensive tax management features."""
    print("\n💰 Testing Comprehensive Tax Management")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test adding various tax records
        tax_records = [
            {
                "tax_type": "road_tax",
                "tax_name": "Car Road Tax 2024",
                "amount": 15000,
                "authority": "Regional Transport Office",
                "due_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "status": "pending",
                "description": "Annual road tax for company vehicle"
            },
            {
                "tax_type": "water_tax",
                "tax_name": "Municipal Water Tax Q1",
                "amount": 5000,
                "authority": "Municipal Corporation",
                "due_date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
                "status": "pending",
                "description": "Quarterly water tax for office premises"
            },
            {
                "tax_type": "professional_tax",
                "tax_name": "Professional Tax March 2024",
                "amount": 2500,
                "authority": "State Professional Tax Department",
                "due_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "paid",
                "payment_date": datetime.now().strftime("%Y-%m-%d"),
                "transaction_number": "TXN123456789",
                "description": "Monthly professional tax payment"
            },
            {
                "tax_type": "municipality_tax",
                "tax_name": "Property Tax 2024",
                "amount": 25000,
                "authority": "Municipal Corporation",
                "due_date": (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d"),
                "status": "pending",
                "description": "Annual property tax for office building"
            }
        ]
        
        added_records = []
        
        for tax_data in tax_records:
            response = requests.post(f"{base_url}/business/tax", json={
                "business_id": business_id,
                "tax_data": tax_data
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result["success"]:
                    added_records.append(result["tax_record_id"])
                    print(f"✅ {tax_data['tax_name']}: ₹{tax_data['amount']:,} - {tax_data['status']}")
                    
                    # Check AI insights
                    if "ai_insights" in result:
                        insights = result["ai_insights"]
                        print(f"   🤖 AI Insights: {len(insights.get('optimization_tips', []))} tips provided")
                else:
                    print(f"❌ Failed to add {tax_data['tax_name']}: {result.get('error')}")
            else:
                print(f"❌ Tax record request failed: {response.status_code}")
        
        print(f"\n📊 Added {len(added_records)} tax records successfully")
        return added_records
        
    except Exception as e:
        print(f"❌ Tax management test error: {e}")
        return []

def test_tax_summary_and_analytics(business_id):
    """Test tax summary and analytics features."""
    print("\n📈 Testing Tax Summary & Analytics")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test comprehensive tax summary
        for period in ["month", "quarter", "year"]:
            response = requests.get(f"{base_url}/business/tax-summary/{business_id}?period={period}", timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result["success"]:
                    summary = result["summary"]
                    print(f"✅ {period.title()} Tax Summary:")
                    print(f"   • Total Paid: ₹{summary['total_tax_paid']:,}")
                    print(f"   • Total Pending: ₹{summary['total_pending']:,}")
                    print(f"   • Overdue Count: {summary['overdue_count']}")
                    print(f"   • Tax Types: {len(summary['tax_breakdown'])}")
                    
                    # Check AI analysis
                    if "ai_analysis" in result:
                        ai_analysis = result["ai_analysis"]
                        print(f"   🤖 AI Health Assessment: {ai_analysis.get('health_assessment', 'Available')}")
                else:
                    print(f"❌ {period.title()} summary failed: {result.get('error')}")
            else:
                print(f"❌ {period.title()} summary request failed: {response.status_code}")
        
        # Test tax reminders
        response = requests.get(f"{base_url}/business/tax-reminders/{business_id}", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print(f"\n🔔 Tax Reminders:")
                print(f"   • Upcoming taxes: {len(result['upcoming_taxes'])}")
                print(f"   • Overdue taxes: {len(result['overdue_taxes'])}")
                print(f"   • Total reminders: {result['reminder_count']}")
                
                # Check AI recommendations
                if "ai_recommendations" in result:
                    ai_recs = result["ai_recommendations"]
                    print(f"   🤖 AI Planning Recommendations: {len(ai_recs.get('immediate_actions', []))} actions")
                
                return True
            else:
                print(f"❌ Tax reminders failed: {result.get('error')}")
        else:
            print(f"❌ Tax reminders request failed: {response.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ Tax summary test error: {e}")
        return False

def test_tax_payment_update(business_id, tax_records):
    """Test tax payment update functionality."""
    print("\n💳 Testing Tax Payment Updates")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        if not tax_records:
            print("⚠️ No tax records to update")
            return False
        
        # Update payment for first tax record
        tax_record_id = tax_records[0]
        payment_data = {
            "business_id": business_id,
            "payment_date": datetime.now().strftime("%Y-%m-%d"),
            "transaction_number": f"TXN{int(datetime.now().timestamp())}"
        }
        
        response = requests.put(f"{base_url}/business/tax-payment/{tax_record_id}", json=payment_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print(f"✅ Tax payment updated: {tax_record_id}")
                print(f"💳 Transaction: {payment_data['transaction_number']}")
                
                # Check AI insights
                if "ai_insights" in result:
                    insights = result["ai_insights"]
                    print(f"🤖 AI Payment Insights: {len(insights.get('next_steps', []))} next steps")
                
                return True
            else:
                print(f"❌ Payment update failed: {result.get('error')}")
        else:
            print(f"❌ Payment update request failed: {response.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ Tax payment update test error: {e}")
        return False

def main():
    """Run comprehensive test of enhanced business tracker."""
    print("🚀 ENHANCED BUSINESS TRACKER TEST")
    print("=" * 70)
    
    start_time = time.time()
    
    # Test enhanced business profile
    business_id = test_enhanced_business_profile()
    
    if business_id:
        # Test comprehensive tax management
        tax_records = test_comprehensive_tax_management(business_id)
        
        # Test tax summary and analytics
        summary_success = test_tax_summary_and_analytics(business_id)
        
        # Test tax payment updates
        payment_success = test_tax_payment_update(business_id, tax_records)
        
        # Summary
        print("\n🎉 ENHANCED BUSINESS TRACKER TEST SUMMARY")
        print("=" * 70)
        
        print(f"\n🏢 Enhanced Business Profile: {'✅ PASS' if business_id else '❌ FAIL'}")
        print(f"💰 Tax Management: {'✅ PASS' if tax_records else '❌ FAIL'}")
        print(f"📈 Tax Analytics: {'✅ PASS' if summary_success else '❌ FAIL'}")
        print(f"💳 Payment Updates: {'✅ PASS' if payment_success else '❌ FAIL'}")
        
        overall_success = business_id and tax_records and summary_success and payment_success
        
        print(f"\n🏆 OVERALL RESULT: {'✅ ALL TESTS PASSED' if overall_success else '⚠️ SOME ISSUES FOUND'}")
        
        elapsed_time = time.time() - start_time
        print(f"⏱️ Test Duration: {elapsed_time:.2f} seconds")
        
        if overall_success:
            print("\n🎉 CONGRATULATIONS!")
            print("Your enhanced business tracker is fully functional!")
            print("\n🌟 Enhanced Features Working:")
            print("   ✅ Comprehensive Business Profiles")
            print("   ✅ Multi-Tax Type Management")
            print("   ✅ Road Tax, Water Tax, Municipality Tax")
            print("   ✅ Professional Tax, Property Tax")
            print("   ✅ Transaction Number Linking")
            print("   ✅ AI Tax Optimization Insights")
            print("   ✅ Comprehensive Tax Analytics")
            print("   ✅ Smart Tax Reminders")
            print("   ✅ Payment Status Tracking")
            
            print(f"\n🎯 Business ID Created: {business_id}")
            print(f"📊 Tax Records Added: {len(tax_records)}")
            print("🔗 Access: http://127.0.0.1:8000/static/business.html")
            
        else:
            print("\n⚠️ Some enhanced features need attention")
            print("Check the details above for specific issues")
        
        return overall_success
    else:
        print("\n❌ Enhanced business profile creation failed")
        print("Cannot proceed with other tests")
        return False

if __name__ == "__main__":
    main()
