"""PolicyCheck AU - Vercel Serverless Scan Function"""
import json
import sys
import os
import traceback
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add project root to path for lib imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.policy_scraper import PrivacyPolicyScraper
from lib.compliance_engine import ComplianceEngine
from lib.report_store import save_report, slugify

ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN', '*')


def _extract_excerpt(policy_text, max_length=500):
    """Extract a meaningful excerpt from the policy text."""
    if not policy_text:
        return None
    text = policy_text.strip()
    if len(text) <= max_length:
        return text
    # Try to cut at a sentence boundary
    cut = text[:max_length]
    last_period = cut.rfind('.')
    if last_period > max_length // 2:
        return cut[:last_period + 1]
    return cut + '...'


def _run_scan(url, sector, business_name):
    """Run a scan and return the result dict."""
    if not url:
        return 400, {'error': 'URL is required'}

    if not url.startswith('http'):
        url = 'https://' + url

    try:
        scraper = PrivacyPolicyScraper(timeout=8, rate_limit_delay=0)
        scrape_result = scraper.scrape_privacy_policy(url)

        policy_text = scrape_result.get('policy_text') if scrape_result['policy_found'] else None

        # Treat empty/whitespace-only text as no policy found
        if not policy_text or not policy_text.strip():
            policy_text = None

        engine = ComplianceEngine()
        report = engine.analyze(policy_text, business_name, sector)

        # Only mark policy_found if we actually extracted text
        actually_found = policy_text is not None

        result = {
            'url': url,
            'sector': sector,
            'business_name': business_name,
            'policy_found': actually_found,
            'policy_url': scrape_result.get('policy_url') if actually_found else None,
            'policy_excerpt': _extract_excerpt(policy_text),
            'analysis': {
                'business_name': business_name,
                'sector': sector,
                'overall_score': report.overall_score,
                'overall_status': report.overall_status,
                'analysis_date': report.analysis_date,
                'analysis_mode': report.analysis_mode,
                'apps': report.apps,
                'adm_check': report.adm_check,
                'summary': report.summary,
                'sector_risk_profile': report.sector_risk_profile,
                'next_steps': report.next_steps,
            }
        }

        # Save report for public report page
        slug_source = business_name or urlparse(url).hostname or ''
        slug = slugify(slug_source)
        if slug:
            result['slug'] = slug
            try:
                save_report(slug, result)
            except Exception:
                pass  # Non-critical, don't fail the scan

        return 200, result

    except Exception:
        print(f"SCAN_ERROR: {traceback.format_exc()}")
        return 500, {'error': 'An error occurred while scanning. Please try again.'}


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        url = params.get('url', [''])[0].strip()
        sector = params.get('sector', ['Other'])[0].strip()
        business_name = params.get('business_name', [''])[0].strip()
        status, result = _run_scan(url, sector, business_name)
        self._json_response(status, result)

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
        except (ValueError, TypeError):
            content_length = 0
        body = self.rfile.read(content_length).decode('utf-8') if content_length else '{}'
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response(400, {'error': 'Invalid JSON'})
            return
        url = data.get('url', '').strip()
        sector = data.get('sector', 'Other')
        business_name = data.get('business_name', '').strip()
        status, result = _run_scan(url, sector, business_name)
        self._json_response(status, result)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', ALLOWED_ORIGIN)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', ALLOWED_ORIGIN)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
