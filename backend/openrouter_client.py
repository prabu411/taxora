"""
OpenRouter AI Client for Taxora
Provides access to multiple AI models through OpenRouter API
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

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mixtral-8x7b-instruct")
OPENROUTER_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "1000"))
OPENROUTER_TEMPERATURE = float(os.getenv("OPENROUTER_TEMPERATURE", "0.7"))

# API URL
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def validate_openrouter_config() -> bool:
    """Validate OpenRouter configuration."""
    if not OPENROUTER_API_KEY:
        logger.error("OpenRouter API key not found in environment variables")
        return False
    
    if not OPENROUTER_API_KEY.startswith("sk-or-v1-"):
        logger.error("Invalid OpenRouter API key format")
        return False
    
    logger.info("OpenRouter configuration validated successfully")
    return True

def openrouter_generate_response(messages: List[Dict], max_retries: int = 2) -> str:
    """Generate response using OpenRouter API."""
    if not validate_openrouter_config():
        return "OpenRouter is not configured. Please add your OpenRouter API key to use this feature."

    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Sending request to OpenRouter API (attempt {attempt + 1}/{max_retries + 1})...")
            start_time = time.time()
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # Add system message for financial advice
            system_message = {
                "role": "system",
                "content": "You are a professional financial advisor. Provide helpful, accurate, and practical financial advice. Keep responses concise but informative. Focus on actionable guidance for budgeting, saving, investing, and financial planning."
            }
            
            # Prepare messages with system instruction
            formatted_messages = [system_message] + messages
            
            # Prepare payload
            payload = {
                "model": OPENROUTER_MODEL,
                "messages": formatted_messages,
                "max_tokens": OPENROUTER_MAX_TOKENS,
                "temperature": OPENROUTER_TEMPERATURE,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
            
            # Make API request
            response = requests.post(
                OPENROUTER_API_URL,
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
                        logger.info(f"OpenRouter response received in {response_time:.2f}s")
                        logger.info(f"Tokens used: {usage.get('total_tokens', 'unknown')}")
                        
                        return ai_response
                    else:
                        logger.error("No content in OpenRouter response")
                        return "I apologize, but I received an empty response. Please try again."
                else:
                    logger.error("No choices in OpenRouter response")
                    return "I apologize, but I couldn't generate a response. Please try again."
            
            elif response.status_code == 429:
                logger.warning(f"OpenRouter rate limit exceeded (attempt {attempt + 1})")
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception("OPENROUTER_RATE_LIMITED: Rate limit exceeded. Please try again later.")
            
            elif response.status_code == 401:
                logger.error("OpenRouter authentication failed - invalid API key")
                raise Exception("OPENROUTER_API_ERROR: Invalid API key")

            elif response.status_code == 402:
                logger.error("OpenRouter insufficient credits")
                raise Exception("OPENROUTER_INSUFFICIENT_CREDITS: Please add credits at https://openrouter.ai/settings/credits")

            elif response.status_code == 400:
                logger.error(f"OpenRouter bad request: {response.text}")
                raise Exception("OPENROUTER_API_ERROR: Bad request")
            
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                if attempt < max_retries:
                    wait_time = 2 ** attempt
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception(f"OPENROUTER_API_ERROR: HTTP {response.status_code}")
        
        except requests.exceptions.Timeout:
            logger.error(f"OpenRouter request timeout (attempt {attempt + 1})")
            if attempt < max_retries:
                continue
            else:
                raise Exception("OPENROUTER_TIMEOUT: Request timed out")
        
        except requests.exceptions.ConnectionError:
            logger.error(f"OpenRouter connection error (attempt {attempt + 1})")
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                raise Exception("OPENROUTER_CONNECTION_ERROR: Could not connect to OpenRouter")
        
        except Exception as e:
            if "OPENROUTER_" in str(e):
                raise e
            else:
                logger.error(f"Unexpected error in OpenRouter client: {e}")
                if attempt < max_retries:
                    continue
                else:
                    raise Exception(f"OPENROUTER_API_ERROR: {str(e)}")
    
    return "I apologize, but I'm having trouble connecting to the AI service. Please try again later."

def test_openrouter_connectivity() -> Dict:
    """Test OpenRouter API connectivity."""
    try:
        if not validate_openrouter_config():
            return {
                "success": False,
                "error": "Configuration validation failed",
                "details": "OpenRouter API key not configured properly"
            }
        
        # Test with a simple message
        test_messages = [{"role": "user", "content": "Hello, can you help with financial advice?"}]
        
        start_time = time.time()
        response = openrouter_generate_response(test_messages)
        response_time = time.time() - start_time
        
        if response and not response.startswith("I apologize"):
            return {
                "success": True,
                "response_time": response_time,
                "model": OPENROUTER_MODEL,
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
            "details": "OpenRouter connectivity test failed"
        }

def get_openrouter_status() -> Dict:
    """Get OpenRouter service status."""
    return {
        "service": "OpenRouter",
        "configured": validate_openrouter_config(),
        "model": OPENROUTER_MODEL,
        "api_key_present": bool(OPENROUTER_API_KEY),
        "api_key_format_valid": OPENROUTER_API_KEY.startswith("sk-or-v1-") if OPENROUTER_API_KEY else False
    }

# Test function for direct execution
if __name__ == "__main__":
    print("🤖 Testing OpenRouter AI Client")
    print("=" * 40)
    
    # Test configuration
    config_status = get_openrouter_status()
    print(f"Configuration Status: {config_status}")
    
    if config_status["configured"]:
        # Test connectivity
        print("\nTesting connectivity...")
        connectivity_result = test_openrouter_connectivity()
        print(f"Connectivity Result: {connectivity_result}")
        
        if connectivity_result["success"]:
            print("\n✅ OpenRouter client is working correctly!")
            print(f"Model: {connectivity_result['model']}")
            print(f"Response time: {connectivity_result['response_time']:.2f}s")
            print(f"Sample response: {connectivity_result['response_preview']}")
        else:
            print(f"\n❌ OpenRouter client test failed: {connectivity_result['error']}")
    else:
        print("\n⚠️ OpenRouter is not configured properly")
        print("Please check your OPENROUTER_API_KEY in the .env file")
