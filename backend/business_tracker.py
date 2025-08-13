"""
Business Credit/Debit Tracker Module for Taxora
Advanced business financial tracking with GST management and AI insights
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

class TransactionType(Enum):
    """Transaction types."""
    CREDIT = "credit"
    DEBIT = "debit"

class GSTSector(Enum):
    """GST sectors with rates."""
    GOODS_5 = "goods_5"      # 5% GST
    GOODS_12 = "goods_12"    # 12% GST
    GOODS_18 = "goods_18"    # 18% GST
    GOODS_28 = "goods_28"    # 28% GST
    SERVICES_18 = "services_18"  # 18% GST for services
    EXEMPT = "exempt"        # 0% GST

class TaxType(Enum):
    """Various tax types for comprehensive tracking."""
    GST = "gst"
    INCOME_TAX = "income_tax"
    ROAD_TAX = "road_tax"
    WATER_TAX = "water_tax"
    MUNICIPALITY_TAX = "municipality_tax"
    PROPERTY_TAX = "property_tax"
    PROFESSIONAL_TAX = "professional_tax"
    ELECTRICITY_TAX = "electricity_tax"
    TRADE_LICENSE = "trade_license"
    POLLUTION_TAX = "pollution_tax"
    LABOR_WELFARE = "labor_welfare"
    ESI_CONTRIBUTION = "esi_contribution"
    PF_CONTRIBUTION = "pf_contribution"
    OTHER_TAX = "other_tax"

@dataclass
class BusinessTransaction:
    """Business transaction data structure."""
    transaction_id: str
    business_id: str
    transaction_type: str  # credit or debit
    amount: float
    description: str
    category: str
    date: str
    gst_applicable: bool
    gst_rate: float
    gst_amount: float
    party_name: str
    party_gst_number: str
    invoice_number: str
    created_at: str

@dataclass
class GSTRecord:
    """GST record for tracking."""
    record_id: str
    business_id: str
    gst_number: str
    sector: str
    gst_rate: float
    taxable_amount: float
    gst_amount: float
    month: str
    year: str
    created_at: str

@dataclass
class TaxRecord:
    """Comprehensive tax record for all tax types."""
    tax_record_id: str
    business_id: str
    tax_type: str
    tax_name: str
    amount: float
    due_date: str
    payment_date: str
    transaction_number: str
    authority: str
    description: str
    status: str  # pending, paid, overdue
    created_at: str

@dataclass
class BusinessProfile:
    """Enhanced business profile with comprehensive details."""
    business_id: str
    business_name: str
    owner_name: str
    gst_number: str
    business_type: str
    sector: str
    registration_date: str
    # Enhanced profile fields
    pan_number: str
    tan_number: str
    cin_number: str
    address: str
    city: str
    state: str
    pincode: str
    phone: str
    email: str
    bank_account: str
    bank_ifsc: str
    # Tax registration details
    professional_tax_number: str
    esi_number: str
    pf_number: str
    trade_license_number: str
    created_at: str

class BusinessTracker:
    """Advanced business financial tracking system."""
    
    def __init__(self):
        self.data_dir = "data/business"
        self.ensure_data_directory()
        
        # GST rates mapping
        self.gst_rates = {
            "goods_5": 5.0,
            "goods_12": 12.0,
            "goods_18": 18.0,
            "goods_28": 28.0,
            "services_18": 18.0,
            "exempt": 0.0
        }
        
    def ensure_data_directory(self):
        """Ensure data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)
        
    def create_business_profile(self, profile_data: Dict) -> Dict:
        """Create a comprehensive business profile."""
        try:
            # Generate unique business ID
            business_id = f"biz_{int(datetime.now().timestamp())}"

            # Validate input data
            required_fields = ["business_name", "owner_name", "gst_number", "business_type", "sector"]
            for field in required_fields:
                if field not in profile_data:
                    return {"success": False, "error": f"Missing required field: {field}"}

            # Create enhanced business profile
            profile = BusinessProfile(
                business_id=business_id,
                business_name=profile_data["business_name"],
                owner_name=profile_data["owner_name"],
                gst_number=profile_data["gst_number"],
                business_type=profile_data["business_type"],
                sector=profile_data["sector"],
                registration_date=profile_data.get("registration_date", datetime.now().strftime("%Y-%m-%d")),
                # Enhanced fields
                pan_number=profile_data.get("pan_number", ""),
                tan_number=profile_data.get("tan_number", ""),
                cin_number=profile_data.get("cin_number", ""),
                address=profile_data.get("address", ""),
                city=profile_data.get("city", ""),
                state=profile_data.get("state", ""),
                pincode=profile_data.get("pincode", ""),
                phone=profile_data.get("phone", ""),
                email=profile_data.get("email", ""),
                bank_account=profile_data.get("bank_account", ""),
                bank_ifsc=profile_data.get("bank_ifsc", ""),
                # Tax registration details
                professional_tax_number=profile_data.get("professional_tax_number", ""),
                esi_number=profile_data.get("esi_number", ""),
                pf_number=profile_data.get("pf_number", ""),
                trade_license_number=profile_data.get("trade_license_number", ""),
                created_at=datetime.now().isoformat()
            )

            # Save profile
            self._save_business_profile(profile)

            # Get AI recommendations for tax setup
            ai_recommendations = self._get_ai_tax_setup_recommendations(profile)

            return {
                "success": True,
                "business_id": business_id,
                "profile": asdict(profile),
                "ai_recommendations": ai_recommendations,
                "message": "Enhanced business profile created successfully!"
            }

        except Exception as e:
            logger.error(f"Error creating business profile: {e}")
            return {"success": False, "error": str(e)}
    
    def add_transaction(self, business_id: str, transaction_data: Dict) -> Dict:
        """Add a business transaction with GST calculation."""
        try:
            # Generate unique transaction ID
            transaction_id = f"txn_{business_id}_{int(datetime.now().timestamp())}"
            
            # Calculate GST if applicable
            gst_applicable = transaction_data.get("gst_applicable", False)
            gst_rate = 0.0
            gst_amount = 0.0
            
            if gst_applicable and "gst_sector" in transaction_data:
                gst_rate = self.gst_rates.get(transaction_data["gst_sector"], 0.0)
                base_amount = float(transaction_data["amount"])
                gst_amount = (base_amount * gst_rate) / 100
            
            # Create transaction
            transaction = BusinessTransaction(
                transaction_id=transaction_id,
                business_id=business_id,
                transaction_type=transaction_data["transaction_type"],
                amount=float(transaction_data["amount"]),
                description=transaction_data["description"],
                category=transaction_data.get("category", "General"),
                date=transaction_data.get("date", datetime.now().strftime("%Y-%m-%d")),
                gst_applicable=gst_applicable,
                gst_rate=gst_rate,
                gst_amount=gst_amount,
                party_name=transaction_data.get("party_name", ""),
                party_gst_number=transaction_data.get("party_gst_number", ""),
                invoice_number=transaction_data.get("invoice_number", ""),
                created_at=datetime.now().isoformat()
            )
            
            # Save transaction
            self._save_transaction(transaction)
            
            # Update GST records if applicable
            if gst_applicable:
                self._update_gst_records(transaction)
            
            # Get AI insights
            ai_insights = self._get_ai_transaction_insights(business_id, transaction)
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "transaction": asdict(transaction),
                "ai_insights": ai_insights,
                "message": "Transaction added successfully!"
            }
            
        except Exception as e:
            logger.error(f"Error adding transaction: {e}")
            return {"success": False, "error": str(e)}
    
    def get_gst_summary(self, business_id: str, month: str, year: str) -> Dict:
        """Get GST summary for a specific month."""
        try:
            transactions = self._load_business_transactions(business_id)
            
            # Filter transactions for the month
            month_transactions = [
                t for t in transactions 
                if t.gst_applicable and 
                datetime.strptime(t.date, "%Y-%m-%d").month == int(month) and
                datetime.strptime(t.date, "%Y-%m-%d").year == int(year)
            ]
            
            # Calculate GST summary
            total_taxable_amount = sum(t.amount for t in month_transactions)
            total_gst_collected = sum(t.gst_amount for t in month_transactions if t.transaction_type == "credit")
            total_gst_paid = sum(t.gst_amount for t in month_transactions if t.transaction_type == "debit")
            net_gst_liability = total_gst_collected - total_gst_paid
            
            # Get AI analysis
            ai_analysis = self._get_ai_gst_analysis(business_id, month_transactions, net_gst_liability)
            
            return {
                "success": True,
                "month": month,
                "year": year,
                "summary": {
                    "total_taxable_amount": total_taxable_amount,
                    "total_gst_collected": total_gst_collected,
                    "total_gst_paid": total_gst_paid,
                    "net_gst_liability": net_gst_liability,
                    "transaction_count": len(month_transactions)
                },
                "transactions": [asdict(t) for t in month_transactions],
                "ai_analysis": ai_analysis
            }
            
        except Exception as e:
            logger.error(f"Error getting GST summary: {e}")
            return {"success": False, "error": str(e)}
    
    def calculate_gst_return(self, business_id: str, month: str, year: str) -> Dict:
        """Calculate GST return amount."""
        try:
            gst_summary = self.get_gst_summary(business_id, month, year)
            
            if not gst_summary["success"]:
                return gst_summary
            
            net_liability = gst_summary["summary"]["net_gst_liability"]
            
            # Get business profile for additional context
            profile = self._load_business_profile(business_id)
            
            # Get AI recommendations for GST return
            ai_recommendations = self._get_ai_gst_return_advice(profile, gst_summary["summary"])
            
            return {
                "success": True,
                "month": month,
                "year": year,
                "gst_return_amount": max(0, net_liability),  # Only positive liability needs to be paid
                "refund_amount": max(0, -net_liability),    # Negative liability means refund
                "due_date": self._calculate_gst_due_date(month, year),
                "ai_recommendations": ai_recommendations,
                "summary": gst_summary["summary"]
            }
            
        except Exception as e:
            logger.error(f"Error calculating GST return: {e}")
            return {"success": False, "error": str(e)}
    
    def get_monthly_reminder_data(self, business_id: str) -> Dict:
        """Get data for monthly GST reminder (20th of every month)."""
        try:
            current_date = datetime.now()
            last_month = current_date.replace(day=1) - timedelta(days=1)
            
            # Get GST return calculation for last month
            gst_return = self.calculate_gst_return(
                business_id, 
                str(last_month.month), 
                str(last_month.year)
            )
            
            if gst_return["success"]:
                return {
                    "success": True,
                    "reminder_date": current_date.strftime("%Y-%m-%d"),
                    "for_month": last_month.strftime("%B %Y"),
                    "gst_return_data": gst_return,
                    "action_required": gst_return["gst_return_amount"] > 0,
                    "message": f"GST return reminder for {last_month.strftime('%B %Y')}"
                }
            
            return gst_return
            
        except Exception as e:
            logger.error(f"Error getting reminder data: {e}")
            return {"success": False, "error": str(e)}
    
    def get_business_analytics(self, business_id: str, period: str = "month") -> Dict:
        """Get comprehensive business analytics with AI insights."""
        try:
            transactions = self._load_business_transactions(business_id)
            
            # Calculate analytics based on period
            if period == "month":
                start_date = datetime.now().replace(day=1)
            elif period == "quarter":
                current_month = datetime.now().month
                quarter_start_month = ((current_month - 1) // 3) * 3 + 1
                start_date = datetime.now().replace(month=quarter_start_month, day=1)
            else:  # year
                start_date = datetime.now().replace(month=1, day=1)
            
            # Filter transactions for period
            period_transactions = [
                t for t in transactions 
                if datetime.strptime(t.date, "%Y-%m-%d") >= start_date
            ]
            
            # Calculate metrics
            total_credits = sum(t.amount for t in period_transactions if t.transaction_type == "credit")
            total_debits = sum(t.amount for t in period_transactions if t.transaction_type == "debit")
            net_profit = total_credits - total_debits
            total_gst = sum(t.gst_amount for t in period_transactions if t.gst_applicable)
            
            # Get AI business insights
            ai_insights = self._get_ai_business_insights(business_id, period_transactions, {
                "total_credits": total_credits,
                "total_debits": total_debits,
                "net_profit": net_profit,
                "total_gst": total_gst
            })
            
            return {
                "success": True,
                "period": period,
                "analytics": {
                    "total_credits": total_credits,
                    "total_debits": total_debits,
                    "net_profit": net_profit,
                    "total_gst": total_gst,
                    "transaction_count": len(period_transactions),
                    "average_transaction": (total_credits + total_debits) / len(period_transactions) if period_transactions else 0
                },
                "ai_insights": ai_insights
            }
            
        except Exception as e:
            logger.error(f"Error getting business analytics: {e}")
            return {"success": False, "error": str(e)}

    def add_tax_record(self, business_id: str, tax_data: Dict) -> Dict:
        """Add a comprehensive tax record with transaction details."""
        try:
            # Generate unique tax record ID
            tax_record_id = f"tax_{business_id}_{int(datetime.now().timestamp())}"

            # Validate input data
            required_fields = ["tax_type", "tax_name", "amount", "due_date", "authority"]
            for field in required_fields:
                if field not in tax_data:
                    return {"success": False, "error": f"Missing required field: {field}"}

            # Create tax record
            tax_record = TaxRecord(
                tax_record_id=tax_record_id,
                business_id=business_id,
                tax_type=tax_data["tax_type"],
                tax_name=tax_data["tax_name"],
                amount=float(tax_data["amount"]),
                due_date=tax_data["due_date"],
                payment_date=tax_data.get("payment_date", ""),
                transaction_number=tax_data.get("transaction_number", ""),
                authority=tax_data["authority"],
                description=tax_data.get("description", ""),
                status=tax_data.get("status", "pending"),
                created_at=datetime.now().isoformat()
            )

            # Save tax record
            self._save_tax_record(tax_record)

            # Get AI insights for tax optimization
            ai_insights = self._get_ai_tax_insights(business_id, tax_record)

            return {
                "success": True,
                "tax_record_id": tax_record_id,
                "tax_record": asdict(tax_record),
                "ai_insights": ai_insights,
                "message": "Tax record added successfully!"
            }

        except Exception as e:
            logger.error(f"Error adding tax record: {e}")
            return {"success": False, "error": str(e)}

    def get_comprehensive_tax_summary(self, business_id: str, period: str = "month") -> Dict:
        """Get comprehensive tax summary for all tax types."""
        try:
            # Calculate period dates
            if period == "month":
                start_date = datetime.now().replace(day=1)
            elif period == "quarter":
                current_month = datetime.now().month
                quarter_start_month = ((current_month - 1) // 3) * 3 + 1
                start_date = datetime.now().replace(month=quarter_start_month, day=1)
            else:  # year
                start_date = datetime.now().replace(month=1, day=1)

            # Load all tax records
            tax_records = self._load_tax_records(business_id)

            # Filter records for period
            period_records = [
                record for record in tax_records
                if datetime.fromisoformat(record.created_at) >= start_date
            ]

            # Group by tax type
            tax_summary = {}
            total_tax_paid = 0
            total_pending = 0
            overdue_count = 0

            for record in period_records:
                tax_type = record.tax_type
                if tax_type not in tax_summary:
                    tax_summary[tax_type] = {
                        "total_amount": 0,
                        "paid_amount": 0,
                        "pending_amount": 0,
                        "record_count": 0,
                        "overdue_count": 0
                    }

                tax_summary[tax_type]["total_amount"] += record.amount
                tax_summary[tax_type]["record_count"] += 1

                if record.status == "paid":
                    tax_summary[tax_type]["paid_amount"] += record.amount
                    total_tax_paid += record.amount
                elif record.status == "pending":
                    tax_summary[tax_type]["pending_amount"] += record.amount
                    total_pending += record.amount
                elif record.status == "overdue":
                    tax_summary[tax_type]["overdue_count"] += 1
                    overdue_count += 1

            # Get AI analysis
            ai_analysis = self._get_ai_comprehensive_tax_analysis(business_id, tax_summary, period_records)

            return {
                "success": True,
                "period": period,
                "summary": {
                    "total_tax_paid": total_tax_paid,
                    "total_pending": total_pending,
                    "overdue_count": overdue_count,
                    "tax_breakdown": tax_summary,
                    "record_count": len(period_records)
                },
                "records": [asdict(record) for record in period_records],
                "ai_analysis": ai_analysis
            }

        except Exception as e:
            logger.error(f"Error getting comprehensive tax summary: {e}")
            return {"success": False, "error": str(e)}

    def get_tax_reminders(self, business_id: str) -> Dict:
        """Get upcoming tax reminders and overdue notifications."""
        try:
            tax_records = self._load_tax_records(business_id)
            current_date = datetime.now()

            upcoming_taxes = []
            overdue_taxes = []

            for record in tax_records:
                if record.status != "paid":
                    due_date = datetime.strptime(record.due_date, "%Y-%m-%d")
                    days_until_due = (due_date - current_date).days

                    if days_until_due < 0:
                        # Overdue
                        overdue_taxes.append({
                            **asdict(record),
                            "days_overdue": abs(days_until_due)
                        })
                    elif days_until_due <= 30:
                        # Due within 30 days
                        upcoming_taxes.append({
                            **asdict(record),
                            "days_until_due": days_until_due
                        })

            # Get AI recommendations for tax planning
            ai_recommendations = self._get_ai_tax_planning_recommendations(business_id, upcoming_taxes, overdue_taxes)

            return {
                "success": True,
                "upcoming_taxes": upcoming_taxes,
                "overdue_taxes": overdue_taxes,
                "ai_recommendations": ai_recommendations,
                "reminder_count": len(upcoming_taxes) + len(overdue_taxes)
            }

        except Exception as e:
            logger.error(f"Error getting tax reminders: {e}")
            return {"success": False, "error": str(e)}

    def update_tax_payment(self, tax_record_id: str, payment_data: Dict) -> Dict:
        """Update tax payment with transaction details."""
        try:
            # Load existing tax records
            business_id = payment_data.get("business_id")
            if not business_id:
                return {"success": False, "error": "business_id is required"}

            tax_records = self._load_tax_records(business_id)

            # Find and update the record
            updated = False
            for record in tax_records:
                if record.tax_record_id == tax_record_id:
                    record.payment_date = payment_data.get("payment_date", datetime.now().strftime("%Y-%m-%d"))
                    record.transaction_number = payment_data.get("transaction_number", "")
                    record.status = "paid"
                    updated = True
                    break

            if not updated:
                return {"success": False, "error": "Tax record not found"}

            # Save updated records
            self._save_all_tax_records(business_id, tax_records)

            # Get AI insights for payment
            ai_insights = self._get_ai_payment_insights(business_id, tax_record_id)

            return {
                "success": True,
                "tax_record_id": tax_record_id,
                "ai_insights": ai_insights,
                "message": "Tax payment updated successfully!"
            }

        except Exception as e:
            logger.error(f"Error updating tax payment: {e}")
            return {"success": False, "error": str(e)}

    def _get_ai_transaction_insights(self, business_id: str, transaction: BusinessTransaction) -> Dict:
        """Get AI insights for a transaction."""
        try:
            from ai_provider_manager import get_ai_manager

            ai_manager = get_ai_manager()

            prompt = f"""
            Analyze this business transaction and provide insights:

            Type: {transaction.transaction_type}
            Amount: ₹{transaction.amount:,.2f}
            Category: {transaction.category}
            GST: {transaction.gst_rate}% (₹{transaction.gst_amount:,.2f})
            Description: {transaction.description}

            Provide:
            1. Transaction categorization suggestions
            2. Tax optimization tips
            3. Cash flow impact analysis

            Format as JSON with keys: categorization, tax_tips, cash_flow_impact
            """

            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)

            if response["success"]:
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return {
                "categorization": "Transaction recorded successfully",
                "tax_tips": "Ensure proper documentation for tax purposes",
                "cash_flow_impact": "Monitor overall cash flow trends"
            }

        except Exception as e:
            logger.error(f"Error getting AI transaction insights: {e}")
            return {
                "categorization": "General business transaction",
                "tax_tips": "Keep proper records",
                "cash_flow_impact": "Regular monitoring recommended"
            }

    def _get_ai_gst_analysis(self, business_id: str, transactions: List[BusinessTransaction], net_liability: float) -> Dict:
        """Get AI analysis of GST situation."""
        try:
            from ai_provider_manager import get_ai_manager

            ai_manager = get_ai_manager()

            total_amount = sum(t.amount for t in transactions)

            prompt = f"""
            Analyze this GST situation for a business:

            Total transactions: {len(transactions)}
            Total amount: ₹{total_amount:,.2f}
            Net GST liability: ₹{net_liability:,.2f}

            Provide:
            1. GST compliance assessment
            2. Optimization suggestions
            3. Risk factors to watch

            Format as JSON with keys: compliance_status, optimization_tips, risk_factors
            """

            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)

            if response["success"]:
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return {
                "compliance_status": "Regular monitoring recommended",
                "optimization_tips": "Maintain proper GST records",
                "risk_factors": "Ensure timely filing"
            }

        except Exception as e:
            logger.error(f"Error getting AI GST analysis: {e}")
            return {
                "compliance_status": "Monitor regularly",
                "optimization_tips": "Keep good records",
                "risk_factors": "File on time"
            }

    def _get_ai_gst_return_advice(self, profile: BusinessProfile, summary: Dict) -> Dict:
        """Get AI advice for GST return."""
        try:
            from ai_provider_manager import get_ai_manager

            ai_manager = get_ai_manager()

            prompt = f"""
            Provide GST return advice for:

            Business: {profile.business_name}
            Sector: {profile.sector}
            GST Number: {profile.gst_number}
            Net Liability: ₹{summary['net_gst_liability']:,.2f}

            Provide specific advice for:
            1. Filing requirements
            2. Payment strategies
            3. Compliance tips

            Format as JSON with keys: filing_advice, payment_strategy, compliance_tips
            """

            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)

            if response["success"]:
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return {
                "filing_advice": "File GST return by due date",
                "payment_strategy": "Pay GST liability on time",
                "compliance_tips": "Maintain proper documentation"
            }

        except Exception as e:
            logger.error(f"Error getting AI GST return advice: {e}")
            return {
                "filing_advice": "File on time",
                "payment_strategy": "Pay promptly",
                "compliance_tips": "Keep records"
            }

    def _get_ai_business_insights(self, business_id: str, transactions: List[BusinessTransaction], metrics: Dict) -> Dict:
        """Get AI insights for business performance."""
        try:
            from ai_provider_manager import get_ai_manager

            ai_manager = get_ai_manager()

            prompt = f"""
            Analyze business performance:

            Total Credits: ₹{metrics['total_credits']:,.2f}
            Total Debits: ₹{metrics['total_debits']:,.2f}
            Net Profit: ₹{metrics['net_profit']:,.2f}
            Total GST: ₹{metrics['total_gst']:,.2f}
            Transactions: {metrics['transaction_count']}

            Provide:
            1. Performance analysis
            2. Growth recommendations
            3. Cost optimization tips

            Format as JSON with keys: performance_analysis, growth_tips, cost_optimization
            """

            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)

            if response["success"]:
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return {
                "performance_analysis": "Business showing activity",
                "growth_tips": "Focus on increasing revenue",
                "cost_optimization": "Monitor expenses closely"
            }

        except Exception as e:
            logger.error(f"Error getting AI business insights: {e}")
            return {
                "performance_analysis": "Regular monitoring needed",
                "growth_tips": "Explore growth opportunities",
                "cost_optimization": "Control costs effectively"
            }

    def _calculate_gst_due_date(self, month: str, year: str) -> str:
        """Calculate GST due date (20th of next month)."""
        try:
            month_int = int(month)
            year_int = int(year)

            if month_int == 12:
                due_month = 1
                due_year = year_int + 1
            else:
                due_month = month_int + 1
                due_year = year_int

            return f"{due_year}-{due_month:02d}-20"

        except:
            return datetime.now().strftime("%Y-%m-20")

    def _save_business_profile(self, profile: BusinessProfile):
        """Save business profile to file."""
        file_path = os.path.join(self.data_dir, f"profile_{profile.business_id}.json")
        with open(file_path, 'w') as f:
            json.dump(asdict(profile), f, indent=2)

    def _save_transaction(self, transaction: BusinessTransaction):
        """Save transaction to file."""
        file_path = os.path.join(self.data_dir, f"transactions_{transaction.business_id}.json")

        # Load existing transactions
        transactions = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                transactions = json.load(f)

        # Add new transaction
        transactions.append(asdict(transaction))

        # Save updated transactions
        with open(file_path, 'w') as f:
            json.dump(transactions, f, indent=2)

    def _update_gst_records(self, transaction: BusinessTransaction):
        """Update GST records for the transaction."""
        try:
            date_obj = datetime.strptime(transaction.date, "%Y-%m-%d")
            month = str(date_obj.month)
            year = str(date_obj.year)

            record = GSTRecord(
                record_id=f"gst_{transaction.transaction_id}",
                business_id=transaction.business_id,
                gst_number=transaction.party_gst_number,
                sector=transaction.category,
                gst_rate=transaction.gst_rate,
                taxable_amount=transaction.amount,
                gst_amount=transaction.gst_amount,
                month=month,
                year=year,
                created_at=datetime.now().isoformat()
            )

            # Save GST record
            file_path = os.path.join(self.data_dir, f"gst_records_{transaction.business_id}.json")

            records = []
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    records = json.load(f)

            records.append(asdict(record))

            with open(file_path, 'w') as f:
                json.dump(records, f, indent=2)

        except Exception as e:
            logger.error(f"Error updating GST records: {e}")

    def _load_business_profile(self, business_id: str) -> Optional[BusinessProfile]:
        """Load business profile from file."""
        file_path = os.path.join(self.data_dir, f"profile_{business_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                return BusinessProfile(**data)
        return None

    def _load_business_transactions(self, business_id: str) -> List[BusinessTransaction]:
        """Load business transactions from file."""
        file_path = os.path.join(self.data_dir, f"transactions_{business_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                transactions_data = json.load(f)
                return [BusinessTransaction(**txn) for txn in transactions_data]
        return []

    def _save_tax_record(self, tax_record: TaxRecord):
        """Save tax record to file."""
        file_path = os.path.join(self.data_dir, f"tax_records_{tax_record.business_id}.json")

        # Load existing records
        records = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                records = json.load(f)

        # Add new record
        records.append(asdict(tax_record))

        # Save updated records
        with open(file_path, 'w') as f:
            json.dump(records, f, indent=2)

    def _load_tax_records(self, business_id: str) -> List[TaxRecord]:
        """Load tax records from file."""
        file_path = os.path.join(self.data_dir, f"tax_records_{business_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                records_data = json.load(f)
                return [TaxRecord(**record) for record in records_data]
        return []

    def _save_all_tax_records(self, business_id: str, tax_records: List[TaxRecord]):
        """Save all tax records to file."""
        file_path = os.path.join(self.data_dir, f"tax_records_{business_id}.json")
        with open(file_path, 'w') as f:
            json.dump([asdict(record) for record in tax_records], f, indent=2)

    def _get_ai_tax_setup_recommendations(self, profile: BusinessProfile) -> Dict:
        """Get AI recommendations for tax setup."""
        try:
            from ai_provider_manager import get_ai_manager

            ai_manager = get_ai_manager()

            prompt = f"""
            Provide tax setup recommendations for this business:

            Business: {profile.business_name}
            Type: {profile.business_type}
            Sector: {profile.sector}
            State: {profile.state}

            Recommend:
            1. Required tax registrations
            2. Applicable tax types
            3. Compliance requirements
            4. Filing frequencies

            Format as JSON with keys: required_registrations, applicable_taxes, compliance_tips, filing_schedule
            """

            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)

            if response["success"]:
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return {
                "required_registrations": ["GST Registration", "Professional Tax", "Trade License"],
                "applicable_taxes": ["GST", "Income Tax", "Professional Tax", "Municipality Tax"],
                "compliance_tips": ["Maintain proper records", "File returns on time", "Keep transaction proofs"],
                "filing_schedule": "Monthly GST, Quarterly Income Tax, Annual Returns"
            }

        except Exception as e:
            logger.error(f"Error getting AI tax setup recommendations: {e}")
            return {
                "required_registrations": ["Basic tax registrations needed"],
                "applicable_taxes": ["Standard business taxes apply"],
                "compliance_tips": ["Maintain good records"],
                "filing_schedule": "Regular filing required"
            }

    def _get_ai_tax_insights(self, business_id: str, tax_record: TaxRecord) -> Dict:
        """Get AI insights for tax record."""
        try:
            from ai_provider_manager import get_ai_manager

            ai_manager = get_ai_manager()

            prompt = f"""
            Analyze this tax payment and provide insights:

            Tax Type: {tax_record.tax_type}
            Tax Name: {tax_record.tax_name}
            Amount: ₹{tax_record.amount:,.2f}
            Authority: {tax_record.authority}
            Due Date: {tax_record.due_date}
            Status: {tax_record.status}

            Provide:
            1. Tax optimization tips
            2. Compliance recommendations
            3. Planning suggestions

            Format as JSON with keys: optimization_tips, compliance_advice, planning_suggestions
            """

            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)

            if response["success"]:
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return {
                "optimization_tips": ["Plan payments in advance", "Maintain proper documentation"],
                "compliance_advice": ["Pay before due date", "Keep payment receipts"],
                "planning_suggestions": ["Set up payment reminders", "Budget for tax payments"]
            }

        except Exception as e:
            logger.error(f"Error getting AI tax insights: {e}")
            return {
                "optimization_tips": ["Regular tax planning needed"],
                "compliance_advice": ["Follow tax regulations"],
                "planning_suggestions": ["Plan tax payments ahead"]
            }

    def _get_ai_comprehensive_tax_analysis(self, business_id: str, tax_summary: Dict, records: List[TaxRecord]) -> Dict:
        """Get AI analysis of comprehensive tax situation."""
        try:
            from ai_provider_manager import get_ai_manager

            ai_manager = get_ai_manager()

            total_taxes = sum(summary["total_amount"] for summary in tax_summary.values())

            prompt = f"""
            Analyze comprehensive tax situation:

            Total Tax Types: {len(tax_summary)}
            Total Tax Amount: ₹{total_taxes:,.2f}
            Total Records: {len(records)}

            Tax Breakdown: {list(tax_summary.keys())}

            Provide:
            1. Overall tax health assessment
            2. Optimization opportunities
            3. Risk factors
            4. Strategic recommendations

            Format as JSON with keys: health_assessment, optimization_opportunities, risk_factors, strategic_recommendations
            """

            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)

            if response["success"]:
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return {
                "health_assessment": "Regular monitoring recommended",
                "optimization_opportunities": ["Consolidate tax payments", "Plan payment schedules"],
                "risk_factors": ["Monitor due dates", "Ensure compliance"],
                "strategic_recommendations": ["Implement tax planning", "Use professional advice"]
            }

        except Exception as e:
            logger.error(f"Error getting AI comprehensive tax analysis: {e}")
            return {
                "health_assessment": "Tax situation needs attention",
                "optimization_opportunities": ["Review tax strategy"],
                "risk_factors": ["Monitor compliance"],
                "strategic_recommendations": ["Seek professional guidance"]
            }

    def _get_ai_tax_planning_recommendations(self, business_id: str, upcoming_taxes: List, overdue_taxes: List) -> Dict:
        """Get AI recommendations for tax planning."""
        try:
            from ai_provider_manager import get_ai_manager

            ai_manager = get_ai_manager()

            prompt = f"""
            Provide tax planning recommendations:

            Upcoming Taxes: {len(upcoming_taxes)} items
            Overdue Taxes: {len(overdue_taxes)} items

            Provide:
            1. Immediate actions needed
            2. Payment prioritization
            3. Cash flow planning
            4. Compliance strategies

            Format as JSON with keys: immediate_actions, payment_priority, cash_flow_tips, compliance_strategy
            """

            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)

            if response["success"]:
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return {
                "immediate_actions": ["Pay overdue taxes first", "Plan upcoming payments"],
                "payment_priority": ["Statutory taxes first", "Then other obligations"],
                "cash_flow_tips": ["Budget for tax payments", "Maintain cash reserves"],
                "compliance_strategy": ["Set up reminders", "Maintain documentation"]
            }

        except Exception as e:
            logger.error(f"Error getting AI tax planning recommendations: {e}")
            return {
                "immediate_actions": ["Review tax obligations"],
                "payment_priority": ["Pay by due dates"],
                "cash_flow_tips": ["Plan payments ahead"],
                "compliance_strategy": ["Stay compliant"]
            }

    def _get_ai_payment_insights(self, business_id: str, tax_record_id: str) -> Dict:
        """Get AI insights for tax payment."""
        try:
            from ai_provider_manager import get_ai_manager

            ai_manager = get_ai_manager()

            prompt = f"""
            Provide insights for completed tax payment:

            Payment completed for tax record: {tax_record_id}

            Provide:
            1. Next steps after payment
            2. Documentation requirements
            3. Future planning tips

            Format as JSON with keys: next_steps, documentation_needed, future_planning
            """

            messages = [{"role": "user", "content": prompt}]
            response = ai_manager.generate_response(messages)

            if response["success"]:
                try:
                    import re
                    json_match = re.search(r'\{.*\}', response["response"], re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass

            return {
                "next_steps": ["Keep payment receipt", "Update records"],
                "documentation_needed": ["Payment proof", "Transaction details"],
                "future_planning": ["Plan next payments", "Set reminders"]
            }

        except Exception as e:
            logger.error(f"Error getting AI payment insights: {e}")
            return {
                "next_steps": ["Maintain records"],
                "documentation_needed": ["Keep receipts"],
                "future_planning": ["Plan ahead"]
            }

# Global instance
business_tracker = BusinessTracker()
