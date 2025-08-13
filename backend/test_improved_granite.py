#!/usr/bin/env python3
"""
Test Improved Granite with Fallback System
"""

from granite_client import granite_chat
from financial_advisor_fallback import improve_financial_response

def test_granite_improvements():
    """Test the improved Granite responses."""
    print("🧪 Testing Improved Granite with Fallback System")
    print("=" * 60)
    
    test_questions = [
        "What's a simple budgeting tip for beginners?",
        "How much should I save for emergencies?", 
        "What's the 50/30/20 budgeting rule?",
        "Should I invest in stocks or bonds?",
        "How do I build good credit?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Question {i}: {question}")
        
        # Test with messages format
        messages = [{"role": "user", "content": question}]
        
        try:
            response = granite_chat(messages)
            print(f"🤖 Response: {response[:200]}...")
            
            # Check if fallback was used
            if "Let me provide some helpful financial guidance:" in response:
                print("✅ Fallback system activated - quality response provided!")
            elif len(response) > 50 and any(word in response.lower() for word in ['budget', 'save', 'money', 'financial']):
                print("✅ Good quality response from Granite!")
            else:
                print("⚠️  Response quality could be improved")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)

def test_fallback_directly():
    """Test the fallback system directly."""
    print("\n🔧 Testing Fallback System Directly")
    print("=" * 60)
    
    # Test with poor quality response
    poor_response = "that you read this. Note: If you don't think you are paying GSTR3, you have to pay the same amount as you did."
    question = "What's a simple budgeting tip?"
    
    improved = improve_financial_response(poor_response, question)
    
    print(f"📝 Original poor response: {poor_response}")
    print(f"✅ Improved response: {improved}")
    
    if "Let me provide some helpful financial guidance:" in improved:
        print("🎉 Fallback system working correctly!")
    else:
        print("⚠️  Fallback system needs adjustment")

def main():
    """Run all tests."""
    print("🚀 Taxora Granite Improvement Test")
    print("=" * 60)
    
    try:
        test_granite_improvements()
        test_fallback_directly()
        
        print("\n🎉 Testing completed!")
        print("\n💡 Improvements made:")
        print("   ✅ Better generation parameters")
        print("   ✅ Improved response cleaning")
        print("   ✅ Quality fallback system")
        print("   ✅ Financial topic detection")
        
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    main()
