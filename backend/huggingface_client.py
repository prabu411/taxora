"""
Hugging Face AI Client for Taxora
Provides access to Hugging Face models through their Inference API
"""

import os
import requests
import json
import logging
import time
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hugging Face Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "gpt2")
HUGGINGFACE_MAX_TOKENS = int(os.getenv("HUGGINGFACE_MAX_TOKENS", "200"))
HUGGINGFACE_TEMPERATURE = float(os.getenv("HUGGINGFACE_TEMPERATURE", "0.7"))

# API URL
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models"

# Available models for financial advice
FINANCIAL_MODELS = {
    "gpt2": "Fast and reliable text generation",
    "distilgpt2": "Lightweight GPT-2 model",
    "microsoft/DialoGPT-small": "Small conversational model",
    "facebook/blenderbot-400M-distill": "Efficient conversational model",
    "microsoft/DialoGPT-medium": "Medium conversational model"
}

def validate_huggingface_config() -> bool:
    """Validate Hugging Face configuration."""
    if not HUGGINGFACE_API_KEY:
        logger.error("Hugging Face API key not found in environment variables")
        return False
    
    if not HUGGINGFACE_API_KEY.startswith("hf_"):
        logger.error("Invalid Hugging Face API key format")
        return False
    
    logger.info("Hugging Face configuration validated successfully")
    return True

def huggingface_generate_response(messages: List[Dict], max_retries: int = 2) -> str:
    """Generate response using Hugging Face Inference API."""
    if not validate_huggingface_config():
        return "Hugging Face is not configured. Please add your Hugging Face API key to use this feature."

    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Sending request to Hugging Face API (attempt {attempt + 1}/{max_retries + 1})...")
            start_time = time.time()
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # Convert messages to a single conversation string
            conversation = ""
            for message in messages:
                role = message.get("role", "user")
                content = message.get("content", "")
                
                if role == "system":
                    conversation += f"System: {content}\n"
                elif role == "user":
                    conversation += f"User: {content}\n"
                elif role == "assistant":
                    conversation += f"Assistant: {content}\n"
            
            # Add financial advisor context
            financial_context = "You are a professional financial advisor. Provide helpful, accurate, and practical financial advice. Keep responses concise but informative. Focus on actionable guidance for budgeting, saving, investing, and financial planning.\n\n"
            conversation = financial_context + conversation + "Assistant:"
            
            # Prepare payload for text generation
            payload = {
                "inputs": conversation,
                "parameters": {
                    "max_new_tokens": HUGGINGFACE_MAX_TOKENS,
                    "temperature": HUGGINGFACE_TEMPERATURE,
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            # Try different models if the primary one fails
            models_to_try = [
                HUGGINGFACE_MODEL,
                "gpt2",
                "distilgpt2",
                "microsoft/DialoGPT-small",
                "facebook/blenderbot-400M-distill"
            ]
            
            for model in models_to_try:
                try:
                    url = f"{HUGGINGFACE_API_URL}/{model}"
                    
                    # Make API request
                    response = requests.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=60
                    )
                    
                    response_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if isinstance(data, list) and len(data) > 0:
                            if "generated_text" in data[0]:
                                ai_response = data[0]["generated_text"].strip()
                                
                                # Clean up the response
                                ai_response = clean_response(ai_response)
                                
                                if ai_response and len(ai_response) > 10:
                                    logger.info(f"Hugging Face response received in {response_time:.2f}s using {model}")
                                    return ai_response
                                else:
                                    logger.warning(f"Empty or too short response from {model}")
                                    continue
                            else:
                                logger.warning(f"No generated_text in response from {model}")
                                continue
                        else:
                            logger.warning(f"Invalid response format from {model}")
                            continue
                    
                    elif response.status_code == 503:
                        logger.warning(f"Model {model} is loading, trying next model...")
                        continue
                    
                    elif response.status_code == 429:
                        logger.warning(f"Rate limit exceeded for {model}")
                        if attempt < max_retries:
                            wait_time = 2 ** attempt
                            logger.info(f"Waiting {wait_time} seconds before retry...")
                            time.sleep(wait_time)
                            break
                        else:
                            continue
                    
                    elif response.status_code == 401:
                        logger.error("Hugging Face authentication failed - invalid API key")
                        raise Exception("HUGGINGFACE_API_ERROR: Invalid API key")
                    
                    else:
                        logger.warning(f"Hugging Face API error for {model}: {response.status_code} - {response.text}")
                        continue
                
                except requests.exceptions.Timeout:
                    logger.warning(f"Timeout for model {model}, trying next...")
                    continue
                
                except requests.exceptions.ConnectionError:
                    logger.warning(f"Connection error for model {model}, trying next...")
                    continue
            
            # If we get here, all models failed for this attempt
            if attempt < max_retries:
                wait_time = 2 ** attempt
                logger.info(f"All models failed, waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                # Generate a fallback response
                return generate_fallback_financial_response(messages)
        
        except Exception as e:
            if "HUGGINGFACE_" in str(e):
                raise e
            else:
                logger.error(f"Unexpected error in Hugging Face client: {e}")
                if attempt < max_retries:
                    continue
                else:
                    return generate_fallback_financial_response(messages)
    
    return "I apologize, but I'm having trouble connecting to the AI service. Please try again later."

def clean_response(response: str) -> str:
    """Clean and format the AI response."""
    # Remove common artifacts
    response = response.replace("Assistant:", "").strip()
    response = response.replace("User:", "").strip()
    response = response.replace("System:", "").strip()
    
    # Remove repetitive patterns
    lines = response.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line and line not in cleaned_lines[-3:]:  # Avoid immediate repetition
            cleaned_lines.append(line)
    
    response = '\n'.join(cleaned_lines)
    
    # Ensure it's a reasonable length
    if len(response) > 2000:
        response = response[:2000] + "..."
    
    return response.strip()

def generate_fallback_financial_response(messages: List[Dict]) -> str:
    """Generate a fallback financial response when AI models fail."""
    last_message = messages[-1] if messages else {"content": ""}
    user_question = last_message.get("content", "").lower()
    
    # Simple keyword-based responses for common financial topics
    if "savings" in user_question or "save" in user_question:
        return """Here are some effective savings strategies:

1. **50/30/20 Rule**: Allocate 50% for needs, 30% for wants, and 20% for savings
2. **Automate Savings**: Set up automatic transfers to your savings account
3. **Emergency Fund**: Build 3-6 months of expenses as an emergency fund
4. **High-Yield Accounts**: Use high-yield savings accounts for better returns
5. **Track Expenses**: Monitor your spending to identify areas to cut back

Start small and gradually increase your savings rate as you build the habit."""
    
    elif "investment" in user_question or "invest" in user_question:
        return """Investment basics for beginners:

1. **Start Early**: Time in the market beats timing the market
2. **Diversify**: Don't put all eggs in one basket
3. **Low-Cost Index Funds**: Great for beginners with broad market exposure
4. **SIP (Systematic Investment Plan)**: Invest regularly regardless of market conditions
5. **Risk Assessment**: Understand your risk tolerance before investing
6. **Emergency Fund First**: Ensure you have emergency savings before investing

Consider consulting with a financial advisor for personalized advice."""
    
    elif "budget" in user_question:
        return """Creating an effective budget:

1. **Track Income**: Know exactly how much money comes in
2. **List All Expenses**: Fixed costs (rent, utilities) and variable costs (food, entertainment)
3. **Categorize Spending**: Needs vs. wants
4. **Set Realistic Goals**: Don't be too restrictive initially
5. **Use Tools**: Apps or spreadsheets to track spending
6. **Review Monthly**: Adjust your budget based on actual spending patterns

Remember, a budget is a plan for your money, not a restriction."""
    
    else:
        return """I'm here to help with your financial questions! I can provide guidance on:

• **Savings Strategies** - Building emergency funds and saving goals
• **Investment Basics** - Getting started with investing
• **Budgeting** - Creating and managing budgets
• **Debt Management** - Strategies to pay off debt
• **Financial Planning** - Long-term financial goals

Please feel free to ask about any specific financial topic you'd like help with."""

def test_huggingface_connectivity() -> Dict:
    """Test Hugging Face API connectivity."""
    try:
        if not validate_huggingface_config():
            return {
                "success": False,
                "error": "Configuration validation failed",
                "details": "Hugging Face API key not configured properly"
            }
        
        # Test with a simple message
        test_messages = [{"role": "user", "content": "Hello, can you help with financial advice?"}]
        
        start_time = time.time()
        response = huggingface_generate_response(test_messages)
        response_time = time.time() - start_time
        
        if response and not response.startswith("I apologize"):
            return {
                "success": True,
                "response_time": response_time,
                "model": HUGGINGFACE_MODEL,
                "response_preview": response[:100] + "..." if len(response) > 100 else response
            }
        else:
            return {
                "success": False,
                "error": "Invalid response received",
                "details": response
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "details": "Hugging Face connectivity test failed"
        }

def get_huggingface_status() -> Dict:
    """Get Hugging Face service status."""
    return {
        "service": "Hugging Face",
        "configured": validate_huggingface_config(),
        "model": HUGGINGFACE_MODEL,
        "api_key_present": bool(HUGGINGFACE_API_KEY),
        "api_key_format_valid": HUGGINGFACE_API_KEY.startswith("hf_") if HUGGINGFACE_API_KEY else False,
        "available_models": list(FINANCIAL_MODELS.keys())
    }

# Test function for direct execution
if __name__ == "__main__":
    print("🤗 Testing Hugging Face AI Client")
    print("=" * 40)
    
    # Test configuration
    config_status = get_huggingface_status()
    print(f"Configuration Status: {config_status}")
    
    if config_status["configured"]:
        # Test connectivity
        print("\nTesting connectivity...")
        connectivity_result = test_huggingface_connectivity()
        print(f"Connectivity Result: {connectivity_result}")
        
        if connectivity_result["success"]:
            print("\n✅ Hugging Face client is working correctly!")
            print(f"Model: {connectivity_result['model']}")
            print(f"Response time: {connectivity_result['response_time']:.2f}s")
            print(f"Sample response: {connectivity_result['response_preview']}")
        else:
            print(f"\n❌ Hugging Face client test failed: {connectivity_result['error']}")
    else:
        print("\n⚠️ Hugging Face is not configured properly")
        print("Please check your HUGGINGFACE_API_KEY in the .env file")
