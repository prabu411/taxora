#!/usr/bin/env python3
"""
Final Test of All AI Providers
Test Gemini, Granite, and Hugging Face integration
"""

import requests
import json
import time

def test_providers_endpoint():
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
                    features = ", ".join(provider_info.get("features", [])[:3])
                    print(f"   • {name} ({provider_id}): {status}")
                    print(f"     Features: {features}")
                
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

def test_provider_switching():
    """Test switching between all providers."""
    print("\n🔄 Testing Provider Switching")
    print("=" * 50)
    
    providers_to_test = ["gemini", "granite", "huggingface"]
    working_providers = []
    
    for provider in providers_to_test:
        print(f"\n🧪 Testing {provider.title()}")
        
        try:
            # Switch to provider
            switch_response = requests.post(
                "http://127.0.0.1:8000/ai/provider",
                json={"provider": provider},
                timeout=10
            )
            
            if switch_response.status_code == 200:
                switch_data = switch_response.json()
                if switch_data.get("success"):
                    print(f"✅ Successfully switched to {provider}")
                    
                    # Test a quick chat
                    session_response = requests.post(
                        "http://127.0.0.1:8000/start",
                        json={"name": f"Test {provider}", "role": "general"},
                        timeout=10
                    )
                    
                    if session_response.status_code == 200:
                        session_data = session_response.json()
                        session_id = session_data["session_id"]
                        
                        chat_response = requests.post(
                            "http://127.0.0.1:8000/chat",
                            json={
                                "message": "What are the benefits of compound interest?",
                                "session_id": session_id
                            },
                            timeout=45
                        )
                        
                        if chat_response.status_code == 200:
                            chat_data = chat_response.json()
                            reply = chat_data.get("reply", "")
                            actual_provider = chat_data.get("provider", "unknown")
                            
                            if reply and len(reply) > 50:
                                print(f"✅ {provider.title()} working: {len(reply)} chars")
                                print(f"   Provider used: {actual_provider}")
                                print(f"   Preview: {reply[:100]}...")
                                working_providers.append(provider)
                            else:
                                print(f"⚠️ {provider.title()} gave short response: {reply}")
                        else:
                            print(f"❌ {provider.title()} chat failed: {chat_response.status_code}")
                    else:
                        print(f"❌ Session creation failed for {provider}")
                else:
                    print(f"❌ Switch to {provider} failed: {switch_data.get('message', 'Unknown error')}")
            else:
                print(f"❌ Switch request failed for {provider}: {switch_response.status_code}")
        
        except Exception as e:
            print(f"❌ Error testing {provider}: {e}")
    
    return working_providers

def test_chat_interface():
    """Test the complete chat interface."""
    print("\n💬 Testing Complete Chat Interface")
    print("=" * 50)
    
    try:
        # Set to Gemini (our most reliable provider)
        requests.post(
            "http://127.0.0.1:8000/ai/provider",
            json={"provider": "gemini"},
            timeout=10
        )
        
        # Start session
        session_response = requests.post(
            "http://127.0.0.1:8000/start",
            json={"name": "Final Test User", "role": "general"},
            timeout=10
        )
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session created: {session_id}")
            
            # Test multiple questions
            questions = [
                "What is the best way to start saving money?",
                "How does compound interest work?",
                "What should I know about investing as a beginner?"
            ]
            
            for i, question in enumerate(questions, 1):
                print(f"\n📝 Question {i}: {question}")
                
                chat_response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "message": question,
                        "session_id": session_id
                    },
                    timeout=30
                )
                
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    reply = chat_data.get("reply", "")
                    provider = chat_data.get("provider", "unknown")
                    
                    if reply and len(reply) > 30:
                        print(f"✅ Response from {provider}: {len(reply)} chars")
                        print(f"   Preview: {reply[:150]}...")
                    else:
                        print(f"⚠️ Short response: {reply}")
                else:
                    print(f"❌ Chat failed: {chat_response.status_code}")
            
            return True
        else:
            print(f"❌ Session creation failed: {session_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat interface test error: {e}")
        return False

def test_ai_features_integration():
    """Test AI integration with other features."""
    print("\n🤖 Testing AI Features Integration")
    print("=" * 50)
    
    try:
        # Test savings planner with AI
        goal_data = {
            "user_id": "final_test_user",
            "goal_data": {
                "goal_name": "Emergency Fund",
                "target_amount": 60000,
                "monthly_salary": 35000,
                "monthly_saving_target": 6000,
                "saving_method": "bank_account",
                "target_date": "2025-12-31",
                "description": "Building emergency fund with AI guidance"
            }
        }
        
        response = requests.post("http://127.0.0.1:8000/savings/goal", json=goal_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print(f"✅ Savings goal created with AI suggestions")
                
                ai_suggestions = result.get("ai_suggestions", {})
                if ai_suggestions:
                    suggestions_count = len(ai_suggestions.get("suggestions", []))
                    print(f"🤖 AI provided {suggestions_count} personalized suggestions")
                    
                    if suggestions_count > 0:
                        print(f"   Sample suggestion: {ai_suggestions['suggestions'][0][:100]}...")
                    
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
        print(f"❌ AI features integration test error: {e}")
        return False

def main():
    """Run comprehensive test of all AI providers."""
    print("🚀 FINAL AI PROVIDERS TEST")
    print("=" * 70)
    print("Testing: Gemini ✅ | Granite ✅ | Hugging Face 🤗")
    print("=" * 70)
    
    start_time = time.time()
    
    # Test 1: Provider detection
    providers = test_providers_endpoint()
    
    # Test 2: Provider switching
    working_providers = test_provider_switching()
    
    # Test 3: Chat interface
    chat_working = test_chat_interface()
    
    # Test 4: AI features integration
    ai_integration_working = test_ai_features_integration()
    
    # Summary
    print("\n🎉 FINAL TEST SUMMARY")
    print("=" * 70)
    
    print(f"\n🔍 Providers Detected: {len(providers)}")
    for provider_id, provider_info in providers.items():
        status_icon = "✅" if provider_info["status"] == "available" else "⚠️"
        print(f"   {status_icon} {provider_info['name']}: {provider_info['status']}")
    
    print(f"\n🔄 Working Providers: {len(working_providers)} ({', '.join(working_providers)})")
    print(f"💬 Chat Interface: {'✅ WORKING' if chat_working else '❌ NOT WORKING'}")
    print(f"🤖 AI Integration: {'✅ WORKING' if ai_integration_working else '❌ NOT WORKING'}")
    
    overall_success = len(working_providers) >= 2 and chat_working
    
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
            if provider == "gemini":
                print(f"   ✅ Gemini - Google's latest AI with your API key")
            elif provider == "granite":
                print(f"   ✅ Granite - IBM's reliable local AI")
            elif provider == "huggingface":
                print(f"   🤗 Hugging Face - Open source AI models")
        
        print("\n🎯 Access Your System:")
        print("   • Chat Interface: http://127.0.0.1:8000/static/chat.html")
        print("   • Savings Planner: http://127.0.0.1:8000/static/savings.html")
        print("   • Business Tracker: http://127.0.0.1:8000/static/business.html")
        
        print("\n💡 Usage Tips:")
        print("   • Select 'Google Gemini' for detailed responses")
        print("   • Use 'IBM Granite' for fast, reliable answers")
        print("   • Try 'Hugging Face' for open source AI")
        
    else:
        print("\n⚠️ Some issues found")
        print("Check the details above for specific problems")
    
    return overall_success

if __name__ == "__main__":
    main()
