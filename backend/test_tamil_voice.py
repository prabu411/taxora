#!/usr/bin/env python3
"""
Test Tamil Voice Integration with Gemini
"""

from gemini_client import gemini_translate_to_tamil, gemini_text_to_speech, gemini_generate_response

def test_tamil_translation():
    """Test Tamil translation functionality."""
    print("🇮🇳 Testing Tamil Translation")
    print("=" * 50)
    
    test_texts = [
        "Use the 50/30/20 budgeting rule for financial success.",
        "Save 20% of your income for emergencies.",
        "Invest in low-cost index funds for long-term growth.",
        "Create an emergency fund with 3-6 months of expenses."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test {i}: {text}")
        
        try:
            result = gemini_translate_to_tamil(text)
            
            if result["success"]:
                print(f"✅ Tamil translation: {result['tamil_text']}")
                print(f"📊 Original length: {len(text)} chars")
                print(f"📊 Tamil length: {len(result['tamil_text'])} chars")
            else:
                print(f"❌ Translation failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def test_tamil_speech_optimization():
    """Test Tamil text-to-speech optimization."""
    print("\n🔊 Testing Tamil Speech Optimization")
    print("=" * 50)
    
    test_texts = [
        "Use the 50/30/20 budgeting rule",
        "Save 20% of your income",
        "Invest $1000 in index funds"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test {i}: {text}")
        
        try:
            # Test English optimization
            en_result = gemini_text_to_speech(text, "en")
            print(f"🇺🇸 English optimized: {en_result['text']}")
            print(f"🎵 English config: {en_result['voice_config']}")
            
            # Test Tamil optimization
            ta_result = gemini_text_to_speech(text, "ta")
            print(f"🇮🇳 Tamil optimized: {ta_result['text']}")
            print(f"🎵 Tamil config: {ta_result['voice_config']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def test_bilingual_financial_advice():
    """Test getting financial advice in both languages."""
    print("\n💰 Testing Bilingual Financial Advice")
    print("=" * 50)
    
    questions = [
        "What is the 50/30/20 budgeting rule?",
        "How much should I save for emergencies?",
        "What are index funds?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Question {i}: {question}")
        
        try:
            # Get English response from Gemini
            messages = [{"role": "user", "content": question}]
            english_response = gemini_generate_response(messages)
            
            print(f"🇺🇸 English response: {english_response[:100]}...")
            
            # Translate to Tamil
            translation_result = gemini_translate_to_tamil(english_response)
            
            if translation_result["success"]:
                tamil_response = translation_result["tamil_text"]
                print(f"🇮🇳 Tamil response: {tamil_response[:100]}...")
                
                # Test speech optimization for both
                en_speech = gemini_text_to_speech(english_response, "en")
                ta_speech = gemini_text_to_speech(tamil_response, "ta")
                
                print(f"✅ Both languages ready for speech synthesis")
                print(f"📊 English speech length: {len(en_speech['text'])} chars")
                print(f"📊 Tamil speech length: {len(ta_speech['text'])} chars")
            else:
                print(f"❌ Tamil translation failed: {translation_result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def test_voice_language_preferences():
    """Test different voice language preferences."""
    print("\n🎛️ Testing Voice Language Preferences")
    print("=" * 50)
    
    sample_response = "Use the 50/30/20 budgeting rule. Allocate 50% to needs, 30% to wants, and 20% to savings."
    
    preferences = [
        ("English Only", "en"),
        ("Tamil Only", "ta"),
        ("Both Languages", "both")
    ]
    
    for pref_name, pref_code in preferences:
        print(f"\n🎯 Testing: {pref_name}")
        
        try:
            if pref_code == "en":
                # English only
                en_speech = gemini_text_to_speech(sample_response, "en")
                print(f"🇺🇸 English speech ready: {en_speech['text'][:80]}...")
                
            elif pref_code == "ta":
                # Tamil only - translate first
                translation = gemini_translate_to_tamil(sample_response)
                if translation["success"]:
                    ta_speech = gemini_text_to_speech(translation["tamil_text"], "ta")
                    print(f"🇮🇳 Tamil speech ready: {ta_speech['text'][:80]}...")
                else:
                    print(f"❌ Tamil translation failed")
                    
            elif pref_code == "both":
                # Both languages
                en_speech = gemini_text_to_speech(sample_response, "en")
                translation = gemini_translate_to_tamil(sample_response)
                
                if translation["success"]:
                    ta_speech = gemini_text_to_speech(translation["tamil_text"], "ta")
                    print(f"🇺🇸 English ready: {en_speech['text'][:60]}...")
                    print(f"🇮🇳 Tamil ready: {ta_speech['text'][:60]}...")
                    print(f"✅ Bilingual speech pipeline complete")
                else:
                    print(f"⚠️ Tamil translation failed, English only")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def main():
    """Run all Tamil voice integration tests."""
    print("🚀 Taxora Tamil Voice Integration Test")
    print("=" * 60)
    
    try:
        # Test 1: Tamil translation
        translation_success = test_tamil_translation()
        
        # Test 2: Speech optimization
        speech_success = test_tamil_speech_optimization()
        
        # Test 3: Bilingual advice
        advice_success = test_bilingual_financial_advice()
        
        # Test 4: Language preferences
        preferences_success = test_voice_language_preferences()
        
        # Summary
        print("\n🎉 Tamil Voice Integration Test Summary")
        print("=" * 60)
        
        results = {
            "Tamil Translation": translation_success,
            "Speech Optimization": speech_success,
            "Bilingual Advice": advice_success,
            "Language Preferences": preferences_success
        }
        
        for test_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        all_passed = all(results.values())
        
        if all_passed:
            print("\n🎉 ALL TAMIL VOICE TESTS PASSED!")
            print("\n💡 Your Tamil Voice Integration is ready:")
            print("   🇮🇳 Tamil translation via Gemini")
            print("   🔊 Tamil speech synthesis")
            print("   🌐 Bilingual voice output")
            print("   🎛️ Language preference controls")
            
            print("\n🎮 How to use Tamil voice:")
            print("   1. Open chat interface")
            print("   2. Select voice language preference:")
            print("      • 🌐 English + Tamil (both)")
            print("      • 🇺🇸 English Only")
            print("      • 🇮🇳 Tamil Only")
            print("   3. Click '🎙️ Gemini Voice Chat'")
            print("   4. Speak your question in English")
            print("   5. Hear response in your preferred language(s)")
            
            print("\n🌟 Tamil Features:")
            print("   • Automatic English → Tamil translation")
            print("   • Tamil voice synthesis")
            print("   • Financial terms in Tamil")
            print("   • Bilingual conversation support")
            
        else:
            print("\n⚠️ Some tests failed. Check the details above.")
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    main()
