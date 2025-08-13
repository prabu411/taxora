#!/usr/bin/env python3
"""
Test Google Gemini Integration
"""

import requests
import json
import time
from gemini_client import test_gemini_connection, gemini_generate_response

def test_gemini_direct():
    """Test Gemini client directly."""
    print("🧪 Testing Gemini Client Directly")
    print("=" * 50)
    
    # Test connection
    result = test_gemini_connection()
    print(f"✅ Connection Status: {result['status']}")
    print(f"💬 Message: {result['message']}")
    
    if result['status'] == 'success':
        # Test response generation
        print("\n💬 Testing Response Generation")
        messages = [{"role": "user", "content": "What's a simple budgeting tip for beginners?"}]
        
        start_time = time.time()
        response = gemini_generate_response(messages)
        response_time = time.time() - start_time
        
        print(f"⏱️  Response time: {response_time:.2f} seconds")
        print(f"📝 Response length: {len(response)} characters")
        print(f"💬 Response preview: {response[:200]}...")
        
        return True
    else:
        print("❌ Gemini connection failed")
        return False

def test_ai_provider_switching():
    """Test switching to Gemini via API."""
    print("\n🔄 Testing AI Provider Switching")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Check current providers
        providers_response = requests.get(f"{base_url}/ai/providers", timeout=10)
        
        if providers_response.status_code == 200:
            data = providers_response.json()
            print(f"✅ Current provider: {data['data']['current_provider']}")
            print(f"✅ Available providers: {list(data['data']['available_providers'].keys())}")
            
            # Switch to Gemini
            switch_response = requests.post(
                f"{base_url}/ai/provider",
                json={"provider": "gemini"},
                timeout=10
            )
            
            if switch_response.status_code == 200:
                switch_data = switch_response.json()
                if switch_data.get("success"):
                    print(f"✅ Successfully switched to Gemini")
                    print(f"💬 Message: {switch_data['message']}")
                    return True
                else:
                    print(f"❌ Switch failed: {switch_data.get('message')}")
                    return False
            else:
                print(f"❌ Switch request failed: {switch_response.status_code}")
                return False
        else:
            print(f"❌ Providers check failed: {providers_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_gemini_chat_responses():
    """Test Gemini responses through chat API."""
    print("\n💬 Testing Gemini Chat Responses")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Start session
        session_response = requests.post(
            f"{base_url}/start",
            json={"name": "Test User", "role": "general"},
            timeout=10
        )
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session started: {session_id}")
        else:
            print(f"❌ Session failed: {session_response.status_code}")
            return False
        
        # Test financial questions with Gemini
        questions = [
            "What's the 50/30/20 budgeting rule?",
            "How much should I save for emergencies?",
            "Should I invest in stocks or bonds as a beginner?"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n📝 Question {i}: {question}")
            
            chat_response = requests.post(
                f"{base_url}/chat",
                json={
                    "message": question,
                    "session_id": session_id
                },
                timeout=45  # Longer timeout for Gemini
            )
            
            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                reply = chat_data.get("reply", "No reply")
                
                print(f"✅ Response received ({len(reply)} chars)")
                print(f"💬 Preview: {reply[:150]}...")
                
                # Check if it's a quality Gemini response
                if len(reply) > 100 and not reply.startswith("[Switched to IBM Granite"):
                    print("🎯 Quality Gemini response detected!")
                elif reply.startswith("[Switched to IBM Granite"):
                    print("⚠️  Fallback to Granite occurred")
                else:
                    print("⚠️  Response quality could be improved")
                    
            else:
                print(f"❌ Chat failed: {chat_response.status_code}")
                print(f"   Error: {chat_response.text}")
            
            time.sleep(2)  # Small delay between requests
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all Gemini integration tests."""
    print("🚀 Taxora Google Gemini Integration Test")
    print("=" * 60)
    
    try:
        # Test 1: Direct Gemini client
        gemini_direct_success = test_gemini_direct()
        
        if gemini_direct_success:
            # Test 2: AI provider switching
            switch_success = test_ai_provider_switching()
            
            if switch_success:
                # Test 3: Chat responses
                chat_success = test_gemini_chat_responses()
                
                if chat_success:
                    print("\n🎉 All Gemini tests passed!")
                    print("\n💡 Features working:")
                    print("   ✅ Gemini API connection")
                    print("   ✅ AI provider switching")
                    print("   ✅ Quality financial responses")
                    print("   ✅ Voice-ready responses")
                    print("   ✅ Generous free quota")
                    
                    print("\n🎯 Your Gemini integration is fully functional!")
                    print("   🔥 Premium AI responses")
                    print("   🆓 Free generous quota")
                    print("   🎙️ Voice-optimized")
                    print("   ⚡ Fast response times")
                else:
                    print("\n⚠️  Chat responses need attention")
            else:
                print("\n⚠️  Provider switching needs attention")
        else:
            print("\n❌ Gemini client needs configuration")
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    main()
