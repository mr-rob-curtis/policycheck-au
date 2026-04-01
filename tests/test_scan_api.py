"""Tests for the scan API endpoint."""
import pytest
import json
from unittest.mock import patch, MagicMock
from api.scan import _run_scan, _extract_excerpt


class TestExtractExcerpt:
    def test_none_input(self):
        assert _extract_excerpt(None) is None

    def test_empty_string(self):
        assert _extract_excerpt("") is None

    def test_short_text(self):
        assert _extract_excerpt("Hello world") == "Hello world"

    def test_long_text_sentence_boundary(self):
        # Period must be past the halfway mark of max_length to be used as cut point
        text = "x" * 30 + ". Rest of the long text. " + "y" * 500
        result = _extract_excerpt(text, max_length=50)
        assert result.endswith('.')
        assert len(result) <= 50

    def test_long_text_no_sentence(self):
        text = "x" * 600
        result = _extract_excerpt(text, max_length=500)
        assert result.endswith('...')
        assert len(result) == 503  # 500 + '...'

    def test_strips_whitespace(self):
        assert _extract_excerpt("  hello  ") == "hello"


class TestRunScan:
    def test_empty_url_returns_400(self):
        status, result = _run_scan("", "Other", "")
        assert status == 400
        assert 'error' in result

    def test_adds_https_prefix(self):
        with patch('api.scan.PrivacyPolicyScraper') as MockScraper, \
             patch('api.scan.ComplianceEngine') as MockEngine:
            mock_scraper = MockScraper.return_value
            mock_scraper.scrape_privacy_policy.return_value = {
                'policy_found': True,
                'policy_text': 'We collect data.',
                'policy_url': 'https://example.com/privacy',
            }
            mock_engine = MockEngine.return_value
            mock_report = MagicMock()
            mock_report.overall_score = 50
            mock_report.overall_status = "Partially Compliant"
            mock_report.analysis_date = "2026-04-01"
            mock_report.analysis_mode = "rule_based"
            mock_report.apps = []
            mock_report.adm_check = {}
            mock_report.summary = {}
            mock_report.sector_risk_profile = {}
            mock_report.next_steps = []
            mock_engine.analyze.return_value = mock_report

            status, result = _run_scan("example.com", "Other", "Test")
            assert status == 200
            # Verify https was prepended
            mock_scraper.scrape_privacy_policy.assert_called_once_with('https://example.com')

    def test_happy_path(self):
        with patch('api.scan.PrivacyPolicyScraper') as MockScraper, \
             patch('api.scan.ComplianceEngine') as MockEngine:
            mock_scraper = MockScraper.return_value
            mock_scraper.scrape_privacy_policy.return_value = {
                'policy_found': True,
                'policy_text': 'Privacy policy text here.',
                'policy_url': 'https://example.com/privacy',
            }
            mock_report = MagicMock()
            mock_report.overall_score = 65
            mock_report.overall_status = "Partially Compliant"
            mock_report.analysis_date = "2026-04-01"
            mock_report.analysis_mode = "rule_based"
            mock_report.apps = [{"app_number": 1, "status": "COMPLIANT"}]
            mock_report.adm_check = {"uses_adm": "NO"}
            mock_report.summary = {"compliant_count": 1}
            mock_report.sector_risk_profile = {}
            mock_report.next_steps = ["Review APP 2"]
            MockEngine.return_value.analyze.return_value = mock_report

            status, result = _run_scan("https://example.com", "Other", "Test Biz")
            assert status == 200
            assert result['url'] == 'https://example.com'
            assert result['policy_found'] is True
            assert result['analysis']['overall_score'] == 65
            assert result['business_name'] == 'Test Biz'

    def test_no_policy_found(self):
        with patch('api.scan.PrivacyPolicyScraper') as MockScraper, \
             patch('api.scan.ComplianceEngine') as MockEngine:
            mock_scraper = MockScraper.return_value
            mock_scraper.scrape_privacy_policy.return_value = {
                'policy_found': False,
                'policy_text': None,
                'policy_url': None,
            }
            mock_report = MagicMock()
            mock_report.overall_score = 0
            mock_report.overall_status = "Non-Compliant"
            mock_report.analysis_date = "2026-04-01"
            mock_report.analysis_mode = "rule_based"
            mock_report.apps = []
            mock_report.adm_check = {}
            mock_report.summary = {}
            mock_report.sector_risk_profile = {}
            mock_report.next_steps = []
            MockEngine.return_value.analyze.return_value = mock_report

            status, result = _run_scan("https://example.com", "Other", "")
            assert status == 200
            assert result['policy_found'] is False

    def test_exception_returns_500(self):
        with patch('api.scan.PrivacyPolicyScraper') as MockScraper:
            MockScraper.return_value.scrape_privacy_policy.side_effect = RuntimeError("boom")
            status, result = _run_scan("https://example.com", "Other", "")
            assert status == 500
            assert 'error' in result
