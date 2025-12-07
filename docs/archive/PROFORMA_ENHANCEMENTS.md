# Pro Forma Display & Export Enhancements

**Date:** 2025-12-04

## Summary of Changes

Enhanced the Internal P&L Pro Forma view and CSV export to display detailed volume assumptions and billing profile information for each service line.

## What Was Added

### 1. On-Screen Display (Internal P&L View)

When viewing the internal P&L projection in the web interface, each revenue line now displays three additional rows:

- **Volume Assumptions**: Shows the assumed daily census (patients) and daily procedure counts
  - Example: "Avg Daily Census: 8.5 patients | Avg Daily Procedures: 3.2"

- **Annual Volumes**: Calculated annual totals based on the daily assumptions
  - Example: "E/M Encounters: 2,184 | Procedures: 832"

- **Billing Profile**: Detailed breakdown of billing codes and their mix percentages
  - Example: "E/M Codes: 99233 (50%), 99291 (50%) | Procedures: 31500 (40%), 32550 (60%)"

### 2. CSV Export Enhancement

When exporting the internal P&L as CSV, each service line revenue line now includes three detail rows:

- `→ Volume Assumptions`: Daily census and procedures
- `→ Annual Volumes`: Annual E/M encounters and procedures
- `→ Billing Profile`: Billing codes with their mix percentages

This makes the CSV export more transparent and auditable, showing the complete calculation chain from volume assumptions to revenue projections.

## Files Modified

### Backend Changes
- **`app/services/proforma_calculator.py`**
  - Updated `generate_internal_pl_table()` method to parse billing profiles from JSON
  - Now includes `avg_daily_census`, `avg_daily_procedures`, `annual_em_encounters`, `annual_procedure_count`, `em_profile`, and `proc_profile` in the service line revenue breakdown dictionary

### Frontend Changes
- **`web/templates/proforma/view.html`**
  - Added three new detail rows in the REVENUE section for each service line:
    - Volume Assumptions row
    - Annual Volumes row
    - Billing Profile row (conditionally shown if profiles exist)

- **`web/routes/proforma.py`**
  - Enhanced the CSV export logic (lines 662-692) to include the same detail rows
  - Uses arrow symbol (→) for visual hierarchy in CSV

## Data Source

All information displayed is already collected and stored in the ServiceLine model:
- `avg_daily_census` - user-provided assumption
- `avg_daily_procedures` - user-provided assumption
- `annual_em_encounters` - calculated from volume × days/year
- `annual_procedure_count` - calculated from volume × days/year
- `em_billing_profile` - JSON string mapping codes to percentages
- `procedure_billing_profile` - JSON string mapping codes to percentages

## Testing

✓ Python syntax validation passed  
✓ Jinja2 template syntax validation passed  
✓ No database schema changes required (all fields already exist)

## Next Steps

1. Navigate to your HFW Renegotiation project Pro Forma
2. Ensure service lines have:
   - `avg_daily_census` and `avg_daily_procedures` populated
   - Billing profiles assigned (E/M and/or Procedure codes)
3. Calculate the Pro Forma
4. View internal P&L - you'll see the new detail rows on screen
5. Download as CSV - the detail rows will be included in the export

## Example CSV Output

```
Service Line,Description,Year 1,Year 2,Year 3
MICU Coverage,$X,$X,$X
  → Volume Assumptions,"Daily Census: 8.5, Daily Procedures: 3.2",,
  → Annual Volumes,"E/M Encounters: 2184, Procedures: 832",,
  → Billing Profile,"E/M: 99233(50%), 99291(50%) | Procedures: 31500(40%), 32550(60%)",,
```

