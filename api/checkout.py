"""Stripe Checkout session creation for draft purchase."""
import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN', '*')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PRICE_ID = os.environ.get('STRIPE_PRICE_ID')
BASE_URL = os.environ.get('BASE_URL', 'https://privacysorted.com')


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        if not STRIPE_SECRET_KEY:
            self._json_response(500, {'error': 'Payment not configured'})
            return

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

        slug = data.get('slug', '').strip()
        business_name = data.get('business_name', '').strip()
        email = data.get('email', '').strip()

        if not slug:
            self._json_response(400, {'error': 'slug is required'})
            return

        try:
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY

            checkout_params = {
                'mode': 'payment',
                'payment_method_types': ['card'],
                'line_items': [{
                    'price': STRIPE_PRICE_ID,
                    'quantity': 1,
                }],
                'success_url': f'{BASE_URL}/report/{slug}?paid=true&session_id={{CHECKOUT_SESSION_ID}}',
                'cancel_url': f'{BASE_URL}/report/{slug}',
                'metadata': {
                    'slug': slug,
                    'business_name': business_name,
                },
            }

            if email:
                checkout_params['customer_email'] = email

            session = stripe.checkout.Session.create(**checkout_params)

            self._json_response(200, {
                'checkout_url': session.url,
                'session_id': session.id,
            })

        except Exception:
            print(f"CHECKOUT_ERROR: {traceback.format_exc()}")
            self._json_response(500, {'error': 'Failed to create checkout session'})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', ALLOWED_ORIGIN)
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', ALLOWED_ORIGIN)
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
