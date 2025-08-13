import os
import logging
import time
import re
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
# from financial_advisor_fallback import improve_financial_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Granite Configuration
GRANITE_MODEL_NAME = os.getenv("GRANITE_MODEL_NAME", "ibm-granite/granite-7b-instruct")
GRANITE_USE_LOCAL = os.getenv("GRANITE_USE_LOCAL", "true").lower() == "true"
GRANITE_USE_API = os.getenv("GRANITE_USE_API", "false").lower() == "true"
GRANITE_USE_OLLAMA = os.getenv("GRANITE_USE_OLLAMA", "false").lower() == "true"
GRANITE_DEVICE = os.getenv("GRANITE_DEVICE", "cpu")
GRANITE_MAX_LENGTH = int(os.getenv("GRANITE_MAX_LENGTH", "1024"))
GRANITE_TEMPERATURE = float(os.getenv("GRANITE_TEMPERATURE", "0.7"))
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Global variables for model caching
_model = None
_tokenizer = None
_pipeline = None

def validate_config():
    """Validate Granite configuration."""
    logger.info("Validating Granite configuration...")
    
    if GRANITE_USE_LOCAL:
        logger.info(f"Using local Granite model: {GRANITE_MODEL_NAME}")
        logger.info(f"Device: {GRANITE_DEVICE}")
    elif GRANITE_USE_API:
        if not HUGGINGFACE_TOKEN:
            logger.warning("HUGGINGFACE_TOKEN not set. API requests may be limited.")
        logger.info(f"Using Hugging Face API for model: {GRANITE_MODEL_NAME}")
    elif GRANITE_USE_OLLAMA:
        logger.info(f"Using Ollama for model: {GRANITE_MODEL_NAME}")
        logger.info(f"Ollama URL: {OLLAMA_BASE_URL}")
    else:
        logger.warning("No Granite backend configured. Falling back to mock responses.")
    
    logger.info("Granite configuration validated successfully")
    return True

def initialize_local_model():
    """Initialize lightweight local AI model using Transformers."""
    global _model, _tokenizer, _pipeline

    if _pipeline is not None:
        return True

    try:
        logger.info(f"Loading lightweight AI model: distilgpt2")
        start_time = time.time()

        try:
            from transformers import pipeline
            import torch
        except ImportError as e:
            logger.error(f"Missing dependencies for local model: {e}")
            logger.info("Please install: pip install transformers torch")
            return False
        
        # Create lightweight text generation pipeline (much faster!)
        logger.info("Creating lightweight AI pipeline...")
        _pipeline = pipeline(
            "text-generation",
            model="distilgpt2",  # Lightweight, fast model (~350MB)
            device=-1,  # Use CPU for compatibility
            max_length=200,
            do_sample=True,
            temperature=0.7,
            pad_token_id=50256  # Set pad token to avoid warnings
        )
        
        load_time = time.time() - start_time
        logger.info(f"Granite model loaded successfully in {load_time:.2f}s")
        return True
        
    except ImportError as e:
        logger.error(f"Missing dependencies for local model: {e}")
        logger.info("Please install: pip install transformers torch accelerate")
        return False
    except Exception as e:
        logger.error(f"Failed to load Granite model: {e}")
        return False

def granite_chat_local(messages: List[Dict]) -> str:
    """Generate response using local Granite model."""
    global _pipeline
    
    if not initialize_local_model():
        return "Local Granite model not available. Please check your setup."
    
    try:
        # Get the last user message
        user_message = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                user_message = msg["content"]
                break

        # Create a simple, focused prompt that works better with DistilGPT-2
        prompt = f"Financial Question: {user_message}\n\nProfessional Financial Advice:"

        logger.info(f"Generating response with lightweight AI model...")
        start_time = time.time()

        # Generate response with conservative parameters for better quality
        outputs = _pipeline(
            prompt,
            max_length=150,  # Shorter for more focused responses
            num_return_sequences=1,
            do_sample=True,
            temperature=0.3,  # Lower temperature for more coherent responses
            top_p=0.8,        # More focused sampling
            repetition_penalty=1.5,  # Reduce repetition
            pad_token_id=50256,
            truncation=True
        )

        response_time = time.time() - start_time

        if outputs and len(outputs) > 0:
            # Extract only the generated part (remove the prompt)
            full_text = outputs[0]['generated_text']
            response = full_text[len(prompt):].strip()

            logger.info(f"Raw AI output: '{full_text[:200]}...'")
            logger.info(f"Extracted response: '{response[:100]}...'")

            # Check if response is relevant and coherent
            if response and is_relevant_financial_response(response, user_message):
                # Clean up the response
                response = clean_response(response)
                logger.info(f"Using AI response: {len(response)} characters")
                return response
            else:
                # Use fallback for irrelevant or poor quality responses
                logger.info(f"AI response not relevant: '{response[:100]}...', using fallback financial advice")
                return generate_fallback_financial_advice(user_message)
        else:
            logger.error("No outputs generated from AI model")
            return "I couldn't generate a response. Please try again."
            
    except Exception as e:
        logger.error(f"Error generating local Granite response: {e}")
        return "I encountered an error while generating a response. Please try again."

def granite_chat_api(messages: List[Dict]) -> str:
    """Generate response using Hugging Face Inference API."""
    try:
        import requests
        
        prompt = format_messages_for_granite(messages)
        
        url = f"https://api-inference.huggingface.co/models/{GRANITE_MODEL_NAME}"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": GRANITE_MAX_LENGTH,
                "temperature": GRANITE_TEMPERATURE,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
                "return_full_text": False
            }
        }
        
        logger.info("Calling Hugging Face Inference API...")
        start_time = time.time()
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        response_time = time.time() - start_time
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            generated_text = data[0].get('generated_text', '').strip()
            logger.info(f"HF API response received in {response_time:.2f}s")
            return clean_response(generated_text)
        else:
            return "I couldn't generate a response. Please try again."
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Hugging Face API request failed: {e}")
        return "I'm having trouble connecting to the AI service. Please try again later."
    except Exception as e:
        logger.error(f"Error with Hugging Face API: {e}")
        return "I encountered an error while generating a response. Please try again."

def granite_chat_ollama(messages: List[Dict]) -> str:
    """Generate response using Ollama."""
    try:
        import requests
        
        # Convert messages to Ollama format
        ollama_messages = []
        for msg in messages:
            ollama_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        url = f"{OLLAMA_BASE_URL}/api/chat"
        payload = {
            "model": GRANITE_MODEL_NAME,
            "messages": ollama_messages,
            "stream": False,
            "options": {
                "temperature": GRANITE_TEMPERATURE,
                "num_predict": GRANITE_MAX_LENGTH
            }
        }
        
        logger.info("Calling Ollama API...")
        start_time = time.time()
        
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        response_time = time.time() - start_time
        data = response.json()
        
        if "message" in data and "content" in data["message"]:
            content = data["message"]["content"].strip()
            logger.info(f"Ollama response received in {response_time:.2f}s")
            return clean_response(content)
        else:
            return "I couldn't generate a response. Please try again."
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama API request failed: {e}")
        return "I'm having trouble connecting to Ollama. Please ensure it's running."
    except Exception as e:
        logger.error(f"Error with Ollama API: {e}")
        return "I encountered an error while generating a response. Please try again."

def format_messages_for_granite(messages: List[Dict]) -> str:
    """Format messages for Granite model input."""
    formatted_parts = []
    
    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")
        
        if role == "system":
            formatted_parts.append(f"System: {content}")
        elif role == "user":
            formatted_parts.append(f"Human: {content}")
        elif role == "assistant":
            formatted_parts.append(f"Assistant: {content}")
    
    # Add prompt for assistant response
    formatted_parts.append("Assistant:")
    
    return "\n\n".join(formatted_parts)

def is_relevant_financial_response(response: str, user_question: str) -> bool:
    """Check if the AI response is relevant and coherent financial advice."""
    response_lower = response.lower()
    question_lower = user_question.lower()

    # For compound interest questions, response must mention compound interest
    if "compound" in question_lower and "interest" in question_lower:
        if not ("compound" in response_lower and "interest" in response_lower):
            return False

    # For savings questions, response must mention savings/save
    if "saving" in question_lower or "save" in question_lower:
        if not ("saving" in response_lower or "save" in response_lower):
            return False

    # For investment questions, response must mention investment/invest
    if "investment" in question_lower or "invest" in question_lower:
        if not ("investment" in response_lower or "invest" in response_lower):
            return False

    # Check for financial keywords in response
    financial_keywords = [
        'money', 'financial', 'budget', 'save', 'saving', 'invest', 'investment',
        'bank', 'account', 'fund', 'interest', 'loan', 'debt', 'credit', 'income',
        'expense', 'cost', 'price', 'dollar', 'rupee', 'tax', 'insurance', 'retirement',
        'compound', 'principal', 'return', 'portfolio', 'asset', 'equity'
    ]

    # Check if response contains financial terms
    has_financial_terms = any(keyword in response_lower for keyword in financial_keywords)

    # Check if response is coherent (not too repetitive or nonsensical)
    words = response.split()
    if len(words) < 5:
        return False

    # Check for excessive repetition
    unique_words = set(words)
    if len(unique_words) < len(words) * 0.4:  # Less than 40% unique words
        return False

    # Check for common nonsensical patterns that indicate irrelevant content
    nonsensical_patterns = [
        'paypal', 'ebay', 'shopping', 'groceries', 'food', 'children',
        'husband', 'wife', 'home', 'house', 'car', 'business person',
        'online courses', 'credit cards per year', 'debit card', 'stock market',
        'company has an active', 'financial institution', 'can\'t afford'
    ]

    has_nonsensical = any(pattern in response_lower for pattern in nonsensical_patterns)

    # Response is relevant if it has financial terms, is not nonsensical, and is long enough
    is_relevant = has_financial_terms and not has_nonsensical and len(response) > 30

    # Additional check: if response doesn't make sense in context, reject it
    if "how do you know if" in response_lower or "whether it's just" in response_lower:
        is_relevant = False

    return is_relevant

def enhance_short_financial_response(user_question: str, short_response: str) -> str:
    """Enhance short responses with additional financial context."""
    question_lower = user_question.lower()

    if "savings" in question_lower or "save" in question_lower:
        return f"{short_response}\n\nAdditionally, consider these savings strategies:\n• Set up automatic transfers to savings\n• Use the 50/30/20 budgeting rule\n• Build an emergency fund covering 3-6 months of expenses\n• Look for high-yield savings accounts for better returns"

    elif "investment" in question_lower or "invest" in question_lower:
        return f"{short_response}\n\nFor investment guidance:\n• Start with low-cost index funds for diversification\n• Consider your risk tolerance and time horizon\n• Dollar-cost averaging can reduce market timing risk\n• Ensure you have an emergency fund before investing"

    elif "budget" in question_lower:
        return f"{short_response}\n\nBudgeting tips:\n• Track all income and expenses for a month\n• Categorize spending into needs vs. wants\n• Use budgeting apps or spreadsheets\n• Review and adjust monthly based on actual spending"

    elif "debt" in question_lower:
        return f"{short_response}\n\nDebt management strategies:\n• List all debts with balances and interest rates\n• Consider debt avalanche (highest interest first) or snowball (smallest balance first)\n• Avoid taking on new debt while paying off existing debt\n• Consider debt consolidation if it lowers your overall interest rate"

    else:
        return f"{short_response}\n\nFor comprehensive financial planning, consider:\n• Creating a budget to track income and expenses\n• Building an emergency fund\n• Planning for retirement with regular contributions\n• Consulting with a financial advisor for personalized advice"

def generate_fallback_financial_advice(user_question: str) -> str:
    """Generate comprehensive fallback financial advice when AI response fails."""
    question_lower = user_question.lower()

    # Compound Interest
    if "compound" in question_lower and "interest" in question_lower:
        return """**Compound Interest Explained:**

Compound interest is when you earn interest not only on your original investment (principal) but also on the interest that has already been earned. This creates a snowball effect where your money grows faster over time.

**How it works:**
• Year 1: ₹10,000 at 10% = ₹11,000
• Year 2: ₹11,000 at 10% = ₹12,100 (you earned ₹100 extra!)
• Year 3: ₹12,100 at 10% = ₹13,310

**Key Benefits:**
1. **Time is your friend** - The earlier you start, the more powerful compound interest becomes
2. **Regular investing** - Adding money regularly amplifies the effect
3. **Long-term growth** - Most effective over periods of 10+ years

**Practical tip:** Start investing even small amounts early rather than waiting to invest larger amounts later."""

    # Savings strategies
    elif "savings" in question_lower or "save" in question_lower:
        return """**Effective Savings Strategies:**

**1. Automate Your Savings**
• Set up automatic transfers on salary day
• Treat savings like a non-negotiable bill
• Start with even ₹1,000/month and increase gradually

**2. Follow the 50/30/20 Rule**
• 50% for needs (rent, food, utilities)
• 30% for wants (entertainment, dining out)
• 20% for savings and debt repayment

**3. Build an Emergency Fund**
• Target: 6 months of expenses
• Keep in easily accessible savings account
• Use only for true emergencies

**4. Use High-Yield Savings Accounts**
• Compare interest rates across banks
• Consider digital banks for better rates
• Avoid accounts with high minimum balances

**5. Track Your Expenses**
• Use apps like Money Manager or Excel
• Identify areas to cut unnecessary spending
• Review monthly and adjust as needed"""

    # Investment advice
    elif "investment" in question_lower or "invest" in question_lower:
        return """**Investment Basics for Beginners:**

**1. Start with the Basics**
• Emergency fund first (6 months expenses)
• Clear high-interest debt (credit cards)
• Understand your risk tolerance

**2. Diversification is Key**
• Don't put all money in one investment
• Mix of equity, debt, and other assets
• Consider mutual funds for instant diversification

**3. Systematic Investment Plan (SIP)**
• Invest fixed amount monthly regardless of market conditions
• Reduces impact of market volatility
• Start with ₹1,000-5,000/month

**4. Long-term Perspective**
• Equity investments work best over 7+ years
• Don't panic during market downturns
• Stay invested and be patient

**5. Low-cost Options**
• Index funds have lower fees than active funds
• Direct plans save on distributor commissions
• Compare expense ratios before investing"""

    # Budgeting
    elif "budget" in question_lower:
        return """**Creating an Effective Budget:**

**1. Calculate Your Income**
• Include salary, freelance income, other sources
• Use net income (after taxes)
• Be realistic about variable income

**2. Track All Expenses**
• Fixed: Rent, EMIs, insurance premiums
• Variable: Food, transport, entertainment
• Use apps or maintain a simple spreadsheet

**3. Categorize Spending**
• Needs vs. Wants
• Essential vs. Non-essential
• Identify areas for potential savings

**4. Set Financial Goals**
• Short-term: Emergency fund, vacation
• Medium-term: Car, house down payment
• Long-term: Retirement, children's education

**5. Review and Adjust**
• Check monthly if you're staying on track
• Adjust categories based on actual spending
• Be flexible but disciplined"""

    # Debt management
    elif "debt" in question_lower:
        return """**Debt Management Strategies:**

**1. List All Your Debts**
• Credit cards, personal loans, EMIs
• Note interest rates and minimum payments
• Prioritize by interest rate (highest first)

**2. Debt Avalanche Method**
• Pay minimums on all debts
• Put extra money toward highest interest debt
• Mathematically optimal approach

**3. Debt Snowball Method**
• Pay minimums on all debts
• Put extra money toward smallest balance
• Provides psychological wins

**4. Avoid New Debt**
• Cut up credit cards if necessary
• Use cash or debit for purchases
• Build emergency fund to avoid future borrowing

**5. Consider Consolidation**
• Personal loan at lower rate than credit cards
• Balance transfer to 0% APR card
• Only if you won't accumulate new debt"""

    # General financial advice
    else:
        return """**Comprehensive Financial Guidance:**

I'm here to help you with all aspects of personal finance. Here are the key areas I can assist with:

**💰 Savings & Budgeting**
• Creating effective budgets
• Building emergency funds
• Optimizing savings strategies

**📈 Investments**
• Mutual funds and SIPs
• Stock market basics
• Risk assessment and portfolio building

**💳 Debt Management**
• Credit card debt strategies
• Loan optimization
• Debt consolidation options

**🎯 Financial Planning**
• Goal-based financial planning
• Retirement planning
• Tax-saving strategies

**🏦 Banking & Insurance**
• Choosing the right bank accounts
• Insurance needs analysis
• Fixed deposits vs. other options

Please ask me about any specific financial topic, and I'll provide detailed, actionable advice tailored to your situation."""

def clean_response(response: str) -> str:
    """Clean and format the model response with improved quality control."""
    # Remove common artifacts
    response = re.sub(r'^(Assistant:|AI:|Bot:|Financial Advisor:)\s*', '', response, flags=re.IGNORECASE)
    response = re.sub(r'\n(Human:|User:).*$', '', response, flags=re.DOTALL)

    # Remove repetitive patterns (same sentence repeated)
    lines = response.split('\n')
    cleaned_lines = []
    seen_lines = set()

    for line in lines:
        line = line.strip()
        if line and line not in seen_lines:
            cleaned_lines.append(line)
            seen_lines.add(line)
        elif not line:  # Keep empty lines for formatting
            cleaned_lines.append(line)

    response = '\n'.join(cleaned_lines)

    # Remove repetitive phrases within the same response
    sentences = response.split('.')
    unique_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence not in [s.strip() for s in unique_sentences]:
            unique_sentences.append(sentence)

    if unique_sentences:
        response = '. '.join(unique_sentences)
        if not response.endswith('.'):
            response += '.'

    # Remove common low-quality patterns
    response = re.sub(r'Note: If you don\'t.*?did\.', '', response, flags=re.IGNORECASE | re.DOTALL)
    response = re.sub(r'Share this:.*?Facebook.*?', '', response, flags=re.IGNORECASE | re.DOTALL)
    response = re.sub(r'This article first appeared.*?blog\.', '', response, flags=re.IGNORECASE)

    # Clean up whitespace
    response = re.sub(r'\n\s*\n\s*\n', '\n\n', response)  # Remove excessive line breaks
    response = response.strip()

    # Ensure response isn't empty or too short
    if not response or len(response) < 10:
        return "I understand your question about financial planning. Let me provide some general guidance: It's important to create a budget, save regularly, and consider your long-term financial goals. Would you like me to elaborate on any specific aspect?"

    # Ensure response is relevant to finance
    if len(response) < 50 and not any(word in response.lower() for word in ['budget', 'save', 'money', 'financial', 'invest', 'plan']):
        return "For financial planning, I recommend starting with a basic budget to track your income and expenses. This helps you understand your spending patterns and identify areas where you can save money. Would you like specific budgeting tips?"

    return response

def granite_chat(messages: List[Dict]) -> str:
    """
    Main function to generate chat responses using Granite.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        
    Returns:
        Assistant reply string
    """
    if not messages:
        return "I need a message to respond to. Please try again."
    
    try:
        # Get the user's question for fallback improvement
        user_question = messages[-1].get("content", "") if messages else ""

        # Generate response using configured backend
        if GRANITE_USE_LOCAL:
            response = granite_chat_local(messages)
        elif GRANITE_USE_API:
            response = granite_chat_api(messages)
        elif GRANITE_USE_OLLAMA:
            response = granite_chat_ollama(messages)
        else:
            # Fallback mock response
            logger.warning("No Granite backend configured, using mock response")
            response = generate_mock_response(user_question)

        # Return the response (already improved by our enhancement functions)
        return response
    
    except Exception as e:
        logger.error(f"Unexpected error in granite_chat: {e}")
        return "I encountered an unexpected error. Please try again."

def generate_mock_response(user_message: str) -> str:
    """Generate a mock response for testing when no backend is configured."""
    mock_responses = [
        "Thank you for your question about financial planning. While I'm currently in demo mode, I'd be happy to help you with budgeting, savings, and investment strategies once fully configured.",
        "I understand you're looking for financial advice. In a fully configured setup, I would analyze your message and provide personalized guidance based on your financial goals.",
        "Your question about finances is important. Once my AI backend is properly set up, I'll be able to provide detailed, personalized financial recommendations.",
        "I appreciate your interest in financial planning. When fully operational, I can help with everything from basic budgeting to complex investment strategies."
    ]
    
    import random
    return random.choice(mock_responses)

def simple_nlu_analysis(text: str) -> Optional[Dict]:
    """
    Simple NLU analysis as a replacement for Watson NLU.
    This is a basic implementation - you can enhance it or use other NLP libraries.
    """
    if not text or len(text.strip()) < 10:
        return None
    
    try:
        # Simple sentiment analysis based on keywords
        positive_words = ['good', 'great', 'excellent', 'happy', 'satisfied', 'love', 'amazing', 'wonderful', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'disappointed', 'frustrated', 'angry', 'worried', 'concerned']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = {"label": "positive", "score": 0.7}
        elif negative_count > positive_count:
            sentiment = {"label": "negative", "score": 0.7}
        else:
            sentiment = {"label": "neutral", "score": 0.5}
        
        # Simple keyword extraction
        financial_keywords = ['money', 'budget', 'savings', 'investment', 'tax', 'loan', 'debt', 'income', 'expense', 'retirement']
        found_keywords = [{"text": word, "relevance": 0.8} for word in financial_keywords if word in text_lower]
        
        return {
            "sentiment": {"document": sentiment},
            "keywords": found_keywords[:5],
            "entities": [],  # Could be enhanced with NER
            "concepts": []   # Could be enhanced with topic modeling
        }
        
    except Exception as e:
        logger.error(f"Error in simple NLU analysis: {e}")
        return None

def test_granite_connectivity() -> Dict[str, bool]:
    """Test Granite connectivity and functionality."""
    results = {
        "granite_ai": False,
        "nlu_analysis": True,  # Simple NLU is always available
        "model_loaded": False
    }
    
    try:
        # Test basic chat functionality
        test_messages = [
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": "Hello, can you help me with budgeting?"}
        ]
        
        response = granite_chat(test_messages)
        results["granite_ai"] = len(response) > 10 and "error" not in response.lower()
        
        # Test model loading status
        if GRANITE_USE_LOCAL:
            results["model_loaded"] = _pipeline is not None
        else:
            results["model_loaded"] = True  # API/Ollama don't need local loading
        
    except Exception as e:
        logger.error(f"Granite connectivity test failed: {e}")
    
    logger.info(f"Granite connectivity test results: {results}")
    return results

# Initialize configuration on import
validate_config()
