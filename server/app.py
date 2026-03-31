#!/usr/bin/env python3
"""
PolicyCheck AU - Internal Operating System
Single Flask application serving API and vanilla JS frontend
"""

import sys
import json
import uuid
from datetime import datetime
from pathlib import Path
from functools import wraps

import flask
from flask import Flask, render_template, jsonify, request, Response
import logging

# Add parent directories to path for imports
sys.path.insert(0, '/sessions/loving-gifted-keller/mnt/outputs/compliance-product/scraper')
sys.path.insert(0, '/sessions/loving-gifted-keller/mnt/outputs/compliance-product/engine')
sys.path.insert(0, '/sessions/loving-gifted-keller/mnt/outputs/compliance-product/reports')

from policy_scraper import PrivacyPolicyScraper
from compliance_engine import ComplianceEngine
from report_generator import HTMLReportGenerator
from app_requirements import SectorSpecificGuidance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

# Data storage
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)
SCANS_FILE = DATA_DIR / 'scans.json'

# Ensure scans.json exists
if not SCANS_FILE.exists():
    SCANS_FILE.write_text(json.dumps({
        'scans': [],
        'created_at': datetime.now().isoformat()
    }))


# ========================================================================================
# UTILITIES
# ========================================================================================

def load_scans():
    """Load all scans from JSON file"""
    try:
        with open(SCANS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('scans', [])
    except Exception as e:
        logger.error(f"Error loading scans: {e}")
        return []


def save_scans(scans):
    """Save scans to JSON file"""
    try:
        with open(SCANS_FILE, 'w') as f:
            json.dump({
                'scans': scans,
                'updated_at': datetime.now().isoformat()
            }, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving scans: {e}")


def find_scan(scan_id):
    """Find a scan by ID"""
    scans = load_scans()
    for scan in scans:
        if scan['scan_id'] == scan_id:
            return scan
    return None


def save_scan(scan_data):
    """Save a new scan to the database"""
    scans = load_scans()
    scans.append(scan_data)
    save_scans(scans)


def sse_event(step, message, **kwargs):
    """Format SSE event data"""
    data = {
        'step': step,
        'message': message,
        **kwargs
    }
    return f"data: {json.dumps(data)}\n\n"


# ========================================================================================
# API ENDPOINTS
# ========================================================================================

@app.route('/')
def index():
    """Serve main dashboard"""
    return render_template('index.html')


@app.route('/api/sectors')
def get_sectors():
    """Get list of available sectors"""
    sectors = [
        "Real Estate",
        "Pharmacy",
        "Legal",
        "Hospitality",
        "Automotive",
        "Jewellery",
        "Other"
    ]
    return jsonify({'sectors': sectors})


@app.route('/api/scan', methods=['POST', 'GET'])
def start_scan():
    """Start a compliance scan - returns SSE stream"""
    if request.method == 'POST':
        data = request.get_json()
    else:
        data = request.args

    url = data.get('url', '').strip()
    sector = data.get('sector', 'Other')
    business_name = data.get('business_name', '').strip()

    # Validate input
    if not url:
        return Response(
            sse_event('error', 'URL is required'),
            mimetype='text/event-stream'
        )

    # Create scan record
    scan_id = str(uuid.uuid4())
    scan_record = {
        'scan_id': scan_id,
        'url': url,
        'sector': sector,
        'business_name': business_name,
        'started_at': datetime.now().isoformat(),
        'status': 'in_progress'
    }

    def generate():
        """Generate SSE stream"""
        try:
            # Step 1: Connecting
            yield sse_event('connecting', f'Connecting to {url}...')

            # Step 2: Scraping
            yield sse_event('scraping', 'Scanning website for privacy policy...')

            scraper = PrivacyPolicyScraper(timeout=15)
            scrape_result = scraper.scrape_privacy_policy(url)

            if not scrape_result['policy_found']:
                yield sse_event(
                    'privacy_not_found',
                    'No privacy policy found on website',
                    severity='critical'
                )
                # Still analyze (will be all NOT_ADDRESSED)
                policy_text = None
            else:
                policy_text = scrape_result['policy_text']
                policy_url = scrape_result['policy_url']
                char_count = len(policy_text) if policy_text else 0
                yield sse_event(
                    'privacy_found',
                    f'Privacy policy found ({char_count:,} chars)',
                    policy_url=policy_url
                )

            # Step 3: Cookies
            yield sse_event('cookies', 'Checking for cookie policy...')

            # Step 4: Terms
            yield sse_event('terms', 'Checking for terms & conditions...')

            # Step 5: Analyzing
            yield sse_event('analyzing', 'Analysing against 13 Australian Privacy Principles...')

            # Run compliance engine
            engine = ComplianceEngine(mode='rule_based')
            report = engine.analyze(policy_text, business_name, sector)

            # Convert report to dict
            result = {
                'scan_id': scan_id,
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

            # Save to database
            scan_record['status'] = 'complete'
            scan_record['completed_at'] = datetime.now().isoformat()
            scan_record['result'] = result
            save_scan(scan_record)

            # Step 6: Complete
            yield sse_event(
                'complete',
                'Analysis complete',
                result=result
            )

        except Exception as e:
            logger.error(f"Error in scan: {e}", exc_info=True)
            yield sse_event('error', f'Scan failed: {str(e)}')

    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/scans')
def get_scans():
    """Get list of all scans"""
    scans = load_scans()
    # Return scan metadata (not full results)
    return jsonify({
        'scans': [
            {
                'scan_id': s['scan_id'],
                'url': s['url'],
                'business_name': s['business_name'],
                'sector': s['sector'],
                'started_at': s['started_at'],
                'status': s['status'],
                'score': s['result']['analysis']['overall_score'] if 'result' in s else None,
                'compliance_status': s['result']['analysis']['overall_status'] if 'result' in s else None,
            }
            for s in scans
        ]
    })


@app.route('/api/scan/<scan_id>')
def get_scan(scan_id):
    """Get a specific scan result"""
    scan = find_scan(scan_id)
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404

    return jsonify(scan)


@app.route('/api/report/<scan_id>/teaser')
def get_teaser_report(scan_id):
    """Get teaser HTML report"""
    scan = find_scan(scan_id)
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404

    if 'result' not in scan:
        return jsonify({'error': 'Scan incomplete'}), 400

    result = scan['result']
    analysis_dict = result['analysis'].copy()
    # Report generator expects business_name and sector at top level
    analysis_dict['business_name'] = result.get('business_name', 'Unknown')
    analysis_dict['sector'] = result.get('sector', 'Other')

    generator = HTMLReportGenerator(analysis_dict)
    html = generator.generate_teaser_html()

    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}


@app.route('/api/report/<scan_id>/full')
def get_full_report(scan_id):
    """Get full HTML report"""
    scan = find_scan(scan_id)
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404

    if 'result' not in scan:
        return jsonify({'error': 'Scan incomplete'}), 400

    result = scan['result']
    analysis_dict = result['analysis'].copy()
    analysis_dict['business_name'] = result.get('business_name', 'Unknown')
    analysis_dict['sector'] = result.get('sector', 'Other')

    generator = HTMLReportGenerator(analysis_dict)
    html = generator.generate_full_html()

    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}


@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    scans = load_scans()
    completed_scans = [s for s in scans if s['status'] == 'complete']

    total_scans = len(completed_scans)

    # Calculate average score
    scores = []
    sectors = set()
    violations = 0

    for scan in completed_scans:
        if 'result' in scan and 'analysis' in scan['result']:
            analysis = scan['result']['analysis']
            scores.append(analysis['overall_score'])
            sectors.add(scan['sector'])

            # Count non-compliant APPs as violations
            non_compliant = sum(1 for app in analysis['apps'] if app['status'] == 'NON_COMPLIANT')
            violations += non_compliant

    avg_score = sum(scores) / len(scores) if scores else 0

    return jsonify({
        'total_scans': total_scans,
        'average_score': round(avg_score, 1),
        'sectors_scanned': len(sectors),
        'violations_found': violations,
        'businesses_analysed': len(set(s['business_name'] for s in completed_scans if s.get('business_name')))
    })


# ========================================================================================
# ERROR HANDLERS
# ========================================================================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal error: {e}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500


# ========================================================================================
# MAIN
# ========================================================================================

if __name__ == '__main__':
    logger.info("Starting PolicyCheck AU server on port 5000")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
