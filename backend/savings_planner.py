"""
Savings Planner Module for Taxora
Advanced savings planning with AI-powered suggestions and tracking
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SavingMethod(Enum):
    """Available saving methods."""
    GPAY = "gpay"
    CASH = "cash"
    BANK_ACCOUNT = "bank_account"
    FIXED_DEPOSIT = "fixed_deposit"
    MUTUAL_FUND = "mutual_fund"
    DIGITAL_WALLET = "digital_wallet"

@dataclass
class SavingsGoal:
    """Savings goal data structure."""
    goal_id: str
    user_id: str
    goal_name: str
    target_amount: float
    monthly_salary: float
    monthly_saving_target: float
    saving_method: str
    start_date: str
    target_date: str
    description: str
    created_at: str
    is_active: bool = True

@dataclass
class SavingsEntry:
    """Individual savings entry."""
    entry_id: str
    goal_id: str
    amount: float
    saving_method: str
    date: str
    description: str
    created_at: str

@dataclass
class SavingsAnalysis:
    """AI-powered savings analysis."""
    goal_id: str
    current_progress: float
    percentage_complete: float
    days_remaining: int
    on_track: bool
    ai_suggestions: List[str]
    areas_to_reduce: List[str]
    areas_to_increase: List[str]
    analysis_date: str

class SavingsPlanner:
    """Advanced savings planning system with AI integration."""
    
    def __init__(self):
        self.data_dir = "data/savings"
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Ensure data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)
        
    def create_savings_goal(self, user_id: str, goal_data: Dict) -> Dict:
        """Create a new savings goal with AI-powered suggestions."""
        try:
            # Generate unique goal ID
            goal_id = f"goal_{user_id}_{int(datetime.now().timestamp())}"
            
            # Validate input data
            required_fields = ["goal_name", "target_amount", "monthly_salary", "monthly_saving_target", "saving_method", "target_date", "description"]
            for field in required_fields:
                if field not in goal_data:
                    return {"success": False, "error": f"Missing required field: {field}"}
            
            # Create savings goal
            goal = SavingsGoal(
                goal_id=goal_id,
                user_id=user_id,
                goal_name=goal_data["goal_name"],
                target_amount=float(goal_data["target_amount"]),
                monthly_salary=float(goal_data["monthly_salary"]),
                monthly_saving_target=float(goal_data["monthly_saving_target"]),
                saving_method=goal_data["saving_method"],
                start_date=datetime.now().strftime("%Y-%m-%d"),
                target_date=goal_data["target_date"],
                description=goal_data["description"],
                created_at=datetime.now().isoformat()
            )
            
            # Get AI-powered suggestions
            ai_analysis = self._get_ai_savings_suggestions(goal)
            
            # Save goal
            self._save_goal(goal)
            
            return {
                "success": True,
                "goal_id": goal_id,
                "goal": asdict(goal),
                "ai_suggestions": ai_analysis,
                "message": "Savings goal created successfully with AI-powered recommendations!"
            }
            
        except Exception as e:
            logger.error(f"Error creating savings goal: {e}")
            return {"success": False, "error": str(e)}
    
    def add_savings_entry(self, goal_id: str, entry_data: Dict) -> Dict:
        """Add a savings entry and get AI feedback."""
        try:
            # Generate unique entry ID
            entry_id = f"entry_{goal_id}_{int(datetime.now().timestamp())}"
            
            # Create savings entry
            entry = SavingsEntry(
                entry_id=entry_id,
                goal_id=goal_id,
                amount=float(entry_data["amount"]),
                saving_method=entry_data["saving_method"],
                date=entry_data.get("date", datetime.now().strftime("%Y-%m-%d")),
                description=entry_data.get("description", ""),
                created_at=datetime.now().isoformat()
            )
            
            # Save entry
            self._save_entry(entry)
            
            # Get updated analysis
            analysis = self.get_savings_analysis(goal_id)
            
            return {
                "success": True,
                "entry_id": entry_id,
                "entry": asdict(entry),
                "analysis": analysis,
                "message": "Savings entry added successfully!"
            }
            
        except Exception as e:
            logger.error(f"Error adding savings entry: {e}")
            return {"success": False, "error": str(e)}
    
    def get_savings_analysis(self, goal_id: str) -> Dict:
        """Get comprehensive AI-powered savings analysis."""
        try:
            goal = self._load_goal(goal_id)
            if not goal:
                return {"success": False, "error": "Goal not found"}
            
            entries = self._load_entries(goal_id)
            
            # Calculate progress
            total_saved = sum(entry.amount for entry in entries)
            percentage_complete = (total_saved / goal.target_amount) * 100
            
            # Calculate days remaining
            target_date = datetime.strptime(goal.target_date, "%Y-%m-%d")
            days_remaining = (target_date - datetime.now()).days
            
            # Determine if on track
            expected_progress = (goal.monthly_saving_target * 
                               ((datetime.now() - datetime.strptime(goal.start_date, "%Y-%m-%d")).days / 30))
            on_track = total_saved >= expected_progress
            
            # Get AI analysis
            ai_analysis = self._get_ai_progress_analysis(goal, entries, total_saved, on_track)
            
            analysis = SavingsAnalysis(
                goal_id=goal_id,
                current_progress=total_saved,
                percentage_complete=percentage_complete,
                days_remaining=days_remaining,
                on_track=on_track,
                ai_suggestions=ai_analysis["suggestions"],
                areas_to_reduce=ai_analysis["reduce_areas"],
                areas_to_increase=ai_analysis["increase_areas"],
                analysis_date=datetime.now().isoformat()
            )
            
            return {
                "success": True,
                "analysis": asdict(analysis),
                "goal": asdict(goal),
                "entries": [asdict(entry) for entry in entries]
            }
            
        except Exception as e:
            logger.error(f"Error getting savings analysis: {e}")
            return {"success": False, "error": str(e)}
    
    def get_30_day_savings_plan(self, goal_id: str) -> Dict:
        """Generate AI-powered 30-day savings plan."""
        try:
            goal = self._load_goal(goal_id)
            if not goal:
                return {"success": False, "error": "Goal not found"}
            
            # Get AI-generated 30-day plan
            ai_plan = self._get_ai_30_day_plan(goal)
            
            return {
                "success": True,
                "goal_id": goal_id,
                "plan": ai_plan,
                "message": "30-day savings plan generated successfully!"
            }
            
        except Exception as e:
            logger.error(f"Error generating 30-day plan: {e}")
            return {"success": False, "error": str(e)}
    
    def check_savings_notifications(self, user_id: str) -> List[Dict]:
        """Check for savings notifications and reminders."""
        try:
            notifications = []
            goals = self._load_user_goals(user_id)
            
            for goal in goals:
                if not goal.is_active:
                    continue
                
                # Check if user hasn't saved in last 3 days
                entries = self._load_entries(goal.goal_id)
                if entries:
                    last_entry_date = datetime.fromisoformat(entries[-1].created_at)
                    days_since_last = (datetime.now() - last_entry_date).days
                    
                    if days_since_last >= 3:
                        notifications.append({
                            "type": "reminder",
                            "goal_id": goal.goal_id,
                            "goal_name": goal.goal_name,
                            "message": f"You haven't saved for {days_since_last} days. Keep up with your {goal.goal_name} goal!",
                            "suggested_amount": goal.monthly_saving_target / 30,
                            "ai_motivation": self._get_ai_motivation(goal)
                        })
                
                # Check if behind target
                analysis = self.get_savings_analysis(goal.goal_id)
                if analysis["success"] and not analysis["analysis"]["on_track"]:
                    notifications.append({
                        "type": "behind_target",
                        "goal_id": goal.goal_id,
                        "goal_name": goal.goal_name,
                        "message": "You're behind your savings target. Here are some AI suggestions:",
                        "ai_suggestions": analysis["analysis"]["ai_suggestions"]
                    })
            
            return notifications
            
        except Exception as e:
            logger.error(f"Error checking notifications: {e}")
            return []
    
    def _get_ai_savings_suggestions(self, goal: SavingsGoal) -> Dict:
        """Get AI-powered savings suggestions."""
        try:
            # Import AI provider manager
            from ai_provider_manager import get_ai_manager
            
            ai_manager = get_ai_manager()
            
            # Create prompt for AI analysis
            prompt = f"""
            As a financial advisor, analyze this savings goal and provide detailed suggestions:
            
            Goal: {goal.goal_name}
            Target Amount: ₹{goal.target_amount:,.2f}
            Monthly Salary: ₹{goal.monthly_salary:,.2f}
            Monthly Saving Target: ₹{goal.monthly_saving_target:,.2f}
            Saving Method: {goal.saving_method}
            Target Date: {goal.target_date}
            
            Please provide:
            1. 3 specific suggestions to achieve this goal
            2. 3 areas where they can reduce expenses
            3. 3 ways to increase their savings
            4. Assessment if the target is realistic
            
            Format as JSON with keys: suggestions, reduce_areas, increase_areas, realistic_assessment
            """
            
            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)
            
            if response["success"]:
                # Try to parse JSON response
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        ai_data = json.loads(json_match.group())
                        return ai_data
                except:
                    pass
                
                # Fallback to text parsing
                return {
                    "suggestions": ["Save consistently every day", "Use automatic transfers", "Track expenses daily"],
                    "reduce_areas": ["Dining out", "Entertainment", "Impulse purchases"],
                    "increase_areas": ["Side income", "Freelancing", "Skill development"],
                    "realistic_assessment": "Goal appears achievable with discipline"
                }
            
            return {
                "suggestions": ["Set up automatic savings", "Track daily expenses", "Review monthly progress"],
                "reduce_areas": ["Unnecessary subscriptions", "Frequent dining out", "Impulse buying"],
                "increase_areas": ["Additional income sources", "Skill monetization", "Investment returns"],
                "realistic_assessment": "Goal requires consistent effort but is achievable"
            }
            
        except Exception as e:
            logger.error(f"Error getting AI suggestions: {e}")
            return {
                "suggestions": ["Save regularly", "Track expenses", "Stay motivated"],
                "reduce_areas": ["Entertainment", "Dining", "Shopping"],
                "increase_areas": ["Income", "Investments", "Side jobs"],
                "realistic_assessment": "Goal requires planning and discipline"
            }
    
    def _save_goal(self, goal: SavingsGoal):
        """Save savings goal to file."""
        file_path = os.path.join(self.data_dir, f"goal_{goal.goal_id}.json")
        with open(file_path, 'w') as f:
            json.dump(asdict(goal), f, indent=2)
    
    def _save_entry(self, entry: SavingsEntry):
        """Save savings entry to file."""
        file_path = os.path.join(self.data_dir, f"entries_{entry.goal_id}.json")
        
        # Load existing entries
        entries = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                entries = json.load(f)
        
        # Add new entry
        entries.append(asdict(entry))
        
        # Save updated entries
        with open(file_path, 'w') as f:
            json.dump(entries, f, indent=2)
    
    def _load_goal(self, goal_id: str) -> Optional[SavingsGoal]:
        """Load savings goal from file."""
        file_path = os.path.join(self.data_dir, f"goal_{goal_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                return SavingsGoal(**data)
        return None
    
    def _load_entries(self, goal_id: str) -> List[SavingsEntry]:
        """Load savings entries from file."""
        file_path = os.path.join(self.data_dir, f"entries_{goal_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                entries_data = json.load(f)
                return [SavingsEntry(**entry) for entry in entries_data]
        return []
    
    def _load_user_goals(self, user_id: str) -> List[SavingsGoal]:
        """Load all goals for a user."""
        goals = []
        for filename in os.listdir(self.data_dir):
            if filename.startswith("goal_") and filename.endswith(".json"):
                goal = self._load_goal(filename.replace("goal_", "").replace(".json", ""))
                if goal and goal.user_id == user_id:
                    goals.append(goal)
        return goals

# Global instance
savings_planner = SavingsPlanner()
