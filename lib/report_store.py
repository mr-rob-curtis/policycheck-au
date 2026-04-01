"""
Report storage: saves and retrieves scan reports by slug.
Uses Vercel Blob in production (needs BLOB_READ_WRITE_TOKEN),
falls back to local filesystem for dev.
"""
import json
import os
import re
import logging
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
BLOB_API = 'https://blob.vercel-storage.com'
LOCAL_DIR = Path(__file__).parent.parent / 'data' / 'reports'

# Only allow safe slug characters
SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9-]{0,80}[a-z0-9]$')


def slugify(text):
    """Create a URL-safe slug from text."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:80]


def _validate_slug(slug):
    if not slug or not SLUG_RE.match(slug):
        raise ValueError(f"Invalid slug: {slug}")


def save_report(slug, data):
    """Save report data by slug. Returns True on success."""
    _validate_slug(slug)

    if BLOB_TOKEN:
        try:
            resp = requests.put(
                f'{BLOB_API}/reports/{slug}.json',
                headers={
                    'Authorization': f'Bearer {BLOB_TOKEN}',
                    'x-content-type': 'application/json',
                    'x-api-version': '7',
                    'x-add-random-suffix': '0',
                },
                params={'access': 'public'},
                data=json.dumps(data),
                timeout=10,
            )
            resp.raise_for_status()
            logger.info(f"Saved report to Vercel Blob: {slug}")
            return True
        except Exception as e:
            logger.warning(f"Failed to save report to Vercel Blob: {e}")
            return False
    else:
        LOCAL_DIR.mkdir(parents=True, exist_ok=True)
        path = LOCAL_DIR / f'{slug}.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        logger.info(f"Saved report locally: {path}")
        return True


def get_report(slug):
    """Retrieve report data by slug. Returns dict or None."""
    _validate_slug(slug)

    if BLOB_TOKEN:
        try:
            resp = requests.get(
                BLOB_API,
                headers={
                    'Authorization': f'Bearer {BLOB_TOKEN}',
                    'x-api-version': '7',
                },
                params={'prefix': f'reports/{slug}.json', 'limit': '1'},
                timeout=10,
            )
            resp.raise_for_status()
            blobs = resp.json().get('blobs', [])
            if not blobs:
                return None
            data_resp = requests.get(blobs[0]['url'], timeout=10)
            data_resp.raise_for_status()
            return data_resp.json()
        except Exception as e:
            logger.warning(f"Failed to retrieve report from Vercel Blob: {e}")
            return None
    else:
        path = LOCAL_DIR / f'{slug}.json'
        if path.exists():
            with open(path, encoding='utf-8') as f:
                return json.load(f)
        return None
