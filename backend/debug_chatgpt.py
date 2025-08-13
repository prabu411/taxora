#!/usr/bin/env python3
"""
Debug ChatGPT API Issues
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_openai_api_directly():
    """Test OpenAI API directly with minimal request."""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"🔑 API Key: {api_key[:20]}...")
    
    # Test with minimal request
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Very simple test payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    print("🧪 Testing OpenAI API directly...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"💬 Response: {data['choices'][0]['message']['content']}")
            return True
        else:
            print("❌ Error Response:")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_api_quota():
    """Check API usage and limits."""
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Try to get usage info
    url = "https://api.openai.com/v1/usage"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"📊 Usage API Status: {response.status_code}")
        if response.status_code == 200:
            print(f"📈 Usage Data: {response.json()}")
        else:
            print(f"⚠️  Usage check failed: {response.text}")
    except Exception as e:
        print(f"⚠️  Could not check usage: {e}")

def test_different_models():
    """Test different OpenAI models."""
    api_key = os.getenv('OPENAI_API_KEY')
    
    models_to_test = [
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0125",
        "gpt-4o-mini"
    ]
    
    for model in models_to_test:
        print(f"\n🧪 Testing model: {model}")
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 10
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ {model} works!")
                return model
            else:
                print(f"   ❌ {model} failed: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ {model} error: {e}")
    
    return None

def main():
    """Run all diagnostics."""
    print("🔍 ChatGPT API Diagnostics")
    print("=" * 50)
    
    # Test 1: Direct API call
    print("\n1️⃣ Testing Direct API Call")
    success = test_openai_api_directly()
    
    if not success:
        print("\n2️⃣ Checking API Quota")
        check_api_quota()
        
        print("\n3️⃣ Testing Different Models")
        working_model = test_different_models()
        
        if working_model:
            print(f"\n✅ Found working model: {working_model}")
        else:
            print("\n❌ No models working - likely API key issue")
    else:
        print("\n✅ ChatGPT API is working correctly!")

if __name__ == "__main__":
    main()
