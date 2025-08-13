"""
Tamil Voice Enhancement Module
Provides better Tamil text processing and voice optimization.
"""

import re
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class TamilVoiceEnhancer:
    """Enhanced Tamil voice processing for better pronunciation."""
    
    def __init__(self):
        # Tamil number mappings for better pronunciation
        self.number_mappings = {
            '0': 'பூஜ்யம்',
            '1': 'ஒன்று',
            '2': 'இரண்டு', 
            '3': 'மூன்று',
            '4': 'நான்கு',
            '5': 'ஐந்து',
            '6': 'ஆறு',
            '7': 'ஏழு',
            '8': 'எட்டு',
            '9': 'ஒன்பது',
            '10': 'பத்து',
            '20': 'இருபது',
            '30': 'முப்பது',
            '40': 'நாற்பது',
            '50': 'ஐம்பது',
            '60': 'அறுபது',
            '70': 'எழுபது',
            '80': 'எண்பது',
            '90': 'தொண்ணூறு',
            '100': 'நூறு'
        }
        
        # Financial terms with proper Tamil pronunciation
        self.financial_terms = {
            'budget': 'வரவு செலவு திட்டம்',
            'budgeting': 'வரவு செலவு திட்டமிடல்',
            'savings': 'சேமிப்பு',
            'save': 'சேமி',
            'investment': 'முதலீடு',
            'invest': 'முதலீடு செய்',
            'emergency fund': 'அவசர நிதி',
            'emergency': 'அவசரம்',
            'income': 'வருமானம்',
            'expenses': 'செலவுகள்',
            'expense': 'செலவு',
            'money': 'பணம்',
            'financial': 'நிதி',
            'finance': 'நிதி',
            'percent': 'சதவீதம்',
            'percentage': 'சதவீதம்',
            'dollar': 'டாலர்',
            'dollars': 'டாலர்கள்',
            'rupee': 'ரூபாய்',
            'rupees': 'ரூபாய்கள்',
            'bank': 'வங்கி',
            'account': 'கணக்கு',
            'credit': 'கடன்',
            'debt': 'கடன்',
            'loan': 'கடன்',
            'interest': 'வட்டி',
            'profit': 'லாபம்',
            'loss': 'நஷ்டம்',
            'tax': 'வரி',
            'insurance': 'காப்பீடு'
        }
        
        # Common phrases for better flow
        self.phrase_mappings = {
            'you should': 'நீங்கள் வேண்டும்',
            'it is important': 'இது முக்கியம்',
            'for example': 'உதாரணமாக',
            'in other words': 'வேறு வார்த்தைகளில்',
            'first step': 'முதல் படி',
            'next step': 'அடுத்த படி',
            'remember': 'நினைவில் கொள்ளுங்கள்',
            'make sure': 'உறுதி செய்யுங்கள்'
        }
    
    def enhance_tamil_text(self, text: str) -> str:
        """Enhance Tamil text for better voice pronunciation."""
        try:
            enhanced_text = text
            
            # Replace numbers with Tamil words
            enhanced_text = self._replace_numbers(enhanced_text)
            
            # Replace financial terms
            enhanced_text = self._replace_financial_terms(enhanced_text)
            
            # Replace common phrases
            enhanced_text = self._replace_phrases(enhanced_text)
            
            # Add pronunciation pauses
            enhanced_text = self._add_pauses(enhanced_text)
            
            # Clean up extra spaces
            enhanced_text = re.sub(r'\s+', ' ', enhanced_text).strip()
            
            logger.info(f"Enhanced Tamil text: {enhanced_text[:100]}...")
            return enhanced_text
            
        except Exception as e:
            logger.error(f"Tamil text enhancement error: {e}")
            return text
    
    def _replace_numbers(self, text: str) -> str:
        """Replace numbers with Tamil words."""
        # Handle special financial ratios
        text = text.replace('50/30/20', 'ஐம்பது முப்பது இருபது விதி')
        text = text.replace('50%', 'ஐம்பது சதவீதம்')
        text = text.replace('30%', 'முப்பது சதவீதம்')
        text = text.replace('20%', 'இருபது சதவீதம்')
        
        # Replace individual numbers
        for num, tamil_num in self.number_mappings.items():
            text = text.replace(f'{num}%', f'{tamil_num} சதவீதம்')
            text = text.replace(f'{num} percent', f'{tamil_num} சதவீதம்')
        
        return text
    
    def _replace_financial_terms(self, text: str) -> str:
        """Replace English financial terms with Tamil equivalents."""
        for english_term, tamil_term in self.financial_terms.items():
            # Case insensitive replacement
            pattern = re.compile(re.escape(english_term), re.IGNORECASE)
            text = pattern.sub(tamil_term, text)
        
        return text
    
    def _replace_phrases(self, text: str) -> str:
        """Replace common English phrases with Tamil equivalents."""
        for english_phrase, tamil_phrase in self.phrase_mappings.items():
            pattern = re.compile(re.escape(english_phrase), re.IGNORECASE)
            text = pattern.sub(tamil_phrase, text)
        
        return text
    
    def _add_pauses(self, text: str) -> str:
        """Add appropriate pauses for better speech flow."""
        # Add pauses after sentences
        text = text.replace('.', '. ')
        text = text.replace(',', ', ')
        text = text.replace(';', '; ')
        text = text.replace(':', ': ')
        
        # Add pauses after important financial terms
        important_terms = ['வரவு செலவு திட்டம்', 'சேமிப்பு', 'முதலீடு', 'அவசர நிதி']
        for term in important_terms:
            text = text.replace(term, f'{term}, ')
        
        return text
    
    def get_voice_settings(self) -> Dict:
        """Get optimized voice settings for Tamil."""
        return {
            "language": "ta-IN",
            "speed": 0.6,  # Slower for clarity
            "pitch": 1.2,  # Higher pitch for Tamil
            "volume": 0.9,
            "voice_name": "Tamil India Female",
            "ssml_gender": "FEMALE"
        }
    
    def create_ssml(self, text: str) -> str:
        """Create SSML markup for better Tamil pronunciation."""
        enhanced_text = self.enhance_tamil_text(text)
        
        ssml = f"""
        <speak>
            <voice name="ta-IN-Wavenet-A" languageCode="ta-IN">
                <prosody rate="0.7" pitch="+2st" volume="loud">
                    {enhanced_text}
                </prosody>
            </voice>
        </speak>
        """
        
        return ssml.strip()

# Global instance
tamil_enhancer = TamilVoiceEnhancer()

def enhance_tamil_for_voice(text: str) -> Dict:
    """Main function to enhance Tamil text for voice output."""
    try:
        enhanced_text = tamil_enhancer.enhance_tamil_text(text)
        voice_settings = tamil_enhancer.get_voice_settings()
        ssml = tamil_enhancer.create_ssml(text)
        
        return {
            "success": True,
            "enhanced_text": enhanced_text,
            "voice_settings": voice_settings,
            "ssml": ssml,
            "original_text": text
        }
        
    except Exception as e:
        logger.error(f"Tamil voice enhancement failed: {e}")
        return {
            "success": False,
            "enhanced_text": text,
            "voice_settings": tamil_enhancer.get_voice_settings(),
            "ssml": text,
            "original_text": text,
            "error": str(e)
        }
