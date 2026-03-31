"""
Test suite for Privacy Policy Scraper
Tests against well-known Australian business websites
"""

import unittest
import json
import os
from pathlib import Path
from policy_scraper import PrivacyPolicyScraper, scrape_urls_batch


class TestPrivacyPolicyScraper(unittest.TestCase):
    """Test cases for PrivacyPolicyScraper class"""

    @classmethod
    def setUpClass(cls):
        """Set up test scraper instance"""
        cls.scraper = PrivacyPolicyScraper()

    def test_url_normalization(self):
        """Test URL normalization adds https:// when missing"""
        test_cases = [
            ('example.com', 'https://example.com'),
            ('https://example.com', 'https://example.com'),
            ('http://example.com', 'http://example.com'),
        ]

        for input_url, expected in test_cases:
            result = self.scraper._normalize_url(input_url)
            self.assertEqual(result, expected, f"Failed for {input_url}")

    def test_domain_extraction(self):
        """Test domain extraction from URLs"""
        test_cases = [
            ('https://example.com/privacy', 'https://example.com'),
            ('http://subdomain.example.com:8080/path', 'http://subdomain.example.com:8080'),
            ('https://example.com.au/legal/privacy', 'https://example.com.au'),
        ]

        for input_url, expected in test_cases:
            result = self.scraper._get_domain(input_url)
            self.assertEqual(result, expected, f"Failed for {input_url}")

    def test_text_extraction(self):
        """Test text extraction from HTML"""
        html = """
        <html>
            <head><title>Test</title><script>alert('test');</script></head>
            <body>
                <h1>Privacy Policy</h1>
                <p>This is a test privacy policy.</p>
                <style>.test { color: red; }</style>
                <p>More content here.</p>
            </body>
        </html>
        """

        text = self.scraper._extract_policy_text(html)

        # Check that text contains expected content
        self.assertIn('Privacy Policy', text)
        self.assertIn('test privacy policy', text)
        self.assertIn('More content here', text)

        # Check that scripts and styles are removed
        self.assertNotIn('alert', text)
        self.assertNotIn('.test { color', text)

    def test_single_url_scrape_cba(self):
        """Test scraping privacy policy from Commonwealth Bank Australia"""
        url = 'https://www.commbank.com.au'

        result = self.scraper.scrape_privacy_policy(url)

        # Verify result structure
        self.assertIn('url', result)
        self.assertIn('policy_found', result)
        self.assertIn('policy_url', result)
        self.assertIn('policy_text', result)
        self.assertIn('scraped_at', result)

        # Verify it found a policy
        self.assertTrue(result['policy_found'], "Should find privacy policy for CBA")

        # Verify policy URL is set
        self.assertIsNotNone(result['policy_url'])
        self.assertTrue(result['policy_url'].startswith('http'))

        # Verify policy text was extracted
        self.assertGreater(len(result['policy_text']), 0, "Should have extracted policy text")

        # Verify text contains privacy-related content
        text_lower = result['policy_text'].lower()
        self.assertTrue(
            'privacy' in text_lower or 'personal' in text_lower or 'data' in text_lower,
            "Policy text should contain privacy-related terms"
        )

        print(f"\nCBA Test - Policy URL: {result['policy_url']}")
        print(f"CBA Test - Text length: {len(result['policy_text'])} characters")

    def test_single_url_scrape_westpac(self):
        """Test scraping privacy policy from Westpac Banking"""
        url = 'https://www.westpac.com.au'

        result = self.scraper.scrape_privacy_policy(url)

        # Verify result structure
        self.assertIn('url', result)
        self.assertIn('policy_found', result)

        # Verify it found a policy
        self.assertTrue(result['policy_found'], "Should find privacy policy for Westpac")

        # Verify policy URL is set
        self.assertIsNotNone(result['policy_url'])

        # Verify policy text was extracted
        self.assertGreater(len(result['policy_text']), 0, "Should have extracted policy text")

        print(f"\nWestpac Test - Policy URL: {result['policy_url']}")
        print(f"Westpac Test - Text length: {len(result['policy_text'])} characters")

    def test_single_url_scrape_nab(self):
        """Test scraping privacy policy from National Australia Bank"""
        url = 'https://www.nab.com.au'

        result = self.scraper.scrape_privacy_policy(url)

        # Verify result structure
        self.assertIn('url', result)
        self.assertIn('policy_found', result)

        # Verify it found a policy
        self.assertTrue(result['policy_found'], "Should find privacy policy for NAB")

        # Verify policy URL is set
        self.assertIsNotNone(result['policy_url'])

        # Verify policy text was extracted
        self.assertGreater(len(result['policy_text']), 0, "Should have extracted policy text")

        print(f"\nNAB Test - Policy URL: {result['policy_url']}")
        print(f"NAB Test - Text length: {len(result['policy_text'])} characters")

    def test_batch_scrape(self):
        """Test batch scraping with multiple URLs"""
        urls = [
            'https://www.commbank.com.au',
            'https://www.westpac.com.au',
            'https://www.nab.com.au',
        ]

        output_file = '/tmp/test_batch_results.json'

        results = scrape_urls_batch(urls, output_file)

        # Verify structure
        self.assertIn('statistics', results)
        self.assertIn('results', results)

        stats = results['statistics']
        self.assertEqual(stats['total_urls'], 3)
        self.assertIn('policies_found', stats)
        self.assertIn('success_rate', stats)

        # Verify all results were returned
        self.assertEqual(len(results['results']), 3)

        # Verify results have required fields
        for result in results['results']:
            self.assertIn('url', result)
            self.assertIn('policy_found', result)
            self.assertIn('policy_url', result)
            self.assertIn('policy_text', result)
            self.assertIn('scraped_at', result)

        # Check output file was created
        self.assertTrue(os.path.exists(output_file))

        # Verify JSON is valid
        with open(output_file, 'r') as f:
            loaded_data = json.load(f)
            self.assertIn('statistics', loaded_data)
            self.assertIn('results', loaded_data)

        print(f"\nBatch Test Results:")
        print(f"  Total URLs: {stats['total_urls']}")
        print(f"  Policies Found: {stats['policies_found']}")
        print(f"  Success Rate: {stats['success_rate']}")
        print(f"  Output: {output_file}")

        # Clean up
        if os.path.exists(output_file):
            os.remove(output_file)


class TestScraperEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    @classmethod
    def setUpClass(cls):
        """Set up test scraper instance"""
        cls.scraper = PrivacyPolicyScraper()

    def test_invalid_url_handling(self):
        """Test handling of invalid URLs"""
        result = self.scraper.scrape_privacy_policy('https://invalid-domain-12345-xyz.example.com')

        # Should have error field
        self.assertIn('error', result)

        # Policy should not be found
        self.assertFalse(result['policy_found'])

        print(f"\nInvalid URL Test - Error: {result.get('error')}")

    def test_rate_limiting(self):
        """Test that rate limiting delays are applied"""
        import time

        scraper = PrivacyPolicyScraper(rate_limit_delay=0.5)

        start = time.time()

        # Make two requests (this will be slow due to rate limiting)
        scraper._apply_rate_limit()
        scraper._apply_rate_limit()

        elapsed = time.time() - start

        # Should have taken at least 0.5 seconds
        self.assertGreaterEqual(elapsed, 0.5)

        print(f"\nRate Limiting Test - Elapsed time: {elapsed:.2f}s")


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPrivacyPolicyScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestScraperEdgeCases))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    print("=" * 70)
    print("Privacy Policy Scraper - Test Suite")
    print("=" * 70)
    print("\nRunning tests against live Australian business websites...")
    print("Note: This may take several minutes due to rate limiting.\n")

    result = run_tests()

    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("All tests passed successfully!")
    else:
        print(f"Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 70)
