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
STATIC_DIR = Path(__file__).parent.parent / 'public' / 'reports'

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
        # Save to both data dir (gitignored) and public/reports (static, deployable)
        for d in [LOCAL_DIR, STATIC_DIR]:
            try:
                d.mkdir(parents=True, exist_ok=True)
                path = d / f'{slug}.json'
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                logger.info(f"Saved report: {path}")
            except Exception as e:
                logger.warning(f"Failed to save to {d}: {e}")
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
        for d in [LOCAL_DIR, STATIC_DIR]:
            path = d / f'{slug}.json'
            if path.exists():
                with open(path, encoding='utf-8') as f:
                    return json.load(f)
        return None


def save_draft(slug, draft_data):
    """Save a generated draft by slug. Returns True on success."""
    _validate_slug(slug)

    if BLOB_TOKEN:
        try:
            resp = requests.put(
                f'{BLOB_API}/drafts/{slug}.json',
                headers={
                    'Authorization': f'Bearer {BLOB_TOKEN}',
                    'x-content-type': 'application/json',
                    'x-api-version': '7',
                    'x-add-random-suffix': '0',
                },
                params={'access': 'public'},
                data=json.dumps(draft_data),
                timeout=10,
            )
            resp.raise_for_status()
            logger.info(f"Saved draft to Vercel Blob: {slug}")
            return True
        except Exception as e:
            logger.warning(f"Failed to save draft to Vercel Blob: {e}")
            return False
    else:
        draft_dir = Path(__file__).parent.parent / 'data' / 'drafts'
        try:
            draft_dir.mkdir(parents=True, exist_ok=True)
            path = draft_dir / f'{slug}.json'
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(draft_data, f, ensure_ascii=False)
            logger.info(f"Saved draft: {path}")
            return True
        except Exception as e:
            logger.warning(f"Failed to save draft: {e}")
            return False


def get_draft(slug):
    """Retrieve draft data by slug. Returns dict or None."""
    _validate_slug(slug)

    if BLOB_TOKEN:
        try:
            resp = requests.get(
                BLOB_API,
                headers={
                    'Authorization': f'Bearer {BLOB_TOKEN}',
                    'x-api-version': '7',
                },
                params={'prefix': f'drafts/{slug}.json', 'limit': '1'},
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
            logger.warning(f"Failed to retrieve draft from Vercel Blob: {e}")
            return None
    else:
        draft_dir = Path(__file__).parent.parent / 'data' / 'drafts'
        path = draft_dir / f'{slug}.json'
        if path.exists():
            with open(path, encoding='utf-8') as f:
                return json.load(f)
        return None


def mark_paid(slug):
    """Mark a report as paid. Updates existing report data with paid=True."""
    report = get_report(slug)
    if not report:
        return False
    report['paid'] = True
    return save_report(slug, report)
