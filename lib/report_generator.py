#!/usr/bin/env python3
"""
Australian Privacy Act Compliance Report Generator

Generates professional HTML reports for APP compliance gap analysis.
Supports both TEASER (limited) and FULL (complete) versions.
"""

import json
import math
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass
from datetime import datetime


@dataclass
class APP:
    app_number: int
    app_name: str
    status: str
    findings: List[str]
    recommended_language: str
    priority: str


@dataclass
class ADMCheck:
    uses_adm: str
    adm_disclosed: bool
    recommendation: str
    examples_found: list = None

    def __post_init__(self):
        if self.examples_found is None:
            self.examples_found = []


@dataclass
class Summary:
    compliant_count: int
    partial_count: int
    non_compliant_count: int
    not_addressed_count: int


@dataclass
class ComplianceAnalysis:
    business_name: str
    sector: str
    analysis_date: str
    overall_score: int
    overall_status: str
    apps: List[APP]
    adm_check: ADMCheck
    summary: Summary


class HTMLReportGenerator:
    """Generates self-contained HTML compliance reports."""

    # Colour scheme
    COLORS = {
        "navy": "#1a1a2e",
        "teal": "#16a085",
        "red": "#e74c3c",
        "amber": "#f39c12",
        "green": "#27ae60",
        "light_grey": "#ecf0f1",
        "dark_grey": "#34495e",
        "grey": "#7f8c8d",
        "white": "#ffffff",
        "black": "#000000",
    }

    # APP names for reference
    APP_NAMES = {
        1: "Open and Transparent Management of Personal Information",
        2: "Collection of Solicited Personal Information",
        3: "Collection of Unsolicited Personal Information",
        4: "Dealing with Personal Information",
        5: "Notification about Personal Information Management",
        6: "Use or Disclosure of Personal Information",
        7: "Direct Marketing",
        8: "Credit Eligibility Information",
        9: "Adoption, Use or Disclosure of Government Related Identifiers",
        10: "Quality of Personal Information",
        11: "Data Security",
        12: "Access and Correction",
        13: "Complaints Management",
    }

    def __init__(self, analysis: Dict):
        """Initialize with analysis data."""
        self._raw_apps = analysis.get("apps", [])
        self.analysis = self._parse_analysis(analysis)

    def _format_sector_name(self, sector: str) -> str:
        """Convert sector codes to human-readable names."""
        sector_mapping = {
            "real_estate": "Real Estate",
            "legal": "Legal Services",
            "pharmacy": "Pharmacy & Health",
            "hospitality": "Hospitality & Licensed Venues",
            "automotive": "Automotive",
            "jewellery": "Jewellery & High-Value Goods",
        }
        # If it's in the mapping, use that; otherwise title case and replace underscores
        if sector.lower() in sector_mapping:
            return sector_mapping[sector.lower()]
        else:
            return sector.replace("_", " ").title()

    def _format_date(self, date_str: str) -> str:
        """Convert ISO date format to human-readable format: '1 April 2026'."""
        try:
            # Handle both string and datetime objects
            if isinstance(date_str, str):
                # Try ISO format with time
                if "T" in date_str:
                    date_obj = datetime.fromisoformat(date_str.split("T")[0])
                else:
                    date_obj = datetime.fromisoformat(date_str)
            else:
                date_obj = date_str
            # Format as "1 April 2026"
            return date_obj.strftime("%-d %B %Y").replace(" 0", " ")
        except (ValueError, AttributeError):
            # Fallback if parsing fails
            return date_str

    def _parse_analysis(self, data: Dict) -> ComplianceAnalysis:
        """Parse input JSON into ComplianceAnalysis dataclass."""
        apps = [
            APP(
                app_number=app["app_number"],
                app_name=app["app_name"],
                status=app["status"],
                findings=app["findings"],
                recommended_language=app["recommended_language"],
                priority=app.get("priority", "MEDIUM"),
            )
            for app in data["apps"]
        ]

        return ComplianceAnalysis(
            business_name=data["business_name"],
            sector=data["sector"],
            analysis_date=data["analysis_date"],
            overall_score=data["overall_score"],
            overall_status=data["overall_status"],
            apps=apps,
            adm_check=ADMCheck(**data["adm_check"]),
            summary=Summary(**data["summary"]),
        )

    def _get_status_color(self, status: str) -> str:
        """Map status to colour."""
        status_lower = status.lower()
        if "partially" in status_lower:
            return self.COLORS["amber"]
        elif "non" in status_lower:
            return self.COLORS["red"]
        elif "compliant" in status_lower:
            return self.COLORS["green"]
        else:
            return self.COLORS["grey"]

    def _get_status_label(self, status: str) -> str:
        """Get human-readable status label."""
        if "NON" in status:
            return "Non-Compliant"
        elif "PARTIAL" in status:
            return "Partially Compliant"
        else:
            return "Compliant"

    def _generate_compliance_gauge(self, score: int) -> str:
        """Generate SVG circular gauge for compliance score."""
        radius = 70
        circumference = 2 * math.pi * radius
        progress = (score / 100) * circumference
        gap = circumference - progress

        # Determine colour based on score
        if score >= 70:
            color = self.COLORS["green"]
        elif score >= 40:
            color = self.COLORS["amber"]
        else:
            color = self.COLORS["red"]

        svg = f'''
        <svg width="200" height="200" viewBox="0 0 200 200" style="margin: 0 auto; display: block;">
            <circle cx="100" cy="100" r="{radius}" fill="none" stroke="{self.COLORS['light_grey']}" stroke-width="12"></circle>
            <circle cx="100" cy="100" r="{radius}" fill="none" stroke="{color}" stroke-width="12"
                    stroke-dasharray="{progress},{gap}" stroke-linecap="round" transform="rotate(-90 100 100)"
                    style="transition: stroke-dasharray 0.5s ease;"></circle>
            <text x="100" y="100" text-anchor="middle" dy="0.3em" font-size="48" font-weight="bold" fill="{color}">{score}%</text>
            <text x="100" y="130" text-anchor="middle" font-size="14" fill="{self.COLORS['dark_grey']}">Compliance</text>
        </svg>
        '''
        return svg

    def _generate_app_grid(self) -> str:
        """Generate 13-APP traffic light grid."""
        grid_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 12px; margin: 24px 0;">'

        for app in self.apps:
            color = self._get_status_color(app.status)
            label = self._get_status_label(app.status)
            grid_html += f'''
            <div style="background: {color}; color: white; padding: 16px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="font-size: 20px; font-weight: bold;">APP {app.app_number}</div>
                <div style="font-size: 11px; margin-top: 8px; opacity: 0.9;">{label}</div>
            </div>
            '''

        grid_html += '</div>'
        return grid_html

    def _generate_app_detail_section(self, app: APP, blurred: bool = False) -> str:
        """Generate detailed section for a single APP."""
        color = self._get_status_color(app.status)
        label = self._get_status_label(app.status)

        findings_html = ''.join(
            f'<li style="margin-bottom: 8px; line-height: 1.6;">{finding}</li>'
            for finding in app.findings
        )

        blur_class = ""
        overlay_html = ""

        if blurred:
            blur_class = 'style="filter: blur(4px); opacity: 0.6; pointer-events: none;"'
            overlay_html = f'''
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255,255,255,0.7); display: flex; align-items: center; justify-content: center; border-radius: 8px;">
                <div style="text-align: center;">
                    <div style="font-size: 18px; font-weight: bold; color: {self.COLORS['navy']}; margin-bottom: 12px;">🔒 Locked</div>
                    <div style="font-size: 14px; color: {self.COLORS['dark_grey']};">Unlock your full report</div>
                </div>
            </div>
            '''

        section_html = f'''
        <div style="position: relative; margin-bottom: 32px; padding: 24px; background: {self.COLORS['light_grey']}; border-left: 4px solid {color}; border-radius: 8px; page-break-inside: avoid;">
            {overlay_html}
            <div {blur_class}>
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
                    <div>
                        <h3 style="margin: 0 0 8px 0; font-size: 18px; color: {self.COLORS['navy']};">APP {app.app_number}: {app.app_name}</h3>
                        <span style="display: inline-block; padding: 4px 12px; background: {color}; color: white; border-radius: 20px; font-size: 12px; font-weight: bold;">{label}</span>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 12px; color: {self.COLORS['dark_grey']}; margin-bottom: 4px;">Priority</div>
                        <div style="font-size: 14px; font-weight: bold; color: {self.COLORS['navy']};">{app.priority}</div>
                    </div>
                </div>

                <div style="margin-top: 12px; padding: 12px; background: rgba(0, 0, 0, 0.05); border-radius: 4px; font-size: 13px; color: {self.COLORS['dark_grey']}; line-height: 1.6;">
                    <strong>Why this score:</strong> {self._build_reasoning_text(app)}
                </div>

                <div style="margin-top: 16px;">
                    <h4 style="margin: 0 0 12px 0; font-size: 14px; color: {self.COLORS['navy']}; font-weight: bold; text-transform: uppercase;">Key Findings</h4>
                    <ul style="margin: 0; padding-left: 20px; color: {self.COLORS['dark_grey']}; line-height: 1.8;">
                        {findings_html}
                    </ul>
                </div>

                <div style="margin-top: 20px; padding-top: 16px; border-top: 1px solid {self.COLORS['dark_grey']};">
                    <h4 style="margin: 0 0 12px 0; font-size: 14px; color: {self.COLORS['navy']}; font-weight: bold; text-transform: uppercase;">Recommended Language</h4>
                    <p style="margin: 0; color: {self.COLORS['dark_grey']}; line-height: 1.8; font-style: italic;">{app.recommended_language}</p>
                </div>
            </div>
        </div>
        '''

        return section_html

    def _build_reasoning_text(self, app: APP) -> str:
        """Build human-readable reasoning text from findings and gaps."""
        # Get the raw data from the original analysis dict
        app_data = None
        for a in self._raw_apps:
            if a.get('app_number') == app.app_number:
                app_data = a
                break

        gaps = app_data.get('gaps', []) if app_data else []
        findings = app.findings

        # Build the "found" part from findings
        found_text = findings[0] if findings else ""

        # Build specific gaps list (clean up "Missing: " prefix)
        gap_items = []
        for g in gaps[:3]:  # Max 3 gaps shown
            cleaned = g.replace("Missing: ", "").strip()
            gap_items.append(cleaned)

        # Compose the reasoning
        parts = []
        if found_text:
            parts.append(found_text)
        if gap_items:
            parts.append(f"Gaps identified: {', '.join(gap_items)}")

        if not parts:
            if app.status == "COMPLIANT":
                return "Policy adequately addresses this principle."
            elif "PARTIAL" in app.status:
                return "Policy partially addresses this principle but has gaps."
            else:
                return "Policy does not adequately address this principle."

        return ". ".join(parts) + "."

    def _generate_adm_callout(self) -> str:
        """Generate highlighted callout for ADM transparency requirement."""
        adm_check = self.analysis.adm_check

        content = (
            f"<strong>Using Automated Decision-Making?</strong> {adm_check.recommendation}"
            if adm_check.uses_adm != "NO"
            else "<strong>ADM Disclosure Not Required</strong> Our analysis indicates automated decision-making is not currently used in your services."
        )

        return f'''
        <div style="margin: 32px 0; padding: 20px; background: {self.COLORS['amber']}; border-left: 4px solid {self.COLORS['red']}; border-radius: 8px; color: {self.COLORS['navy']}; line-height: 1.8;">
            <div style="font-weight: bold; margin-bottom: 8px;">📢 December 2026 ADM Transparency Requirement</div>
            {content}
        </div>
        '''

    def _generate_policy_template(self) -> str:
        """Generate ready-to-paste privacy policy template."""
        sector = self.analysis.sector
        business_name = self.analysis.business_name

        template = f'''
<privacy-policy-template>

PRIVACY POLICY

{business_name}

Last Updated: {datetime.now().strftime('%B %Y')}

---

APP 1: OPEN AND TRANSPARENT MANAGEMENT OF PERSONAL INFORMATION

{business_name} ("we", "us", or "our") is committed to managing your personal information in an open and transparent way. This Privacy Policy sets out how we collect, use, disclose, secure and provide access to your personal information.

---

APP 2 & 3: COLLECTION OF PERSONAL INFORMATION

We collect personal information that is reasonably necessary to provide our {sector.lower()} services. This may include:
- Name and contact details
- Identification information
- Payment information
- Service-related information

We obtain personal information directly from you or with your consent.

---

APP 4: DEALING WITH PERSONAL INFORMATION

We use and disclose your personal information for:
- Providing our services
- Processing transactions
- Communicating with you
- Improving our service delivery

We do not sell or rent your personal information to third parties without your consent.

---

APP 5: NOTIFICATION ABOUT PERSONAL INFORMATION MANAGEMENT

When we collect personal information, we will take reasonable steps to notify you of:
- Our identity and contact details
- How to access your information
- How to complain about privacy breaches
- Whether disclosure is required by law

---

APP 6: USE OR DISCLOSURE OF PERSONAL INFORMATION

We will only use or disclose your personal information for the primary purpose it was collected, or a related secondary purpose. If we use it for another purpose, we will obtain your consent unless required by law.

---

APP 7: DIRECT MARKETING

If you provide us with your contact details, we may use them for direct marketing. You can opt out at any time by contacting us.

---

APP 8: CREDIT ELIGIBILITY INFORMATION

Where applicable, we comply with all requirements regarding credit eligibility information and do not misuse credit information.

---

APP 9: ADOPTION, USE OR DISCLOSURE OF GOVERNMENT-RELATED IDENTIFIERS

We do not adopt government-related identifiers (such as ABN or tax file numbers) as our own identifier for individuals unless required by law or you consent.

---

APP 10: QUALITY OF PERSONAL INFORMATION

We take reasonable steps to ensure the personal information we collect, use and disclose is accurate, up-to-date, complete and relevant.

---

APP 11: DATA SECURITY

We take reasonable steps to protect your personal information from:
- Misuse and loss
- Unauthorised access, modification and disclosure

This includes implementing appropriate physical, electronic and procedural safeguards.

---

APP 12: ACCESS AND CORRECTION

You have the right to access the personal information we hold about you and request correction of inaccurate information. Please contact us in writing to exercise these rights.

---

APP 13: COMPLAINTS MANAGEMENT

If you have a privacy complaint, please contact us in writing. We will respond to complaints within 30 days. If you are not satisfied, you can lodge a complaint with the Office of the Australian Information Commissioner (OAIC).

Contact Details:
{business_name}
Email: [your-privacy-contact@company.com]
Phone: [your-phone-number]

---

This policy is provided as a template for {sector} sector compliance and should be customised to your specific circumstances. Consult with a qualified privacy professional before implementing.

</privacy-policy-template>
        '''
        return template

    def _generate_css(self) -> str:
        """Generate embedded CSS."""
        return f'''
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: {self.COLORS['dark_grey']};
                background: {self.COLORS['white']};
                padding: 0;
            }}

            .container {{
                max-width: 900px;
                margin: 0 auto;
                padding: 40px 20px;
            }}

            header {{
                background: linear-gradient(135deg, {self.COLORS['navy']} 0%, {self.COLORS['teal']} 100%);
                color: {self.COLORS['white']};
                padding: 48px 20px;
                margin: -40px -20px 40px -20px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}

            header h1 {{
                font-size: 32px;
                margin-bottom: 8px;
                font-weight: 600;
            }}

            header p {{
                font-size: 16px;
                opacity: 0.9;
                margin-bottom: 4px;
            }}

            header .meta {{
                font-size: 13px;
                opacity: 0.8;
                margin-top: 12px;
            }}

            .score-section {{
                background: {self.COLORS['light_grey']};
                border-radius: 12px;
                padding: 40px 20px;
                margin: 32px 0;
                text-align: center;
            }}

            .score-section h2 {{
                font-size: 18px;
                color: {self.COLORS['navy']};
                margin-bottom: 20px;
                text-transform: uppercase;
                font-weight: 600;
            }}

            .summary {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 16px;
                margin: 32px 0;
                text-align: center;
            }}

            .summary-item {{
                padding: 16px;
                background: {self.COLORS['light_grey']};
                border-radius: 8px;
            }}

            .summary-item .number {{
                font-size: 28px;
                font-weight: bold;
                color: {self.COLORS['teal']};
            }}

            .summary-item .label {{
                font-size: 13px;
                color: {self.COLORS['dark_grey']};
                margin-top: 8px;
                text-transform: uppercase;
            }}

            .disclaimer {{
                background: {self.COLORS['navy']};
                color: {self.COLORS['white']};
                padding: 20px;
                border-radius: 8px;
                margin: 32px 0;
                font-size: 13px;
                line-height: 1.8;
            }}

            .disclaimer strong {{
                color: {self.COLORS['teal']};
            }}

            h2 {{
                font-size: 24px;
                color: {self.COLORS['navy']};
                margin: 40px 0 20px 0;
                padding-bottom: 12px;
                border-bottom: 2px solid {self.COLORS['teal']};
                font-weight: 600;
            }}

            h3 {{
                color: {self.COLORS['navy']};
            }}

            .paywall {{
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, {self.COLORS['light_grey']} 0%, {self.COLORS['white']} 100%);
                border-radius: 12px;
                margin: 32px 0;
            }}

            .paywall-amount {{
                font-size: 36px;
                font-weight: bold;
                color: {self.COLORS['teal']};
                margin: 16px 0;
            }}

            .paywall-button {{
                display: inline-block;
                background: linear-gradient(135deg, {self.COLORS['teal']} 0%, {self.COLORS['navy']} 100%);
                color: {self.COLORS['white']};
                padding: 16px 32px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                text-decoration: none;
                border: none;
                cursor: pointer;
                margin-top: 16px;
                box-shadow: 0 4px 12px rgba(22, 160, 133, 0.3);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}

            .paywall-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(22, 160, 133, 0.4);
            }}

            .code-block {{
                background: {self.COLORS['navy']};
                color: {self.COLORS['light_grey']};
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                font-family: 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.6;
                margin: 20px 0;
            }}

            .copy-button {{
                background: {self.COLORS['teal']};
                color: {self.COLORS['white']};
                padding: 8px 16px;
                border-radius: 4px;
                border: none;
                cursor: pointer;
                font-size: 12px;
                margin-bottom: 12px;
            }}

            footer {{
                margin-top: 60px;
                padding-top: 20px;
                border-top: 1px solid {self.COLORS['light_grey']};
                text-align: center;
                font-size: 12px;
                color: {self.COLORS['dark_grey']};
            }}

            @media (max-width: 768px) {{
                header h1 {{
                    font-size: 24px;
                }}

                h2 {{
                    font-size: 20px;
                }}

                .summary {{
                    grid-template-columns: 1fr;
                }}

                .container {{
                    padding: 20px 16px;
                }}

                header {{
                    margin: -20px -16px 30px -16px;
                    padding: 32px 16px;
                }}
            }}

            @media print {{
                body {{
                    background: {self.COLORS['white']};
                }}

                .paywall {{
                    display: none;
                }}

                .code-block {{
                    page-break-inside: avoid;
                }}
            }}
        </style>
        '''

    def generate_teaser_html(self) -> str:
        """Generate TEASER version (limited detail, paywall)."""
        self.apps = self.analysis.apps

        header = f'''
        <header>
            <h1>{self.analysis.business_name}</h1>
            <p>{self._format_sector_name(self.analysis.sector)}</p>
            <div class="meta">Privacy Compliance Report • {self._format_date(self.analysis.analysis_date)}</div>
        </header>
        '''

        score_section = f'''
        <div class="score-section">
            <h2>Overall Compliance Score</h2>
            {self._generate_compliance_gauge(self.analysis.overall_score)}
        </div>
        '''

        summary = f'''
        <h2>Compliance Summary</h2>
        <div class="summary">
            <div class="summary-item">
                <div class="number">{self.analysis.summary.compliant_count}</div>
                <div class="label">Compliant</div>
            </div>
            <div class="summary-item">
                <div class="number">{self.analysis.summary.partial_count}</div>
                <div class="label">Partially Compliant</div>
            </div>
            <div class="summary-item">
                <div class="number">{self.analysis.summary.non_compliant_count}</div>
                <div class="label">Non-Compliant</div>
            </div>
        </div>
        '''

        app_grid = f'''
        <h2>All 13 Australian Privacy Principles</h2>
        {self._generate_app_grid()}
        '''

        # APP 1 detailed (unblurred)
        app1_detail = self._generate_app_detail_section(self.apps[0], blurred=False)

        # All other APPs blurred with paywall
        other_apps_blurred = ''.join(
            self._generate_app_detail_section(app, blurred=True) for app in self.apps[1:]
        )

        paywall = f'''
        <h2>Unlock Your Complete Gap Analysis</h2>
        <div class="paywall">
            <div style="font-size: 18px; color: {self.COLORS['navy']}; margin-bottom: 8px;">Get the Full Report</div>
            <div class="paywall-amount">A$149</div>
            <p style="margin-bottom: 16px; color: {self.COLORS['dark_grey']};">Complete analysis of all 13 APPs with recommended policy language customised to your sector</p>
            <button class="paywall-button" onclick="alert('In a production environment, this would redirect to your checkout flow.')">Unlock Full Report</button>
        </div>
        '''

        adm = self._generate_adm_callout()

        disclaimer = f'''
        <div class="disclaimer">
            <strong>⚠️ Disclaimer:</strong> This report is for informational purposes only and does not constitute legal advice. The Australian Privacy Act and Privacy Principles are complex and may apply differently to your specific circumstances. Please consult a qualified privacy professional or legal advisor for advice specific to your business before implementing any changes to your privacy practices.
        </div>
        '''

        footer = f'''
        <footer>
            <p>Report generated on {datetime.now().strftime('%d %B %Y at %H:%M')} UTC</p>
            <p>© 2026 Privacy Compliance Tools. All rights reserved.</p>
        </footer>
        '''

        html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Privacy Compliance Report - {self.analysis.business_name}</title>
            {self._generate_css()}
        </head>
        <body>
            <div class="container">
                {header}
                {score_section}
                {summary}
                {app_grid}

                <h2>Detailed Analysis</h2>
                {app1_detail}
                {other_apps_blurred}

                {paywall}
                {adm}
                {disclaimer}
                {footer}
            </div>
        </body>
        </html>
        '''

        return html

    def generate_full_html(self) -> str:
        """Generate FULL version (complete analysis, all APPs detailed)."""
        self.apps = self.analysis.apps

        header = f'''
        <header>
            <h1>{self.analysis.business_name}</h1>
            <p>{self._format_sector_name(self.analysis.sector)}</p>
            <div class="meta">Complete Privacy Compliance Report • {self._format_date(self.analysis.analysis_date)}</div>
        </header>
        '''

        score_section = f'''
        <div class="score-section">
            <h2>Overall Compliance Score</h2>
            {self._generate_compliance_gauge(self.analysis.overall_score)}
        </div>
        '''

        summary = f'''
        <h2>Compliance Summary</h2>
        <div class="summary">
            <div class="summary-item">
                <div class="number">{self.analysis.summary.compliant_count}</div>
                <div class="label">Compliant</div>
            </div>
            <div class="summary-item">
                <div class="number">{self.analysis.summary.partial_count}</div>
                <div class="label">Partially Compliant</div>
            </div>
            <div class="summary-item">
                <div class="number">{self.analysis.summary.non_compliant_count}</div>
                <div class="label">Non-Compliant</div>
            </div>
        </div>
        '''

        app_grid = f'''
        <h2>All 13 Australian Privacy Principles</h2>
        {self._generate_app_grid()}
        '''

        # All APPs detailed (no blur)
        all_apps_detail = ''.join(
            self._generate_app_detail_section(app, blurred=False) for app in self.apps
        )

        adm = self._generate_adm_callout()

        # Privacy policy template
        policy_template = self._generate_policy_template()
        template_section = f'''
        <h2>Customised Privacy Policy Template</h2>
        <p style="margin-bottom: 16px; color: {self.COLORS['dark_grey']};">Below is a ready-to-customise privacy policy template for the {self.analysis.sector} sector. Copy the entire code block and adapt it to your specific circumstances.</p>
        <button class="copy-button" onclick="copyToClipboard()">📋 Copy to Clipboard</button>
        <div class="code-block" id="template-code">{policy_template}</div>
        '''

        disclaimer = f'''
        <div class="disclaimer">
            <strong>⚠️ Disclaimer:</strong> This report is for informational purposes only and does not constitute legal advice. The Australian Privacy Act and Privacy Principles are complex and may apply differently to your specific circumstances. Please consult a qualified privacy professional or legal advisor for advice specific to your business before implementing any changes to your privacy practices.
        </div>
        '''

        footer = f'''
        <footer>
            <p>Report generated on {datetime.now().strftime('%d %B %Y at %H:%M')} UTC</p>
            <p>© 2026 Privacy Compliance Tools. All rights reserved.</p>
        </footer>
        '''

        # JavaScript for copy functionality
        script = '''
        <script>
            function copyToClipboard() {
                const codeBlock = document.getElementById('template-code');
                const text = codeBlock.innerText;
                navigator.clipboard.writeText(text).then(() => {
                    const button = event.target;
                    const originalText = button.innerText;
                    button.innerText = '✓ Copied!';
                    button.style.background = '#27ae60';
                    setTimeout(() => {
                        button.innerText = originalText;
                        button.style.background = '';
                    }, 2000);
                }).catch(err => {
                    alert('Failed to copy to clipboard');
                });
            }
        </script>
        '''

        html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Privacy Compliance Report - {self.analysis.business_name}</title>
            {self._generate_css()}
        </head>
        <body>
            <div class="container">
                {header}
                {score_section}
                {summary}
                {app_grid}

                <h2>Detailed Analysis</h2>
                {all_apps_detail}

                {adm}
                {template_section}
                {disclaimer}
                {footer}
            </div>
            {script}
        </body>
        </html>
        '''

        return html


def main():
    """Example usage."""
    # Sample data
    sample_data = {
        "business_name": "Coastal Properties Realty",
        "sector": "Real Estate",
        "analysis_date": "2026-04-01",
        "overall_score": 32,
        "overall_status": "NON_COMPLIANT",
        "apps": [
            {
                "app_number": 1,
                "app_name": "Open and Transparent Management of Personal Information",
                "status": "NON_COMPLIANT",
                "findings": [
                    "No privacy policy found on website",
                    "No information about data handling practices visible to customers",
                    "No contact details for privacy queries",
                ],
                "recommended_language": "Coastal Properties Realty is committed to protecting your personal information and managing it in an open and transparent way. We comply with the Australian Privacy Principles and understand the importance of your privacy.",
                "priority": "HIGH",
            },
            {
                "app_number": 2,
                "app_name": "Collection of Solicited Personal Information",
                "status": "PARTIALLY_COMPLIANT",
                "findings": [
                    "Collection practices not fully documented",
                    "Some forms lack required consent language",
                ],
                "recommended_language": "We collect personal information including your name, contact details, and property preferences. We only collect information necessary to provide our real estate services and with your consent.",
                "priority": "HIGH",
            },
            {
                "app_number": 3,
                "app_name": "Collection of Unsolicited Personal Information",
                "status": "NON_COMPLIANT",
                "findings": [
                    "No procedure for handling unsolicited information",
                    "Unclear how unsolicited data is managed",
                ],
                "recommended_language": "If we receive personal information that we did not solicit, we will assess whether we could have solicited it. If not, we will destroy or de-identify it as soon as practicable.",
                "priority": "MEDIUM",
            },
            {
                "app_number": 4,
                "app_name": "Dealing with Personal Information",
                "status": "PARTIALLY_COMPLIANT",
                "findings": [
                    "Use of personal information for secondary purposes not fully disclosed",
                    "No clear procedure for obtaining additional consent",
                ],
                "recommended_language": "We use your personal information for the primary purpose it was provided. Secondary uses are only made with your consent or where otherwise permitted by law.",
                "priority": "HIGH",
            },
            {
                "app_number": 5,
                "app_name": "Notification about Personal Information Management",
                "status": "NON_COMPLIANT",
                "findings": [
                    "Notification statements missing from collection points",
                    "No reference to OAIC or complaint procedures",
                ],
                "recommended_language": "When we collect your personal information, we provide notification of our identity, how to access your information, and how to lodge a complaint with the Office of the Australian Information Commissioner.",
                "priority": "HIGH",
            },
            {
                "app_number": 6,
                "app_name": "Use or Disclosure of Personal Information",
                "status": "NON_COMPLIANT",
                "findings": [
                    "Unsecured email used for client communications",
                    "Disclosure to third parties not adequately disclosed",
                ],
                "recommended_language": "We do not disclose your personal information to third parties without your consent, except where required by law or to provide our services.",
                "priority": "CRITICAL",
            },
            {
                "app_number": 7,
                "app_name": "Direct Marketing",
                "status": "COMPLIANT",
                "findings": [
                    "Email marketing complies with requirements",
                    "Unsubscribe mechanism in place",
                ],
                "recommended_language": "We comply with all direct marketing requirements and provide clear opt-out mechanisms for all marketing communications.",
                "priority": "LOW",
            },
            {
                "app_number": 8,
                "app_name": "Credit Eligibility Information",
                "status": "NOT_ADDRESSED",
                "findings": [
                    "Not applicable - business does not handle credit eligibility information",
                ],
                "recommended_language": "This principle is not applicable to our business as we do not provide credit services or collect credit eligibility information.",
                "priority": "LOW",
            },
            {
                "app_number": 9,
                "app_name": "Adoption, Use or Disclosure of Government Related Identifiers",
                "status": "COMPLIANT",
                "findings": [
                    "No government identifiers stored as primary identifier",
                    "ABN not used as customer ID",
                ],
                "recommended_language": "We do not adopt government-related identifiers such as ABN as our own identifier for individuals, in accordance with the Privacy Principles.",
                "priority": "LOW",
            },
            {
                "app_number": 10,
                "app_name": "Quality of Personal Information",
                "status": "PARTIALLY_COMPLIANT",
                "findings": [
                    "No regular data quality audits conducted",
                    "Limited mechanisms for customers to update information",
                ],
                "recommended_language": "We take reasonable steps to ensure your personal information is accurate, up-to-date, complete and relevant. You can request updates to your information at any time.",
                "priority": "MEDIUM",
            },
            {
                "app_number": 11,
                "app_name": "Data Security",
                "status": "NON_COMPLIANT",
                "findings": [
                    "No encryption on customer database",
                    "Staff access controls not implemented",
                    "No incident response procedure",
                ],
                "recommended_language": "We implement appropriate physical, electronic and procedural safeguards to protect your personal information from misuse, loss, unauthorised access, modification and disclosure.",
                "priority": "CRITICAL",
            },
            {
                "app_number": 12,
                "app_name": "Access and Correction",
                "status": "NON_COMPLIANT",
                "findings": [
                    "No formal access request procedure documented",
                    "No SLA for responding to access requests",
                ],
                "recommended_language": "You have the right to access and correct your personal information. Submit a written request to our Privacy Officer and we will respond within 30 days.",
                "priority": "HIGH",
            },
            {
                "app_number": 13,
                "app_name": "Complaints Management",
                "status": "NON_COMPLIANT",
                "findings": [
                    "No complaints procedure documented",
                    "No reference to OAIC escalation path",
                ],
                "recommended_language": "We have a complaints procedure in place. Contact our Privacy Officer with any concerns. If unsatisfied, you can lodge a complaint with the Office of the Australian Information Commissioner.",
                "priority": "HIGH",
            },
        ],
        "adm_check": {
            "uses_adm": "NO",
            "adm_disclosed": False,
            "recommendation": "Our analysis indicates you do not currently use automated decision-making in your client services.",
        },
        "summary": {
            "compliant_count": 2,
            "partial_count": 4,
            "non_compliant_count": 6,
            "not_addressed_count": 1,
        },
    }

    # Generate reports
    generator = HTMLReportGenerator(sample_data)

    # Save teaser
    teaser_html = generator.generate_teaser_html()
    with open(
        "/sessions/loving-gifted-keller/mnt/outputs/compliance-product/reports/sample_teaser.html",
        "w",
    ) as f:
        f.write(teaser_html)
    print(
        "✓ Teaser report saved to sample_teaser.html"
    )

    # Save full
    full_html = generator.generate_full_html()
    with open(
        "/sessions/loving-gifted-keller/mnt/outputs/compliance-product/reports/sample_full.html",
        "w",
    ) as f:
        f.write(full_html)
    print(
        "✓ Full report saved to sample_full.html"
    )


if __name__ == "__main__":
    main()
