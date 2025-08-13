#!/usr/bin/env python3
"""
Test Gemini directly to see if it's working
"""

import requests
import json

def test_gemini_direct():
    """Test Gemini directly without fallbacks."""
    print("🧪 Testing Gemini Direct Response")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Start session
        session_response = requests.post(
            f"{base_url}/start",
            json={"name": "Direct Test", "role": "general"},
            timeout=10
        )
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session started: {session_id}")
        else:
            print(f"❌ Session failed: {session_response.status_code}")
            return False
        
        # Test simple message
        chat_response = requests.post(
            f"{base_url}/chat",
            json={
                "message": "What is budgeting?",
                "session_id": session_id
            },
            timeout=30
        )
        
        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            reply = chat_data.get("reply", "No reply")
            
            print(f"✅ Response received ({len(reply)} chars)")
            print(f"💬 Response: {reply[:300]}...")
            
            # Check if it's a fallback response
            if "[Switched" in reply:
                print("❌ FALLBACK DETECTED - This should be direct Gemini!")
                print("🔍 Checking why fallback occurred...")
                
                # Check rate limit status
                providers_response = requests.get(f"{base_url}/ai/providers")
                if providers_response.status_code == 200:
                    providers_data = providers_response.json()
                    if providers_data.get("success"):
                        providers = providers_data["data"]["available_providers"]
                        if "gemini" in providers:
                            gemini_info = providers["gemini"]
                            if "rate_limit_status" in gemini_info:
                                rate_status = gemini_info["rate_limit_status"]
                                print(f"📊 Rate Limit Status:")
                                print(f"   • Requests last minute: {rate_status['requests_last_minute']}/{rate_status['minute_limit']}")
                                print(f"   • Minute remaining: {rate_status['minute_remaining']}")
                                
                                if rate_status['minute_remaining'] > 0:
                                    print("⚠️ Rate limits are fine, but fallback still occurred!")
                                    print("🐛 This indicates a bug in the fallback logic")
                                else:
                                    print("✅ Fallback correctly triggered due to rate limits")
                
                return False
            else:
                print("✅ Direct Gemini response - no fallback!")
                return True
                
        else:
            print(f"❌ Chat failed: {chat_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gemini_direct()
