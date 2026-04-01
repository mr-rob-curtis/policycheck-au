"""PolicyCheck AU - Retrieve saved scan reports by slug."""
import json
import sys
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.report_store import get_report

ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN', '*')


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        slug = params.get('slug', [''])[0].strip()

        if not slug:
            self._json_response(400, {'error': 'slug parameter is required'})
            return

        data = get_report(slug)
        if data is None:
            self._json_response(404, {'error': 'Report not found'})
            return

        self._json_response(200, data)

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
