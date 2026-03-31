"""PolicyCheck AU - Vercel Serverless Scan Function"""
import json
import sys
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add project root to path for lib imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.policy_scraper import PrivacyPolicyScraper
from lib.compliance_engine import ComplianceEngine


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET request with query params"""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        url = params.get('url', [''])[0].strip()
        sector = params.get('sector', ['Other'])[0].strip()
        business_name = params.get('business_name', [''])[0].strip()

        if not url:
            self._json_response(400, {'error': 'URL is required'})
            return

        # Ensure URL has protocol
        if not url.startswith('http'):
            url = 'https://' + url

        try:
            # Step 1: Scrape
            scraper = PrivacyPolicyScraper(timeout=12)
            scrape_result = scraper.scrape_privacy_policy(url)

            policy_text = scrape_result.get('policy_text') if scrape_result['policy_found'] else None

            # Step 2: Analyse
            engine = ComplianceEngine(mode='rule_based')
            report = engine.analyze(policy_text, business_name, sector)

            # Build result
            result = {
                'url': url,
                'sector': sector,
                'business_name': business_name,
                'policy_found': scrape_result['policy_found'],
                'policy_url': scrape_result.get('policy_url'),
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

            self._json_response(200, result)

        except Exception as e:
            self._json_response(500, {'error': str(e)})

    def do_POST(self):
        """Handle POST request with JSON body"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length else '{}'

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response(400, {'error': 'Invalid JSON'})
            return

        url = data.get('url', '').strip()
        sector = data.get('sector', 'Other')
        business_name = data.get('business_name', '').strip()

        if not url:
            self._json_response(400, {'error': 'URL is required'})
            return

        if not url.startswith('http'):
            url = 'https://' + url

        try:
            scraper = PrivacyPolicyScraper(timeout=12)
            scrape_result = scraper.scrape_privacy_policy(url)

            policy_text = scrape_result.get('policy_text') if scrape_result['policy_found'] else None

            engine = ComplianceEngine(mode='rule_based')
            report = engine.analyze(policy_text, business_name, sector)

            result = {
                'url': url,
                'sector': sector,
                'business_name': business_name,
                'policy_found': scrape_result['policy_found'],
                'policy_url': scrape_result.get('policy_url'),
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

            self._json_response(200, result)

        except Exception as e:
            self._json_response(500, {'error': str(e)})

    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
