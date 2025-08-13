#!/usr/bin/env python3
"""
Test New AI Providers Integration
Tests Claude, Grok, and Perplexity integration with Taxora
"""

import requests
import json
import time

def test_ai_providers_endpoint():
    """Test that new AI providers are detected."""
    print("🔍 Testing AI Providers Detection")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        response = requests.get(f"{base_url}/ai/providers", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                providers = data["data"]["available_providers"]
                
                print(f"✅ Available providers: {list(providers.keys())}")
                
                # Check for new providers
                expected_providers = ["granite", "gemini", "claude", "grok", "perplexity"]
                found_providers = []
                
                for provider in expected_providers:
                    if provider in providers:
                        status = providers[provider]["status"]
                        print(f"   • {provider}: {status}")
                        found_providers.append(provider)
                    else:
                        print(f"   • {provider}: NOT FOUND")
                
                return found_providers
            else:
                print("❌ Providers data invalid")
                return []
        else:
            print(f"❌ Providers check failed: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def test_provider_switching():
    """Test switching between different AI providers."""
    print("\n🔄 Testing Provider Switching")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # Get available providers first
    try:
        providers_response = requests.get(f"{base_url}/ai/providers")
        if providers_response.status_code != 200:
            print("❌ Could not get providers list")
            return False
        
        providers_data = providers_response.json()
        available_providers = providers_data["data"]["available_providers"]
        
        # Test switching to each available provider
        test_results = {}
        
        for provider_id, provider_info in available_providers.items():
            if provider_info["status"] == "available":
                print(f"\n🧪 Testing {provider_info['name']} ({provider_id})")
                
                # Switch to provider
                switch_response = requests.post(
                    f"{base_url}/ai/provider",
                    json={"provider": provider_id},
                    timeout=10
                )
                
                if switch_response.status_code == 200:
                    switch_data = switch_response.json()
                    if switch_data.get("success"):
                        print(f"✅ Successfully switched to {provider_info['name']}")
                        
                        # Test a simple chat
                        session_response = requests.post(
                            f"{base_url}/start",
                            json={"name": f"Test {provider_id}", "role": "general"},
                            timeout=10
                        )
                        
                        if session_response.status_code == 200:
                            session_data = session_response.json()
                            session_id = session_data["session_id"]
                            
                            # Test chat with this provider
                            chat_response = requests.post(
                                f"{base_url}/chat",
                                json={
                                    "message": "What is compound interest?",
                                    "session_id": session_id
                                },
                                timeout=30
                            )
                            
                            if chat_response.status_code == 200:
                                chat_data = chat_response.json()
                                reply = chat_data.get("reply", "")
                                
                                if reply and len(reply) > 50:
                                    print(f"✅ {provider_info['name']} response: {len(reply)} chars")
                                    print(f"💬 Preview: {reply[:100]}...")
                                    test_results[provider_id] = "✅ WORKING"
                                else:
                                    print(f"⚠️ {provider_info['name']} gave short response")
                                    test_results[provider_id] = "⚠️ SHORT RESPONSE"
                            else:
                                print(f"❌ {provider_info['name']} chat failed: {chat_response.status_code}")
                                test_results[provider_id] = "❌ CHAT FAILED"
                        else:
                            print(f"❌ Session creation failed for {provider_info['name']}")
                            test_results[provider_id] = "❌ SESSION FAILED"
                    else:
                        print(f"❌ Switch to {provider_info['name']} failed")
                        test_results[provider_id] = "❌ SWITCH FAILED"
                else:
                    print(f"❌ Switch request failed for {provider_info['name']}: {switch_response.status_code}")
                    test_results[provider_id] = "❌ REQUEST FAILED"
            else:
                print(f"⚠️ {provider_info['name']} not available: {provider_info['status']}")
                test_results[provider_id] = f"⚠️ {provider_info['status'].upper()}"
        
        return test_results
        
    except Exception as e:
        print(f"❌ Provider switching test error: {e}")
        return {}

def test_api_key_configuration():
    """Test API key configuration for new providers."""
    print("\n🔑 Testing API Key Configuration")
    print("=" * 50)
    
    # Test individual client configurations
    clients_to_test = [
        ("claude_client", "Claude"),
        ("grok_client", "Grok"),
        ("perplexity_client", "Perplexity")
    ]
    
    config_results = {}
    
    for client_module, provider_name in clients_to_test:
        try:
            print(f"\n🧪 Testing {provider_name} Configuration")
            
            # Import and test the client
            if client_module == "claude_client":
                from claude_client import validate_claude_config
                is_configured = validate_claude_config()
            elif client_module == "grok_client":
                from grok_client import validate_grok_config
                is_configured = validate_grok_config()
            elif client_module == "perplexity_client":
                from perplexity_client import validate_perplexity_config
                is_configured = validate_perplexity_config()
            
            if is_configured:
                print(f"✅ {provider_name} is properly configured")
                config_results[provider_name] = "✅ CONFIGURED"
            else:
                print(f"⚠️ {provider_name} is not configured (API key needed)")
                config_results[provider_name] = "⚠️ NOT CONFIGURED"
                
        except Exception as e:
            print(f"❌ {provider_name} configuration test failed: {e}")
            config_results[provider_name] = f"❌ ERROR: {str(e)}"
    
    return config_results

def main():
    """Run comprehensive test of new AI providers."""
    print("🤖 NEW AI PROVIDERS INTEGRATION TEST")
    print("=" * 70)
    
    start_time = time.time()
    
    # Test 1: Provider detection
    found_providers = test_ai_providers_endpoint()
    
    # Test 2: API key configuration
    config_results = test_api_key_configuration()
    
    # Test 3: Provider switching and functionality
    switching_results = test_provider_switching()
    
    # Summary
    print("\n🎉 NEW AI PROVIDERS TEST SUMMARY")
    print("=" * 70)
    
    print(f"\n🔍 Provider Detection:")
    expected_providers = ["granite", "gemini", "claude", "grok", "perplexity"]
    for provider in expected_providers:
        if provider in found_providers:
            print(f"   ✅ {provider.title()}: Detected")
        else:
            print(f"   ❌ {provider.title()}: Not detected")
    
    print(f"\n🔑 Configuration Status:")
    for provider, status in config_results.items():
        print(f"   {provider}: {status}")
    
    print(f"\n🔄 Provider Functionality:")
    for provider, status in switching_results.items():
        print(f"   {provider.title()}: {status}")
    
    # Overall assessment
    total_providers = len(expected_providers)
    detected_providers = len(found_providers)
    working_providers = len([r for r in switching_results.values() if "✅" in r])
    
    print(f"\n📊 Overall Results:")
    print(f"   • Providers Detected: {detected_providers}/{total_providers}")
    print(f"   • Providers Working: {working_providers}/{len(switching_results)}")
    
    elapsed_time = time.time() - start_time
    print(f"⏱️ Test Duration: {elapsed_time:.2f} seconds")
    
    if detected_providers == total_providers:
        print("\n🎉 SUCCESS!")
        print("All new AI providers have been successfully integrated!")
        print("\n🌟 Your Taxora now supports:")
        print("   ✅ IBM Granite - Fast, lightweight responses")
        print("   ✅ Google Gemini - Advanced reasoning with voice")
        print("   ✅ Anthropic Claude - Thoughtful, analytical responses")
        print("   ✅ xAI Grok - Witty insights with real-time data")
        print("   ✅ Perplexity AI - Real-time information with citations")
        
        print("\n🔑 To activate additional providers:")
        print("   1. Get API keys from the respective providers")
        print("   2. Update your .env file with the API keys")
        print("   3. Restart the server")
        print("   4. Switch providers using the chat interface")
        
    else:
        print("\n⚠️ Integration partially complete")
        print("Some providers may need additional configuration")
    
    return detected_providers == total_providers

if __name__ == "__main__":
    main()
