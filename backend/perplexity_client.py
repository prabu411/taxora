"""
Perplexity AI Client for Taxora
Integrates with Perplexity API for financial conversations with real-time information
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

# Perplexity Configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_MODEL = os.getenv("PERPLEXITY_MODEL", "llama-3.1-sonar-small-128k-online")
PERPLEXITY_MAX_TOKENS = int(os.getenv("PERPLEXITY_MAX_TOKENS", "1000"))
PERPLEXITY_TEMPERATURE = float(os.getenv("PERPLEXITY_TEMPERATURE", "0.7"))

# API URLs
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

def validate_perplexity_config() -> bool:
    """Validate Perplexity API configuration."""
    if not PERPLEXITY_API_KEY:
        logger.warning("Perplexity API key not configured")
        return False
    
    if not PERPLEXITY_API_KEY.startswith('pplx-'):
        logger.warning("Perplexity API key format appears invalid (should start with 'pplx-')")
        return False
    
    logger.info("Perplexity configuration validated successfully")
    return True

def format_messages_for_perplexity(messages: List[Dict]) -> List[Dict]:
    """Format messages for Perplexity API."""
    formatted_messages = []
    
    # Add system message for financial advice with real-time information
    formatted_messages.append({
        "role": "system",
        "content": "You are a professional financial advisor powered by Perplexity AI with access to real-time information. Provide helpful, accurate, and up-to-date financial advice. Include current market information, recent financial news, and real-time data when relevant. Keep responses concise but informative. Focus on actionable guidance for budgeting, saving, investing, and financial planning. Cite sources when providing current market data or financial news."
    })
    
    # Format conversation messages
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        
        # Map roles to Perplexity format
        if role == "assistant":
            role = "assistant"
        else:
            role = "user"
        
        formatted_messages.append({
            "role": role,
            "content": content
        })
    
    return formatted_messages

def perplexity_generate_response(messages: List[Dict], max_retries: int = 2) -> str:
    """Generate response using Perplexity AI API with real-time information."""
    if not validate_perplexity_config():
        return "Perplexity is not configured. Please add your Perplexity API key to use this feature."
    
    for attempt in range(max_retries + 1):
        try:
            # Format messages for Perplexity
            formatted_messages = format_messages_for_perplexity(messages)
            
            logger.info(f"Sending request to Perplexity API (attempt {attempt + 1}/{max_retries + 1})...")
            start_time = time.time()
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": PERPLEXITY_MODEL,
                "messages": formatted_messages,
                "max_tokens": PERPLEXITY_MAX_TOKENS,
                "temperature": PERPLEXITY_TEMPERATURE,
                "stream": False
            }
            
            # Make API request
            response = requests.post(
                PERPLEXITY_API_URL,
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
                        logger.info(f"Perplexity response received in {response_time:.2f}s")
                        logger.info(f"Tokens used: {usage.get('total_tokens', 'unknown')}")
                        
                        return ai_response
                    else:
                        logger.error("No content in Perplexity response")
                        return "I couldn't generate a response. Please try again."
                else:
                    logger.error("No choices in Perplexity response")
                    return "I couldn't generate a response. Please try again."
                    
            elif response.status_code == 401:
                logger.error("Invalid Perplexity API key")
                return "Invalid API key. Please check your Perplexity configuration."
                
            elif response.status_code == 429:
                retry_after = int(response.headers.get('retry-after', '10'))
                logger.warning(f"Perplexity rate limit hit, attempt {attempt + 1}/{max_retries + 1}")

                if attempt < max_retries:
                    logger.info(f"Waiting {retry_after} seconds before retry...")
                    time.sleep(min(retry_after, 20))
                    continue
                else:
                    logger.error("Max retries exceeded for Perplexity rate limit")
                    raise Exception(f"PERPLEXITY_RATE_LIMITED: Perplexity is experiencing high demand. Retry in {retry_after} seconds.")
                
            elif response.status_code == 400:
                logger.error(f"Bad request to Perplexity API: {response.text}")
                return "There was an issue with your request. Please try rephrasing your question."
                
            else:
                logger.error(f"Perplexity API error {response.status_code}: {response.text}")
                if attempt < max_retries:
                    logger.info("Retrying after API error...")
                    time.sleep(5)
                    continue
                else:
                    raise Exception("PERPLEXITY_API_ERROR: I'm having trouble connecting to Perplexity.")
                    
        except requests.exceptions.Timeout:
            logger.warning(f"Perplexity API timeout, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                raise Exception("PERPLEXITY_TIMEOUT: The request took too long.")
                
        except requests.exceptions.ConnectionError:
            logger.warning(f"Perplexity connection error, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                raise Exception("PERPLEXITY_CONNECTION_ERROR: I can't connect to Perplexity right now.")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from Perplexity API")
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                raise Exception("PERPLEXITY_API_ERROR: I received an unexpected response.")
                
        except Exception as e:
            error_str = str(e)
            logger.error(f"Unexpected error with Perplexity API: {e}")
            
            # Re-raise specific Perplexity errors to trigger fallback
            if any(error_type in error_str for error_type in ["PERPLEXITY_RATE_LIMITED", "PERPLEXITY_API_ERROR", "PERPLEXITY_CONNECTION_ERROR", "PERPLEXITY_TIMEOUT"]):
                raise e
            
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                raise Exception(f"PERPLEXITY_API_ERROR: I encountered an unexpected error: {str(e)}")
    
    # If we get here, all retries failed
    raise Exception("PERPLEXITY_API_ERROR: Perplexity is currently unavailable after all retries.")

def test_perplexity_connection() -> Dict:
    """Test Perplexity API connection."""
    if not validate_perplexity_config():
        return {
            "status": "error",
            "message": "Perplexity API key not configured",
            "working": False
        }
    
    try:
        test_messages = [{"role": "user", "content": "What are the current interest rates for savings accounts?"}]
        response = perplexity_generate_response(test_messages)
        
        if response and "error" not in response.lower():
            return {
                "status": "success",
                "message": "Perplexity connection successful",
                "working": True,
                "response_length": len(response)
            }
        else:
            return {
                "status": "error",
                "message": f"Perplexity test failed: {response}",
                "working": False
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Perplexity connection failed: {str(e)}",
            "working": False
        }

def validate_perplexity_api_key(api_key: str) -> bool:
    """Validate Perplexity API key format."""
    return api_key and api_key.startswith('pplx-') and len(api_key) > 20

if __name__ == "__main__":
    # Test the Perplexity client
    print("🧪 Testing Perplexity Client")
    print("=" * 50)
    
    # Test configuration
    if validate_perplexity_config():
        print("✅ Configuration valid")
        
        # Test connection
        test_result = test_perplexity_connection()
        print(f"Connection test: {test_result}")
        
        if test_result["working"]:
            # Test actual response
            test_messages = [{"role": "user", "content": "What are the current mortgage rates in the US?"}]
            response = perplexity_generate_response(test_messages)
            print(f"Test response: {response[:200]}...")
        
    else:
        print("❌ Configuration invalid")
        print("Please set PERPLEXITY_API_KEY in your .env file")
        print("Get your API key from: https://www.perplexity.ai/settings/api")
