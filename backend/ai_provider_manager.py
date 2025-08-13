"""
AI Provider Manager for Taxora
Manages multiple AI providers and handles switching between them.
"""

import os
import logging
from typing import List, Dict, Optional
from enum import Enum
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import AI clients
from granite_client import granite_chat, validate_config as validate_granite_config
from gemini_client import gemini_generate_response, validate_gemini_config, test_gemini_connection
from huggingface_client import huggingface_generate_response, validate_huggingface_config, test_huggingface_connectivity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIProvider(Enum):
    """Available AI providers."""
    GRANITE = "granite"
    GEMINI = "gemini"
    HUGGINGFACE = "huggingface"

# Configuration
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "granite")
ALLOW_AI_SWITCHING = os.getenv("ALLOW_AI_SWITCHING", "true").lower() == "true"

class AIProviderManager:
    """Manages AI provider selection and routing."""
    
    def __init__(self):
        self.current_provider = DEFAULT_AI_PROVIDER
        self.available_providers = self._get_available_providers()
        logger.info(f"AI Provider Manager initialized with default: {self.current_provider}")
        logger.info(f"Available providers: {list(self.available_providers.keys())}")
    
    def _get_available_providers(self) -> Dict[str, Dict]:
        """Get list of available and configured AI providers."""
        providers = {}
        
        # Check IBM Granite
        try:
            granite_status = validate_granite_config()
            providers["granite"] = {
                "name": "IBM Granite",
                "description": "Lightweight local AI model (fast, free, offline)",
                "status": "available" if granite_status else "error",
                "features": ["Local processing", "No API costs", "Fast responses"],
                "requires_api_key": False
            }
        except Exception as e:
            providers["granite"] = {
                "name": "IBM Granite",
                "description": "Lightweight local AI model",
                "status": "error",
                "error": str(e),
                "requires_api_key": False
            }
        
        # Check Google Gemini
        try:
            gemini_status = validate_gemini_config()
            providers["gemini"] = {
                "name": "Google Gemini",
                "description": "Google's advanced Gemini AI with generous free quota",
                "status": "available" if gemini_status else "not_configured",
                "features": ["Advanced reasoning", "Multimodal capabilities", "High quality responses", "Free quota"],
                "requires_api_key": True
            }
        except Exception as e:
            providers["gemini"] = {
                "name": "Google Gemini",
                "description": "Google's advanced Gemini AI with generous free quota",
                "status": "error",
                "error": str(e),
                "requires_api_key": True
            }

        # Check Hugging Face
        try:
            huggingface_status = validate_huggingface_config()
            providers["huggingface"] = {
                "name": "Hugging Face (Multiple Models)",
                "description": "Access to multiple AI models through Hugging Face Inference API",
                "status": "available" if huggingface_status else "not_configured",
                "features": ["Multiple models", "DialoGPT", "BlenderBot", "Free tier available", "Open source models"],
                "requires_api_key": True
            }
        except Exception as e:
            providers["huggingface"] = {
                "name": "Hugging Face (Multiple Models)",
                "description": "Access to multiple AI models through Hugging Face Inference API",
                "status": "error",
                "error": str(e),
                "requires_api_key": True
            }



        return providers
    
    def get_provider_status(self) -> Dict:
        """Get current provider status and available options."""
        return {
            "current_provider": self.current_provider,
            "allow_switching": ALLOW_AI_SWITCHING,
            "available_providers": self.available_providers,
            "provider_count": len([p for p in self.available_providers.values() if p["status"] == "available"])
        }

    def get_available_providers(self) -> Dict:
        """Get available providers in the expected format."""
        return {
            "success": True,
            "data": {
                "available_providers": self.available_providers,
                "current_provider": self.current_provider
            }
        }

    def set_provider(self, provider: str) -> Dict:
        """Set the current AI provider."""
        if not ALLOW_AI_SWITCHING:
            return {
                "success": False,
                "message": "AI provider switching is disabled",
                "current_provider": self.current_provider
            }
        
        if provider not in self.available_providers:
            return {
                "success": False,
                "message": f"Unknown AI provider: {provider}",
                "current_provider": self.current_provider
            }
        
        provider_info = self.available_providers[provider]
        if provider_info["status"] != "available":
            return {
                "success": False,
                "message": f"AI provider {provider} is not available: {provider_info.get('error', 'Not configured')}",
                "current_provider": self.current_provider
            }
        
        old_provider = self.current_provider
        self.current_provider = provider
        
        logger.info(f"AI provider switched from {old_provider} to {provider}")
        
        return {
            "success": True,
            "message": f"Switched to {provider_info['name']}",
            "previous_provider": old_provider,
            "current_provider": self.current_provider
        }
    
    def generate_response(self, messages: List[Dict], provider: Optional[str] = None, auto_fallback: bool = True) -> Dict:
        """Generate response using the specified or current AI provider with automatic fallback."""
        # Use specified provider or current default
        active_provider = provider if provider else self.current_provider

        if active_provider not in self.available_providers:
            return {
                "success": False,
                "response": f"Unknown AI provider: {active_provider}",
                "provider": active_provider,
                "error": "invalid_provider"
            }

        provider_info = self.available_providers[active_provider]
        if provider_info["status"] != "available":
            return {
                "success": False,
                "response": f"AI provider {active_provider} is not available. Please check configuration.",
                "provider": active_provider,
                "error": "provider_unavailable"
            }

        try:
            logger.info(f"Generating response using {provider_info['name']}")

            # Route to appropriate AI provider
            if active_provider == "granite":
                response = granite_chat(messages)
            elif active_provider == "gemini":
                response = gemini_generate_response(messages)
            elif active_provider == "huggingface":
                response = huggingface_generate_response(messages)
            else:
                return {
                    "success": False,
                    "response": f"Provider {active_provider} not implemented yet",
                    "provider": active_provider,
                    "error": "not_implemented"
                }

            # Check if response indicates actual API errors (not content about rate limits)
            # Only trigger fallback for actual API error responses, not content that mentions rate limits
            api_quota_exceeded = (
                "quota exceeded" in response.lower() and len(response) < 200 and
                ("check your plan" in response.lower() or "billing" in response.lower())
            )
            api_rate_limited = (
                "temporarily unavailable" in response.lower() and len(response) < 200 and
                "gemini" in response.lower()
            )

            if api_quota_exceeded or api_rate_limited:
                if auto_fallback and active_provider == "gemini" and "granite" in self.available_providers:
                    if api_quota_exceeded:
                        logger.warning("Gemini API quota exceeded, falling back to IBM Granite")
                        fallback_message = "[Gemini quota exceeded - check quota at https://aistudio.google.com/app/apikey]"
                    else:
                        logger.info("Gemini API temporarily unavailable, falling back to IBM Granite")
                        fallback_message = "[Switched to IBM Granite due to Gemini API unavailability]"

                    fallback_response = granite_chat(messages)
                    return {
                        "success": True,
                        "response": f"{fallback_message}\n\n{fallback_response}",
                        "provider": "granite",
                        "provider_name": "IBM Granite (Fallback)",
                        "fallback_used": True,
                        "original_provider": active_provider,
                        "fallback_reason": "quota_exceeded" if api_quota_exceeded else "api_unavailable"
                    }

            return {
                "success": True,
                "response": response,
                "provider": active_provider,
                "provider_name": provider_info["name"]
            }

        except Exception as e:
            error_str = str(e)
            logger.error(f"Error generating response with {active_provider}: {e}")

            # Handle specific provider errors with intelligent fallback
            provider_errors = {
                "GEMINI": ["GEMINI_RATE_LIMITED", "GEMINI_API_ERROR", "GEMINI_CONNECTION_ERROR", "GEMINI_TIMEOUT"],
                "HUGGINGFACE": ["HUGGINGFACE_RATE_LIMITED", "HUGGINGFACE_API_ERROR", "HUGGINGFACE_CONNECTION_ERROR", "HUGGINGFACE_TIMEOUT"]
            }

            # Check if this is a known provider error
            failed_provider = None
            for provider, error_types in provider_errors.items():
                if any(error_type in error_str for error_type in error_types):
                    failed_provider = provider.lower()
                    break

            if failed_provider and auto_fallback and "granite" in self.available_providers and self.available_providers["granite"]["status"] == "available":
                try:
                    if "RATE_LIMITED" in error_str:
                        logger.info(f"{failed_provider.title()} rate limited, falling back to IBM Granite")
                        fallback_message = f"[Switched to IBM Granite due to {failed_provider.title()} rate limits]"
                    else:
                        logger.info(f"{failed_provider.title()} error, falling back to IBM Granite")
                        fallback_message = f"[Switched to IBM Granite due to {failed_provider.title()} unavailability]"

                    fallback_response = granite_chat(messages)
                    return {
                        "success": True,
                        "response": f"{fallback_message}\n\n{fallback_response}",
                        "provider": "granite",
                        "provider_name": "IBM Granite (Fallback)",
                        "fallback_used": True,
                        "original_provider": active_provider,
                        "fallback_reason": f"{failed_provider}_error"
                    }
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")

                # If no fallback available, return appropriate message
                if "RATE_LIMITED" in error_str:
                    return {
                        "success": False,
                        "response": f"{failed_provider.title()} is temporarily rate limited. Please try again later or switch to IBM Granite.",
                        "provider": active_provider,
                        "error": "rate_limited"
                    }
                else:
                    return {
                        "success": False,
                        "response": f"{failed_provider.title()} is temporarily unavailable. Please try again later or switch to IBM Granite.",
                        "provider": active_provider,
                        "error": "gemini_unavailable"
                    }

            # Try fallback if enabled and other error occurred with Gemini
            if auto_fallback and active_provider == "gemini" and "granite" in self.available_providers:
                try:
                    logger.info("Gemini failed, falling back to IBM Granite")
                    fallback_response = granite_chat(messages)
                    return {
                        "success": True,
                        "response": f"[Switched to IBM Granite due to Gemini error]\n\n{fallback_response}",
                        "provider": "granite",
                        "provider_name": "IBM Granite (Fallback)",
                        "fallback_used": True,
                        "original_provider": active_provider,
                        "fallback_reason": "error"
                    }
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")

            return {
                "success": False,
                "response": f"Error generating response: {str(e)}",
                "provider": active_provider,
                "error": "generation_error"
            }
    
    def test_all_providers(self) -> Dict:
        """Test all available AI providers."""
        results = {}
        
        for provider_id, provider_info in self.available_providers.items():
            if provider_info["status"] == "available":
                try:
                    if provider_id == "granite":
                        test_messages = [{"role": "user", "content": "Hello, test message"}]
                        response = granite_chat(test_messages)
                        results[provider_id] = {
                            "status": "success",
                            "response_length": len(response),
                            "working": True
                        }
                    elif provider_id == "gemini":
                        test_result = test_gemini_connection()
                        results[provider_id] = test_result
                    
                except Exception as e:
                    results[provider_id] = {
                        "status": "error",
                        "message": str(e),
                        "working": False
                    }
            else:
                results[provider_id] = {
                    "status": provider_info["status"],
                    "message": provider_info.get("error", "Not configured"),
                    "working": False
                }
        
        return results

# Global AI provider manager instance
ai_manager = AIProviderManager()

def get_ai_manager() -> AIProviderManager:
    """Get the global AI provider manager instance."""
    return ai_manager

if __name__ == "__main__":
    # Test the AI provider manager
    print("🧪 Testing AI Provider Manager")
    print("=" * 50)
    
    manager = AIProviderManager()
    
    # Show status
    status = manager.get_provider_status()
    print(f"Status: {status}")
    
    # Test all providers
    test_results = manager.test_all_providers()
    print(f"Test Results: {test_results}")
    
    # Test response generation
    test_messages = [{"role": "user", "content": "I need help with budgeting"}]
    response = manager.generate_response(test_messages)
    print(f"Response: {response}")
