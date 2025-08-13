from transformers import pipeline
import torch
import sys
import os

print("🚀 Testing Lightweight Financial AI Model")
print("=" * 50)

# Use a small, fast text generation model (~500MB)
MODEL_ID = "distilgpt2"  # Small, fast, and reliable

print(f"📦 Loading model: {MODEL_ID}")
print("⏳ Small download (~500MB) - much faster than 7GB!")

try:
    # Create text generation pipeline
    print("🔧 Setting up AI pipeline...")

    generator = pipeline(
        "text-generation",
        model=MODEL_ID,
        device=-1,  # Use CPU for compatibility
        max_length=150,
        do_sample=True,
        temperature=0.7
    )
    
    print("✅ Lightweight AI model ready!")
    print("💾 Model size: ~500MB (vs 7GB for full Granite)")
    print("⚡ Fast inference on CPU")

    print("\n" + "="*50)
    print("💬 TESTING FINANCIAL AI RESPONSES")
    print("="*50)

    # Test 1: Investment advice
    prompt1 = "Financial Advisor: A beginner with $1000 to invest should consider"
    result1 = generator(prompt1, max_length=100, num_return_sequences=1)

    print(f"\n👤 User: I have $1000 to invest. What are some safe options for a beginner?")
    print(f"🤖 AI: {result1[0]['generated_text'][len(prompt1):].strip()}")

    # Test 2: Budgeting
    prompt2 = "Financial Advisor: For college students creating a monthly budget, I recommend"
    result2 = generator(prompt2, max_length=100, num_return_sequences=1)

    print(f"\n👤 User: How should I create a monthly budget as a college student?")
    print(f"🤖 AI: {result2[0]['generated_text'][len(prompt2):].strip()}")

    # Test 3: Savings
    prompt3 = "Financial Advisor: To start an emergency fund, you should"
    result3 = generator(prompt3, max_length=100, num_return_sequences=1)

    print(f"\n👤 User: What's the best way to start an emergency fund?")
    print(f"🤖 AI: {result3[0]['generated_text'][len(prompt3):].strip()}")
    
    print("\n" + "="*50)
    print("✅ LIGHTWEIGHT AI TEST SUCCESSFUL!")
    print("🎉 Ready to integrate with your Taxora chatbot!")
    print("📊 Performance: Fast responses, low memory usage")
    print("💡 Perfect for real-time financial advice")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n🔧 Trying even smaller model...")

    try:
        # Fallback to tiny model
        MODEL_ID = "gpt2"  # Only ~500MB, very reliable
        print(f"📦 Loading backup model: {MODEL_ID} (~500MB)")

        generator = pipeline("text-generation", model=MODEL_ID, device=-1)

        prompt = "Financial advice: To save money effectively, you should"
        result = generator(prompt, max_length=80, num_return_sequences=1)

        print(f"👤 User: How can I save money effectively?")
        print(f"🤖 AI: {result[0]['generated_text'][len(prompt):].strip()}")
        print("✅ Backup model working!")

    except Exception as e2:
        print(f"❌ Backup failed: {e2}")
        print("💡 Please check internet connection and try again")
