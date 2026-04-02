"""Draft status polling endpoint. Frontend checks this after payment."""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN', '*')


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        slug = params.get('slug', [''])[0].strip()

        if not slug:
            self._json_response(400, {'error': 'slug is required'})
            return

        from lib.report_store import get_draft, get_report

        # Check if paid
        report = get_report(slug)
        if not report or not report.get('paid'):
            self._json_response(200, {'status': 'unpaid'})
            return

        # Check if draft exists
        draft = get_draft(slug)
        if draft:
            self._json_response(200, {
                'status': 'ready',
                'draft_text': draft.get('draft_text', ''),
                'generated_at': draft.get('generated_at', ''),
            })
        else:
            self._json_response(200, {'status': 'generating'})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', ALLOWED_ORIGIN)
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', ALLOWED_ORIGIN)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
