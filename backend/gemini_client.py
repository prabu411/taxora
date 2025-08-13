"""
Google Gemini API Client
Provides integration with Google's Gemini AI for chat responses and voice interaction.
"""

import os
import logging
import time
import json
import base64
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv
from tamil_voice_enhancer import enhance_tamil_for_voice
import threading
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gemini Configuration with backup key support
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY_BACKUP = os.getenv("GEMINI_API_KEY_BACKUP")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_MAX_TOKENS = int(os.getenv("GEMINI_MAX_TOKENS", "1000"))
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))

# API URLs
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

# Track which API key is currently being used
current_api_key = GEMINI_API_KEY
using_backup_key = False

# Rate limiting configuration
class GeminiRateLimiter:
    """Rate limiter for Gemini API to prevent quota exceeded errors."""

    def __init__(self):
        self.requests_per_minute = 50  # Increased limit - Gemini allows 60/min
        self.requests_per_day = 1500   # Daily limit
        self.request_times = []
        self.daily_requests = {}
        self.lock = threading.Lock()

    def can_make_request(self) -> tuple[bool, str]:
        """Check if we can make a request without hitting rate limits."""
        with self.lock:
            now = datetime.now()
            today = now.date()

            # Clean old request times (older than 1 minute)
            minute_ago = now - timedelta(minutes=1)
            self.request_times = [t for t in self.request_times if t > minute_ago]

            # Check daily limit
            if today not in self.daily_requests:
                self.daily_requests[today] = 0

            # Clean old daily counts
            for date in list(self.daily_requests.keys()):
                if date < today:
                    del self.daily_requests[date]

            # Check limits
            if len(self.request_times) >= self.requests_per_minute:
                wait_time = 60 - (now - self.request_times[0]).seconds
                return False, f"Rate limit: {len(self.request_times)} requests in last minute. Wait {wait_time}s"

            if self.daily_requests[today] >= self.requests_per_day:
                return False, f"Daily quota exceeded: {self.daily_requests[today]} requests today"

            return True, "OK"

    def record_request(self):
        """Record a successful request."""
        with self.lock:
            now = datetime.now()
            today = now.date()

            self.request_times.append(now)
            if today not in self.daily_requests:
                self.daily_requests[today] = 0
            self.daily_requests[today] += 1

    def get_status(self) -> Dict:
        """Get current rate limiting status."""
        with self.lock:
            now = datetime.now()
            today = now.date()
            minute_ago = now - timedelta(minutes=1)

            recent_requests = len([t for t in self.request_times if t > minute_ago])
            daily_requests = self.daily_requests.get(today, 0)

            return {
                "requests_last_minute": recent_requests,
                "requests_today": daily_requests,
                "minute_limit": self.requests_per_minute,
                "daily_limit": self.requests_per_day,
                "minute_remaining": self.requests_per_minute - recent_requests,
                "daily_remaining": self.requests_per_day - daily_requests
            }

# Global rate limiter instance
gemini_rate_limiter = GeminiRateLimiter()

def validate_gemini_config() -> bool:
    """Validate Gemini API configuration."""
    if not GEMINI_API_KEY:
        logger.warning("Gemini API key not configured")
        return False
    
    if not GEMINI_API_KEY.startswith('AIza'):
        logger.warning("Invalid Gemini API key format")
        return False
    
    logger.info("Gemini configuration validated successfully")
    return True

def format_messages_for_gemini(messages: List[Dict]) -> List[Dict]:
    """Format conversation messages for Gemini API."""
    formatted_messages = []
    
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        
        # Convert roles to Gemini format
        if role == "user":
            gemini_role = "user"
        elif role == "assistant" or role == "bot":
            gemini_role = "model"
        else:
            gemini_role = "user"  # Default fallback
        
        formatted_messages.append({
            "role": gemini_role,
            "parts": [{"text": content}]
        })
    
    return formatted_messages

def gemini_generate_response(messages: List[Dict], max_retries: int = 2) -> str:
    """Generate response using Google Gemini API with rate limiting and backup key support."""
    global current_api_key, using_backup_key

    if not validate_gemini_config():
        return "Gemini is not configured. Please add your Google AI API key to use this feature."

    # Check rate limits before making request
    can_request, rate_message = gemini_rate_limiter.can_make_request()
    if not can_request:
        logger.warning(f"Gemini rate limit exceeded: {rate_message}")
        # Try switching to backup key if available
        if not using_backup_key and GEMINI_API_KEY_BACKUP:
            logger.info("Switching to backup Gemini API key")
            current_api_key = GEMINI_API_KEY_BACKUP
            using_backup_key = True
            # Reset rate limiter for new key
            gemini_rate_limiter.reset()
        else:
            raise Exception(f"GEMINI_RATE_LIMITED: {rate_message}")

    for attempt in range(max_retries + 1):
        try:
            # Format messages for Gemini 2.0 Flash
            formatted_messages = format_messages_for_gemini(messages)

            logger.info(f"Sending request to Gemini API (attempt {attempt + 1}/{max_retries + 1}) using {'backup' if using_backup_key else 'primary'} key...")
            start_time = time.time()

            # Prepare API request for Gemini 2.0 Flash
            url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent"

            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": current_api_key
            }
            
            # Add system context to the first user message instead of separate instruction
            if formatted_messages and formatted_messages[0]["role"] == "user":
                original_text = formatted_messages[0]["parts"][0]["text"]
                formatted_messages[0]["parts"][0]["text"] = f"You are a professional financial advisor. Provide helpful, accurate, and practical financial advice. Keep responses concise but informative. Focus on actionable guidance for budgeting, saving, investing, and financial planning.\n\nUser question: {original_text}"

            # Prepare payload for Gemini 2.0 Flash
            payload = {
                "contents": formatted_messages,
                "generationConfig": {
                    "temperature": GEMINI_TEMPERATURE,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": GEMINI_MAX_TOKENS,
                    "stopSequences": []
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            }
            
            # Make API request with new format
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if "candidates" in data and len(data["candidates"]) > 0:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        ai_response = candidate["content"]["parts"][0]["text"].strip()
                        
                        # Record successful request for rate limiting
                        gemini_rate_limiter.record_request()

                        # Log usage statistics
                        usage = data.get("usageMetadata", {})
                        logger.info(f"Gemini response received in {response_time:.2f}s")
                        logger.info(f"Tokens used: {usage.get('totalTokenCount', 'unknown')}")

                        return ai_response
                    else:
                        logger.error("No content in Gemini response")
                        return "I couldn't generate a response. Please try again."
                else:
                    logger.error("No candidates in Gemini response")
                    return "I couldn't generate a response. Please try again."
                    
            elif response.status_code == 401:
                logger.error("Invalid Gemini API key")
                return "Invalid API key. Please check your Google AI configuration."
                
            elif response.status_code == 429:
                retry_after = int(response.headers.get('retry-after', '10'))
                logger.warning(f"Rate limit hit, attempt {attempt + 1}/{max_retries + 1}")

                if attempt < max_retries:
                    logger.info(f"Waiting {retry_after} seconds before retry...")
                    time.sleep(min(retry_after, 20))  # Cap wait time at 20 seconds
                    continue
                else:
                    logger.error("Max retries exceeded for rate limit")
                    # Raise exception to trigger automatic fallback
                    raise Exception(f"GEMINI_RATE_LIMITED: Gemini is experiencing high demand. Retry in {retry_after} seconds.")
                
            elif response.status_code == 400:
                logger.error(f"Bad request to Gemini API: {response.text}")
                return "There was an issue with your request. Please try rephrasing your question."
                
            else:
                logger.error(f"Gemini API error {response.status_code}: {response.text}")
                if attempt < max_retries:
                    logger.info("Retrying after API error...")
                    time.sleep(5)  # Wait 5 seconds before retry
                    continue
                else:
                    # Raise exception to trigger automatic fallback
                    raise Exception("GEMINI_API_ERROR: I'm having trouble connecting to Gemini.")
                    
        except requests.exceptions.Timeout:
            logger.warning(f"Gemini API timeout, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                # Raise exception to trigger automatic fallback
                raise Exception("GEMINI_TIMEOUT: The request took too long.")
                
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error, attempt {attempt + 1}/{max_retries + 1}")
            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                # Raise exception to trigger automatic fallback
                raise Exception("GEMINI_CONNECTION_ERROR: I can't connect to Gemini right now.")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from Gemini API")
            if attempt < max_retries:
                time.sleep(2)
                continue
            else:
                raise Exception("GEMINI_API_ERROR: I received an unexpected response.")

        except Exception as e:
            error_str = str(e)
            logger.error(f"Unexpected error with Gemini API: {e}")

            # Re-raise specific Gemini errors to trigger fallback
            if "GEMINI_RATE_LIMITED" in error_str or "GEMINI_API_ERROR" in error_str or "GEMINI_CONNECTION_ERROR" in error_str or "GEMINI_TIMEOUT" in error_str:
                raise e

            if attempt < max_retries:
                time.sleep(5)
                continue
            else:
                raise Exception(f"GEMINI_API_ERROR: I encountered an unexpected error: {str(e)}")
    
    # If we get here, all retries failed
    raise Exception("GEMINI_API_ERROR: Gemini is currently unavailable after all retries.")

def test_gemini_connection() -> Dict:
    """Test Gemini API connection."""
    if not validate_gemini_config():
        return {
            "status": "error",
            "message": "API key not configured"
        }
    
    try:
        test_messages = [
            {"role": "user", "content": "Hello, can you help with financial advice?"}
        ]
        
        response = gemini_generate_response(test_messages)
        
        if "API key" in response or "error" in response.lower():
            return {
                "status": "error",
                "message": response
            }
        else:
            return {
                "status": "success",
                "message": "Gemini is working correctly"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Connection test failed: {str(e)}"
        }

def gemini_translate_to_tamil(english_text: str) -> Dict:
    """Translate English financial advice to Tamil using Gemini."""
    if not validate_gemini_config():
        return {
            "success": False,
            "error": "Gemini not configured",
            "tamil_text": english_text
        }

    try:
        logger.info("Translating to Tamil using Gemini...")

        # Prepare translation request
        url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent"
        params = {"key": GEMINI_API_KEY}

        translation_prompt = f"""
        Translate the following financial advice from English to Tamil with these requirements:

        1. Use simple, clear Tamil that sounds natural when spoken aloud
        2. Convert numbers to Tamil words (50 = ஐம்பது, 30 = முப்பது, 20 = இருபது)
        3. Use common Tamil financial terms that people understand
        4. Keep sentences shorter for better voice clarity
        5. Add appropriate pauses with punctuation
        6. Make it sound like a Tamil financial advisor speaking

        Financial terms to use:
        - Budget = பட்ஜெட் or வரவு செலவு திட்டம்
        - Savings = சேமிப்பு
        - Investment = முதலீடு
        - Emergency fund = அவசர நிதி
        - Income = வருமானம்
        - Expenses = செலவுகள்
        - Percent = சதவீதம்

        English text: {english_text}

        Natural Tamil translation for voice:
        """

        payload = {
            "contents": [{
                "parts": [{"text": translation_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,  # Lower temperature for accurate translation
                "maxOutputTokens": 1000
            }
        }

        response = requests.post(url, params=params, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    tamil_text = candidate["content"]["parts"][0]["text"].strip()

                    logger.info(f"Translation completed: {tamil_text[:50]}...")

                    return {
                        "success": True,
                        "tamil_text": tamil_text,
                        "english_text": english_text
                    }

        logger.error(f"Translation failed: {response.status_code}")
        return {
            "success": False,
            "error": f"API error: {response.status_code}",
            "tamil_text": english_text
        }

    except Exception as e:
        logger.error(f"Translation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "tamil_text": english_text
        }

def validate_gemini_api_key(api_key: str) -> bool:
    """Validate Gemini API key format."""
    return api_key and api_key.startswith('AIza') and len(api_key) > 20

def get_gemini_rate_limit_status() -> Dict:
    """Get current Gemini rate limit status."""
    return gemini_rate_limiter.get_status()

def gemini_speech_to_text(audio_data: bytes, audio_format: str = "webm") -> Dict:
    """Convert speech to text using Gemini's multimodal capabilities."""
    if not validate_gemini_config():
        return {
            "success": False,
            "error": "Gemini not configured",
            "text": ""
        }

    try:
        logger.info("Converting speech to text using Gemini...")

        # Encode audio data to base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        # Prepare API request for speech recognition
        url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent"
        params = {"key": GEMINI_API_KEY}

        payload = {
            "contents": [{
                "parts": [
                    {
                        "text": "Please transcribe this audio to text. Only return the transcribed text, nothing else."
                    },
                    {
                        "inline_data": {
                            "mime_type": f"audio/{audio_format}",
                            "data": audio_base64
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.1,  # Low temperature for accurate transcription
                "maxOutputTokens": 500
            }
        }

        response = requests.post(url, params=params, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    transcribed_text = candidate["content"]["parts"][0]["text"].strip()

                    logger.info(f"Speech transcribed successfully: {transcribed_text[:50]}...")

                    return {
                        "success": True,
                        "text": transcribed_text,
                        "confidence": 0.95  # Gemini typically has high confidence
                    }

        logger.error(f"Speech to text failed: {response.status_code}")
        return {
            "success": False,
            "error": f"API error: {response.status_code}",
            "text": ""
        }

    except Exception as e:
        logger.error(f"Speech to text error: {e}")
        return {
            "success": False,
            "error": str(e),
            "text": ""
        }

def gemini_text_to_speech(text: str, language: str = "en") -> Dict:
    """Convert text to speech with enhanced Tamil voice support."""
    try:
        # Clean text for better speech synthesis
        clean_text = text.replace('[', '').replace(']', '').replace('*', '').strip()

        if language == "en":
            # Optimize English text for speech
            speech_optimized_text = clean_text.replace('50/30/20', 'fifty thirty twenty')
            speech_optimized_text = speech_optimized_text.replace('%', ' percent')
            speech_optimized_text = speech_optimized_text.replace('$', ' dollars ')

            voice_config = {
                "voice_name": "Google US English",
                "language": "en-US",
                "speed": 0.9,
                "pitch": 1.0,
                "volume": 0.8
            }
        elif language == "ta":
            # Use enhanced Tamil voice processing
            try:
                tamil_enhancement = enhance_tamil_for_voice(clean_text)

                if tamil_enhancement["success"]:
                    speech_optimized_text = tamil_enhancement["enhanced_text"]
                    voice_config = tamil_enhancement["voice_settings"]

                    # Add additional optimizations
                    voice_config.update({
                        "voice_name": "Tamil India Enhanced",
                        "voice_uri": "ta-IN-Wavenet-A",
                        "ssml_gender": "FEMALE",
                        "enhanced": True,
                        "ssml": tamil_enhancement["ssml"]
                    })

                    logger.info(f"Enhanced Tamil text: {speech_optimized_text[:100]}...")
                else:
                    # Fallback to basic Tamil processing
                    speech_optimized_text = clean_text
                    speech_optimized_text = speech_optimized_text.replace('50/30/20', 'ஐம்பது முப்பது இருபது விதி')
                    speech_optimized_text = speech_optimized_text.replace('%', ' சதவீதம்')
                    speech_optimized_text = speech_optimized_text.replace('$', ' டாலர் ')

                    voice_config = {
                        "voice_name": "Tamil India Basic",
                        "language": "ta-IN",
                        "speed": 0.6,
                        "pitch": 1.2,
                        "volume": 0.9,
                        "enhanced": False
                    }

            except Exception as e:
                logger.error(f"Tamil enhancement failed: {e}")
                # Basic fallback
                speech_optimized_text = clean_text
                voice_config = {
                    "voice_name": "Tamil India Fallback",
                    "language": "ta-IN",
                    "speed": 0.6,
                    "pitch": 1.2,
                    "volume": 0.9,
                    "enhanced": False
                }
        else:
            # Default to English
            speech_optimized_text = clean_text
            voice_config = {
                "voice_name": "Google US English",
                "language": "en-US",
                "speed": 0.9,
                "pitch": 1.0,
                "volume": 0.8
            }

        return {
            "success": True,
            "text": speech_optimized_text,
            "audio_url": None,  # Will use enhanced browser TTS
            "voice_config": voice_config,
            "language": language,
            "enhanced_tamil": language == "ta"
        }

    except Exception as e:
        logger.error(f"Text to speech preparation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "text": text
        }

def gemini_voice_chat(audio_data: bytes, conversation_history: List[Dict] = None, include_tamil: bool = True) -> Dict:
    """Complete voice chat pipeline with Tamil support and rate limit handling."""
    try:
        logger.info("Starting Gemini voice chat pipeline with Tamil support...")

        # Check rate limits before starting
        can_request, rate_message = gemini_rate_limiter.can_make_request()
        if not can_request:
            logger.warning(f"Gemini voice chat blocked by rate limits: {rate_message}")
            # Raise exception to trigger proper fallback handling
            raise Exception(f"GEMINI_RATE_LIMITED: {rate_message}")

        # Step 1: Convert speech to text
        stt_result = gemini_speech_to_text(audio_data)

        if not stt_result["success"]:
            return {
                "success": False,
                "error": "Speech recognition failed",
                "user_text": "",
                "ai_response": "",
                "tamil_response": "",
                "speech_config": None
            }

        user_text = stt_result["text"]
        logger.info(f"User said: {user_text}")

        # Step 2: Generate Gemini response in English with rate limit handling
        messages = conversation_history or []
        messages.append({"role": "user", "content": user_text})

        ai_response = gemini_generate_response(messages)

        # Check if response indicates rate limiting
        if "rate limit" in ai_response.lower() or "temporarily unavailable" in ai_response.lower():
            return {
                "success": False,
                "error": "Gemini rate limit exceeded during voice chat",
                "user_text": user_text,
                "ai_response": ai_response,
                "tamil_response": "",
                "speech_config": None,
                "fallback_recommended": True
            }

        # Step 3: Translate to Tamil if requested
        tamil_response = ""
        if include_tamil:
            translation_result = gemini_translate_to_tamil(ai_response)
            if translation_result["success"]:
                tamil_response = translation_result["tamil_text"]
                logger.info("Tamil translation completed")
            else:
                logger.warning("Tamil translation failed, using English only")

        # Step 4: Prepare for text-to-speech (English)
        tts_english = gemini_text_to_speech(ai_response, "en")

        # Step 5: Prepare for text-to-speech (Tamil)
        tts_tamil = None
        if tamil_response:
            tts_tamil = gemini_text_to_speech(tamil_response, "ta")

        return {
            "success": True,
            "user_text": user_text,
            "ai_response": ai_response,
            "tamil_response": tamil_response,
            "speech_config_english": tts_english.get("voice_config"),
            "speech_config_tamil": tts_tamil.get("voice_config") if tts_tamil else None,
            "optimized_speech_text_english": tts_english.get("text", ai_response),
            "optimized_speech_text_tamil": tts_tamil.get("text", tamil_response) if tts_tamil else ""
        }

    except Exception as e:
        logger.error(f"Voice chat pipeline error: {e}")
        return {
            "success": False,
            "error": str(e),
            "user_text": "",
            "ai_response": "",
            "tamil_response": "",
            "speech_config": None
        }
