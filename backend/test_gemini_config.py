#!/usr/bin/env python3
"""
Test Gemini configuration directly
"""

import os
from dotenv import load_dotenv
from gemini_client import validate_gemini_config, gemini_generate_response

def test_gemini_config():
    """Test Gemini configuration."""
    print("🔧 Testing Gemini Configuration")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    else:
        print("❌ No API key found")
        return False
    
    # Check configuration
    if validate_gemini_config():
        print("✅ Gemini configuration valid")
    else:
        print("❌ Gemini configuration invalid")
        return False
    
    # Test simple request
    try:
        print("\n🧪 Testing simple Gemini request...")
        messages = [{"role": "user", "content": "Hello, what is 2+2?"}]
        response = gemini_generate_response(messages)
        
        print(f"✅ Response: {response[:100]}...")
        
        if "error" in response.lower() or "unexpected" in response.lower():
            print("⚠️ Response indicates an error")
            return False
        else:
            print("✅ Gemini working correctly!")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gemini_config()
