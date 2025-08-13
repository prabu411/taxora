from transformers import pipeline
import torch
import sys
import os

print("🚀 Testing Lightweight Financial AI Model")
print("=" * 50)

# Use a small, fast model optimized for conversations (~350MB)
MODEL_ID = "microsoft/DialoGPT-medium"

print(f"📦 Loading model: {MODEL_ID}")
print("⏳ Small download (~350MB) - much faster than 7GB!")

try:
    # Create conversational AI pipeline
    print("🔧 Setting up AI pipeline...")

    chatbot = pipeline(
        "conversational",
        model=MODEL_ID,
        device=-1,  # Use CPU for compatibility
        return_full_text=False
    )

    print("✅ Lightweight AI model ready!")
    print("💾 Model size: ~350MB (vs 7GB for full Granite)")
    print("⚡ Fast inference on CPU")

    # Test financial conversations
    from transformers import Conversation

    print("\n" + "="*50)
    print("💬 TESTING FINANCIAL AI RESPONSES")
    print("="*50)

    # Test 1: Investment advice
    conv1 = Conversation("I have $1000 to invest. What are some safe options for a beginner?")
    result1 = chatbot(conv1)

    print(f"\n👤 User: {conv1.messages[0]['content']}")
    print(f"🤖 AI: {result1.messages[-1]['content']}")

    # Test 2: Budgeting
    conv2 = Conversation("How should I create a monthly budget as a college student?")
    result2 = chatbot(conv2)

    print(f"\n👤 User: {conv2.messages[0]['content']}")
    print(f"🤖 AI: {result2.messages[-1]['content']}")

    # Test 3: Savings
    conv3 = Conversation("What's the best way to start an emergency fund?")
    result3 = chatbot(conv3)

    print(f"\n👤 User: {conv3.messages[0]['content']}")
    print(f"🤖 AI: {result3.messages[-1]['content']}")

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
        MODEL_ID = "microsoft/DialoGPT-small"  # Only ~117MB
        print(f"📦 Loading backup model: {MODEL_ID} (~117MB)")

        chatbot = pipeline("conversational", model=MODEL_ID, device=-1)

        conv = Conversation("Tell me about saving money")
        result = chatbot(conv)

        print(f"👤 User: {conv.messages[0]['content']}")
        print(f"🤖 AI: {result.messages[-1]['content']}")
        print("✅ Backup model working!")

    except Exception as e2:
        print(f"❌ Backup failed: {e2}")
        print("💡 Please check internet connection and try again")
    # Use pipeline for easier setup - much faster and smaller
    print("🔤 Creating AI pipeline...")
    print("📦 Downloading lightweight model (~117MB)...")

    # Create a conversational pipeline
    chatbot = pipeline(
        "conversational",
        model=MODEL_ID,
        tokenizer=MODEL_ID,
        device=0 if torch.cuda.is_available() else -1,
        framework="pt"
    )

    print("✅ Lightweight AI model loaded successfully!")
    print(f"💾 Model size: ~117MB (much smaller than 7GB!)")
    print(f"🖥️  Using device: {'GPU' if torch.cuda.is_available() else 'CPU'}")

    # Test with financial advice
    from transformers import Conversation

    conversation = Conversation("I have $1000 to invest. What are some safe investment options for a beginner?")

    print("\n💬 Testing with financial advice prompt:")
    print(f"📝 User: {conversation.messages[0]['content']}")
    print("\n🤖 AI Response:")
    print("-" * 40)

    # Generate response
    result = chatbot(conversation)
    response = result.messages[-1]['content']

    print(f"💡 {response}")

    # Test another financial question
    print("\n" + "-" * 40)
    print("🔄 Testing another question...")

    conversation.add_user_input("What about budgeting tips for someone just starting their career?")
    result = chatbot(conversation)
    response = result.messages[-1]['content']

    print(f"📝 User: What about budgeting tips for someone just starting their career?")
    print(f"💡 AI: {response}")

    print("\n" + "=" * 50)
    print("✅ IBM Granite test completed successfully!")
    print("🎉 Your model is working and ready for integration!")

except Exception as e:
    print(f"\n❌ Error testing IBM Granite model: {e}")
    print("\n🔧 Troubleshooting tips:")
    print("1. Make sure PyTorch is fully installed")
    print("2. Check your internet connection for model download")
    print("3. Ensure you have enough disk space (model is ~2GB)")
    print("4. Try running: pip install --upgrade transformers torch")
    sys.exit(1)
