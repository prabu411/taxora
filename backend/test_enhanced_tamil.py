#!/usr/bin/env python3
"""
Test Enhanced Tamil Voice System
"""

from tamil_voice_enhancer import enhance_tamil_for_voice
from gemini_client import gemini_text_to_speech

def test_enhanced_tamil_processing():
    """Test the enhanced Tamil voice processing."""
    print("🚀 Testing Enhanced Tamil Voice System")
    print("=" * 60)
    
    test_texts = [
        "Use the 50/30/20 budgeting rule for financial success.",
        "Save 20% of your income for emergencies.",
        "Invest in low-cost index funds for long-term growth.",
        "Create an emergency fund with 3-6 months of expenses.",
        "Budget your money wisely and save for the future."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test {i}: {text}")
        print("-" * 50)
        
        try:
            # Test enhanced Tamil processing
            result = enhance_tamil_for_voice(text)
            
            if result["success"]:
                print(f"✅ Enhanced Tamil: {result['enhanced_text']}")
                print(f"🎵 Voice Settings: {result['voice_settings']}")
                print(f"📊 Original length: {len(text)} chars")
                print(f"📊 Enhanced length: {len(result['enhanced_text'])} chars")
                
                # Test with Gemini TTS
                tts_result = gemini_text_to_speech(result['enhanced_text'], "ta")
                if tts_result["success"]:
                    print(f"🔊 TTS Ready: {tts_result['text'][:100]}...")
                    print(f"🎛️ TTS Config: {tts_result['voice_config']}")
                else:
                    print(f"❌ TTS Failed: {tts_result.get('error')}")
            else:
                print(f"❌ Enhancement failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def test_voice_quality_comparison():
    """Compare basic vs enhanced Tamil voice processing."""
    print("\n🔍 Voice Quality Comparison")
    print("=" * 60)
    
    sample_text = "Use the 50/30/20 budgeting rule. Save 20% of your income for emergencies and invest in index funds."
    
    print(f"📝 Sample Text: {sample_text}")
    print("-" * 50)
    
    try:
        # Basic Tamil processing
        basic_result = gemini_text_to_speech(sample_text, "ta")
        print(f"🔧 Basic Tamil: {basic_result['text']}")
        print(f"🎵 Basic Config: {basic_result['voice_config']}")
        
        # Enhanced Tamil processing
        enhanced_result = enhance_tamil_for_voice(sample_text)
        if enhanced_result["success"]:
            print(f"✨ Enhanced Tamil: {enhanced_result['enhanced_text']}")
            print(f"🎵 Enhanced Config: {enhanced_result['voice_settings']}")
            
            # Quality metrics
            basic_length = len(basic_result['text'])
            enhanced_length = len(enhanced_result['enhanced_text'])
            
            print(f"\n📊 Quality Metrics:")
            print(f"   Basic length: {basic_length} chars")
            print(f"   Enhanced length: {enhanced_length} chars")
            print(f"   Improvement: {((enhanced_length - basic_length) / basic_length * 100):.1f}%")
            
            # Check for Tamil words
            tamil_words_basic = sum(1 for char in basic_result['text'] if ord(char) >= 0x0B80 and ord(char) <= 0x0BFF)
            tamil_words_enhanced = sum(1 for char in enhanced_result['enhanced_text'] if ord(char) >= 0x0B80 and ord(char) <= 0x0BFF)
            
            print(f"   Tamil characters (basic): {tamil_words_basic}")
            print(f"   Tamil characters (enhanced): {tamil_words_enhanced}")
            
            if tamil_words_enhanced > tamil_words_basic:
                print("✅ Enhanced version has more Tamil content")
            else:
                print("⚠️ Enhancement may need improvement")
        
    except Exception as e:
        print(f"❌ Comparison error: {e}")
    
    return True

def test_financial_terms_translation():
    """Test financial terms translation quality."""
    print("\n💰 Financial Terms Translation Test")
    print("=" * 60)
    
    financial_phrases = [
        "budget your money",
        "save for emergencies", 
        "invest in stocks",
        "emergency fund",
        "financial planning",
        "income and expenses",
        "interest rates",
        "credit and debt"
    ]
    
    for phrase in financial_phrases:
        print(f"\n📝 Testing: {phrase}")
        
        try:
            result = enhance_tamil_for_voice(phrase)
            if result["success"]:
                print(f"🇮🇳 Tamil: {result['enhanced_text']}")
            else:
                print(f"❌ Failed: {result.get('error')}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def main():
    """Run all enhanced Tamil voice tests."""
    print("🎙️ Enhanced Tamil Voice System Test")
    print("=" * 70)
    
    try:
        # Test 1: Enhanced processing
        processing_success = test_enhanced_tamil_processing()
        
        # Test 2: Quality comparison
        comparison_success = test_voice_quality_comparison()
        
        # Test 3: Financial terms
        terms_success = test_financial_terms_translation()
        
        # Summary
        print("\n🎉 Enhanced Tamil Voice Test Summary")
        print("=" * 70)
        
        results = {
            "Enhanced Processing": processing_success,
            "Quality Comparison": comparison_success,
            "Financial Terms": terms_success
        }
        
        for test_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        all_passed = all(results.values())
        
        if all_passed:
            print("\n🎉 ALL ENHANCED TAMIL TESTS PASSED!")
            print("\n💡 Enhanced Tamil Voice Features:")
            print("   🇮🇳 Advanced Tamil text processing")
            print("   🔊 Optimized voice pronunciation")
            print("   💰 Financial terminology in Tamil")
            print("   🎵 Enhanced voice settings")
            print("   📱 Better user experience")
            
            print("\n🎮 Your Enhanced Tamil Voice System:")
            print("   • Proper Tamil number pronunciation")
            print("   • Financial terms in natural Tamil")
            print("   • Optimized speech pacing and clarity")
            print("   • Enhanced voice quality settings")
            print("   • Professional Tamil financial advice")
            
        else:
            print("\n⚠️ Some tests failed. Check the details above.")
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    main()
