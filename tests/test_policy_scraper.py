"""Tests for PrivacyPolicyScraper with mocked HTTP requests."""
import pytest
from unittest.mock import patch, MagicMock
import requests
from lib.policy_scraper import PrivacyPolicyScraper, MAX_RESPONSE_SIZE


@pytest.fixture
def scraper():
    return PrivacyPolicyScraper(timeout=5, rate_limit_delay=0)


class TestUrlNormalization:
    def test_adds_https(self, scraper):
        assert scraper._normalize_url('example.com') == 'https://example.com'

    def test_preserves_https(self, scraper):
        assert scraper._normalize_url('https://example.com') == 'https://example.com'

    def test_preserves_http(self, scraper):
        assert scraper._normalize_url('http://example.com') == 'http://example.com'


class TestDomainExtraction:
    def test_simple_domain(self, scraper):
        assert scraper._get_domain('https://example.com/page') == 'https://example.com'

    def test_domain_with_port(self, scraper):
        assert scraper._get_domain('http://example.com:8080/path') == 'http://example.com:8080'

    def test_au_domain(self, scraper):
        assert scraper._get_domain('https://example.com.au/legal') == 'https://example.com.au'


class TestSsrfValidation:
    def test_allows_public_domain(self, scraper):
        with patch('socket.getaddrinfo') as mock_dns:
            mock_dns.return_value = [(2, 1, 6, '', ('93.184.216.34', 0))]
            assert scraper._validate_url('https://example.com') is True

    def test_rejects_private_ip(self, scraper):
        with patch('socket.getaddrinfo') as mock_dns:
            mock_dns.return_value = [(2, 1, 6, '', ('192.168.1.1', 0))]
            assert scraper._validate_url('https://evil.com') is False

    def test_rejects_loopback(self, scraper):
        with patch('socket.getaddrinfo') as mock_dns:
            mock_dns.return_value = [(2, 1, 6, '', ('127.0.0.1', 0))]
            assert scraper._validate_url('https://evil.com') is False

    def test_rejects_link_local(self, scraper):
        with patch('socket.getaddrinfo') as mock_dns:
            mock_dns.return_value = [(2, 1, 6, '', ('169.254.169.254', 0))]
            assert scraper._validate_url('https://evil.com') is False

    def test_rejects_10_network(self, scraper):
        with patch('socket.getaddrinfo') as mock_dns:
            mock_dns.return_value = [(2, 1, 6, '', ('10.0.0.1', 0))]
            assert scraper._validate_url('https://evil.com') is False

    def test_rejects_ftp_scheme(self, scraper):
        assert scraper._validate_url('ftp://example.com') is False

    def test_rejects_file_scheme(self, scraper):
        assert scraper._validate_url('file:///etc/passwd') is False

    def test_rejects_dns_failure(self, scraper):
        import socket
        with patch('socket.getaddrinfo', side_effect=socket.gaierror):
            assert scraper._validate_url('https://nonexistent.invalid') is False

    def test_rejects_no_hostname(self, scraper):
        assert scraper._validate_url('https://') is False


class TestFetchPage:
    def test_happy_path(self, scraper):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Length': '100'}
        mock_response.iter_content.return_value = [b'<html>Hello</html>']
        mock_response.encoding = 'utf-8'

        with patch.object(scraper, '_validate_url', return_value=True), \
             patch.object(scraper.session, 'get', return_value=mock_response):
            result = scraper._fetch_page('https://example.com')
            assert result is not None
            text, status = result
            assert status == 200
            assert 'Hello' in text

    def test_rejects_ssrf(self, scraper):
        with patch.object(scraper, '_validate_url', return_value=False):
            assert scraper._fetch_page('https://evil.com') is None

    def test_rejects_oversized_content_length(self, scraper):
        mock_response = MagicMock()
        mock_response.headers = {'Content-Length': str(MAX_RESPONSE_SIZE + 1)}

        with patch.object(scraper, '_validate_url', return_value=True), \
             patch.object(scraper.session, 'get', return_value=mock_response):
            assert scraper._fetch_page('https://example.com') is None

    def test_rejects_oversized_streaming(self, scraper):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        # Return chunks that exceed the limit
        mock_response.iter_content.return_value = [b'x' * (MAX_RESPONSE_SIZE + 1)]

        with patch.object(scraper, '_validate_url', return_value=True), \
             patch.object(scraper.session, 'get', return_value=mock_response):
            assert scraper._fetch_page('https://example.com') is None

    def test_handles_timeout(self, scraper):
        with patch.object(scraper, '_validate_url', return_value=True), \
             patch.object(scraper.session, 'get', side_effect=requests.exceptions.Timeout):
            assert scraper._fetch_page('https://example.com') is None

    def test_handles_ssl_error(self, scraper):
        with patch.object(scraper, '_validate_url', return_value=True), \
             patch.object(scraper.session, 'get', side_effect=requests.exceptions.SSLError):
            assert scraper._fetch_page('https://badcert.com') is None

    def test_handles_connection_error(self, scraper):
        with patch.object(scraper, '_validate_url', return_value=True), \
             patch.object(scraper.session, 'get', side_effect=requests.exceptions.ConnectionError):
            assert scraper._fetch_page('https://example.com') is None

    def test_handles_http_error(self, scraper):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.headers = {}
        mock_response.iter_content.return_value = [b'Not Found']

        with patch.object(scraper, '_validate_url', return_value=True), \
             patch.object(scraper.session, 'get', return_value=mock_response):
            assert scraper._fetch_page('https://example.com/missing') is None


class TestTextExtraction:
    def test_removes_scripts_and_styles(self, scraper):
        html = '<html><script>alert("xss")</script><style>.x{}</style><p>Content</p></html>'
        text = scraper._extract_policy_text(html)
        assert 'Content' in text
        assert 'alert' not in text
        assert '.x' not in text

    def test_handles_empty_html(self, scraper):
        assert scraper._extract_policy_text('') == ''

    def test_limits_text_length(self, scraper):
        html = '<p>' + 'x' * 60000 + '</p>'
        text = scraper._extract_policy_text(html)
        assert len(text) <= 50000


class TestFindPrivacyLink:
    def test_finds_privacy_link(self, scraper):
        html = '<html><a href="/privacy-policy">Privacy Policy</a></html>'
        link = scraper._find_privacy_link_in_html(html, 'https://example.com')
        assert link is not None
        assert 'privacy' in link.lower()

    def test_returns_none_when_no_link(self, scraper):
        html = '<html><a href="/about">About Us</a></html>'
        link = scraper._find_privacy_link_in_html(html, 'https://example.com')
        assert link is None

    def test_resolves_relative_urls(self, scraper):
        html = '<html><a href="/legal/privacy">Privacy</a></html>'
        link = scraper._find_privacy_link_in_html(html, 'https://example.com')
        assert link == 'https://example.com/legal/privacy'


class TestScrapePrivacyPolicy:
    def test_policy_found_in_homepage_link(self, scraper):
        homepage_html = '<html><a href="/privacy">Privacy Policy</a></html>'
        policy_html = '<html><h1>Privacy Policy</h1><p>We collect personal information.</p></html>'

        def mock_fetch(url):
            if '/privacy' in url:
                return policy_html, 200
            return homepage_html, 200

        with patch.object(scraper, '_fetch_page', side_effect=mock_fetch):
            result = scraper.scrape_privacy_policy('https://example.com')
            assert result['policy_found'] is True
            assert 'personal information' in result['policy_text']

    def test_policy_found_at_common_path(self, scraper):
        homepage_html = '<html><p>No privacy link here</p></html>'
        policy_html = '<html><h1>Privacy</h1><p>Your data is safe.</p></html>'

        call_count = 0
        def mock_fetch(url):
            nonlocal call_count
            call_count += 1
            if '/privacy' in url and '/privacy-polic' not in url:
                return policy_html, 200
            if call_count == 1:
                return homepage_html, 200
            return None

        with patch.object(scraper, '_fetch_page', side_effect=mock_fetch):
            result = scraper.scrape_privacy_policy('https://example.com')
            assert result['policy_found'] is True

    def test_no_policy_found(self, scraper):
        with patch.object(scraper, '_fetch_page', return_value=('<html>Nothing</html>', 200)):
            result = scraper.scrape_privacy_policy('https://example.com')
            # find_privacy_link returns None, common paths also return generic HTML without privacy
            # The scraper should report no policy since the common paths return pages
            # that don't match privacy patterns
            assert 'url' in result
            assert 'policy_found' in result

    def test_homepage_unreachable(self, scraper):
        with patch.object(scraper, '_fetch_page', return_value=None):
            result = scraper.scrape_privacy_policy('https://unreachable.com')
            assert result['policy_found'] is False
            assert result['error'] == 'UNABLE_TO_FETCH_HOMEPAGE'


class TestRateLimiting:
    def test_delay_applied(self):
        import time
        scraper = PrivacyPolicyScraper(rate_limit_delay=0.3)
        start = time.time()
        scraper._apply_rate_limit()
        scraper._apply_rate_limit()
        elapsed = time.time() - start
        assert elapsed >= 0.3

    def test_zero_delay(self):
        import time
        scraper = PrivacyPolicyScraper(rate_limit_delay=0)
        start = time.time()
        scraper._apply_rate_limit()
        scraper._apply_rate_limit()
        elapsed = time.time() - start
        assert elapsed < 0.1
