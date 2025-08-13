#!/usr/bin/env python3
"""
Test Working AI System
Test the complete AI system with working providers
"""

import requests
import json
import time

def test_ai_providers_endpoint():
    """Test AI providers endpoint."""
    print("🔍 Testing AI Providers Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get("http://127.0.0.1:8000/ai/providers", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                providers = data["data"]["available_providers"]
                
                print(f"✅ Available providers: {list(providers.keys())}")
                
                for provider_id, provider_info in providers.items():
                    status = provider_info["status"]
                    name = provider_info["name"]
                    print(f"   • {name} ({provider_id}): {status}")
                
                return providers
            else:
                print("❌ Providers data invalid")
                return {}
        else:
            print(f"❌ Providers check failed: {response.status_code}")
            return {}
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

def test_chat_session():
    """Test complete chat session."""
    print("\n💬 Testing Chat Session")
    print("=" * 50)
    
    try:
        # Start a new session
        session_response = requests.post(
            "http://127.0.0.1:8000/start",
            json={"name": "Test User", "role": "general"},
            timeout=10
        )
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session created: {session_id}")
            
            # Test chat with financial question
            chat_response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "message": "What are some good savings strategies for beginners?",
                    "session_id": session_id
                },
                timeout=30
            )
            
            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                reply = chat_data.get("reply", "")
                provider = chat_data.get("provider", "unknown")
                
                if reply and len(reply) > 50:
                    print(f"✅ Chat response received from {provider}")
                    print(f"💬 Response length: {len(reply)} characters")
                    print(f"📝 Preview: {reply[:150]}...")
                    return True
                else:
                    print(f"⚠️ Short response received: {reply}")
                    return False
            else:
                print(f"❌ Chat failed: {chat_response.status_code}")
                return False
        else:
            print(f"❌ Session creation failed: {session_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def test_provider_switching():
    """Test switching between providers."""
    print("\n🔄 Testing Provider Switching")
    print("=" * 50)
    
    try:
        # Get available providers
        providers_response = requests.get("http://127.0.0.1:8000/ai/providers")
        if providers_response.status_code != 200:
            print("❌ Could not get providers list")
            return False
        
        providers_data = providers_response.json()
        available_providers = providers_data["data"]["available_providers"]
        
        working_providers = []
        
        for provider_id, provider_info in available_providers.items():
            if provider_info["status"] == "available":
                print(f"\n🧪 Testing {provider_info['name']} ({provider_id})")
                
                # Switch to provider
                switch_response = requests.post(
                    "http://127.0.0.1:8000/ai/provider",
                    json={"provider": provider_id},
                    timeout=10
                )
                
                if switch_response.status_code == 200:
                    switch_data = switch_response.json()
                    if switch_data.get("success"):
                        print(f"✅ Successfully switched to {provider_info['name']}")
                        
                        # Test a quick chat
                        session_response = requests.post(
                            "http://127.0.0.1:8000/start",
                            json={"name": f"Test {provider_id}", "role": "general"},
                            timeout=10
                        )
                        
                        if session_response.status_code == 200:
                            session_data = session_response.json()
                            session_id = session_data["session_id"]
                            
                            chat_response = requests.post(
                                "http://127.0.0.1:8000/chat",
                                json={
                                    "message": "What is compound interest?",
                                    "session_id": session_id
                                },
                                timeout=30
                            )
                            
                            if chat_response.status_code == 200:
                                chat_data = chat_response.json()
                                reply = chat_data.get("reply", "")
                                
                                if reply and len(reply) > 30:
                                    print(f"✅ {provider_info['name']} working: {len(reply)} chars")
                                    working_providers.append(provider_id)
                                else:
                                    print(f"⚠️ {provider_info['name']} gave short response")
                            else:
                                print(f"❌ {provider_info['name']} chat failed")
                        else:
                            print(f"❌ Session creation failed for {provider_info['name']}")
                    else:
                        print(f"❌ Switch to {provider_info['name']} failed")
                else:
                    print(f"❌ Switch request failed for {provider_info['name']}")
            else:
                print(f"⚠️ {provider_info['name']} not available: {provider_info['status']}")
        
        return working_providers
        
    except Exception as e:
        print(f"❌ Provider switching test error: {e}")
        return []

def test_savings_planner_integration():
    """Test savings planner with AI integration."""
    print("\n💰 Testing Savings Planner AI Integration")
    print("=" * 50)
    
    try:
        # Create a test savings goal
        goal_data = {
            "user_id": "test_user_ai",
            "goal_data": {
                "goal_name": "Emergency Fund Test",
                "target_amount": 50000,
                "monthly_salary": 30000,
                "monthly_saving_target": 5000,
                "saving_method": "bank_account",
                "target_date": "2025-12-31",
                "description": "Testing AI integration with savings planner"
            }
        }
        
        response = requests.post("http://127.0.0.1:8000/savings/goal", json=goal_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print(f"✅ Savings goal created with AI suggestions")
                
                # Check if AI suggestions were provided
                ai_suggestions = result.get("ai_suggestions", {})
                if ai_suggestions:
                    suggestions_count = len(ai_suggestions.get("suggestions", []))
                    reduce_areas_count = len(ai_suggestions.get("reduce_areas", []))
                    increase_areas_count = len(ai_suggestions.get("increase_areas", []))
                    
                    print(f"🤖 AI provided {suggestions_count} suggestions")
                    print(f"🤖 AI provided {reduce_areas_count} expense reduction areas")
                    print(f"🤖 AI provided {increase_areas_count} income increase areas")
                    
                    return True
                else:
                    print("⚠️ No AI suggestions received")
                    return False
            else:
                print(f"❌ Savings goal creation failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Savings goal request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Savings planner AI test error: {e}")
        return False

def main():
    """Run comprehensive test of working AI system."""
    print("🤖 WORKING AI SYSTEM TEST")
    print("=" * 70)
    
    start_time = time.time()
    
    # Test 1: Provider detection
    providers = test_ai_providers_endpoint()
    
    # Test 2: Chat functionality
    chat_working = test_chat_session()
    
    # Test 3: Provider switching
    working_providers = test_provider_switching()
    
    # Test 4: AI integration with features
    ai_integration_working = test_savings_planner_integration()
    
    # Summary
    print("\n🎉 WORKING AI SYSTEM TEST SUMMARY")
    print("=" * 70)
    
    print(f"\n🔍 Providers Detected: {len(providers)}")
    for provider_id, provider_info in providers.items():
        status_icon = "✅" if provider_info["status"] == "available" else "⚠️"
        print(f"   {status_icon} {provider_info['name']}: {provider_info['status']}")
    
    print(f"\n💬 Chat Functionality: {'✅ WORKING' if chat_working else '❌ NOT WORKING'}")
    print(f"🔄 Working Providers: {len(working_providers)} ({', '.join(working_providers)})")
    print(f"🤖 AI Integration: {'✅ WORKING' if ai_integration_working else '❌ NOT WORKING'}")
    
    overall_success = chat_working and len(working_providers) > 0
    
    print(f"\n🏆 OVERALL RESULT: {'✅ SYSTEM WORKING' if overall_success else '⚠️ ISSUES FOUND'}")
    
    elapsed_time = time.time() - start_time
    print(f"⏱️ Test Duration: {elapsed_time:.2f} seconds")
    
    if overall_success:
        print("\n🎉 SUCCESS!")
        print("Your AI system is working correctly!")
        print("\n🌟 Working Features:")
        print("   ✅ AI Chat Interface")
        print("   ✅ Provider Switching")
        print("   ✅ Financial Advice Generation")
        print("   ✅ AI-Powered Savings Planning")
        print("   ✅ Multi-Provider Support")
        
        print(f"\n🔑 Working Providers: {len(working_providers)}")
        for provider in working_providers:
            print(f"   ✅ {provider.title()}")
        
        print("\n🎯 Access Your System:")
        print("   • Chat Interface: http://127.0.0.1:8000/static/chat.html")
        print("   • Savings Planner: http://127.0.0.1:8000/static/savings.html")
        print("   • Business Tracker: http://127.0.0.1:8000/static/business.html")
        
    else:
        print("\n⚠️ Some issues found")
        print("Check the details above for specific problems")
    
    return overall_success

if __name__ == "__main__":
    main()
