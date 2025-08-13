"""
Advanced AI System with Unique Innovations
- Real-time dual-persona switching based on user expertise
- Persistent contextual memory for ongoing financial coaching
- Emotional intelligence integration with mood detection
- Human-centered design for evolving financial mentorship
"""

import json
import time
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import re

logger = logging.getLogger(__name__)

class UserExpertiseLevel(Enum):
    """User financial expertise levels for dynamic persona switching."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class EmotionalState(Enum):
    """Detected emotional states for adaptive communication."""
    CONFIDENT = "confident"
    ANXIOUS = "anxious"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    EXCITED = "excited"
    OVERWHELMED = "overwhelmed"
    NEUTRAL = "neutral"

@dataclass
class UserProfile:
    """Comprehensive user profile for personalized coaching."""
    user_id: str
    name: str
    expertise_level: UserExpertiseLevel
    emotional_state: EmotionalState
    financial_goals: List[str]
    learning_preferences: Dict[str, str]
    interaction_history: List[Dict]
    progress_metrics: Dict[str, float]
    last_updated: float
    session_count: int
    preferred_language: str = "en"
    voice_preference: str = "both"

class AdvancedAISystem:
    """Advanced AI system with unique innovations for financial coaching."""
    
    def __init__(self):
        self.user_profiles = {}  # Persistent user memory
        self.expertise_indicators = self._load_expertise_indicators()
        self.emotional_patterns = self._load_emotional_patterns()
        self.persona_templates = self._load_persona_templates()
        
    def _load_expertise_indicators(self) -> Dict:
        """Load indicators for automatic expertise level detection."""
        return {
            "beginner": [
                "what is", "how do i start", "basic", "simple", "explain", 
                "don't understand", "new to", "first time", "help me learn"
            ],
            "intermediate": [
                "compare", "which is better", "pros and cons", "should i", 
                "next step", "optimize", "improve", "strategy"
            ],
            "advanced": [
                "portfolio", "diversification", "risk management", "asset allocation",
                "tax implications", "compound interest", "market analysis"
            ],
            "expert": [
                "derivatives", "hedge", "arbitrage", "quantitative", "algorithmic",
                "sophisticated", "complex", "institutional", "advanced strategies"
            ]
        }
    
    def _load_emotional_patterns(self) -> Dict:
        """Load patterns for emotional state detection."""
        return {
            "anxious": [
                "worried", "scared", "nervous", "afraid", "concerned", "stress",
                "panic", "overwhelmed", "don't know what to do", "help me"
            ],
            "confused": [
                "don't understand", "confused", "unclear", "complicated", 
                "makes no sense", "lost", "explain again", "what does this mean"
            ],
            "frustrated": [
                "frustrated", "annoying", "difficult", "hard", "impossible",
                "giving up", "tired of", "fed up", "not working"
            ],
            "excited": [
                "excited", "great", "awesome", "amazing", "love this", 
                "fantastic", "perfect", "exactly what i needed"
            ],
            "confident": [
                "ready", "let's do this", "confident", "sure", "understand",
                "got it", "makes sense", "clear", "ready to move forward"
            ]
        }
    
    def _load_persona_templates(self) -> Dict:
        """Load persona templates for different expertise levels and emotional states."""
        return {
            "beginner": {
                "confident": {
                    "tone": "encouraging and supportive",
                    "style": "step-by-step guidance with simple explanations",
                    "language": "friendly, non-technical, reassuring"
                },
                "anxious": {
                    "tone": "calm and reassuring",
                    "style": "gentle guidance with lots of encouragement",
                    "language": "soothing, confidence-building, patient"
                },
                "confused": {
                    "tone": "patient and clear",
                    "style": "break down concepts into tiny steps",
                    "language": "simple, repetitive, visual examples"
                }
            },
            "intermediate": {
                "confident": {
                    "tone": "collaborative and informative",
                    "style": "detailed explanations with options",
                    "language": "professional but accessible"
                },
                "frustrated": {
                    "tone": "understanding and solution-focused",
                    "style": "acknowledge challenges, provide clear paths forward",
                    "language": "empathetic, practical, actionable"
                }
            },
            "advanced": {
                "confident": {
                    "tone": "professional and analytical",
                    "style": "comprehensive analysis with data",
                    "language": "technical, precise, detailed"
                },
                "excited": {
                    "tone": "enthusiastic and collaborative",
                    "style": "explore advanced strategies together",
                    "language": "engaging, sophisticated, innovative"
                }
            }
        }
    
    def detect_expertise_level(self, user_input: str, interaction_history: List[Dict]) -> UserExpertiseLevel:
        """Real-time expertise detection based on language patterns and history."""
        user_input_lower = user_input.lower()
        
        # Score each expertise level
        scores = {level: 0 for level in UserExpertiseLevel}
        
        # Analyze current input
        for level, indicators in self.expertise_indicators.items():
            for indicator in indicators:
                if indicator in user_input_lower:
                    scores[UserExpertiseLevel(level)] += 1
        
        # Analyze interaction history for context
        if interaction_history:
            recent_interactions = interaction_history[-5:]  # Last 5 interactions
            for interaction in recent_interactions:
                content = interaction.get('content', '').lower()
                for level, indicators in self.expertise_indicators.items():
                    for indicator in indicators:
                        if indicator in content:
                            scores[UserExpertiseLevel(level)] += 0.5
        
        # Determine expertise level
        if scores[UserExpertiseLevel.EXPERT] > 0:
            return UserExpertiseLevel.EXPERT
        elif scores[UserExpertiseLevel.ADVANCED] > 1:
            return UserExpertiseLevel.ADVANCED
        elif scores[UserExpertiseLevel.INTERMEDIATE] > 1:
            return UserExpertiseLevel.INTERMEDIATE
        else:
            return UserExpertiseLevel.BEGINNER
    
    def detect_emotional_state(self, user_input: str, interaction_context: Dict) -> EmotionalState:
        """Emotional intelligence integration for mood detection."""
        user_input_lower = user_input.lower()
        
        # Score emotional states
        emotion_scores = {emotion: 0 for emotion in EmotionalState}
        
        # Analyze language patterns
        for emotion, patterns in self.emotional_patterns.items():
            for pattern in patterns:
                if pattern in user_input_lower:
                    emotion_scores[EmotionalState(emotion)] += 1
        
        # Analyze punctuation and capitalization for emotional intensity
        if "!" in user_input:
            emotion_scores[EmotionalState.EXCITED] += 1
        if "???" in user_input or user_input.count("?") > 2:
            emotion_scores[EmotionalState.CONFUSED] += 1
        if user_input.isupper() and len(user_input) > 10:
            emotion_scores[EmotionalState.FRUSTRATED] += 1
        
        # Consider interaction context
        response_time = interaction_context.get('response_time', 0)
        if response_time < 5:  # Quick response might indicate confidence
            emotion_scores[EmotionalState.CONFIDENT] += 0.5
        elif response_time > 30:  # Slow response might indicate confusion
            emotion_scores[EmotionalState.CONFUSED] += 0.5
        
        # Return dominant emotion or neutral
        max_emotion = max(emotion_scores, key=emotion_scores.get)
        return max_emotion if emotion_scores[max_emotion] > 0 else EmotionalState.NEUTRAL
    
    def generate_adaptive_persona(self, expertise: UserExpertiseLevel, emotion: EmotionalState) -> Dict:
        """Generate adaptive persona based on expertise and emotional state."""
        # Get base persona template
        persona_key = expertise.value
        emotion_key = emotion.value
        
        # Find best matching persona template
        if persona_key in self.persona_templates:
            if emotion_key in self.persona_templates[persona_key]:
                base_persona = self.persona_templates[persona_key][emotion_key]
            else:
                # Use default for expertise level
                base_persona = list(self.persona_templates[persona_key].values())[0]
        else:
            # Fallback to beginner confident
            base_persona = self.persona_templates["beginner"]["confident"]
        
        # Enhance with dynamic elements
        enhanced_persona = {
            **base_persona,
            "expertise_level": expertise.value,
            "emotional_state": emotion.value,
            "adaptation_timestamp": time.time(),
            "unique_innovations": [
                "Real-time dual-persona switching",
                "Emotional intelligence integration",
                "Contextual memory persistence",
                "Human-centered adaptive design"
            ]
        }
        
        return enhanced_persona
    
    def build_enhanced_system_prompt(self, user_profile: UserProfile, current_persona: Dict) -> str:
        """Build enhanced system prompt with unique innovations."""
        
        expertise_guidance = {
            "beginner": "Use simple language, provide step-by-step guidance, include encouraging examples, avoid jargon",
            "intermediate": "Provide detailed explanations, offer multiple options, use some technical terms with explanations",
            "advanced": "Use professional language, provide comprehensive analysis, include technical details and data",
            "expert": "Engage in sophisticated discussion, use advanced terminology, provide complex strategies and analysis"
        }
        
        emotional_guidance = {
            "anxious": "Be extra reassuring, acknowledge concerns, provide confidence-building steps, use calming language",
            "confused": "Break down concepts clearly, use simple examples, repeat key points, check understanding",
            "frustrated": "Acknowledge difficulties, provide clear solutions, be patient and understanding",
            "excited": "Match enthusiasm, explore advanced topics, encourage continued learning",
            "confident": "Provide comprehensive information, challenge with advanced concepts when appropriate"
        }
        
        system_prompt = f"""
You are an advanced AI financial advisor with unique innovations that set you apart from traditional chatbots:

🚀 UNIQUE INNOVATIONS:
• Real-time dual-persona switching: Automatically adjust communication style based on user expertise without manual setup
• Persistent contextual memory: Remember user's financial journey across multiple sessions for ongoing coaching
• Emotional intelligence integration: Detect user moods and adapt advice style accordingly
• Human-centered design: Continuously evolve mentorship approach based on user progress

👤 USER PROFILE:
• Name: {user_profile.name}
• Expertise Level: {user_profile.expertise_level.value.title()}
• Current Emotional State: {user_profile.emotional_state.value.title()}
• Session Count: {user_profile.session_count}
• Financial Goals: {', '.join(user_profile.financial_goals) if user_profile.financial_goals else 'Not specified'}
• Preferred Language: {user_profile.preferred_language}

🎭 CURRENT ADAPTIVE PERSONA:
• Tone: {current_persona['tone']}
• Style: {current_persona['style']}
• Language: {current_persona['language']}

📋 EXPERTISE-BASED GUIDANCE:
{expertise_guidance.get(user_profile.expertise_level.value, expertise_guidance['beginner'])}

💭 EMOTIONAL ADAPTATION:
{emotional_guidance.get(user_profile.emotional_state.value, emotional_guidance['confident'])}

🎯 COACHING APPROACH:
• Build on previous conversations and progress
• Adapt complexity based on demonstrated understanding
• Provide personalized recommendations based on goals
• Use encouraging language that builds financial confidence
• Integrate cultural context for Tamil speakers when appropriate

🌟 BUSINESS & SOCIAL IMPACT:
• Democratize financial education through personalized AI coaching
• Bridge expertise gaps with adaptive communication
• Provide 24/7 financial mentorship at scale
• Support financial inclusion across language and cultural barriers
• Enable continuous learning and financial empowerment

Remember: You're not just providing information—you're building a long-term coaching relationship that evolves with the user's financial journey. Each interaction should feel personalized, contextually aware, and emotionally intelligent.

Respond in a way that showcases these unique innovations while providing excellent financial advice.
"""
        
        return system_prompt.strip()
    
    def update_user_profile(self, user_id: str, interaction_data: Dict) -> UserProfile:
        """Update user profile with new interaction data for persistent memory."""
        current_time = time.time()
        
        if user_id not in self.user_profiles:
            # Create new user profile
            self.user_profiles[user_id] = UserProfile(
                user_id=user_id,
                name=interaction_data.get('name', 'User'),
                expertise_level=UserExpertiseLevel.BEGINNER,
                emotional_state=EmotionalState.NEUTRAL,
                financial_goals=[],
                learning_preferences={},
                interaction_history=[],
                progress_metrics={},
                last_updated=current_time,
                session_count=0
            )
        
        profile = self.user_profiles[user_id]
        
        # Update expertise level based on current interaction
        new_expertise = self.detect_expertise_level(
            interaction_data.get('user_input', ''),
            profile.interaction_history
        )
        
        # Update emotional state
        new_emotion = self.detect_emotional_state(
            interaction_data.get('user_input', ''),
            interaction_data
        )
        
        # Update profile
        profile.expertise_level = new_expertise
        profile.emotional_state = new_emotion
        profile.last_updated = current_time
        profile.session_count += 1
        
        # Add to interaction history
        profile.interaction_history.append({
            'timestamp': current_time,
            'user_input': interaction_data.get('user_input', ''),
            'expertise_detected': new_expertise.value,
            'emotion_detected': new_emotion.value,
            'response_time': interaction_data.get('response_time', 0)
        })
        
        # Keep only last 50 interactions for memory efficiency
        if len(profile.interaction_history) > 50:
            profile.interaction_history = profile.interaction_history[-50:]
        
        return profile
    
    def get_contextual_insights(self, user_profile: UserProfile) -> Dict:
        """Generate contextual insights for ongoing coaching."""
        insights = {
            "learning_progress": "Analyzing user's financial knowledge growth",
            "expertise_evolution": f"Progressed from basic to {user_profile.expertise_level.value} level",
            "emotional_patterns": "Tracking confidence and engagement levels",
            "personalization_level": "High - based on extensive interaction history",
            "coaching_recommendations": []
        }
        
        # Add specific coaching recommendations based on profile
        if user_profile.session_count > 5:
            insights["coaching_recommendations"].append("Ready for more advanced topics")
        
        if user_profile.emotional_state == EmotionalState.CONFIDENT:
            insights["coaching_recommendations"].append("Introduce challenging concepts")
        elif user_profile.emotional_state == EmotionalState.ANXIOUS:
            insights["coaching_recommendations"].append("Focus on confidence building")
        
        return insights

# Global advanced AI system instance
advanced_ai = AdvancedAISystem()

def get_advanced_ai_system() -> AdvancedAISystem:
    """Get the global advanced AI system instance."""
    return advanced_ai
