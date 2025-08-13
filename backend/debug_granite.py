#!/usr/bin/env python3
"""
Debug Granite Client
Test Granite client step by step to identify issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_granite_imports():
    """Test Granite client imports."""
    print("🔍 Testing Granite Imports")
    print("=" * 40)
    
    try:
        from granite_client import validate_config, granite_chat, initialize_local_model
        print("✅ Granite client imports successful")
        return True
    except Exception as e:
        print(f"❌ Granite import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_granite_config():
    """Test Granite configuration."""
    print("\n🔍 Testing Granite Configuration")
    print("=" * 40)
    
    try:
        from granite_client import validate_config
        
        config_valid = validate_config()
        print(f"Configuration valid: {config_valid}")
        
        # Check environment variables
        print(f"GRANITE_USE_LOCAL: {os.getenv('GRANITE_USE_LOCAL', 'true')}")
        print(f"GRANITE_MODEL_NAME: {os.getenv('GRANITE_MODEL_NAME', 'ibm-granite/granite-7b-instruct')}")
        print(f"GRANITE_DEVICE: {os.getenv('GRANITE_DEVICE', 'cpu')}")
        
        return config_valid
    except Exception as e:
        print(f"❌ Granite config error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_granite_model_init():
    """Test Granite model initialization."""
    print("\n🔍 Testing Granite Model Initialization")
    print("=" * 40)
    
    try:
        from granite_client import initialize_local_model
        
        print("Attempting to initialize local model...")
        init_success = initialize_local_model()
        print(f"Model initialization: {'✅ SUCCESS' if init_success else '❌ FAILED'}")
        
        return init_success
    except Exception as e:
        print(f"❌ Granite model init error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_granite_chat_direct():
    """Test Granite chat function directly."""
    print("\n🔍 Testing Granite Chat Direct")
    print("=" * 40)
    
    try:
        from granite_client import granite_chat
        
        # Test with simple message
        messages = [{"role": "user", "content": "What is compound interest?"}]
        
        print("Sending test message to Granite...")
        response = granite_chat(messages)
        
        print(f"Response received: {len(response)} characters")
        print(f"Response preview: {response[:200]}...")
        
        if response and len(response) > 50:
            print("✅ Granite chat working")
            return True
        else:
            print("⚠️ Granite chat gave short response")
            return False
            
    except Exception as e:
        print(f"❌ Granite chat error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_granite_local_function():
    """Test Granite local function specifically."""
    print("\n🔍 Testing Granite Local Function")
    print("=" * 40)
    
    try:
        from granite_client import granite_chat_local
        
        # Test with simple message
        messages = [{"role": "user", "content": "Hello, can you help with savings?"}]
        
        print("Testing granite_chat_local function...")
        response = granite_chat_local(messages)
        
        print(f"Local response: {len(response)} characters")
        print(f"Local response preview: {response[:200]}...")
        
        if "not available" in response.lower() or "error" in response.lower():
            print("❌ Local model not working properly")
            return False
        else:
            print("✅ Local model working")
            return True
            
    except Exception as e:
        print(f"❌ Granite local function error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_granite_via_ai_manager():
    """Test Granite via AI manager."""
    print("\n🔍 Testing Granite via AI Manager")
    print("=" * 40)
    
    try:
        from ai_provider_manager import get_ai_manager
        
        ai_manager = get_ai_manager()
        
        # Set provider to granite
        set_result = ai_manager.set_provider("granite")
        print(f"Set provider result: {set_result}")
        
        if set_result.get("success"):
            # Test generation
            messages = [{"role": "user", "content": "What are good savings strategies?"}]
            response = ai_manager.generate_response(messages)
            
            if response["success"]:
                print(f"✅ AI Manager Granite working: {len(response['response'])} chars")
                print(f"Provider used: {response.get('provider', 'unknown')}")
                print(f"Response preview: {response['response'][:200]}...")
                return True
            else:
                print(f"❌ AI Manager Granite failed: {response.get('error', 'unknown error')}")
                return False
        else:
            print(f"❌ Failed to set Granite provider: {set_result.get('message', 'unknown error')}")
            return False
        
    except Exception as e:
        print(f"❌ AI Manager test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive Granite debug."""
    print("🔧 GRANITE CLIENT DEBUG")
    print("=" * 60)
    
    # Test individual components
    imports_working = test_granite_imports()
    config_working = test_granite_config()
    model_init_working = test_granite_model_init()
    chat_working = test_granite_chat_direct()
    local_working = test_granite_local_function()
    ai_manager_working = test_granite_via_ai_manager()
    
    # Summary
    print("\n🎯 GRANITE DEBUG SUMMARY")
    print("=" * 60)
    
    print(f"📦 Imports: {'✅ WORKING' if imports_working else '❌ FAILED'}")
    print(f"⚙️ Configuration: {'✅ WORKING' if config_working else '❌ FAILED'}")
    print(f"🤖 Model Init: {'✅ WORKING' if model_init_working else '❌ FAILED'}")
    print(f"💬 Chat Function: {'✅ WORKING' if chat_working else '❌ FAILED'}")
    print(f"🏠 Local Function: {'✅ WORKING' if local_working else '❌ FAILED'}")
    print(f"🔄 AI Manager: {'✅ WORKING' if ai_manager_working else '❌ FAILED'}")
    
    overall_working = imports_working and config_working and chat_working
    
    print(f"\n🏆 OVERALL: {'✅ GRANITE WORKING' if overall_working else '❌ GRANITE NOT WORKING'}")
    
    if not overall_working:
        print("\n🔧 TROUBLESHOOTING SUGGESTIONS:")
        if not imports_working:
            print("   • Check granite_client.py file exists and is valid")
        if not config_working:
            print("   • Check environment variables in .env file")
        if not model_init_working:
            print("   • Check transformers and torch installation")
        if not chat_working:
            print("   • Check granite_chat function implementation")
        if not local_working:
            print("   • Check granite_chat_local function")
        if not ai_manager_working:
            print("   • Check AI manager integration")
    
    return overall_working

if __name__ == "__main__":
    main()
