"""PrivacySorted - Contact Form Submission Handler"""
import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length else '{}'

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response(400, {'error': 'Invalid JSON'})
            return

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        scan_url = data.get('scan_url', '').strip()
        scan_score = data.get('scan_score', '')

        if not name or not email:
            self._json_response(400, {'error': 'Name and email are required'})
            return

        # For MVP, log the lead. In production, this would go to a database or CRM.
        lead = {
            'name': name,
            'email': email,
            'phone': phone,
            'scan_url': scan_url,
            'scan_score': scan_score,
            'submitted_at': datetime.now().isoformat(),
        }

        # Log to stdout (visible in Vercel function logs)
        print(f"NEW_LEAD: {json.dumps(lead)}")

        self._json_response(200, {'success': True, 'message': 'Thanks! We\'ll be in touch.'})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
