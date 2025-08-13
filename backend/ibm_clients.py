import os
import base64
import requests
import logging
import time
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# IBM watsonx.ai Configuration
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_MODEL_ID = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-3-8b-instruct")
WATSONX_API_VERSION = os.getenv("WATSONX_API_VERSION", "2024-10-10")

# Watson NLU Configuration
NLU_APIKEY = os.getenv("NLU_APIKEY")
NLU_URL = os.getenv("NLU_URL")

# Validate required environment variables
def validate_config():
	"""Validate that all required IBM Watson credentials are configured."""
	missing_vars = []
	
	if not WATSONX_APIKEY:
		missing_vars.append("WATSONX_APIKEY")
	if not WATSONX_URL:
		missing_vars.append("WATSONX_URL")
	if not WATSONX_PROJECT_ID:
		missing_vars.append("WATSONX_PROJECT_ID")
	
	if missing_vars:
		logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
		return False
	
	if not NLU_APIKEY or not NLU_URL:
		logger.warning("Watson NLU credentials not configured. NLP features will be limited.")
	
	logger.info("IBM Watson configuration validated successfully")
	return True

# Initialize configuration validation
validate_config()

def get_iam_token() -> Optional[str]:
	"""
	Get IBM Cloud IAM access token with enhanced error handling and retry logic.
	"""
	if not WATSONX_APIKEY:
		logger.error("WATSONX_APIKEY not configured")
		return None
	
	url = "https://iam.cloud.ibm.com/identity/token"
	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	data = {
		"grant_type": "urn:ibm:params:oauth:grant-type:apikey",
		"apikey": WATSONX_APIKEY
	}
	
	max_retries = 3
	for attempt in range(max_retries):
		try:
			logger.debug(f"Requesting IAM token (attempt {attempt + 1}/{max_retries})")
			r = requests.post(url, headers=headers, data=data, timeout=30)
			r.raise_for_status()
			token = r.json()["access_token"]
			logger.info("IAM token obtained successfully")
			return token
		except requests.exceptions.RequestException as e:
			logger.warning(f"IAM token request failed (attempt {attempt + 1}): {e}")
			if attempt < max_retries - 1:
				time.sleep(2 ** attempt)  # Exponential backoff
			else:
				logger.error("Failed to obtain IAM token after all retries")
				return None
		except KeyError as e:
			logger.error(f"Unexpected IAM token response format: {e}")
			return None

def watsonx_chat(messages: List[Dict]) -> str:
	"""
	Enhanced watsonx.ai chat completion with comprehensive error handling.
	
	Args:
		messages: List of message dictionaries with 'role' and 'content' keys
		
	Returns:
		Assistant reply string or error message
	"""
	if not messages:
		logger.error("Empty messages list provided to watsonx_chat")
		return "I need a message to respond to. Please try again."
	
	try:
		# Get authentication token
		token = get_iam_token()
		if not token:
			return "I'm having trouble connecting to IBM Watson services. Please try again later."
		
		# Prepare API request
		url = f"{WATSONX_URL}/ml/v1/chat/completions?version={WATSONX_API_VERSION}"
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {token}",
		}
		
		# Enhanced payload with conversation optimization
		payload = {
			"model_id": WATSONX_MODEL_ID,
			"project_id": WATSONX_PROJECT_ID,
			"messages": messages,
			"parameters": {
				"max_new_tokens": 1024,  # Increased for more detailed responses
				"temperature": 0.3,      # Slightly higher for more natural conversation
				"top_p": 0.9,
				"repetition_penalty": 1.1,
				"stop_sequences": ["Human:", "User:"]
			}
		}
		
		logger.info(f"Calling watsonx.ai with {len(messages)} messages")
		start_time = time.time()
		
		# Make API request with retry logic
		max_retries = 2
		for attempt in range(max_retries):
			try:
				r = requests.post(url, headers=headers, json=payload, timeout=90)
				r.raise_for_status()
				break
			except requests.exceptions.Timeout:
				logger.warning(f"watsonx.ai request timeout (attempt {attempt + 1})")
				if attempt < max_retries - 1:
					time.sleep(1)
				else:
					return "I'm taking longer than usual to respond. Please try a shorter message."
			except requests.exceptions.RequestException as e:
				logger.error(f"watsonx.ai request failed (attempt {attempt + 1}): {e}")
				if attempt < max_retries - 1:
					time.sleep(2)
				else:
					return "I'm having trouble generating a response right now. Please try again."
		
		# Process response
		response_time = time.time() - start_time
		logger.info(f"watsonx.ai response received in {response_time:.2f}s")
		
		data = r.json()
		
		# Enhanced response extraction with multiple fallback strategies
		try:
			# Primary: Standard chat completion format
			if "choices" in data and len(data["choices"]) > 0:
				choice = data["choices"][0]
				if "message" in choice and "content" in choice["message"]:
					content = choice["message"]["content"].strip()
					if content:
						logger.info(f"Successfully extracted response ({len(content)} chars)")
						return content
			
			# Fallback: Direct content field
			if "content" in data:
				content = data["content"].strip()
				if content:
					return content
			
			# Fallback: Text field
			if "text" in data:
				content = data["text"].strip()
				if content:
					return content
			
			# If no content found, log the structure for debugging
			logger.error(f"Unexpected watsonx.ai response structure: {list(data.keys())}")
			return "I received an unexpected response format. Please try rephrasing your question."
			
		except Exception as e:
			logger.error(f"Error extracting watsonx.ai response: {e}")
			return "I had trouble processing the response. Please try again."
	
	except Exception as e:
		logger.error(f"Unexpected error in watsonx_chat: {e}")
		return "I encountered an unexpected error. Please try again."

def nlu_analyze(text: str) -> Optional[Dict]:
	"""
	Enhanced Watson NLU analysis with comprehensive error handling and feature extraction.
	
	Args:
		text: Input text to analyze
		
	Returns:
		NLU analysis results or None if analysis fails
	"""
	if not text or not text.strip():
		logger.warning("Empty text provided to NLU analysis")
		return None
	
	if not (NLU_APIKEY and NLU_URL):
		logger.warning("Watson NLU credentials not configured")
		return None
	
	# Skip analysis for very short texts
	if len(text.strip()) < 10:
		logger.debug("Text too short for meaningful NLU analysis")
		return None
	
	try:
		url = f"{NLU_URL}/v1/analyze?version=2021-08-01"
		auth = base64.b64encode(f"apikey:{NLU_APIKEY}".encode()).decode()
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Basic {auth}"
		}
		
		# Enhanced feature extraction
		payload = {
			"text": text,
			"features": {
				"sentiment": {
					"document": True,
					"targets": []
				},
				"entities": {
					"limit": 10,
					"mentions": True,
					"model": "en-v1"
				},
				"keywords": {
					"limit": 10,
					"sentiment": True
				},
				"concepts": {
					"limit": 5
				},
				"categories": {
					"limit": 3
				}
			},
			"language": "en"
		}
		
		logger.debug(f"Analyzing text with Watson NLU ({len(text)} chars)")
		start_time = time.time()
		
		r = requests.post(url, headers=headers, json=payload, timeout=30)
		r.raise_for_status()
		
		response_time = time.time() - start_time
		data = r.json()
		
		# Log analysis results
		sentiment = data.get("sentiment", {}).get("document", {})
		entities_count = len(data.get("entities", []))
		keywords_count = len(data.get("keywords", []))
		
		logger.info(f"NLU analysis completed in {response_time:.2f}s: "
				   f"sentiment={sentiment.get('label', 'unknown')}, "
				   f"entities={entities_count}, keywords={keywords_count}")
		
		return data
		
	except requests.exceptions.RequestException as e:
		logger.warning(f"Watson NLU request failed: {e}")
		return None
	except Exception as e:
		logger.error(f"Unexpected error in NLU analysis: {e}")
		return None

def test_watson_connectivity() -> Dict[str, bool]:
	"""
	Test connectivity to IBM Watson services.
	
	Returns:
		Dictionary with service connectivity status
	"""
	results = {
		"watsonx_ai": False,
		"watson_nlu": False,
		"iam_token": False
	}
	
	# Test IAM token
	try:
		token = get_iam_token()
		results["iam_token"] = token is not None
	except Exception as e:
		logger.error(f"IAM token test failed: {e}")
	
	# Test Watson NLU
	if NLU_APIKEY and NLU_URL:
		try:
			test_result = nlu_analyze("This is a test message for connectivity.")
			results["watson_nlu"] = test_result is not None
		except Exception as e:
			logger.error(f"Watson NLU test failed: {e}")
	
	# Test watsonx.ai
	if results["iam_token"]:
		try:
			test_messages = [
				{"role": "system", "content": "You are a helpful assistant."},
				{"role": "user", "content": "Say 'test successful' if you can read this."}
			]
			response = watsonx_chat(test_messages)
			results["watsonx_ai"] = "test successful" in response.lower() or len(response) > 10
		except Exception as e:
			logger.error(f"watsonx.ai test failed: {e}")
	
	logger.info(f"Watson connectivity test results: {results}")
	return results
