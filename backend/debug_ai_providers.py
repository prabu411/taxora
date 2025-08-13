#!/usr/bin/env python3
"""
Debug AI Providers
Test each provider individually to identify issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_direct():
    """Test Gemini directly."""
    print("🔍 Testing Gemini Direct")
    print("=" * 40)
    
    try:
        from gemini_client import gemini_generate_response, validate_gemini_config
        
        # Check configuration
        config_valid = validate_gemini_config()
        print(f"Configuration valid: {config_valid}")
        
        if config_valid:
            # Test with simple message
            messages = [{"role": "user", "content": "What is compound interest?"}]
            
            print("Sending test message...")
            response = gemini_generate_response(messages)
            
            print(f"Response received: {len(response)} characters")
            print(f"Response preview: {response[:200]}...")
            
            return True
        else:
            print("❌ Gemini configuration invalid")
            return False
            
    except Exception as e:
        print(f"❌ Gemini test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_openrouter_direct():
    """Test OpenRouter directly."""
    print("\n🔍 Testing OpenRouter Direct")
    print("=" * 40)
    
    try:
        from openrouter_client import openrouter_generate_response, validate_openrouter_config
        
        # Check configuration
        config_valid = validate_openrouter_config()
        print(f"Configuration valid: {config_valid}")
        
        if config_valid:
            # Test with simple message
            messages = [{"role": "user", "content": "What is compound interest?"}]
            
            print("Sending test message...")
            response = openrouter_generate_response(messages)
            
            print(f"Response received: {len(response)} characters")
            print(f"Response preview: {response[:200]}...")
            
            return True
        else:
            print("❌ OpenRouter configuration invalid")
            return False
            
    except Exception as e:
        print(f"❌ OpenRouter test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_manager():
    """Test AI manager."""
    print("\n🔍 Testing AI Manager")
    print("=" * 40)
    
    try:
        from ai_provider_manager import get_ai_manager
        
        ai_manager = get_ai_manager()
        
        # Test provider detection
        providers = ai_manager.get_available_providers()
        print(f"Available providers: {list(providers['data']['available_providers'].keys())}")
        
        # Test with Gemini
        print("\nTesting with Gemini...")
        ai_manager.set_provider("gemini")
        
        messages = [{"role": "user", "content": "What is compound interest?"}]
        response = ai_manager.generate_response(messages)
        
        if response["success"]:
            print(f"✅ AI Manager Gemini working: {len(response['response'])} chars")
            print(f"Provider used: {response.get('provider', 'unknown')}")
            print(f"Response preview: {response['response'][:200]}...")
        else:
            print(f"❌ AI Manager Gemini failed: {response.get('error', 'unknown error')}")
        
        # Test with OpenRouter
        print("\nTesting with OpenRouter...")
        ai_manager.set_provider("openrouter")
        
        response2 = ai_manager.generate_response(messages)
        
        if response2["success"]:
            print(f"✅ AI Manager OpenRouter working: {len(response2['response'])} chars")
            print(f"Provider used: {response2.get('provider', 'unknown')}")
        else:
            print(f"❌ AI Manager OpenRouter failed: {response2.get('error', 'unknown error')}")
            print(f"Fallback provider: {response2.get('fallback_provider', 'none')}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Manager test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_endpoint():
    """Test chat endpoint."""
    print("\n🔍 Testing Chat Endpoint")
    print("=" * 40)
    
    try:
        import requests
        
        # Start session
        session_response = requests.post(
            "http://127.0.0.1:8000/start",
            json={"name": "Debug User", "role": "general"},
            timeout=10
        )
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session created: {session_id}")
            
            # Test chat with Gemini
            print("Testing chat with Gemini...")
            chat_response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "message": "What is compound interest?",
                    "session_id": session_id,
                    "provider": "gemini"
                },
                timeout=30
            )
            
            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                print(f"✅ Chat response: {len(chat_data.get('reply', ''))} chars")
                print(f"Provider: {chat_data.get('provider', 'unknown')}")
                print(f"Preview: {chat_data.get('reply', '')[:200]}...")
            else:
                print(f"❌ Chat failed: {chat_response.status_code}")
                print(f"Error: {chat_response.text}")
            
            return True
        else:
            print(f"❌ Session creation failed: {session_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat endpoint test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run debug tests."""
    print("🐛 AI PROVIDERS DEBUG")
    print("=" * 60)
    
    # Test individual components
    gemini_working = test_gemini_direct()
    openrouter_working = test_openrouter_direct()
    ai_manager_working = test_ai_manager()
    chat_working = test_chat_endpoint()
    
    # Summary
    print("\n🎯 DEBUG SUMMARY")
    print("=" * 60)
    
    print(f"🎯 Gemini Direct: {'✅ WORKING' if gemini_working else '❌ FAILED'}")
    print(f"🚀 OpenRouter Direct: {'✅ WORKING' if openrouter_working else '❌ FAILED'}")
    print(f"🤖 AI Manager: {'✅ WORKING' if ai_manager_working else '❌ FAILED'}")
    print(f"💬 Chat Endpoint: {'✅ WORKING' if chat_working else '❌ FAILED'}")
    
    if gemini_working:
        print("\n✅ Gemini is working - issue might be in AI manager or chat endpoint")
    
    if not openrouter_working:
        print("\n⚠️ OpenRouter needs credits - add credits at https://openrouter.ai/settings/credits")
    
    return gemini_working or openrouter_working

if __name__ == "__main__":
    main()
