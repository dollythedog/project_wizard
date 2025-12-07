"""
Pro Forma calculation engine.

Performs all financial calculations for staffing expenses, FTE requirements,
and revenue projections (internal version only).
"""

import json
from typing import Dict, List, Tuple
from decimal import Decimal, ROUND_HALF_UP

from app.models.proforma import ProForma, ServiceLine, BillingCode
from sqlmodel import Session, select


class ProFormaCalculator:
    """
    Calculator for Pro Forma financial projections.
    
    Handles:
    - FTE calculations from shift requirements
    - Staffing expense calculations
    - Revenue projections (E/M + procedures)
    - Direct and indirect cost calculations
    """
    
    # Standard assumptions
    WEEKS_PER_YEAR = 52
    AVG_WEEKS_PER_MONTH = 4.33  # 52 weeks / 12 months
    
    def __init__(self, session: Session = None):
        """Initialize calculator with optional database session for billing code lookup."""
        self.session = session
        self._billing_codes_cache = {}
    
    def calculate_service_line(
        self,
        service_line: ServiceLine,
        physician_hourly_rate: float,
        app_hourly_rate: float,
        shifts_per_physician_per_month: int = 20,
        shifts_per_app_per_month: int = 22
    ) -> ServiceLine:
        """
        Calculate all metrics for a single service line using HYBRID logic.
        
        FTE Calculation (SHIFT-BASED):
        - Monthly shift requirement = Days/Week × 4.33 (avg weeks/month)
        - FTE = Monthly shift requirement / Shifts per provider per month
        
        Cost Calculation (HOURLY-BASED):
        - Annual hours = Hours/Shift × Days/Week × 52 weeks
        - Annual cost = Annual hours × Hourly rate
        
        Args:
            service_line: ServiceLine instance with input data
            physician_hourly_rate: Default hourly rate for physicians (for billing)
            app_hourly_rate: Default hourly rate for APPs (for billing)
            
        Returns:
            Updated ServiceLine with all calculations populated
        """
        # Use overrides if present, otherwise use defaults
        phys_rate = service_line.physician_hourly_rate_override or physician_hourly_rate
        app_rate = service_line.app_hourly_rate_override or app_hourly_rate
        
        # Calculate annual shift requirements
        annual_shifts = service_line.days_per_week * self.WEEKS_PER_YEAR
        
        # Calculate monthly shift requirements (for FTE calculation only)
        monthly_shifts = service_line.days_per_week * self.AVG_WEEKS_PER_MONTH
        
        # Physician calculations
        service_line.annual_physician_shifts = annual_shifts * service_line.physicians_per_day
        
        # FTE Calculation (SHIFT-BASED): Monthly shifts needed / Shifts per physician per month
        if service_line.physicians_per_day > 0 and shifts_per_physician_per_month:
            service_line.physician_fte = self._round_decimal(
                (monthly_shifts * service_line.physicians_per_day) / shifts_per_physician_per_month,
                2
            )
        else:
            service_line.physician_fte = 0.0
        
        # Cost Calculation (HOURLY-BASED): Annual hours × Hourly rate
        annual_physician_hours = service_line.annual_physician_shifts * service_line.physician_hours_per_shift
        service_line.annual_physician_cost = self._round_decimal(
            annual_physician_hours * phys_rate, 2
        )
        
        # APP calculations
        service_line.annual_app_shifts = annual_shifts * service_line.apps_per_day
        
        # FTE Calculation (SHIFT-BASED): Monthly shifts needed / Shifts per APP per month
        if service_line.apps_per_day > 0 and shifts_per_app_per_month:
            service_line.app_fte = self._round_decimal(
                (monthly_shifts * service_line.apps_per_day) / shifts_per_app_per_month,
                2
            )
        else:
            service_line.app_fte = 0.0
        
        # Cost Calculation (HOURLY-BASED): Annual hours × Hourly rate
        annual_app_hours = service_line.annual_app_shifts * service_line.app_hours_per_shift
        service_line.annual_app_cost = self._round_decimal(
            annual_app_hours * app_rate, 2
        )
        
        # Total cost for this service line
        service_line.total_annual_cost = self._round_decimal(
            service_line.annual_physician_cost + service_line.annual_app_cost, 2
        )
        
        # Calculate revenue if census and billing data provided (internal only)
        if service_line.avg_daily_census and service_line.em_billing_profile:
            self._calculate_service_line_revenue(service_line)
        
        return service_line
    
    def _get_billing_code_rate(self, code: str) -> float:
        """Get billing rate for a code (with caching)."""
        if code in self._billing_codes_cache:
            return self._billing_codes_cache[code]
        
        if self.session:
            billing_code = self.session.exec(
                select(BillingCode).where(BillingCode.code == code)
            ).first()
            
            if billing_code:
                self._billing_codes_cache[code] = billing_code.rate
                return billing_code.rate
        
        return 0.0
    
    def _calculate_service_line_revenue(self, service_line: ServiceLine):
        """Calculate revenue projections for a service line (internal only)."""
        # Annual E/M encounters
        service_line.annual_em_encounters = self._round_decimal(
            service_line.avg_daily_census * 
            service_line.days_per_week * 
            self.WEEKS_PER_YEAR,
            0
        )
        
        # Parse E/M billing profile
        em_profile = json.loads(service_line.em_billing_profile) if service_line.em_billing_profile else {}
        
        # Calculate E/M revenue
        em_revenue = 0.0
        for code, mix_pct in em_profile.items():
            encounters_for_code = service_line.annual_em_encounters * mix_pct
            rate = self._get_billing_code_rate(code)
            em_revenue += encounters_for_code * rate
        
        # Calculate procedure revenue if applicable
        procedure_revenue = 0.0
        if service_line.avg_daily_procedures and service_line.procedure_billing_profile:
            service_line.annual_procedure_count = self._round_decimal(
                service_line.avg_daily_procedures *
                service_line.days_per_week *
                self.WEEKS_PER_YEAR,
                0
            )
            
            proc_profile = json.loads(service_line.procedure_billing_profile)
            for code, mix_pct in proc_profile.items():
                procedures_for_code = service_line.annual_procedure_count * mix_pct
                rate = self._get_billing_code_rate(code)
                procedure_revenue += procedures_for_code * rate
        
        service_line.projected_revenue = self._round_decimal(
            em_revenue + procedure_revenue, 2
        )
    
    def calculate_proforma_totals(
        self,
        proforma: ProForma,
        service_lines: List[ServiceLine]
    ) -> ProForma:
        """
        Calculate aggregate totals across all service lines.
        
        Args:
            proforma: ProForma instance
            service_lines: List of calculated ServiceLine instances
            
        Returns:
            Updated ProForma with totals populated
        """
        # Sum staffing metrics
        proforma.total_physician_fte = self._round_decimal(
            sum(sl.physician_fte or 0 for sl in service_lines), 2
        )
        proforma.total_app_fte = self._round_decimal(
            sum(sl.app_fte or 0 for sl in service_lines), 2
        )
        
        # Sum external costs (what we bill the hospital)
        proforma.total_annual_cost = self._round_decimal(
            sum(sl.total_annual_cost or 0 for sl in service_lines), 2
        )
        
        # Calculate internal P&L if we have salary data
        if proforma.physician_salary:
            self._calculate_internal_pl(proforma, service_lines)
        
        return proforma
    
    def _calculate_internal_pl(
        self,
        proforma: ProForma,
        service_lines: List[ServiceLine]
    ):
        """Calculate full P&L for internal version."""
        # Direct costs
        physician_comp_per_fte = (
            proforma.physician_salary +
            proforma.physician_benefits_taxes +
            proforma.physician_malpractice
        )
        total_physician_comp = physician_comp_per_fte * proforma.total_physician_fte
        
        app_comp_per_fte = (
            proforma.app_salary +
            proforma.app_benefits_taxes +
            proforma.app_malpractice
        )
        total_app_comp = app_comp_per_fte * proforma.total_app_fte
        
        proforma.total_direct_expenses = self._round_decimal(
            total_physician_comp + total_app_comp, 2
        )
        
        # Indirect costs (as % of direct costs)
        admin_overhead = proforma.total_direct_expenses * proforma.admin_overhead_pct
        financial_oversight = proforma.total_direct_expenses * proforma.financial_oversight_pct
        office_materials = proforma.total_direct_expenses * proforma.office_materials_pct
        credentialing = proforma.total_direct_expenses * proforma.credentialing_pct
        rcm = proforma.total_direct_expenses * proforma.rcm_pct
        
        proforma.total_indirect_expenses = self._round_decimal(
            admin_overhead + financial_oversight + office_materials + credentialing + rcm,
            2
        )
        
        # Revenue
        proforma.total_projected_revenue = self._round_decimal(
            sum(sl.projected_revenue or 0 for sl in service_lines), 2
        )
        
        # Net income
        total_expenses = proforma.total_direct_expenses + proforma.total_indirect_expenses
        proforma.net_income = self._round_decimal(
            proforma.total_projected_revenue - total_expenses, 2
        )
    
    def generate_external_breakdown(
        self,
        proforma: ProForma,
        service_lines: List[ServiceLine]
    ) -> List[Dict]:
        """
        Generate hospital-facing expense breakdown table.
        
        Returns:
            List of dictionaries with service line breakdown for markdown table
        """
        breakdown = []
        
        for sl in sorted(service_lines, key=lambda x: x.order):
            # Build description
            parts = []
            if sl.physicians_per_day > 0:
                parts.append(f"{sl.physicians_per_day} Physician ({sl.physician_hours_per_shift}hr)")
            if sl.apps_per_day > 0:
                parts.append(f"{sl.apps_per_day} APP ({sl.app_hours_per_shift}hr)")
            
            provider_desc = " + ".join(parts)
            description = f"{provider_desc}, {sl.days_per_week} days/week"
            
            # Calculate daily rate for display
            daily_rate = sl.total_annual_cost / (sl.days_per_week * self.WEEKS_PER_YEAR)
            
            breakdown.append({
                "service_line": sl.name,
                "description": description,
                "daily_rate": f"${daily_rate:,.2f} per day",
                "annual_cost": f"${sl.total_annual_cost:,.2f}",
                "physician_fte": f"{sl.physician_fte:.2f}",
                "app_fte": f"{sl.app_fte:.2f}"
            })
        
        return breakdown
    
    def generate_internal_pl_table(
        self,
        proforma: ProForma,
        service_lines: List[ServiceLine],
        years: int = 3
    ) -> Dict:
        """
        Generate internal P&L table (multi-year projection).
        
        Args:
            proforma: ProForma with calculated totals
            years: Number of years to project (default 3)
            
        Returns:
            Dictionary with P&L data for table generation
        """
        # For now, assume flat revenue/expenses across years
        # In future, could add growth rates
        
        physician_comp_per_fte = (
            proforma.physician_salary +
            proforma.physician_benefits_taxes +
            proforma.physician_malpractice
        )
        
        app_comp_per_fte = (
            proforma.app_salary +
            proforma.app_benefits_taxes +
            proforma.app_malpractice
        )
        
        # Build service line revenue breakdown with volume and billing details
        service_line_revenues = []
        for sl in sorted(service_lines, key=lambda x: x.order):
            if sl.projected_revenue and sl.projected_revenue > 0:
                # Build calculation note
                calc_parts = []
                if sl.annual_em_encounters and sl.annual_em_encounters > 0:
                    calc_parts.append(f"{sl.annual_em_encounters:,.0f} E/M encounters")
                if sl.annual_procedure_count and sl.annual_procedure_count > 0:
                    calc_parts.append(f"{sl.annual_procedure_count:,.0f} procedures")
                
                calc_note = " + ".join(calc_parts) if calc_parts else "Revenue projection"
                
                # Parse billing profiles for detailed breakdown
                em_profile = json.loads(sl.em_billing_profile) if sl.em_billing_profile else {}
                proc_profile = json.loads(sl.procedure_billing_profile) if sl.procedure_billing_profile else {}
                
                service_line_revenues.append({
                    "name": sl.name,
                    "revenue": sl.projected_revenue,
                    "calc_note": calc_note,
                    "avg_daily_census": sl.avg_daily_census,
                    "avg_daily_procedures": sl.avg_daily_procedures,
                    "annual_em_encounters": sl.annual_em_encounters,
                    "annual_procedure_count": sl.annual_procedure_count,
                    "em_profile": em_profile,
                    "proc_profile": proc_profile
                })
        
        pl_data = {
            "years": list(range(1, years + 1)),
            "physician_fte": proforma.total_physician_fte,
            "app_fte": proforma.total_app_fte,
            "total_fte": proforma.total_physician_fte + proforma.total_app_fte,
            
            # Revenue (same across years for now)
            "projected_revenue": [proforma.total_projected_revenue] * years,
            "service_line_revenues": service_line_revenues,
            
            # Direct costs
            "physician_salary": proforma.physician_salary,
            "physician_benefits": proforma.physician_benefits_taxes,
            "physician_malpractice": proforma.physician_malpractice,
            "physician_comp_per_fte": physician_comp_per_fte,
            "total_physician_comp": [physician_comp_per_fte * proforma.total_physician_fte] * years,
            
            "app_salary": proforma.app_salary,
            "app_benefits": proforma.app_benefits_taxes,
            "app_malpractice": proforma.app_malpractice,
            "app_comp_per_fte": app_comp_per_fte,
            "total_app_comp": [app_comp_per_fte * proforma.total_app_fte] * years,
            
            "total_direct_expenses": [proforma.total_direct_expenses] * years,
            
            # Indirect costs
            "admin_overhead": [proforma.total_direct_expenses * proforma.admin_overhead_pct] * years,
            "financial_oversight": [proforma.total_direct_expenses * proforma.financial_oversight_pct] * years,
            "office_materials": [proforma.total_direct_expenses * proforma.office_materials_pct] * years,
            "credentialing": [proforma.total_direct_expenses * proforma.credentialing_pct] * years,
            "rcm": [proforma.total_direct_expenses * proforma.rcm_pct] * years,
            "total_indirect_expenses": [proforma.total_indirect_expenses] * years,
            
            # Totals
            "total_expenses": [proforma.total_direct_expenses + proforma.total_indirect_expenses] * years,
            "net_income": [proforma.net_income] * years
        }
        
        return pl_data
    
    @staticmethod
    def _round_decimal(value: float, places: int = 2) -> float:
        """Round to specified decimal places using banker's rounding."""
        if value is None:
            return 0.0
        d = Decimal(str(value))
        quantizer = Decimal(10) ** -places
        return float(d.quantize(quantizer, rounding=ROUND_HALF_UP))
