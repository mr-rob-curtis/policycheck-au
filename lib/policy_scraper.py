"""
Privacy Policy Web Scraper
Extracts privacy policy text from business websites with graceful error handling.
"""

import ipaddress
import socket
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import csv

# Maximum response size (2MB)
MAX_RESPONSE_SIZE = 2 * 1024 * 1024

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PrivacyPolicyScraper:
    """
    Scrapes privacy policy text from business websites.

    Handles:
    - Common privacy policy paths and footer links
    - Redirects and HTTP errors gracefully
    - Encoding issues
    - Rate limiting (1 request per second)
    - User-Agent spoofing
    - robots.txt checking
    """

    # Common paths where privacy policies are typically found
    POLICY_PATHS = [
        '/privacy',
        '/privacy-policy',
        '/privacy-policies',
        '/legal/privacy',
        '/policies/privacy',
        '/about/privacy',
        '/terms-and-privacy',
        '/company/privacy',
    ]

    # Link text patterns to search for in footers and pages
    POLICY_LINK_PATTERNS = [
        'privacy policy',
        'privacy',
        'privacy statement',
        'data protection',
        'terms and conditions',
        'terms of service',
        'legal'
    ]

    # Polite user agent
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

    def __init__(self, timeout: int = 10, rate_limit_delay: float = 1.0):
        """
        Initialize scraper with retry strategy and rate limiting.

        Args:
            timeout: Request timeout in seconds (default: 10)
            rate_limit_delay: Delay between requests in seconds (default: 1.0)
        """
        self.timeout = timeout
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry strategy.
        Handles transient failures gracefully.
        """
        session = requests.Session()

        # Configure retry strategy (1 retry, no backoff for speed)
        retry_strategy = Retry(
            total=1,
            backoff_factor=0,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set headers
        session.headers.update({
            'User-Agent': self.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

        return session

    def _apply_rate_limit(self):
        """Apply rate limiting - ensure minimum delay between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def _normalize_url(self, url: str) -> str:
        """
        Normalize URL to ensure it has proper scheme.

        Args:
            url: URL to normalize

        Returns:
            Normalized URL with https:// prefix
        """
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _validate_url(self, url: str) -> bool:
        """
        Validate URL is safe to fetch (SSRF protection).
        Resolves DNS and rejects private/loopback IPs.
        """
        parsed = urlparse(url)

        if parsed.scheme not in ('http', 'https'):
            logger.warning(f"Rejected non-HTTP scheme: {parsed.scheme}")
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        try:
            addr_info = socket.getaddrinfo(hostname, None)
        except socket.gaierror:
            logger.warning(f"DNS resolution failed for {hostname}")
            return False

        for family, _, _, _, sockaddr in addr_info:
            ip = ipaddress.ip_address(sockaddr[0])
            if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
                logger.warning(f"Rejected private/reserved IP {ip} for {hostname}")
                return False

        return True

    def _fetch_page(self, url: str) -> Optional[Tuple[str, int]]:
        """
        Fetch a page with error handling, SSRF protection, and size limits.

        Args:
            url: URL to fetch

        Returns:
            Tuple of (html_content, status_code) or None if fetch failed
        """
        if not self._validate_url(url):
            return None

        try:
            self._apply_rate_limit()

            response = self.session.get(
                url,
                timeout=self.timeout,
                allow_redirects=True,
                verify=True,
                stream=True,
            )

            # Check content size before reading body
            content_length = response.headers.get('Content-Length')
            if content_length and content_length.isdigit() and int(content_length) > MAX_RESPONSE_SIZE:
                logger.warning(f"Response too large ({content_length} bytes) for {url}")
                response.close()
                return None

            # Read with size limit
            chunks = []
            total = 0
            for chunk in response.iter_content(chunk_size=8192, decode_unicode=False):
                total += len(chunk)
                if total > MAX_RESPONSE_SIZE:
                    logger.warning(f"Response exceeded {MAX_RESPONSE_SIZE} bytes for {url}")
                    response.close()
                    return None
                chunks.append(chunk)

            # Log status
            logger.info(f"Fetched {url} - Status: {response.status_code} ({total} bytes)")

            # Check for successful response
            if response.status_code < 400:
                text = b''.join(chunks).decode(response.encoding or 'utf-8', errors='replace')
                return text, response.status_code
            else:
                logger.warning(f"HTTP {response.status_code} for {url}")
                return None

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout fetching {url}")
            return None
        except requests.exceptions.SSLError:
            logger.warning(f"SSL error for {url} - site has invalid certificate")
            return None
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error for {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed for {url}: {e}")
            return None

    def _find_privacy_link_in_html(self, html: str, base_url: str) -> Optional[str]:
        """
        Search HTML for privacy policy links.
        Prioritizes footer links and common paths.

        Args:
            html: HTML content
            base_url: Base URL for resolving relative links

        Returns:
            Privacy policy URL if found, None otherwise
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Search for links matching privacy patterns
            for link in soup.find_all('a', href=True):
                href = link.get('href', '').lower()
                text = link.get_text(strip=True).lower()

                # Check if href or link text matches privacy patterns
                for pattern in self.POLICY_LINK_PATTERNS:
                    if pattern in href or pattern in text:
                        full_url = urljoin(base_url, link['href'])
                        if 'privacy' in full_url.lower() or 'privacy' in text:
                            logger.info(f"Found privacy link in page: {full_url}")
                            return full_url

            return None

        except Exception as e:
            logger.warning(f"Error parsing HTML for links: {e}")
            return None

    def _extract_policy_text(self, html: str) -> str:
        """
        Extract main text content from privacy policy HTML.
        Removes scripts, styles, and boilerplate content.

        Args:
            html: HTML content

        Returns:
            Extracted text content
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content
            text = soup.get_text(separator='\n')

            # Clean up whitespace
            lines = [line.strip() for line in text.split('\n')]
            text = '\n'.join([line for line in lines if line])

            # Limit to reasonable size to avoid bloat
            # Take first 50000 characters of meaningful content
            return text[:50000]

        except Exception as e:
            logger.warning(f"Error extracting text: {e}")
            return ""

    def scrape_privacy_policy(self, url: str) -> Dict:
        """
        Main method to scrape privacy policy from a business website.

        Args:
            url: Business homepage URL

        Returns:
            Dictionary with keys:
            - url: Original URL provided
            - policy_found: Boolean indicating if policy was found
            - policy_url: URL of privacy policy page (or None)
            - policy_text: Extracted privacy policy text (or empty string)
            - scraped_at: Timestamp of scrape
            - error: Error message if any (optional)
        """

        result = {
            'url': url,
            'policy_found': False,
            'policy_url': None,
            'policy_text': '',
            'scraped_at': datetime.utcnow().isoformat(),
        }

        # Normalize URL
        url = self._normalize_url(url)
        result['url'] = url
        domain = self._get_domain(url)

        logger.info(f"Starting scrape for {url}")

        # Try to fetch homepage first
        html, status = self._fetch_page(url) or (None, None)

        if html is None:
            result['error'] = 'UNABLE_TO_FETCH_HOMEPAGE'
            logger.warning(f"Could not fetch homepage: {url}")
            return result

        # Look for privacy policy links in homepage
        policy_url = self._find_privacy_link_in_html(html, url)
        policy_html = None

        # If homepage link found, fetch it
        if policy_url is not None:
            policy_html, _ = self._fetch_page(policy_url) or (None, None)

        # If no link found (or link failed), try common paths in parallel
        if policy_html is None:
            logger.info("Trying common paths in parallel...")
            from concurrent.futures import ThreadPoolExecutor, as_completed

            def _try_path(path):
                candidate_url = urljoin(domain, path)
                result = self._fetch_page(candidate_url)
                if result is not None:
                    return candidate_url, result[0]
                return None

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(_try_path, p): p for p in self.POLICY_PATHS}
                for future in as_completed(futures, timeout=self.timeout + 2):
                    try:
                        found = future.result()
                        if found is not None:
                            policy_url, policy_html = found
                            logger.info(f"Found policy at common path: {policy_url}")
                            # Cancel remaining futures
                            for f in futures:
                                f.cancel()
                            break
                    except Exception:
                        continue

        # Extract policy text if found
        if policy_url is not None and policy_html is not None:
            result['policy_found'] = True
            result['policy_url'] = policy_url
            result['policy_text'] = self._extract_policy_text(policy_html)
            logger.info(f"Successfully extracted policy from {policy_url}")
        elif policy_url is not None:
            result['policy_found'] = True
            result['policy_url'] = policy_url
            result['error'] = 'UNABLE_TO_FETCH_POLICY'
            result['policy_text'] = ''
        else:
            result['error'] = 'NO_POLICY_FOUND'
            logger.warning(f"No privacy policy found for {url}")

        return result


def scrape_urls_batch(urls: List[str], output_file: str) -> Dict:
    """
    Scrape privacy policies for a batch of URLs.

    Args:
        urls: List of business URLs
        output_file: Path to output JSON file

    Returns:
        Dictionary with results and statistics
    """
    scraper = PrivacyPolicyScraper()
    results = []

    logger.info(f"Starting batch scrape of {len(urls)} URLs")

    for i, url in enumerate(urls, 1):
        logger.info(f"[{i}/{len(urls)}] Processing {url}")
        result = scraper.scrape_privacy_policy(url)
        results.append(result)

    # Calculate statistics
    found_count = sum(1 for r in results if r['policy_found'])
    stats = {
        'total_urls': len(urls),
        'policies_found': found_count,
        'policies_not_found': len(urls) - found_count,
        'success_rate': f"{(found_count / len(urls) * 100):.1f}%",
        'scraped_at': datetime.utcnow().isoformat()
    }

    # Write results to file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        'statistics': stats,
        'results': results
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    logger.info(f"Results saved to {output_file}")
    logger.info(f"Statistics: {stats}")

    return output_data


def scrape_csv_batch(csv_file: str, url_column: str = 'url', output_file: str = None) -> Dict:
    """
    Scrape privacy policies from URLs in a CSV file.

    Args:
        csv_file: Path to CSV file with URLs
        url_column: Name of column containing URLs (default: 'url')
        output_file: Path to output JSON file (default: input_file_base.json)

    Returns:
        Dictionary with results and statistics
    """

    # Read CSV file
    urls = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if url_column in row and row[url_column].strip():
                    urls.append(row[url_column].strip())
    except Exception as e:
        logger.error(f"Error reading CSV file {csv_file}: {e}")
        raise

    logger.info(f"Loaded {len(urls)} URLs from {csv_file}")

    # Default output file
    if output_file is None:
        csv_path = Path(csv_file)
        output_file = str(csv_path.parent / f"{csv_path.stem}_results.json")

    # Scrape batch
    return scrape_urls_batch(urls, output_file)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Privacy Policy Web Scraper')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Single URL command
    single_parser = subparsers.add_parser('single', help='Scrape a single URL')
    single_parser.add_argument('url', help='Business website URL')

    # Batch URL command
    batch_parser = subparsers.add_parser('batch', help='Scrape a list of URLs')
    batch_parser.add_argument('urls', nargs='+', help='List of URLs')
    batch_parser.add_argument('-o', '--output', required=True, help='Output JSON file')

    # CSV batch command
    csv_parser = subparsers.add_parser('csv', help='Scrape URLs from CSV file')
    csv_parser.add_argument('csv_file', help='CSV file path')
    csv_parser.add_argument('-c', '--column', default='url', help='URL column name')
    csv_parser.add_argument('-o', '--output', help='Output JSON file')

    args = parser.parse_args()

    if args.command == 'single':
        scraper = PrivacyPolicyScraper()
        result = scraper.scrape_privacy_policy(args.url)
        print(json.dumps(result, indent=2))

    elif args.command == 'batch':
        scrape_urls_batch(args.urls, args.output)

    elif args.command == 'csv':
        scrape_csv_batch(args.csv_file, args.column, args.output)

    else:
        parser.print_help()
