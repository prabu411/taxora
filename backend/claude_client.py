"""
Claude AI Client for Taxora
Integrates with Anthropic's Claude API for financial conversations
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

# Claude Configuration
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "1000"))
CLAUDE_TEMPERATURE = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))

# API URLs
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

def validate_claude_config() -> bool:
    """Validate Claude API configuration."""
    if not CLAUDE_API_KEY:
        logger.warning("Claude API key not configured")
        return False
    
    if not CLAUDE_API_KEY.startswith('sk-ant-'):
        logger.warning("Claude API key format appears invalid (should start with 'sk-ant-')")
        return False
    
    logger.info("Claude configuration validated successfully")
    return True

def format_messages_for_claude(messages: List[Dict]) -> tuple[str, List[Dict]]:
    """Format messages for Claude API."""
    system_message = "You are a professional financial advisor powered by Claude AI. Provide helpful, accurate, and practical financial advice. Keep responses concise but informative. Focus on actionable guidance for budgeting, saving, investing, and financial planning. Use a thoughtful and analytical approach to financial questions."
    
    formatted_messages = []
    
    # Format conversation messages
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        
        # Map roles to Claude format
        if role == "assistant":
            role = "assistant"
        else:
            role = "user"
        
        formatted_messages.append({
            "role": role,
            "content": content
        })
    
    return system_message, formatted_messages

def claude_generate_response(messages: List[Dict], max_retries: int = 2) -> str:
    """Generate response using Claude AI API."""
    if not validate_claude_config():
        return "Claude is not configured. Please add your Anthropic API key to use this feature."
    
    for attempt in range(max_retries + 1):
        try:
            # Format messages for Claude
            system_message, formatted_messages = format_messages_for_claude(messages)
            
            logger.info(f"Sending request to Claude API (attempt {attempt + 1}/{max_retries + 1})...")
            start_time = time.time()
            
            # Prepare API request
            headers = {
                "x-api-key": CLAUDE_API_KEY,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": CLAUDE_MODEL,
                "max_tokens": CLAUDE_MAX_TOKENS,
                "temperature": CLAUDE_TEMPERATURE,
                "system": system_message,
                "messages": formatted_messages
            }
            
            # Make API request
            response = requests.post(
                CLAUDE_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if "content" in data and len(data["content"]) > 0:
                    content_block = data["content"][0]
                    if "text" in content_block:
                        ai_response = content_block["text"].strip()
                        
                        # Log usage statistics
                        usage = data.get("usage", {})
                        logger.info(f"Claude response received in {response_time:.2f}s")
                        logger.info(f"Tokens used: {usage.get('output_tokens', 'unknown')}")
                        
                        return ai_response
                    else:
                        logger.error("No text in Claude response")
                        return "I couldn't generate a response. Please try again."
                else:
                    logger.error("No content in Claude response")
                    return "I couldn't generate a response. Please try again."
                    
            elif response.status_code == 401:
                logger.error("Invalid Claude API key")
                return "Invalid API key. Please check your Anthropic configuration."
                
            elif response.status_code == 429:
                retry_after = int(response.headers.get('retry-after', '10'))
                logger.warning(f"Claude rate limit hit, attempt {attempt + 1}/{max_retries + 1}")

                if attempt < max_retries:
                    logger.info(f"Waiting {retry_after} seconds before retry...")
                    time.sleep(min(retry_after, 20))
                    continue
                else:
                    logger.error("Max retries exceeded for Claude rate limit")
                    raise Exception(f"CLAUDE_RATE_LIMITED: Claude is experiencing high demand. Retry in {retry_after} seconds.")
                
            elif response.status_code == 400:
                logger.error(f"Bad request to Claude API: {response.text}")
                return "There was an issue with your request. Please try rephrasing your question."
                
            else:
                logger.error(f"Claude API error {response.status_code}: {response.text}")
                if attempt < max_retries:
                    logger.info("Retrying after API error...")
                    time.sleep(5)
                    continue
                else:
                    raise Exception("CLAUDE_API_ERROR: I'm having trouble connecting to Claude.")
                    
        except requests.exceptions.Timeout:
            logger.warning(f"Claude API timeout, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                raise Exception("CLAUDE_TIMEOUT: The request took too long.")
                
        except requests.exceptions.ConnectionError:
            logger.warning(f"Claude connection error, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                raise Exception("CLAUDE_CONNECTION_ERROR: I can't connect to Claude right now.")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from Claude API")
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                raise Exception("CLAUDE_API_ERROR: I received an unexpected response.")
                
        except Exception as e:
            error_str = str(e)
            logger.error(f"Unexpected error with Claude API: {e}")
            
            # Re-raise specific Claude errors to trigger fallback
            if any(error_type in error_str for error_type in ["CLAUDE_RATE_LIMITED", "CLAUDE_API_ERROR", "CLAUDE_CONNECTION_ERROR", "CLAUDE_TIMEOUT"]):
                raise e
            
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                raise Exception(f"CLAUDE_API_ERROR: I encountered an unexpected error: {str(e)}")
    
    # If we get here, all retries failed
    raise Exception("CLAUDE_API_ERROR: Claude is currently unavailable after all retries.")

def test_claude_connection() -> Dict:
    """Test Claude API connection."""
    if not validate_claude_config():
        return {
            "status": "error",
            "message": "Claude API key not configured",
            "working": False
        }
    
    try:
        test_messages = [{"role": "user", "content": "Hello, this is a test message for financial advice."}]
        response = claude_generate_response(test_messages)
        
        if response and "error" not in response.lower():
            return {
                "status": "success",
                "message": "Claude connection successful",
                "working": True,
                "response_length": len(response)
            }
        else:
            return {
                "status": "error",
                "message": f"Claude test failed: {response}",
                "working": False
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Claude connection failed: {str(e)}",
            "working": False
        }

def validate_claude_api_key(api_key: str) -> bool:
    """Validate Claude API key format."""
    return api_key and api_key.startswith('sk-ant-') and len(api_key) > 20

if __name__ == "__main__":
    # Test the Claude client
    print("🧪 Testing Claude Client")
    print("=" * 50)
    
    # Test configuration
    if validate_claude_config():
        print("✅ Configuration valid")
        
        # Test connection
        test_result = test_claude_connection()
        print(f"Connection test: {test_result}")
        
        if test_result["working"]:
            # Test actual response
            test_messages = [{"role": "user", "content": "What are the key principles of personal finance?"}]
            response = claude_generate_response(test_messages)
            print(f"Test response: {response[:200]}...")
        
    else:
        print("❌ Configuration invalid")
        print("Please set CLAUDE_API_KEY in your .env file")
        print("Get your API key from: https://console.anthropic.com/")
