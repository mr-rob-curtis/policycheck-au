"""PolicyCheck AU - Vercel Serverless Report Function
Takes scan result as POST body, returns rendered HTML report.
"""
import json
import sys
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.report_generator import HTMLReportGenerator


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        """Generate HTML report from analysis data"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length else '{}'

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._error(400, 'Invalid JSON')
            return

        analysis = data.get('analysis', {})
        report_type = data.get('type', 'teaser')

        if not analysis or 'apps' not in analysis:
            self._error(400, 'Missing analysis data')
            return

        try:
            generator = HTMLReportGenerator(analysis)
            if report_type == 'full':
                html = generator.generate_full_html()
            else:
                html = generator.generate_teaser_html()

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        except Exception as e:
            self._error(500, str(e))

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _error(self, status, msg):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'error': msg}).encode('utf-8'))
