"""
ChatGPT API Integration for Taxora
Provides OpenAI ChatGPT integration with financial advisory capabilities.
"""

import os
import logging
import time
from typing import List, Dict, Optional
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# OpenAI API endpoint
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def validate_chatgpt_config() -> bool:
    """Validate ChatGPT configuration."""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        logger.warning("OpenAI API key not configured")
        return False
    
    logger.info("ChatGPT configuration validated successfully")
    return True

def format_messages_for_chatgpt(messages: List[Dict]) -> List[Dict]:
    """Format messages for ChatGPT API."""
    formatted_messages = [
        {
            "role": "system",
            "content": """You are Taxora, a professional financial advisor AI assistant. 
            You provide helpful, accurate, and personalized financial advice on topics like:
            - Investment strategies and portfolio management
            - Budgeting and expense tracking
            - Savings plans and emergency funds
            - Debt management and credit improvement
            - Tax planning and optimization
            - Retirement planning
            - Insurance and risk management
            
            Always provide practical, actionable advice while emphasizing the importance of 
            consulting with qualified financial professionals for major decisions. Keep responses 
            concise but informative, and tailor advice to the user's experience level."""
        }
    ]
    
    # Add conversation history
    for msg in messages:
        if msg["role"] in ["user", "assistant"]:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
    
    return formatted_messages

def chatgpt_generate_response(messages: List[Dict], max_retries: int = 1) -> str:
    """Generate response using OpenAI ChatGPT API with retry logic."""
    if not validate_chatgpt_config():
        return "ChatGPT is not configured. Please add your OpenAI API key to use this feature."

    for attempt in range(max_retries + 1):
        try:
            # Format messages for ChatGPT
            formatted_messages = format_messages_for_chatgpt(messages)

            logger.info(f"Sending request to ChatGPT API (attempt {attempt + 1}/{max_retries + 1})...")
            start_time = time.time()

            # Prepare API request with optimized settings for free tier
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }

            # Reduce token usage for free tier
            max_tokens = min(OPENAI_MAX_TOKENS, 500)  # Limit tokens to reduce costs

            payload = {
                "model": "gpt-3.5-turbo",  # Use most cost-effective model
                "messages": formatted_messages,
                "max_tokens": max_tokens,
                "temperature": 0.7,  # Slightly lower for more focused responses
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }

            # Make API request with longer timeout for free tier
            response = requests.post(
                OPENAI_API_URL,
                headers=headers,
                json=payload,
                timeout=90  # Longer timeout for free tier
            )

            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()

                if "choices" in data and len(data["choices"]) > 0:
                    ai_response = data["choices"][0]["message"]["content"].strip()

                    # Log usage statistics
                    usage = data.get("usage", {})
                    logger.info(f"ChatGPT response received in {response_time:.2f}s")
                    logger.info(f"Tokens used: {usage.get('total_tokens', 'unknown')}")

                    return ai_response
                else:
                    logger.error("No choices in ChatGPT response")
                    return "I couldn't generate a response. Please try again."

            elif response.status_code == 401:
                logger.error("Invalid OpenAI API key")
                return "Invalid API key. Please check your OpenAI configuration."

            elif response.status_code == 429:
                error_data = response.json() if response.content else {}
                error_message = error_data.get('error', {}).get('message', '')

                if 'quota' in error_message.lower() or 'exceeded' in error_message.lower():
                    logger.error(f"OpenAI API quota exceeded: {error_message}")
                    return "ChatGPT quota exceeded. Please check your OpenAI billing at https://platform.openai.com/account/billing. Using IBM Granite for now."
                else:
                    retry_after = int(response.headers.get('retry-after', '20'))
                    logger.warning(f"Rate limit hit, attempt {attempt + 1}/{max_retries + 1}")

                    if attempt < max_retries:
                        logger.info(f"Waiting {retry_after} seconds before retry...")
                        time.sleep(min(retry_after, 10))  # Reduced wait time
                        continue
                    else:
                        logger.error("Max retries exceeded for rate limit")
                        return f"ChatGPT is experiencing high demand. Please try again in {retry_after} seconds, or switch to IBM Granite for immediate responses."

            elif response.status_code == 400:
                logger.error(f"Bad request to OpenAI API: {response.text}")
                return "There was an issue with your request. Please try rephrasing your question."
            
            else:
                logger.error(f"OpenAI API error {response.status_code}: {response.text}")
                if attempt < max_retries:
                    logger.info("Retrying after API error...")
                    time.sleep(5)  # Wait 5 seconds before retry
                    continue
                else:
                    return "I'm having trouble connecting to ChatGPT. Please try again later or switch to IBM Granite."

        except requests.exceptions.Timeout:
            logger.warning(f"ChatGPT API timeout, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                return "The request took too long. Please try again with a shorter question or switch to IBM Granite."

        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                return "I can't connect to ChatGPT right now. Please check your internet connection or switch to IBM Granite."

        except json.JSONDecodeError:
            logger.error("Invalid JSON response from OpenAI API")
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                return "I received an unexpected response. Please try again or switch to IBM Granite."

        except Exception as e:
            logger.error(f"Unexpected error with ChatGPT API: {e}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                return "I encountered an unexpected error. Please try again or switch to IBM Granite."

    # If we get here, all retries failed
    return "ChatGPT is currently unavailable. Please try again later or switch to IBM Granite for immediate responses."

def test_chatgpt_connection() -> Dict:
    """Test ChatGPT API connection and return status."""
    if not validate_chatgpt_config():
        return {
            "status": "error",
            "message": "API key not configured",
            "configured": False
        }
    
    try:
        # Simple test message
        test_messages = [{"role": "user", "content": "Hello, are you working?"}]
        response = chatgpt_generate_response(test_messages)
        
        if "API key" in response or "error" in response.lower():
            return {
                "status": "error",
                "message": response,
                "configured": True
            }
        else:
            return {
                "status": "success",
                "message": "ChatGPT is working correctly",
                "configured": True
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Connection test failed: {str(e)}",
            "configured": True
        }

if __name__ == "__main__":
    # Test the ChatGPT integration
    print("🧪 Testing ChatGPT Integration")
    print("=" * 50)
    
    status = test_chatgpt_connection()
    print(f"Status: {status}")
    
    if status["status"] == "success":
        test_messages = [
            {"role": "user", "content": "I have $1000 to invest. What should I do?"}
        ]
        response = chatgpt_generate_response(test_messages)
        print(f"Test Response: {response}")
