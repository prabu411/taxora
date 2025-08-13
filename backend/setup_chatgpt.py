#!/usr/bin/env python3
"""
ChatGPT Setup Script for Taxora
Helps configure OpenAI API key for ChatGPT integration.
"""

import os
import re

def setup_chatgpt():
    """Interactive setup for ChatGPT integration."""
    
    print("🤖 Taxora ChatGPT Setup")
    print("=" * 50)
    print()
    
    # Check current status
    env_file = ".env"
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        return
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Check if API key is already configured
    if 'OPENAI_API_KEY=' in content and not 'your_openai_api_key_here' in content:
        print("✅ ChatGPT appears to be already configured!")
        print("   If you're having issues, you may need to update your API key.")
        print()
    
    print("📋 To enable ChatGPT, you need an OpenAI API key:")
    print()
    print("1. 🌐 Visit: https://platform.openai.com/api-keys")
    print("2. 📝 Sign up for a free OpenAI account")
    print("3. 🔑 Click 'Create new secret key'")
    print("4. 📋 Copy the API key (starts with 'sk-')")
    print()
    
    # Get API key from user
    api_key = input("🔑 Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⏭️  Skipped ChatGPT setup. You can run this script again later.")
        return
    
    # Validate API key format
    if not api_key.startswith('sk-') or len(api_key) < 20:
        print("❌ Invalid API key format. OpenAI keys start with 'sk-' and are longer.")
        return
    
    # Update .env file
    try:
        # Replace the API key line
        new_content = re.sub(
            r'#?\s*OPENAI_API_KEY=.*',
            f'OPENAI_API_KEY={api_key}',
            content
        )
        
        with open(env_file, 'w') as f:
            f.write(new_content)
        
        print("✅ ChatGPT configured successfully!")
        print()
        print("🚀 Next steps:")
        print("1. Restart your Taxora server")
        print("2. Refresh the chat interface")
        print("3. Switch to ChatGPT in the AI provider dropdown")
        print()
        print("💡 Your first few API calls are free, then it's pay-per-use.")
        print("   Typical cost: $0.001-0.002 per message")
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")

def test_chatgpt():
    """Test ChatGPT configuration."""
    print("🧪 Testing ChatGPT Configuration")
    print("=" * 50)
    
    try:
        from chatgpt_client import test_chatgpt_connection
        
        result = test_chatgpt_connection()
        
        if result["status"] == "success":
            print("✅ ChatGPT is working correctly!")
            print(f"   Message: {result['message']}")
        else:
            print("❌ ChatGPT test failed:")
            print(f"   Error: {result['message']}")
            
            if "API key" in result["message"]:
                print()
                print("💡 Solution: Run this script again to configure your API key")
                
    except ImportError:
        print("❌ ChatGPT client not available. Please check your installation.")
    except Exception as e:
        print(f"❌ Test error: {e}")

def main():
    """Main setup function."""
    print("🤖 Taxora ChatGPT Setup & Test Tool")
    print("=" * 50)
    print()
    print("Choose an option:")
    print("1. 🔧 Setup ChatGPT API key")
    print("2. 🧪 Test ChatGPT connection")
    print("3. ❌ Exit")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        setup_chatgpt()
    elif choice == "2":
        test_chatgpt()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
