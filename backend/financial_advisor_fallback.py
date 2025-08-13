"""
Financial Advisor Fallback System
Provides quality financial advice when AI models give poor responses.
"""

import re
from typing import Dict, List

class FinancialAdvisorFallback:
    """Rule-based financial advisor for fallback responses."""
    
    def __init__(self):
        self.financial_topics = {
            'budget': {
                'keywords': ['budget', 'budgeting', 'spending', 'expenses', 'income'],
                'response': "Here's a simple budgeting approach: Follow the 50/30/20 rule - allocate 50% of your income to needs (rent, groceries, utilities), 30% to wants (entertainment, dining out), and 20% to savings and debt repayment. Start by tracking your expenses for a month to understand your spending patterns."
            },
            'emergency_fund': {
                'keywords': ['emergency', 'emergency fund', 'save for emergencies', 'rainy day'],
                'response': "An emergency fund should cover 3-6 months of living expenses. Start small - even $500 can help with unexpected costs. Keep this money in a high-yield savings account that's easily accessible but separate from your checking account."
            },
            'investing': {
                'keywords': ['invest', 'investment', 'stocks', 'bonds', 'portfolio', 'retirement'],
                'response': "For beginners, consider starting with low-cost index funds or ETFs that track the market. These provide instant diversification. A common approach is to invest in a mix of stock and bond index funds based on your age and risk tolerance. Consider maxing out employer 401(k) matching first."
            },
            'debt': {
                'keywords': ['debt', 'credit card', 'loan', 'pay off', 'interest'],
                'response': "Focus on high-interest debt first (like credit cards). Consider the debt avalanche method: pay minimums on all debts, then put extra money toward the highest interest rate debt. Alternatively, the debt snowball method pays off smallest balances first for psychological wins."
            },
            'savings': {
                'keywords': ['save', 'saving', 'savings account', 'money market'],
                'response': "Start by automating your savings - set up automatic transfers to a savings account. Aim to save at least 20% of your income if possible. Use high-yield savings accounts for better interest rates. Consider separate accounts for different goals (vacation, car, etc.)."
            },
            'retirement': {
                'keywords': ['retirement', '401k', 'ira', 'roth', 'pension'],
                'response': "Start retirement saving as early as possible to benefit from compound interest. Contribute enough to your 401(k) to get full employer matching. Consider a Roth IRA for tax-free growth. A general rule is to save 10-15% of your income for retirement."
            },
            'credit': {
                'keywords': ['credit score', 'credit report', 'credit card', 'credit history'],
                'response': "Build good credit by paying bills on time, keeping credit utilization below 30%, and maintaining old accounts. Check your credit report annually for errors. Consider a secured credit card if you're building credit from scratch."
            }
        }
    
    def get_financial_advice(self, question: str) -> str:
        """Get relevant financial advice based on the question."""
        question_lower = question.lower()
        
        # Find matching topics
        for topic, info in self.financial_topics.items():
            if any(keyword in question_lower for keyword in info['keywords']):
                return info['response']
        
        # Default general advice
        return "Here are some fundamental financial principles: 1) Create and stick to a budget, 2) Build an emergency fund, 3) Pay off high-interest debt, 4) Start investing early, 5) Save for retirement. Would you like me to elaborate on any of these areas?"
    
    def is_response_poor_quality(self, response: str) -> bool:
        """Check if a response is of poor quality and needs fallback."""
        if not response or len(response.strip()) < 20:
            return True

        # Check for repetitive content
        sentences = response.split('.')
        if len(sentences) > 3:
            unique_sentences = set(s.strip().lower() for s in sentences if s.strip())
            if len(unique_sentences) < len(sentences) * 0.7:  # More than 30% repetition
                return True

        # Check for irrelevant content
        irrelevant_patterns = [
            r'gstr\d+',
            r'share this:.*facebook',
            r'this article first appeared',
            r'note: if you don\'t think',
            r'twitter.*facebook',
            r'blog\..*share',
            r'contact.*email.*protected',
            r'emergency management agency',
            r'call 911',
            r'ems office',
            r'please contact me at'
        ]

        for pattern in irrelevant_patterns:
            if re.search(pattern, response.lower()):
                return True

        # Check if response is too generic, nonsensical, or unhelpful
        poor_quality_indicators = [
            len(response) < 50 and not any(word in response.lower() for word in
                                         ['budget', 'save', 'money', 'financial', 'invest', 'plan', 'debt', 'credit']),
            'how to get started with your own financial plan' in response.lower() and len(response) < 100,
            'if you are a financial advisor' in response.lower(),
            'contact me at' in response.lower(),
            'emergency management' in response.lower(),
            'call 911' in response.lower(),
            'email me at' in response.lower(),
            'please email me' in response.lower(),
            'if you have any questions' in response.lower() and len(response) < 100,
            'if you have a car or vehicle' in response.lower(),
            'insurance company' in response.lower() and 'emergency' in response.lower(),
            'online account' in response.lower() and 'get your money back' in response.lower(),
            len(response) > 200 and response.count('you') > 10 and 'financial' not in response.lower()[:100],
            # Generic unhelpful responses
            response.lower().startswith('if you') and len(response) < 150 and 'budget' not in response.lower()
        ]

        return any(poor_quality_indicators)
    
    def improve_response(self, original_response: str, question: str) -> str:
        """Improve a poor quality response with fallback advice."""
        if self.is_response_poor_quality(original_response):
            fallback_advice = self.get_financial_advice(question)
            return f"Let me provide some helpful financial guidance: {fallback_advice}"
        
        return original_response

# Global instance
financial_fallback = FinancialAdvisorFallback()

def improve_financial_response(response: str, question: str) -> str:
    """Improve financial response quality using fallback system."""
    return financial_fallback.improve_response(response, question)
