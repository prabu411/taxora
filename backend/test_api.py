import requests
import json

def test_chat_api():
    """Test the chat API with the lightweight AI model."""
    
    print("🧪 Testing Taxora Chat API with Lightweight AI")
    print("=" * 50)
    
    # Test data
    test_messages = [
        "I have $500 to invest. What should I do?",
        "How can I create a budget as a student?",
        "What's the best way to save for an emergency fund?",
        "Should I pay off debt or invest first?"
    ]
    
    base_url = "http://127.0.0.1:8000"

    # First, start a session
    print("🚀 Starting new session...")
    try:
        start_response = requests.post(
            f"{base_url}/start",
            json={
                "name": "Test User",
                "role": "general"
            }
        )

        if start_response.status_code == 200:
            session_data = start_response.json()
            session_id = session_data.get("session_id")
            print(f"✅ Session started: {session_id}")
        else:
            print(f"❌ Failed to start session: {start_response.text}")
            return

    except Exception as e:
        print(f"❌ Error starting session: {e}")
        return

    for i, message in enumerate(test_messages, 1):
        print(f"\n🔄 Test {i}/4")
        print(f"👤 User: {message}")
        
        try:
            # Send chat request
            response = requests.post(
                f"{base_url}/chat",
                json={
                    "message": message,
                    "session_id": session_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "No response")
                print(f"🤖 AI: {ai_response}")
                print(f"✅ Response time: {response.elapsed.total_seconds():.2f}s")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ Request timed out")
        except requests.exceptions.ConnectionError:
            print("🔌 Connection error - is the server running?")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*50}")
    print("🎉 API Test Complete!")

if __name__ == "__main__":
    test_chat_api()
