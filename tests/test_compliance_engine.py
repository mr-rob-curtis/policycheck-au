"""Tests for ComplianceEngine rule-based analysis."""
import pytest
from lib.compliance_engine import ComplianceEngine


@pytest.fixture
def engine():
    return ComplianceEngine()


SAMPLE_POLICY = """
Privacy Policy

We collect personal information including your name, email address, and phone number
when you register for our services. We collect this information directly from you.

We use your personal information to provide our services, process transactions,
and communicate with you about your account.

We may disclose your personal information to third parties such as service providers,
payment processors, and government authorities when required by law.

We take reasonable steps to protect your personal information from misuse,
interference, loss, and unauthorised access. We use encryption and secure servers.

You have the right to access your personal information that we hold about you.
You can request access by contacting our privacy officer.

You may request correction of your personal information if it is inaccurate,
out-of-date, incomplete, or misleading.

We will not use or disclose your personal information for direct marketing
without your consent. You can opt out of marketing communications at any time.

We do not transfer personal information overseas without appropriate safeguards.

We will notify you and the OAIC if we experience a data breach that is likely to
result in serious harm.

We have a process for handling complaints about our handling of personal information.
Contact our privacy officer to make a complaint.
"""

MINIMAL_POLICY = "We have a privacy policy. Contact us for details."


class TestEngineInit:
    def test_creates_successfully(self):
        engine = ComplianceEngine()
        assert engine.app_requirements is not None
        assert engine.scoring_rules is not None


class TestAnalyzeWithPolicy:
    def test_happy_path(self, engine):
        report = engine.analyze(SAMPLE_POLICY, "Test Business", "Other")
        assert report.business_name == "Test Business"
        assert report.sector == "Other"
        assert 0 <= report.overall_score <= 100
        assert report.overall_status in [
            "COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT"
        ]
        assert len(report.apps) == 13
        assert report.analysis_mode == "rule_based"

    def test_each_app_has_required_fields(self, engine):
        report = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        for app in report.apps:
            assert 'app_number' in app
            assert 'app_name' in app
            assert 'status' in app
            assert 'findings' in app
            assert 'gaps' in app
            assert 'priority' in app
            assert app['app_number'] >= 1
            assert app['app_number'] <= 13

    def test_comprehensive_policy_scores_higher(self, engine):
        comprehensive = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        minimal = engine.analyze(MINIMAL_POLICY, "Test", "Other")
        assert comprehensive.overall_score > minimal.overall_score

    def test_sector_specific_analysis(self, engine):
        report_re = engine.analyze(SAMPLE_POLICY, "Test", "real_estate")
        report_other = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        # Both should produce valid reports
        assert len(report_re.apps) == 13
        assert len(report_other.apps) == 13

    def test_adm_check_present(self, engine):
        report = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        assert report.adm_check is not None
        assert 'uses_adm' in report.adm_check

    def test_summary_counts(self, engine):
        report = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        total = (
            report.summary['compliant_count'] +
            report.summary['partial_count'] +
            report.summary['non_compliant_count'] +
            report.summary['not_addressed_count']
        )
        assert total == 13

    def test_next_steps_generated(self, engine):
        report = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        assert isinstance(report.next_steps, list)
        assert len(report.next_steps) > 0


class TestAnalyzeMissingPolicy:
    def test_no_policy_text(self, engine):
        report = engine.analyze(None, "Test", "Other")
        assert report.overall_score == 0
        for app in report.apps:
            assert app['status'] == 'NOT_ADDRESSED'

    def test_empty_string(self, engine):
        report = engine.analyze("", "Test", "Other")
        assert report.overall_score == 0

    def test_whitespace_only(self, engine):
        report = engine.analyze("   \n\t  ", "Test", "Other")
        assert report.overall_score == 0


class TestScoreThresholds:
    def test_score_is_integer(self, engine):
        report = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        assert isinstance(report.overall_score, int)

    def test_score_in_range(self, engine):
        report = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        assert 0 <= report.overall_score <= 100

    def test_zero_score_for_missing(self, engine):
        report = engine.analyze(None, "Test", "Other")
        assert report.overall_score == 0


class TestReportSerialization:
    def test_to_json(self, engine):
        report = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        json_str = report.to_json()
        assert '"business_name"' in json_str
        assert '"overall_score"' in json_str
        assert '"apps"' in json_str

    def test_to_json_valid(self, engine):
        import json
        report = engine.analyze(SAMPLE_POLICY, "Test", "Other")
        data = json.loads(report.to_json())
        assert data['business_name'] == 'Test'
        assert len(data['apps']) == 13
