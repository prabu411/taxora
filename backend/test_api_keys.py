#!/usr/bin/env python3
"""
Test API Keys Configuration
Verify that all API keys are properly loaded and working
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API with the new key."""
    print("🔍 Testing Gemini API")
    print("=" * 40)
    
    api_key = os.getenv("GEMINI_API_KEY")
    backup_key = os.getenv("GEMINI_API_KEY_BACKUP")
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    print(f"Primary API Key: {api_key[:20]}..." if api_key else "Primary API Key: Not found")
    print(f"Backup API Key: {backup_key[:20]}..." if backup_key else "Backup API Key: Not found")
    print(f"Model: {model}")
    
    if not api_key:
        print("❌ No Gemini API key found")
        return False
    
    # Test API call
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello, can you help with financial advice?"
            }]
        }]
    }
    
    try:
        print("🔄 Testing primary API key...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"✅ Primary Gemini API working!")
                print(f"Response preview: {content[:100]}...")
                return True
            else:
                print("❌ Invalid response format from Gemini")
                return False
        elif response.status_code == 400:
            print(f"❌ Bad request to Gemini API: {response.text}")
            
            # Try backup key if available
            if backup_key:
                print("🔄 Testing backup API key...")
                headers["X-goog-api-key"] = backup_key
                backup_response = requests.post(url, headers=headers, json=payload, timeout=30)
                
                if backup_response.status_code == 200:
                    data = backup_response.json()
                    if "candidates" in data and len(data["candidates"]) > 0:
                        content = data["candidates"][0]["content"]["parts"][0]["text"]
                        print(f"✅ Backup Gemini API working!")
                        print(f"Response preview: {content[:100]}...")
                        return True
                else:
                    print(f"❌ Backup key also failed: {backup_response.status_code}")
            
            return False
        else:
            print(f"❌ Gemini API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test error: {e}")
        return False

def test_openrouter_api():
    """Test OpenRouter API."""
    print("\n🔍 Testing OpenRouter API")
    print("=" * 40)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "mistralai/mixtral-8x7b-instruct")
    
    print(f"API Key: {api_key[:20]}..." if api_key else "API Key: Not found")
    print(f"Model: {model}")
    
    if not api_key:
        print("❌ No OpenRouter API key found")
        return False
    
    # Test API call
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Hello, can you help with financial advice?"}
        ],
        "max_tokens": 100
    }
    
    try:
        print("🔄 Testing OpenRouter API...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                print(f"✅ OpenRouter API working!")
                print(f"Response preview: {content[:100]}...")
                return True
            else:
                print("❌ Invalid response format from OpenRouter")
                return False
        elif response.status_code == 401:
            print(f"❌ OpenRouter authentication failed - invalid API key")
            return False
        else:
            print(f"❌ OpenRouter API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OpenRouter API test error: {e}")
        return False

def test_environment_loading():
    """Test environment variable loading."""
    print("\n🔍 Testing Environment Variables")
    print("=" * 40)
    
    env_vars = [
        "GEMINI_API_KEY",
        "GEMINI_API_KEY_BACKUP", 
        "GEMINI_MODEL",
        "OPENROUTER_API_KEY",
        "OPENROUTER_MODEL"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if "API_KEY" in var:
                print(f"✅ {var}: {value[:20]}...")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not found")

def main():
    """Run comprehensive API key tests."""
    print("🔑 API KEYS CONFIGURATION TEST")
    print("=" * 60)
    
    # Test environment loading
    test_environment_loading()
    
    # Test Gemini API
    gemini_working = test_gemini_api()
    
    # Test OpenRouter API
    openrouter_working = test_openrouter_api()
    
    # Summary
    print("\n🎉 API KEYS TEST SUMMARY")
    print("=" * 60)
    
    print(f"🔍 Gemini API: {'✅ WORKING' if gemini_working else '❌ NOT WORKING'}")
    print(f"🔍 OpenRouter API: {'✅ WORKING' if openrouter_working else '❌ NOT WORKING'}")
    
    if gemini_working or openrouter_working:
        print("\n🎉 SUCCESS!")
        print("At least one AI provider is working correctly!")
        
        if gemini_working:
            print("✅ Gemini API is ready for use")
        if openrouter_working:
            print("✅ OpenRouter API is ready for use")
            
        print("\n🚀 Your Taxora AI system is ready!")
    else:
        print("\n⚠️ NO WORKING AI PROVIDERS")
        print("Please check your API keys and try again")
    
    return gemini_working or openrouter_working

if __name__ == "__main__":
    main()
