"""Tests for HTMLReportGenerator."""
import pytest
from lib.report_generator import HTMLReportGenerator


SAMPLE_ANALYSIS = {
    "business_name": "Test Business",
    "sector": "Other",
    "analysis_date": "2026-04-01T12:00:00",
    "analysis_mode": "rule_based",
    "overall_score": 55,
    "overall_status": "Partially Compliant",
    "apps": [
        {
            "app_number": i,
            "app_name": f"APP {i}",
            "status": "COMPLIANT" if i <= 5 else "NON_COMPLIANT",
            "findings": [f"Finding for APP {i}"],
            "gaps": [f"Gap for APP {i}"] if i > 5 else [],
            "recommended_language": f"Recommended language for APP {i}",
            "priority": "HIGH" if i > 5 else "LOW",
        }
        for i in range(1, 14)
    ],
    "adm_check": {
        "uses_adm": "NO",
        "adm_disclosed": False,
        "examples_found": [],
        "recommendation": "Monitor for ADM usage",
    },
    "summary": {
        "compliant_count": 5,
        "partial_count": 0,
        "non_compliant_count": 8,
        "not_addressed_count": 0,
    },
    "sector_risk_profile": {
        "data_sensitivity": "medium",
        "regulatory_complexity": "medium",
    },
    "next_steps": ["Review non-compliant APPs", "Consult privacy professional"],
}


class TestHTMLReportGenerator:
    def test_init(self):
        gen = HTMLReportGenerator(SAMPLE_ANALYSIS)
        assert gen is not None

    def test_generate_teaser_html(self):
        gen = HTMLReportGenerator(SAMPLE_ANALYSIS)
        html = gen.generate_teaser_html()
        assert isinstance(html, str)
        assert len(html) > 100
        assert '<html' in html.lower() or '<!doctype' in html.lower() or 'div' in html.lower()
        assert 'Test Business' in html

    def test_generate_full_html(self):
        gen = HTMLReportGenerator(SAMPLE_ANALYSIS)
        html = gen.generate_full_html()
        assert isinstance(html, str)
        assert len(html) > 100
        assert 'Test Business' in html

    def test_both_reports_are_substantial(self):
        gen = HTMLReportGenerator(SAMPLE_ANALYSIS)
        teaser = gen.generate_teaser_html()
        full = gen.generate_full_html()
        # Both should produce substantial HTML output
        assert len(teaser) > 1000
        assert len(full) > 1000

    def test_score_in_output(self):
        gen = HTMLReportGenerator(SAMPLE_ANALYSIS)
        html = gen.generate_teaser_html()
        assert '55' in html

    def test_handles_zero_score(self):
        analysis = {**SAMPLE_ANALYSIS, "overall_score": 0, "overall_status": "Non-Compliant"}
        gen = HTMLReportGenerator(analysis)
        html = gen.generate_teaser_html()
        assert isinstance(html, str)
