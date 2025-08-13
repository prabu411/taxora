"""
Grok AI Client for Taxora
Integrates with xAI's Grok API for financial conversations
"""

import os
import logging
import time
import json
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Grok Configuration
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-beta")
GROK_MAX_TOKENS = int(os.getenv("GROK_MAX_TOKENS", "1000"))
GROK_TEMPERATURE = float(os.getenv("GROK_TEMPERATURE", "0.7"))

# API URLs
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

def validate_grok_config() -> bool:
    """Validate Grok API configuration."""
    if not GROK_API_KEY:
        logger.warning("Grok API key not configured")
        return False
    
    if not GROK_API_KEY.startswith('xai-'):
        logger.warning("Grok API key format appears invalid (should start with 'xai-')")
        return False
    
    logger.info("Grok configuration validated successfully")
    return True

def format_messages_for_grok(messages: List[Dict]) -> List[Dict]:
    """Format messages for Grok API."""
    formatted_messages = []
    
    # Add system message for financial advice
    formatted_messages.append({
        "role": "system",
        "content": "You are a professional financial advisor powered by Grok AI. Provide helpful, accurate, and practical financial advice. Keep responses concise but informative. Focus on actionable guidance for budgeting, saving, investing, and financial planning. Use a friendly but professional tone."
    })
    
    # Format conversation messages
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        
        # Map roles to Grok format
        if role == "assistant":
            role = "assistant"
        else:
            role = "user"
        
        formatted_messages.append({
            "role": role,
            "content": content
        })
    
    return formatted_messages

def grok_generate_response(messages: List[Dict], max_retries: int = 2) -> str:
    """Generate response using Grok AI API."""
    if not validate_grok_config():
        return "Grok is not configured. Please add your xAI API key to use this feature."
    
    for attempt in range(max_retries + 1):
        try:
            # Format messages for Grok
            formatted_messages = format_messages_for_grok(messages)
            
            logger.info(f"Sending request to Grok API (attempt {attempt + 1}/{max_retries + 1})...")
            start_time = time.time()
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": formatted_messages,
                "model": GROK_MODEL,
                "max_tokens": GROK_MAX_TOKENS,
                "temperature": GROK_TEMPERATURE,
                "stream": False
            }
            
            # Make API request
            response = requests.post(
                GROK_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        ai_response = choice["message"]["content"].strip()
                        
                        # Log usage statistics
                        usage = data.get("usage", {})
                        logger.info(f"Grok response received in {response_time:.2f}s")
                        logger.info(f"Tokens used: {usage.get('total_tokens', 'unknown')}")
                        
                        return ai_response
                    else:
                        logger.error("No content in Grok response")
                        return "I couldn't generate a response. Please try again."
                else:
                    logger.error("No choices in Grok response")
                    return "I couldn't generate a response. Please try again."
                    
            elif response.status_code == 401:
                logger.error("Invalid Grok API key")
                return "Invalid API key. Please check your xAI configuration."
                
            elif response.status_code == 429:
                retry_after = int(response.headers.get('retry-after', '10'))
                logger.warning(f"Grok rate limit hit, attempt {attempt + 1}/{max_retries + 1}")

                if attempt < max_retries:
                    logger.info(f"Waiting {retry_after} seconds before retry...")
                    time.sleep(min(retry_after, 20))
                    continue
                else:
                    logger.error("Max retries exceeded for Grok rate limit")
                    raise Exception(f"GROK_RATE_LIMITED: Grok is experiencing high demand. Retry in {retry_after} seconds.")
                
            elif response.status_code == 400:
                logger.error(f"Bad request to Grok API: {response.text}")
                return "There was an issue with your request. Please try rephrasing your question."
                
            else:
                logger.error(f"Grok API error {response.status_code}: {response.text}")
                if attempt < max_retries:
                    logger.info("Retrying after API error...")
                    time.sleep(5)
                    continue
                else:
                    raise Exception("GROK_API_ERROR: I'm having trouble connecting to Grok.")
                    
        except requests.exceptions.Timeout:
            logger.warning(f"Grok API timeout, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                raise Exception("GROK_TIMEOUT: The request took too long.")
                
        except requests.exceptions.ConnectionError:
            logger.warning(f"Grok connection error, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                raise Exception("GROK_CONNECTION_ERROR: I can't connect to Grok right now.")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from Grok API")
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                raise Exception("GROK_API_ERROR: I received an unexpected response.")
                
        except Exception as e:
            error_str = str(e)
            logger.error(f"Unexpected error with Grok API: {e}")
            
            # Re-raise specific Grok errors to trigger fallback
            if any(error_type in error_str for error_type in ["GROK_RATE_LIMITED", "GROK_API_ERROR", "GROK_CONNECTION_ERROR", "GROK_TIMEOUT"]):
                raise e
            
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                raise Exception(f"GROK_API_ERROR: I encountered an unexpected error: {str(e)}")
    
    # If we get here, all retries failed
    raise Exception("GROK_API_ERROR: Grok is currently unavailable after all retries.")

def test_grok_connection() -> Dict:
    """Test Grok API connection."""
    if not validate_grok_config():
        return {
            "status": "error",
            "message": "Grok API key not configured",
            "working": False
        }
    
    try:
        test_messages = [{"role": "user", "content": "Hello, this is a test message for financial advice."}]
        response = grok_generate_response(test_messages)
        
        if response and "error" not in response.lower():
            return {
                "status": "success",
                "message": "Grok connection successful",
                "working": True,
                "response_length": len(response)
            }
        else:
            return {
                "status": "error",
                "message": f"Grok test failed: {response}",
                "working": False
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Grok connection failed: {str(e)}",
            "working": False
        }

def validate_grok_api_key(api_key: str) -> bool:
    """Validate Grok API key format."""
    return api_key and api_key.startswith('xai-') and len(api_key) > 20

if __name__ == "__main__":
    # Test the Grok client
    print("🧪 Testing Grok Client")
    print("=" * 50)
    
    # Test configuration
    if validate_grok_config():
        print("✅ Configuration valid")
        
        # Test connection
        test_result = test_grok_connection()
        print(f"Connection test: {test_result}")
        
        if test_result["working"]:
            # Test actual response
            test_messages = [{"role": "user", "content": "What is the 50/30/20 budgeting rule?"}]
            response = grok_generate_response(test_messages)
            print(f"Test response: {response[:200]}...")
        
    else:
        print("❌ Configuration invalid")
        print("Please set GROK_API_KEY in your .env file")
        print("Get your API key from: https://console.x.ai/")
