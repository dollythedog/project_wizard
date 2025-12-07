"""
Pro Forma routes for creating and managing financial projections.
"""

import json
from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.models.database import Project
from app.models.proforma import ProForma, ServiceLine, BillingCode
from app.services.database import get_db_session
from app.services.project_registry import ProjectRegistry
from app.services.proforma_calculator import ProFormaCalculator

from pathlib import Path

router = APIRouter(prefix="/proforma", tags=["proforma"])

# Templates
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/project/{project_id}/create", response_class=HTMLResponse)
async def create_proforma_form(
    request: Request,
    project_id: int,
    session: Session = Depends(get_db_session)
):
    """Show form to create new Pro Forma."""
    registry = ProjectRegistry(session)
    project = registry.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if Pro Forma already exists for this project
    existing = session.exec(
        select(ProForma).where(ProForma.project_id == project_id)
    ).first()
    
    return templates.TemplateResponse(
        "proforma/create.html",
        {
            "request": request,
            "project": project,
            "existing_proforma": existing
        }
    )


@router.post("/project/{project_id}/create")
async def create_proforma(
    project_id: int,
    title: str = Form(...),
    description: str = Form(None),
    physician_hourly_rate: float = Form(175.0),
    app_hourly_rate: float = Form(90.0),
    shifts_per_physician_per_month: int = Form(20),
    shifts_per_app_per_month: int = Form(22),
    include_internal: bool = Form(False),
    # Internal P&L cost fields (optional)
    physician_salary: float = Form(None),
    physician_benefits_taxes: float = Form(None),
    physician_malpractice: float = Form(None),
    app_salary: float = Form(None),
    app_benefits_taxes: float = Form(None),
    app_malpractice: float = Form(None),
    session: Session = Depends(get_db_session)
):
    """Create new Pro Forma."""
    proforma = ProForma(
        project_id=project_id,
        title=title,
        description=description,
        default_physician_hourly_rate=physician_hourly_rate,
        default_app_hourly_rate=app_hourly_rate,
        default_shifts_per_physician_per_month=shifts_per_physician_per_month,
        default_shifts_per_app_per_month=shifts_per_app_per_month
    )
    
    # If internal version, set salary data (use provided values or model defaults)
    if include_internal:
        if physician_salary is not None:
            proforma.physician_salary = physician_salary
        if physician_benefits_taxes is not None:
            proforma.physician_benefits_taxes = physician_benefits_taxes
        if physician_malpractice is not None:
            proforma.physician_malpractice = physician_malpractice
        if app_salary is not None:
            proforma.app_salary = app_salary
        if app_benefits_taxes is not None:
            proforma.app_benefits_taxes = app_benefits_taxes
        if app_malpractice is not None:
            proforma.app_malpractice = app_malpractice
        # Defaults already set in model for other fields
    else:
        # Null out internal fields
        proforma.physician_salary = None
        proforma.app_salary = None
    
    session.add(proforma)
    session.commit()
    session.refresh(proforma)
    
    return RedirectResponse(
        url=f"/proforma/{proforma.id}/edit",
        status_code=303
    )


@router.get("/{proforma_id}/edit", response_class=HTMLResponse)
async def edit_proforma(
    request: Request,
    proforma_id: int,
    session: Session = Depends(get_db_session)
):
    """Edit Pro Forma and manage service lines."""
    proforma = session.get(ProForma, proforma_id)
    if not proforma:
        raise HTTPException(status_code=404, detail="Pro Forma not found")
    
    project = session.get(Project, proforma.project_id)
    
    # Get service lines
    service_lines = session.exec(
        select(ServiceLine)
        .where(ServiceLine.proforma_id == proforma_id)
        .order_by(ServiceLine.order)
    ).all()
    
    return templates.TemplateResponse(
        "proforma/edit.html",
        {
            "request": request,
            "project": project,
            "proforma": proforma,
            "service_lines": service_lines,
            "has_internal": proforma.physician_salary is not None
        }
    )


@router.post("/{proforma_id}/update-settings")
async def update_proforma_settings(
    proforma_id: int,
    physician_hourly_rate: float = Form(...),
    app_hourly_rate: float = Form(...),
    shifts_per_physician_per_month: int = Form(...),
    shifts_per_app_per_month: int = Form(...),
    session: Session = Depends(get_db_session)
):
    """Update Pro Forma global settings."""
    proforma = session.get(ProForma, proforma_id)
    if not proforma:
        raise HTTPException(status_code=404, detail="Pro Forma not found")
    
    # Update settings
    proforma.default_physician_hourly_rate = physician_hourly_rate
    proforma.default_app_hourly_rate = app_hourly_rate
    proforma.default_shifts_per_physician_per_month = shifts_per_physician_per_month
    proforma.default_shifts_per_app_per_month = shifts_per_app_per_month
    proforma.updated_at = datetime.utcnow()
    
    session.add(proforma)
    session.commit()
    
    return RedirectResponse(
        url=f"/proforma/{proforma_id}/edit",
        status_code=303
    )


@router.post("/{proforma_id}/service-line/add")
async def add_service_line(
    proforma_id: int,
    name: str = Form(...),
    physician_hours_per_shift: float = Form(12.0),
    app_hours_per_shift: float = Form(12.0),
    physicians_per_day: int = Form(0),
    apps_per_day: int = Form(0),
    days_per_week: int = Form(7),
    # Revenue inputs (optional, for internal P&L)
    avg_daily_census: float = Form(None),
    avg_daily_procedures: float = Form(None),
    session: Session = Depends(get_db_session)
):
    """Add service line to Pro Forma."""
    proforma = session.get(ProForma, proforma_id)
    if not proforma:
        raise HTTPException(status_code=404, detail="Pro Forma not found")
    
    # Get max order
    max_order = session.exec(
        select(ServiceLine.order)
        .where(ServiceLine.proforma_id == proforma_id)
        .order_by(ServiceLine.order.desc())
    ).first() or 0
    
    service_line = ServiceLine(
        proforma_id=proforma_id,
        name=name,
        physician_hours_per_shift=physician_hours_per_shift,
        app_hours_per_shift=app_hours_per_shift,
        physicians_per_day=physicians_per_day,
        apps_per_day=apps_per_day,
        days_per_week=days_per_week,
        avg_daily_census=avg_daily_census,
        avg_daily_procedures=avg_daily_procedures,
        order=max_order + 1
    )
    
    session.add(service_line)
    session.commit()
    
    return RedirectResponse(
        url=f"/proforma/{proforma_id}/edit",
        status_code=303
    )


@router.post("/{proforma_id}/calculate")
async def calculate_proforma(
    proforma_id: int,
    session: Session = Depends(get_db_session)
):
    """Calculate all Pro Forma metrics."""
    proforma = session.get(ProForma, proforma_id)
    if not proforma:
        raise HTTPException(status_code=404, detail="Pro Forma not found")
    
    service_lines = session.exec(
        select(ServiceLine).where(ServiceLine.proforma_id == proforma_id)
    ).all()
    
    # Calculate using ProFormaCalculator (pass session for billing code lookup)
    calculator = ProFormaCalculator(session=session)
    
    # Calculate each service line
    for sl in service_lines:
        calculator.calculate_service_line(
            sl,
            proforma.default_physician_hourly_rate,
            proforma.default_app_hourly_rate,
            proforma.default_shifts_per_physician_per_month,
            proforma.default_shifts_per_app_per_month
        )
        session.add(sl)
    
    # Calculate totals
    calculator.calculate_proforma_totals(proforma, service_lines)
    proforma.updated_at = datetime.utcnow()
    
    session.add(proforma)
    session.commit()
    
    return RedirectResponse(
        url=f"/proforma/{proforma_id}/view",
        status_code=303
    )


@router.get("/{proforma_id}/view", response_class=HTMLResponse)
async def view_proforma(
    request: Request,
    proforma_id: int,
    version: str = "external",
    session: Session = Depends(get_db_session)
):
    """View calculated Pro Forma (external or internal version)."""
    proforma = session.get(ProForma, proforma_id)
    if not proforma:
        raise HTTPException(status_code=404, detail="Pro Forma not found")
    
    project = session.get(Project, proforma.project_id)
    
    service_lines = session.exec(
        select(ServiceLine)
        .where(ServiceLine.proforma_id == proforma_id)
        .order_by(ServiceLine.order)
    ).all()
    
    calculator = ProFormaCalculator(session=session)
    
    # Generate breakdown for display
    external_breakdown = calculator.generate_external_breakdown(proforma, service_lines)
    
    internal_pl = None
    if version == "internal" and proforma.physician_salary:
        internal_pl = calculator.generate_internal_pl_table(proforma, service_lines, years=3)
    
    return templates.TemplateResponse(
        "proforma/view.html",
        {
            "request": request,
            "project": project,
            "proforma": proforma,
            "service_lines": service_lines,
            "external_breakdown": external_breakdown,
            "internal_pl": internal_pl,
            "version": version,
            "has_internal": proforma.physician_salary is not None
        }
    )


@router.post("/{proforma_id}/save-as-note")
async def save_proforma_as_note(
    proforma_id: int,
    session: Session = Depends(get_db_session)
):
    """Save Pro Forma as a project note for easy copy/paste into proposals."""
    proforma = session.get(ProForma, proforma_id)
    if not proforma:
        raise HTTPException(status_code=404, detail="Pro Forma not found")
    
    project = session.get(Project, proforma.project_id)
    
    service_lines = session.exec(
        select(ServiceLine)
        .where(ServiceLine.proforma_id == proforma_id)
        .order_by(ServiceLine.order)
    ).all()
    
    calculator = ProFormaCalculator(session=session)
    external_breakdown = calculator.generate_external_breakdown(proforma, service_lines)
    
    # Generate markdown content
    markdown_content = f"""# {proforma.title}

**Total Annual Cost:** ${proforma.total_annual_cost:,.2f}
**Total FTE:** {proforma.total_physician_fte + proforma.total_app_fte:.2f} ({proforma.total_physician_fte:.2f} Physician + {proforma.total_app_fte:.2f} APP)

## Service Line Breakdown

| Service Line | Description | Physician FTE | APP FTE | Annual Cost |
|--------------|-------------|---------------|---------|-------------|
"""
    
    for item in external_breakdown:
        markdown_content += f"| {item['service_line']} | {item['description']} | {item['physician_fte']} | {item['app_fte']} | {item['annual_cost']} |\n"
    
    markdown_content += "\n\n---\n\n*Generated from Pro Forma on " + datetime.utcnow().strftime("%Y-%m-%d") + "*"
    
    # Create project note
    registry = ProjectRegistry(session)
    note = registry.create_note(
        project_id=proforma.project_id,
        title=f"{proforma.title} - Financial Breakdown",
        content=markdown_content,
        note_type="financial",
        tags="proforma,financial,pricing"
    )
    
    if not note:
        raise HTTPException(status_code=500, detail="Failed to create note")
    
    return RedirectResponse(
        url=f"/projects/{proforma.project_id}",
        status_code=303
    )


@router.get("/{proforma_id}/service-line/{service_line_id}/edit", response_class=HTMLResponse)
async def edit_service_line_form(
    request: Request,
    proforma_id: int,
    service_line_id: int,
    session: Session = Depends(get_db_session)
):
    """Show form to edit a service line."""
    proforma = session.get(ProForma, proforma_id)
    service_line = session.get(ServiceLine, service_line_id)
    
    if not proforma or not service_line or service_line.proforma_id != proforma_id:
        raise HTTPException(status_code=404, detail="Not found")
    
    project = session.get(Project, proforma.project_id)
    
    return templates.TemplateResponse(
        "proforma/edit_service_line.html",
        {
            "request": request,
            "project": project,
            "proforma": proforma,
            "service_line": service_line,
            "has_internal": proforma.physician_salary is not None
        }
    )


@router.post("/{proforma_id}/service-line/{service_line_id}/edit")
async def update_service_line(
    proforma_id: int,
    service_line_id: int,
    name: str = Form(...),
    physician_hours_per_shift: float = Form(12.0),
    app_hours_per_shift: float = Form(12.0),
    physicians_per_day: int = Form(0),
    apps_per_day: int = Form(0),
    days_per_week: int = Form(7),
    # Revenue inputs (optional)
    avg_daily_census: float = Form(None),
    avg_daily_procedures: float = Form(None),
    session: Session = Depends(get_db_session)
):
    """Update a service line."""
    service_line = session.get(ServiceLine, service_line_id)
    if not service_line or service_line.proforma_id != proforma_id:
        raise HTTPException(status_code=404, detail="Not found")
    
    # Update fields
    service_line.name = name
    service_line.physician_hours_per_shift = physician_hours_per_shift
    service_line.app_hours_per_shift = app_hours_per_shift
    service_line.physicians_per_day = physicians_per_day
    service_line.apps_per_day = apps_per_day
    service_line.days_per_week = days_per_week
    service_line.avg_daily_census = avg_daily_census
    service_line.avg_daily_procedures = avg_daily_procedures
    service_line.updated_at = datetime.utcnow()
    
    session.add(service_line)
    session.commit()
    
    return RedirectResponse(
        url=f"/proforma/{proforma_id}/edit",
        status_code=303
    )


@router.get("/{proforma_id}/service-line/{service_line_id}/billing-profile", response_class=HTMLResponse)
async def edit_billing_profile(
    request: Request,
    proforma_id: int,
    service_line_id: int,
    session: Session = Depends(get_db_session)
):
    """Edit billing profile for a service line."""
    proforma = session.get(ProForma, proforma_id)
    service_line = session.get(ServiceLine, service_line_id)
    
    if not proforma or not service_line or service_line.proforma_id != proforma_id:
        raise HTTPException(status_code=404, detail="Not found")
    
    # Get all billing codes
    em_codes = session.exec(
        select(BillingCode).where(BillingCode.code_type == "em")
    ).all()
    
    procedure_codes = session.exec(
        select(BillingCode).where(BillingCode.code_type == "procedure")
    ).all()
    
    # Parse existing profiles
    em_profile = json.loads(service_line.em_billing_profile) if service_line.em_billing_profile else {}
    proc_profile = json.loads(service_line.procedure_billing_profile) if service_line.procedure_billing_profile else {}
    
    return templates.TemplateResponse(
        "proforma/billing_profile.html",
        {
            "request": request,
            "proforma": proforma,
            "service_line": service_line,
            "em_codes": em_codes,
            "procedure_codes": procedure_codes,
            "em_profile": em_profile,
            "proc_profile": proc_profile
        }
    )


@router.post("/{proforma_id}/service-line/{service_line_id}/billing-profile")
async def save_billing_profile(
    proforma_id: int,
    service_line_id: int,
    request: Request,
    session: Session = Depends(get_db_session)
):
    """Save billing profile for a service line."""
    service_line = session.get(ServiceLine, service_line_id)
    if not service_line or service_line.proforma_id != proforma_id:
        raise HTTPException(status_code=404, detail="Not found")
    
    # Parse form data
    form_data = await request.form()
    
    # Build E/M profile
    em_profile = {}
    for key, value in form_data.items():
        if key.startswith("em_") and value:
            code = key.replace("em_", "")
            em_profile[code] = float(value) / 100.0  # Convert percentage to decimal
    
    # Build procedure profile
    proc_profile = {}
    for key, value in form_data.items():
        if key.startswith("proc_") and value:
            code = key.replace("proc_", "")
            proc_profile[code] = float(value) / 100.0
    
    # Save as JSON
    service_line.em_billing_profile = json.dumps(em_profile) if em_profile else None
    service_line.procedure_billing_profile = json.dumps(proc_profile) if proc_profile else None
    service_line.updated_at = datetime.utcnow()
    
    session.add(service_line)
    session.commit()
    
    return RedirectResponse(
        url=f"/proforma/{proforma_id}/edit",
        status_code=303
    )


@router.get("/{proforma_id}/delete")
async def delete_service_line(
    proforma_id: int,
    service_line_id: int,
    session: Session = Depends(get_db_session)
):
    """Delete a service line."""
    service_line = session.get(ServiceLine, service_line_id)
    if service_line and service_line.proforma_id == proforma_id:
        session.delete(service_line)
        session.commit()
    
    return RedirectResponse(
        url=f"/proforma/{proforma_id}/edit",
        status_code=303
    )


@router.get("/{proforma_id}/download/markdown")
async def download_markdown(
    proforma_id: int,
    version: str = "external",
    session: Session = Depends(get_db_session)
):
    """Download Pro Forma as Markdown."""
    from fastapi.responses import Response
    
    proforma = session.get(ProForma, proforma_id)
    if not proforma:
        raise HTTPException(status_code=404, detail="Pro Forma not found")
    
    service_lines = session.exec(
        select(ServiceLine)
        .where(ServiceLine.proforma_id == proforma_id)
        .order_by(ServiceLine.order)
    ).all()
    
    calculator = ProFormaCalculator(session=session)
    
    if version == "internal" and proforma.physician_salary:
        # Generate internal P&L markdown
        internal_pl = calculator.generate_internal_pl_table(proforma, service_lines, years=3)
        
        md_lines = [
            f"# {proforma.title} - Internal P&L",
            "",
            f"**Total FTE:** {proforma.total_physician_fte + proforma.total_app_fte:.2f} ({proforma.total_physician_fte:.2f} Physician + {proforma.total_app_fte:.2f} APP)",
            "",
            "## 3-Year P&L Projection",
            "",
            "| Line Item | Year 1 | Year 2 | Year 3 |",
            "|-----------|--------|--------|--------|",
            "| **REVENUE** | | | |"
        ]
        
        # Revenue by service line
        for sl_rev in internal_pl.get('service_line_revenues', []):
            md_lines.append(f"| {sl_rev['name']} | ${sl_rev['revenue']:,.2f} | ${sl_rev['revenue']:,.2f} | ${sl_rev['revenue']:,.2f} |")
        
        md_lines.extend([
            f"| **Total Revenue** | ${internal_pl['projected_revenue'][0]:,.2f} | ${internal_pl['projected_revenue'][1]:,.2f} | ${internal_pl['projected_revenue'][2]:,.2f} |",
            "| **DIRECT COSTS** | | | |",
            f"| Physician Compensation | ${internal_pl['total_physician_comp'][0]:,.2f} | ${internal_pl['total_physician_comp'][1]:,.2f} | ${internal_pl['total_physician_comp'][2]:,.2f} |",
            f"| APP Compensation | ${internal_pl['total_app_comp'][0]:,.2f} | ${internal_pl['total_app_comp'][1]:,.2f} | ${internal_pl['total_app_comp'][2]:,.2f} |",
            f"| **Total Direct Costs** | ${internal_pl['total_direct_expenses'][0]:,.2f} | ${internal_pl['total_direct_expenses'][1]:,.2f} | ${internal_pl['total_direct_expenses'][2]:,.2f} |",
            "| **INDIRECT COSTS** | | | |",
            f"| Administrative Overhead | ${internal_pl['admin_overhead'][0]:,.2f} | ${internal_pl['admin_overhead'][1]:,.2f} | ${internal_pl['admin_overhead'][2]:,.2f} |",
            f"| Financial Oversight | ${internal_pl['financial_oversight'][0]:,.2f} | ${internal_pl['financial_oversight'][1]:,.2f} | ${internal_pl['financial_oversight'][2]:,.2f} |",
            f"| Office & Materials | ${internal_pl['office_materials'][0]:,.2f} | ${internal_pl['office_materials'][1]:,.2f} | ${internal_pl['office_materials'][2]:,.2f} |",
            f"| Credentialing | ${internal_pl['credentialing'][0]:,.2f} | ${internal_pl['credentialing'][1]:,.2f} | ${internal_pl['credentialing'][2]:,.2f} |",
            f"| Revenue Cycle Management | ${internal_pl['rcm'][0]:,.2f} | ${internal_pl['rcm'][1]:,.2f} | ${internal_pl['rcm'][2]:,.2f} |",
            f"| **Total Indirect Costs** | ${internal_pl['total_indirect_expenses'][0]:,.2f} | ${internal_pl['total_indirect_expenses'][1]:,.2f} | ${internal_pl['total_indirect_expenses'][2]:,.2f} |",
            f"| **NET INCOME** | ${internal_pl['net_income'][0]:,.2f} | ${internal_pl['net_income'][1]:,.2f} | ${internal_pl['net_income'][2]:,.2f} |"
        ])
        
        md_content = "\n".join(md_lines)
    else:
        # Generate external breakdown markdown
        external_breakdown = calculator.generate_external_breakdown(proforma, service_lines)
        
        md_lines = [
            f"# {proforma.title}",
            "",
            f"**Total Annual Cost:** ${proforma.total_annual_cost:,.2f}",
            f"**Total FTE:** {proforma.total_physician_fte + proforma.total_app_fte:.2f} ({proforma.total_physician_fte:.2f} Physician + {proforma.total_app_fte:.2f} APP)",
            "",
            "## Service Line Breakdown",
            "",
            "| Service Line | Description | Physician FTE | APP FTE | Annual Cost |",
            "|--------------|-------------|---------------|---------|-------------|"
        ]
        
        for item in external_breakdown:
            md_lines.append(
                f"| {item['service_line']} | {item['description']} | {item['physician_fte']} | {item['app_fte']} | {item['annual_cost']} |"
            )
        
        md_content = "\n".join(md_lines)
    
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{proforma.title.replace(" ", "_")}.md"'}
    )


@router.get("/{proforma_id}/download/csv")
async def download_csv(
    proforma_id: int,
    version: str = "external",
    session: Session = Depends(get_db_session)
):
    """Download Pro Forma as CSV."""
    from fastapi.responses import Response
    import csv
    from io import StringIO
    
    proforma = session.get(ProForma, proforma_id)
    if not proforma:
        raise HTTPException(status_code=404, detail="Pro Forma not found")
    
    service_lines = session.exec(
        select(ServiceLine)
        .where(ServiceLine.proforma_id == proforma_id)
        .order_by(ServiceLine.order)
    ).all()
    
    calculator = ProFormaCalculator(session=session)
    
    output = StringIO()
    writer = csv.writer(output)
    
    if version == "internal" and proforma.physician_salary:
        # Generate internal P&L CSV
        internal_pl = calculator.generate_internal_pl_table(proforma, service_lines, years=3)
        
        writer.writerow(["Line Item", "Year 1", "Year 2", "Year 3"])
        writer.writerow(["STAFFING", "", "", ""])
        writer.writerow(["Physician FTE", internal_pl['physician_fte'], internal_pl['physician_fte'], internal_pl['physician_fte']])
        writer.writerow(["APP FTE", internal_pl['app_fte'], internal_pl['app_fte'], internal_pl['app_fte']])
        writer.writerow(["Total FTE", internal_pl['total_fte'], internal_pl['total_fte'], internal_pl['total_fte']])
        writer.writerow([])
        
        writer.writerow(["REVENUE", "", "", "", "Daily Volume Assumptions", "Annual Volumes", "E/M Billing Profile", "Procedure Billing Profile"])
        for sl_rev in internal_pl.get('service_line_revenues', []):
            # Build volume and billing info for adjacent columns
            volume_assumptions = ""
            if sl_rev.get('avg_daily_census') or sl_rev.get('avg_daily_procedures'):
                vol_parts = []
                if sl_rev.get('avg_daily_census'):
                    vol_parts.append(f"Census: {sl_rev['avg_daily_census']:.1f}")
                if sl_rev.get('avg_daily_procedures'):
                    vol_parts.append(f"Procedures: {sl_rev['avg_daily_procedures']:.1f}")
                volume_assumptions = "; ".join(vol_parts)
            
            annual_volumes = ""
            if sl_rev.get('annual_em_encounters') or sl_rev.get('annual_procedure_count'):
                annual_parts = []
                if sl_rev.get('annual_em_encounters'):
                    annual_parts.append(f"E/M: {sl_rev['annual_em_encounters']:.0f}")
                if sl_rev.get('annual_procedure_count'):
                    annual_parts.append(f"Procs: {sl_rev['annual_procedure_count']:.0f}")
                annual_volumes = "; ".join(annual_parts)
            
            # E/M billing profile (filter out zero-percent codes)
            em_billing = ""
            if sl_rev.get('em_profile'):
                em_codes = [f"{code}({pct*100:.0f}%)" for code, pct in sl_rev['em_profile'].items() if pct > 0]
                if em_codes:
                    em_billing = ", ".join(em_codes)
            
            # Procedure billing profile (filter out zero-percent codes)
            proc_billing = ""
            if sl_rev.get('proc_profile'):
                proc_codes = [f"{code}({pct*100:.0f}%)" for code, pct in sl_rev['proc_profile'].items() if pct > 0]
                if proc_codes:
                    proc_billing = ", ".join(proc_codes)
            
            writer.writerow([
                sl_rev['name'],
                f"${sl_rev['revenue']:,.2f}",
                f"${sl_rev['revenue']:,.2f}",
                f"${sl_rev['revenue']:,.2f}",
                volume_assumptions,
                annual_volumes,
                em_billing,
                proc_billing
            ])
        writer.writerow(["Total Revenue", f"${internal_pl['projected_revenue'][0]:,.2f}", f"${internal_pl['projected_revenue'][1]:,.2f}", f"${internal_pl['projected_revenue'][2]:,.2f}", "", "", "", ""])
        writer.writerow([])
        
        writer.writerow(["DIRECT COSTS", "", "", ""])
        writer.writerow(["Physician Compensation", f"${internal_pl['total_physician_comp'][0]:,.2f}", f"${internal_pl['total_physician_comp'][1]:,.2f}", f"${internal_pl['total_physician_comp'][2]:,.2f}"])
        writer.writerow(["APP Compensation", f"${internal_pl['total_app_comp'][0]:,.2f}", f"${internal_pl['total_app_comp'][1]:,.2f}", f"${internal_pl['total_app_comp'][2]:,.2f}"])
        writer.writerow(["Total Direct Costs", f"${internal_pl['total_direct_expenses'][0]:,.2f}", f"${internal_pl['total_direct_expenses'][1]:,.2f}", f"${internal_pl['total_direct_expenses'][2]:,.2f}"])
        writer.writerow([])
        
        writer.writerow(["INDIRECT COSTS", "", "", ""])
        writer.writerow(["Administrative Overhead", f"${internal_pl['admin_overhead'][0]:,.2f}", f"${internal_pl['admin_overhead'][1]:,.2f}", f"${internal_pl['admin_overhead'][2]:,.2f}"])
        writer.writerow(["Financial Oversight", f"${internal_pl['financial_oversight'][0]:,.2f}", f"${internal_pl['financial_oversight'][1]:,.2f}", f"${internal_pl['financial_oversight'][2]:,.2f}"])
        writer.writerow(["Office & Materials", f"${internal_pl['office_materials'][0]:,.2f}", f"${internal_pl['office_materials'][1]:,.2f}", f"${internal_pl['office_materials'][2]:,.2f}"])
        writer.writerow(["Credentialing", f"${internal_pl['credentialing'][0]:,.2f}", f"${internal_pl['credentialing'][1]:,.2f}", f"${internal_pl['credentialing'][2]:,.2f}"])
        writer.writerow(["Revenue Cycle Management", f"${internal_pl['rcm'][0]:,.2f}", f"${internal_pl['rcm'][1]:,.2f}", f"${internal_pl['rcm'][2]:,.2f}"])
        writer.writerow(["Total Indirect Costs", f"${internal_pl['total_indirect_expenses'][0]:,.2f}", f"${internal_pl['total_indirect_expenses'][1]:,.2f}", f"${internal_pl['total_indirect_expenses'][2]:,.2f}"])
        writer.writerow([])
        
        writer.writerow(["NET INCOME", f"${internal_pl['net_income'][0]:,.2f}", f"${internal_pl['net_income'][1]:,.2f}", f"${internal_pl['net_income'][2]:,.2f}"])
    else:
        # Generate external breakdown CSV
        external_breakdown = calculator.generate_external_breakdown(proforma, service_lines)
        
        writer.writerow(["Service Line", "Description", "Physician FTE", "APP FTE", "Annual Cost"])
        for item in external_breakdown:
            writer.writerow([
                item['service_line'],
                item['description'],
                item['physician_fte'],
                item['app_fte'],
                item['annual_cost']
            ])
        
        writer.writerow(["TOTAL", "", f"{proforma.total_physician_fte:.2f}", f"{proforma.total_app_fte:.2f}", f"${proforma.total_annual_cost:,.2f}"])
    
    csv_content = output.getvalue()
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{proforma.title.replace(" ", "_")}.csv"'}
    )
