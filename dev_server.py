"""Local Flask dev server that mirrors Vercel's routing."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, send_from_directory, jsonify
from api.scan import _run_scan, _extract_excerpt
from lib.report_generator import HTMLReportGenerator
from lib.report_store import get_report

app = Flask(__name__, static_folder='public')


@app.route('/api/scan', methods=['GET', 'POST', 'OPTIONS'])
def scan():
    if request.method == 'OPTIONS':
        return _cors_response('')
    if request.method == 'GET':
        url = request.args.get('url', '').strip()
        sector = request.args.get('sector', 'Other').strip()
        business_name = request.args.get('business_name', '').strip()
    else:
        data = request.get_json(silent=True) or {}
        url = data.get('url', '').strip()
        sector = data.get('sector', 'Other')
        business_name = data.get('business_name', '').strip()
    status, result = _run_scan(url, sector, business_name)
    resp = jsonify(result)
    resp.status_code = status
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/report', methods=['POST', 'OPTIONS'])
def report():
    if request.method == 'OPTIONS':
        return _cors_response('')
    data = request.get_json(silent=True) or {}
    analysis = data.get('analysis', {})
    report_type = data.get('type', 'teaser')
    if not analysis or 'apps' not in analysis:
        resp = jsonify({'error': 'Missing analysis data'})
        resp.status_code = 400
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    try:
        generator = HTMLReportGenerator(analysis)
        if report_type == 'full':
            html = generator.generate_full_html()
        else:
            html = generator.generate_teaser_html()
        resp = app.make_response(html)
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
        import traceback
        print(f"REPORT_ERROR: {traceback.format_exc()}")
        resp = jsonify({'error': 'An error occurred generating the report.'})
        resp.status_code = 500
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/api/report_data', methods=['GET', 'OPTIONS'])
def report_data():
    if request.method == 'OPTIONS':
        return _cors_response('')
    slug = request.args.get('slug', '').strip()
    if not slug:
        resp = jsonify({'error': 'slug parameter is required'})
        resp.status_code = 400
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    data = get_report(slug)
    if data is None:
        resp = jsonify({'error': 'Report not found'})
        resp.status_code = 404
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/contact', methods=['POST', 'OPTIONS'])
def contact():
    if request.method == 'OPTIONS':
        return _cors_response('')
    import json
    from datetime import datetime
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    if not name or not email:
        resp = jsonify({'error': 'Name and email are required'})
        resp.status_code = 400
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    lead = {
        'name': name,
        'email': email,
        'phone': data.get('phone', '').strip(),
        'scan_url': data.get('scan_url', '').strip(),
        'scan_score': data.get('scan_score', ''),
        'submitted_at': datetime.now().isoformat(),
    }
    print(f"NEW_LEAD: {json.dumps(lead)}")
    resp = jsonify({'success': True, 'message': "Thanks! We'll be in touch."})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/dashboard')
def dashboard():
    return send_from_directory('public', 'dashboard.html')


@app.route('/report/<slug>')
def report_page(slug):
    return send_from_directory('public', 'report.html')


@app.route('/')
def index():
    return send_from_directory('public', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)


def _cors_response(body):
    resp = app.make_response(body)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
