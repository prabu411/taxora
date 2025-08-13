import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from granite_client import granite_chat

def test_granite_direct():
    """Test the granite_client directly."""
    
    print("🧪 Testing Granite Client Directly")
    print("=" * 50)
    
    # Test messages
    test_messages = [
        [{"role": "user", "content": "I have $500 to invest. What should I do?"}],
        [{"role": "user", "content": "How can I create a budget as a student?"}],
        [{"role": "user", "content": "What's the best way to save for an emergency fund?"}]
    ]
    
    for i, messages in enumerate(test_messages, 1):
        print(f"\n🔄 Test {i}/3")
        print(f"👤 User: {messages[0]['content']}")
        
        try:
            response = granite_chat(messages)
            print(f"🤖 AI: {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*50}")
    print("🎉 Direct Test Complete!")

if __name__ == "__main__":
    test_granite_direct()
