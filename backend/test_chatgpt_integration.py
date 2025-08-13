#!/usr/bin/env python3
"""
Test ChatGPT Integration
"""

import requests
import json

def test_providers():
    """Test AI providers endpoint."""
    print("🧪 Testing AI Providers")
    print("=" * 50)
    
    try:
        response = requests.get("http://127.0.0.1:8000/ai/providers")
        data = response.json()
        
        if data["success"]:
            providers = data["data"]["available_providers"]
            current = data["data"]["current_provider"]
            
            print(f"✅ Current provider: {current}")
            print(f"✅ Available providers: {list(providers.keys())}")
            print(f"✅ Provider count: {data['data']['provider_count']}")
            
            for provider_id, provider_info in providers.items():
                status = provider_info["status"]
                name = provider_info["name"]
                print(f"   - {name}: {status}")
                
            return True
        else:
            print("❌ Failed to get providers")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_switch_to_chatgpt():
    """Test switching to ChatGPT."""
    print("\n🔄 Testing Switch to ChatGPT")
    print("=" * 50)
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ai/provider",
            json={"provider": "chatgpt"}
        )
        data = response.json()
        
        if data.get("success"):
            print(f"✅ Successfully switched to ChatGPT")
            print(f"   Message: {data['message']}")
            return True
        else:
            print(f"❌ Failed to switch: {data.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chatgpt_response():
    """Test getting a response from ChatGPT."""
    print("\n💬 Testing ChatGPT Response")
    print("=" * 50)
    
    try:
        # First start a session
        session_response = requests.post(
            "http://127.0.0.1:8000/start",
            json={"name": "Test User", "role": "general"}
        )
        
        if session_response.status_code != 200:
            print("❌ Failed to start session")
            return False
            
        session_data = session_response.json()
        session_id = session_data["session_id"]
        print(f"✅ Session started: {session_id}")
        
        # Send a test message
        chat_response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "message": "What's a simple budgeting tip for beginners?",
                "session_id": session_id
            }
        )
        
        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            reply = chat_data.get("reply", "No reply")
            print(f"✅ ChatGPT Response received:")
            print(f"   {reply[:100]}...")
            return True
        else:
            print(f"❌ Chat failed: {chat_response.status_code}")
            print(f"   {chat_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🤖 Taxora ChatGPT Integration Test")
    print("=" * 50)
    
    # Test 1: Check providers
    if not test_providers():
        return
    
    # Test 2: Switch to ChatGPT
    if not test_switch_to_chatgpt():
        return
    
    # Test 3: Get ChatGPT response
    if not test_chatgpt_response():
        return
    
    print("\n🎉 All tests passed! ChatGPT integration is working!")
    print("\n💡 You can now:")
    print("   - Switch between IBM Granite and ChatGPT in the interface")
    print("   - Get high-quality responses from OpenAI's ChatGPT")
    print("   - Compare responses from both AI providers")

if __name__ == "__main__":
    main()
