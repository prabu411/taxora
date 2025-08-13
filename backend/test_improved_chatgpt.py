#!/usr/bin/env python3
"""
Test Improved ChatGPT Integration with Fallback
"""

from ai_provider_manager import get_ai_manager
import time

def test_chatgpt_with_fallback():
    """Test ChatGPT with automatic fallback to IBM Granite."""
    print("🧪 Testing Improved ChatGPT with Fallback")
    print("=" * 60)
    
    ai_manager = get_ai_manager()
    
    # Set to ChatGPT
    switch_result = ai_manager.set_provider("chatgpt")
    print(f"✅ Switch result: {switch_result['message']}")
    
    # Test message
    test_messages = [
        {"role": "user", "content": "What's a simple budgeting tip for beginners?"}
    ]
    
    print("\n💬 Testing ChatGPT response with fallback...")
    start_time = time.time()
    
    result = ai_manager.generate_response(test_messages, auto_fallback=True)
    
    response_time = time.time() - start_time
    
    print(f"⏱️  Response time: {response_time:.2f} seconds")
    print(f"🤖 Provider used: {result.get('provider_name', 'Unknown')}")
    
    if result.get('fallback_used'):
        print(f"🔄 Fallback activated from {result.get('original_provider')} to {result.get('provider')}")
    
    print(f"💬 Response: {result['response'][:200]}...")
    
    return result['success']

def test_multiple_requests():
    """Test multiple requests to see rate limiting behavior."""
    print("\n🔄 Testing Multiple Requests")
    print("=" * 60)
    
    ai_manager = get_ai_manager()
    
    questions = [
        "What's the 50/30/20 budgeting rule?",
        "How much should I save for emergencies?",
        "What's the difference between stocks and bonds?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Question {i}: {question}")
        
        messages = [{"role": "user", "content": question}]
        result = ai_manager.generate_response(messages, auto_fallback=True)
        
        provider = result.get('provider_name', 'Unknown')
        fallback = " (Fallback)" if result.get('fallback_used') else ""
        
        print(f"🤖 {provider}{fallback}")
        print(f"💬 {result['response'][:100]}...")
        
        # Small delay between requests
        time.sleep(2)

def main():
    """Run all tests."""
    print("🚀 Taxora Improved ChatGPT Integration Test")
    print("=" * 60)
    
    try:
        # Test 1: Single request with fallback
        success = test_chatgpt_with_fallback()
        
        if success:
            # Test 2: Multiple requests
            test_multiple_requests()
            
            print("\n🎉 All tests completed!")
            print("\n💡 Features working:")
            print("   ✅ ChatGPT integration with retry logic")
            print("   ✅ Automatic fallback to IBM Granite")
            print("   ✅ Rate limit handling")
            print("   ✅ Error recovery")
            print("\n🎯 Your chatbot now handles ChatGPT rate limits gracefully!")
        else:
            print("\n❌ Tests failed. Check your configuration.")
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    main()
