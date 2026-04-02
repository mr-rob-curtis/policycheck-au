"""Stripe webhook handler. Marks reports as paid and triggers draft generation."""
import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        if not STRIPE_SECRET_KEY or not STRIPE_WEBHOOK_SECRET:
            self._json_response(500, {'error': 'Webhook not configured'})
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
        except (ValueError, TypeError):
            content_length = 0
        payload = self.rfile.read(content_length).decode('utf-8') if content_length else ''
        sig_header = self.headers.get('Stripe-Signature', '')

        try:
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY

            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            self._json_response(400, {'error': 'Invalid signature'})
            return
        except Exception:
            print(f"WEBHOOK_PARSE_ERROR: {traceback.format_exc()}")
            self._json_response(400, {'error': 'Invalid payload'})
            return

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            slug = session.get('metadata', {}).get('slug')
            customer_email = session.get('customer_details', {}).get('email', '')

            if slug:
                try:
                    from lib.report_store import mark_paid, get_report, save_draft
                    from lib.draft_generator import generate_draft

                    # Mark as paid
                    mark_paid(slug)
                    print(f"PAYMENT_SUCCESS: slug={slug} email={customer_email}")

                    # Generate draft
                    report = get_report(slug)
                    if report:
                        draft_result = generate_draft(report)
                        draft_result['customer_email'] = customer_email
                        draft_result['stripe_session_id'] = session.get('id')
                        save_draft(slug, draft_result)
                        print(f"DRAFT_GENERATED: slug={slug}")
                    else:
                        print(f"DRAFT_ERROR: report not found for slug={slug}")

                except Exception:
                    print(f"DRAFT_ERROR: {traceback.format_exc()}")
                    # Payment succeeded but draft failed. Log for manual recovery.
                    # The customer will see "generating..." and can contact support.

        self._json_response(200, {'received': True})

    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
