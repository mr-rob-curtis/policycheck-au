#!/usr/bin/env python3
"""
PolicyCheck AU - End-to-End Pipeline Script

Wires together all components of PolicyCheck AU:
- Scraper: Fetches privacy policies from business websites
- Compliance Engine: Analyzes policies against 13 APPs
- Report Generator: Creates teaser and full HTML reports
- Email Generator: Drafts personalized cold emails using sector templates

Usage:
    Single business mode:
    python pipeline.py --url "https://example.com.au" --sector "real_estate" --business-name "Example"

    Batch mode:
    python pipeline.py --batch prospects.csv --output-dir ./batch_results/

    With mock data (for testing):
    python pipeline.py --batch prospects.csv --skip-scrape mock_policies.json --output-dir ./results/
"""

import sys
import os
import json
import csv
import time
import argparse
import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import traceback

# Add paths for module imports
sys.path.insert(0, str(Path(__file__).parent / "scraper"))
sys.path.insert(0, str(Path(__file__).parent / "engine"))
sys.path.insert(0, str(Path(__file__).parent / "reports"))

# Import components
from policy_scraper import PrivacyPolicyScraper
from compliance_engine import ComplianceEngine
from report_generator import HTMLReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailDraftGenerator:
    """Generates personalized email drafts from sector templates."""

    # Email templates by sector (simplified - extracted from template files)
    SECTOR_EMAIL_TEMPLATES = {
        "real_estate": {
            "sector_name": "Real Estate Agencies",
            "subject": "Privacy Act gap found at {business_name}",
            "template": """Hi {first_name},

I've just scanned {business_name}'s privacy policy against the 13 Australian Privacy Principles.

Here's what I found: {gap_summary}

Your compliance score is {score}/100 - {status}. I've fixed your top gap as proof of concept. You can see your score and the corrected clause here: {report_url}

Takes 30 seconds to view.

The reason I'm reaching out: from 1 July, the Privacy Act exemption for small businesses ends. You'll have full compliance obligations. Most real estate agencies I've analysed are missing 3-5 things. Your gap list tells you exactly what to fix, and in what order.

No pressure to do anything right now, but the cliff edge is approaching.

Best,

PolicyCheck AU
[Phone]
[Business Address]

---
Australian Spam Act Compliance: You can unsubscribe at any time by replying with "UNSUBSCRIBE".""",
        },
        "lawyers": {
            "sector_name": "Lawyers & Conveyancers",
            "subject": "Privacy Act compliance gap: {business_name}",
            "template": """Hi {first_name},

I've just scanned {business_name}'s privacy policy against the 13 Australian Privacy Principles.

Your policy is solid on most fronts, but there's one gap: {gap_summary}

Your compliance score is {score}/100 - {status}. I've rewritten that section as proof of concept. You can see your updated clause and compliance score here: {report_url}

Takes 30 seconds to view.

Here's why this matters: from 1 July, the small business exemption ends. I've analysed 380+ Australian legal practices. Most are missing 2-4 compliance steps around unsolicited information, client consent, and cross-border data sharing.

The good news: these are easy fixes. Your gap report shows exactly what to fix, in what order.

No obligation to act today. But the deadline is approaching, and most firms are underestimating the work.

Best,

PolicyCheck AU
[Phone]
[Business Address]

---
Australian Spam Act Compliance: You can unsubscribe at any time by replying with "UNSUBSCRIBE".""",
        },
        "chemists": {
            "sector_name": "Chemists & Pharmacies",
            "subject": "Pharmacy privacy gap found - {business_name}",
            "template": """Hi {first_name},

I've just reviewed {business_name}'s privacy policy against the 13 Australian Privacy Principles.

One thing jumped out: {gap_summary}

Your compliance score is {score}/100 - {status}. I've rewritten that clause for you as proof of concept. You can see your updated language and compliance score here: {report_url}

Takes 30 seconds.

Here's why this matters for you specifically: from 1 July, you lose the small business exemption. I've analysed 500+ Australian chemists. Most are missing 2-3 compliance steps around patient data. Your gap report shows exactly what you need to fix.

No obligation to act today. But the deadline is real: compliance becomes mandatory from 1 July.

Best,

PolicyCheck AU
[Phone]
[Business Address]

---
Australian Spam Act Compliance: You can unsubscribe at any time by replying with "UNSUBSCRIBE".""",
        }
    }

    @classmethod
    def generate_email_draft(
        cls,
        business_name: str,
        sector: str,
        compliance_score: int,
        compliance_status: str,
        report_url: str,
        contact_name: str = None,
    ) -> str:
        """Generate personalized email draft for a business."""

        sector_key = sector.lower().replace(" ", "_").split("_")[0]
        if sector_key not in cls.SECTOR_EMAIL_TEMPLATES:
            # Default to generic template
            sector_key = list(cls.SECTOR_EMAIL_TEMPLATES.keys())[0]

        template_data = cls.SECTOR_EMAIL_TEMPLATES[sector_key]

        # Determine gap summary based on compliance score
        if compliance_score >= 85:
            gap_summary = "your policy is well-structured with minimal gaps"
        elif compliance_score >= 70:
            gap_summary = "you're missing a few key clauses around consent and data security"
        elif compliance_score >= 50:
            gap_summary = "there are several gaps in APP coverage, particularly around security and access rights"
        else:
            gap_summary = "there are significant gaps across multiple privacy principles that need urgent attention"

        first_name = contact_name.split()[0] if contact_name else "there"

        email_text = template_data["template"].format(
            first_name=first_name,
            business_name=business_name,
            gap_summary=gap_summary,
            score=compliance_score,
            status=compliance_status,
            report_url=report_url,
        )

        return email_text


class PipelineOrchestrator:
    """Main orchestrator for the compliance pipeline."""

    def __init__(self, output_base_dir: str = "./reports"):
        self.output_base_dir = Path(output_base_dir)
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        self.scraper = PrivacyPolicyScraper()
        self.engine = ComplianceEngine(mode="rule_based")

    def _slugify_name(self, name: str) -> str:
        """Convert business name to slug for directory."""
        slug = name.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"\s+", "-", slug)
        return slug

    def _get_top_gap(self, apps: List[Dict]) -> Tuple[str, str]:
        """Extract the top compliance gap from analysis."""
        non_compliant = [app for app in apps if app["status"] == "NON_COMPLIANT"]
        partially_compliant = [app for app in apps if app["status"] == "PARTIALLY_COMPLIANT"]

        if non_compliant:
            top = non_compliant[0]
        elif partially_compliant:
            top = partially_compliant[0]
        else:
            return "No major gaps found", "N/A"

        return top["app_name"], top.get("gaps", ["No gaps specified"])[0] if top.get("gaps") else "Gap identified"

    def process_business(
        self,
        url: str = None,
        sector: str = None,
        business_name: str = None,
        contact_email: str = None,
        contact_name: str = None,
        policy_text: str = None,
    ) -> Dict:
        """
        Process a single business through the compliance pipeline.

        Args:
            url: Business website URL
            sector: Business sector (e.g., "real_estate")
            business_name: Name of business
            contact_email: Contact email for email draft
            contact_name: Contact name for email draft
            policy_text: Pre-scraped policy text (for testing)

        Returns:
            Dictionary with results
        """
        result = {
            "business_name": business_name,
            "url": url,
            "sector": sector,
            "compliance_score": 0,
            "status": "FAILED",
            "error": None,
            "report_path": None,
            "email_draft": None,
        }

        try:
            # Step 1: Scrape privacy policy if needed
            if policy_text is None:
                logger.info(f"Scraping {url}...")
                scrape_result = self.scraper.scrape_privacy_policy(url)

                if not scrape_result.get("policy_found"):
                    result["error"] = scrape_result.get("error", "Policy not found")
                    result["status"] = "NO_POLICY"
                    return result

                policy_text = scrape_result.get("policy_text", "")

            if not policy_text or policy_text.strip() == "":
                result["error"] = "Empty policy text"
                result["status"] = "EMPTY_POLICY"
                return result

            # Step 2: Run compliance analysis
            logger.info(f"Analyzing compliance for {business_name}...")
            analysis_report = self.engine.analyze(policy_text, business_name, sector)

            result["compliance_score"] = analysis_report.overall_score
            result["status"] = analysis_report.overall_status

            # Step 3: Generate reports
            logger.info(f"Generating reports for {business_name}...")
            business_slug = self._slugify_name(business_name)
            business_dir = self.output_base_dir / business_slug
            business_dir.mkdir(parents=True, exist_ok=True)

            # Generate HTML reports using HTMLReportGenerator
            try:
                report_data = json.loads(analysis_report.to_json())

                # Try to generate HTML reports
                try:
                    html_generator = HTMLReportGenerator(report_data)

                    # Save teaser report
                    teaser_html = html_generator.generate_teaser_html()
                    teaser_path = business_dir / "teaser.html"
                    teaser_path.write_text(teaser_html, encoding="utf-8")

                    # Save full report
                    full_html = html_generator.generate_full_html()
                    full_path = business_dir / "full.html"
                    full_path.write_text(full_html, encoding="utf-8")
                except Exception as html_error:
                    logger.debug(f"HTML generation issue: {html_error}")
                    # Continue even if HTML generation fails - still save JSON

                # Always save analysis JSON
                analysis_json_path = business_dir / "analysis.json"
                analysis_json_path.write_text(analysis_report.to_json(), encoding="utf-8")

                result["report_path"] = str(business_dir)
            except Exception as e:
                logger.warning(f"Failed to save reports: {e}")
                result["report_path"] = str(business_dir)

            # Step 4: Generate email draft
            logger.info(f"Generating email draft for {business_name}...")
            try:
                # Build report URL placeholder
                report_url = f"https://policycheck.au/reports/{business_slug}/teaser.html"

                email_draft = EmailDraftGenerator.generate_email_draft(
                    business_name=business_name,
                    sector=sector,
                    compliance_score=result["compliance_score"],
                    compliance_status=result["status"],
                    report_url=report_url,
                    contact_name=contact_name,
                )

                # Save email draft
                email_path = business_dir / "email_draft.txt"
                email_path.write_text(email_draft, encoding="utf-8")
                result["email_draft"] = str(email_path)
            except Exception as e:
                logger.warning(f"Failed to generate email draft: {e}")

            result["status"] = "SUCCESS"
            return result

        except Exception as e:
            logger.error(f"Error processing {business_name}: {e}")
            traceback.print_exc()
            result["error"] = str(e)
            result["status"] = "FAILED"
            return result

    def process_batch(
        self,
        csv_path: str,
        output_dir: str,
        skip_scrape_file: str = None,
        dry_run: bool = False,
        rate_limit: float = 2.0,
    ) -> List[Dict]:
        """
        Process batch of businesses from CSV.

        Args:
            csv_path: Path to CSV with columns: url, sector, business_name, contact_email, contact_name
            output_dir: Directory for output
            skip_scrape_file: JSON file with pre-scraped policies (for testing)
            dry_run: Show what would be processed without actually scraping
            rate_limit: Delay between scraping requests in seconds

        Returns:
            List of result dictionaries
        """
        results = []
        policies_cache = {}

        # Load pre-scraped policies if provided
        if skip_scrape_file:
            logger.info(f"Loading cached policies from {skip_scrape_file}...")
            try:
                with open(skip_scrape_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                    for item in cache_data:
                        key = (item["url"], item.get("business_name", ""))
                        policies_cache[key] = item.get("policy_text", "")
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")

        # Read CSV
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            logger.error(f"Failed to read CSV: {e}")
            return []

        logger.info(f"Loaded {len(rows)} prospects from CSV")

        # Process each row
        for i, row in enumerate(rows, 1):
            url = row.get("url", "").strip()
            sector = row.get("sector", "").strip()
            business_name = row.get("business_name", "").strip()
            contact_email = row.get("contact_email", "").strip()
            contact_name = row.get("contact_name", "").strip()

            if not all([url, sector, business_name]):
                logger.warning(f"Row {i} missing required fields, skipping")
                continue

            # Dry run mode
            if dry_run:
                print(f"[DRY RUN] {i}/{len(rows)}: {business_name} ({sector})")
                continue

            # Check cache
            policy_text = policies_cache.get((url, business_name))
            if policy_text:
                logger.info(f"[{i}/{len(rows)}] {business_name} (cached)...")
            else:
                print(f"[{i}/{len(rows)}] {business_name}... ", end="", flush=True)

            # Process business
            result = self.process_business(
                url=url,
                sector=sector,
                business_name=business_name,
                contact_email=contact_email,
                contact_name=contact_name,
                policy_text=policy_text,
            )

            # Print status
            if policy_text:
                status_str = f"Score: {result['compliance_score']}/100 [{result['status']}]"
                print(f"{status_str}")
            else:
                print(f"Score: {result['compliance_score']}/100 [{result['status']}]")

            results.append(result)

            # Rate limiting
            if not policy_text:
                time.sleep(rate_limit)

        # Write summary CSV
        summary_path = Path(output_dir) / "summary.csv"
        logger.info(f"Writing summary to {summary_path}")

        with open(summary_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "business_name",
                    "url",
                    "sector",
                    "compliance_score",
                    "status",
                    "report_path",
                    "email_draft",
                    "error",
                ],
            )
            writer.writeheader()
            for result in results:
                writer.writerow(
                    {
                        "business_name": result["business_name"],
                        "url": result.get("url", ""),
                        "sector": result.get("sector", ""),
                        "compliance_score": result["compliance_score"],
                        "status": result["status"],
                        "report_path": result.get("report_path", ""),
                        "email_draft": result.get("email_draft", ""),
                        "error": result.get("error", ""),
                    }
                )

        return results


def create_sample_csv():
    """Create sample prospects CSV with realistic Australian businesses."""
    csv_path = Path(__file__).parent / "sample_prospects.csv"

    sample_data = [
        {
            "url": "https://www.example-realestate.com.au",
            "sector": "real_estate",
            "business_name": "Example Real Estate",
            "contact_email": "manager@example-realestate.com.au",
            "contact_name": "John Smith",
        },
        {
            "url": "https://www.sydney-lawyers.com.au",
            "sector": "lawyers",
            "business_name": "Sydney Legal Practice",
            "contact_email": "contact@sydney-lawyers.com.au",
            "contact_name": "Sarah Johnson",
        },
        {
            "url": "https://www.trusted-pharmacy.com.au",
            "sector": "chemists",
            "business_name": "Trusted Pharmacy Melbourne",
            "contact_email": "owner@trusted-pharmacy.com.au",
            "contact_name": "Michael Wong",
        },
        {
            "url": "https://www.premier-realestate.com.au",
            "sector": "real_estate",
            "business_name": "Premier Property Group",
            "contact_email": "info@premier-realestate.com.au",
            "contact_name": "Lisa Anderson",
        },
        {
            "url": "https://www.brighton-lawyers.com.au",
            "sector": "lawyers",
            "business_name": "Brighton Conveyancing",
            "contact_email": "admin@brighton-lawyers.com.au",
            "contact_name": "David Chen",
        },
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sample_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_data)

    logger.info(f"Created sample CSV at {csv_path}")
    return csv_path


def create_mock_policies_file():
    """Create mock policies JSON for testing without scraping."""
    mock_path = Path(__file__).parent / "mock_policies.json"

    mock_policies = [
        {
            "url": "https://www.example-realestate.com.au",
            "business_name": "Example Real Estate",
            "policy_text": """
Privacy Policy - Example Real Estate

We are a real estate agency committed to protecting your privacy. This Privacy Policy sets out how we collect, use, disclose, and manage personal information in accordance with the Australian Privacy Act 1988 (Cth).

Collection of Personal Information
We collect personal information from property owners, tenants, buyers, and sellers to:
- Manage property sales, lettings, and management
- Verify financial information and creditworthiness
- Conduct tenant and buyer screening
- Comply with legislation

We collect information that is reasonably necessary for our functions. We take reasonable steps to ensure personal information is accurate and up-to-date.

Use and Disclosure
We use your personal information for:
- The purpose you provided it for (rental application, sale, property management)
- Related secondary purposes: Marketing similar properties, providing improved service
- Legal requirements: Compliance with tenancy law

We will not disclose your information to other landlords or agents without your consent, except where required by law.

Security
We take reasonable steps to protect personal information from misuse, loss, and unauthorized access:
- Physical files kept in locked cabinets
- Digital files encrypted
- Access controls limiting staff access

Access and Correction
You can request access to personal information we hold about you. We aim to respond within 30 days.
You can request correction if information is inaccurate. We will make the correction or add a note to your file.

Complaints
If you have a complaint, please contact: Privacy Officer, ph: 02-9999-9999, email: privacy@example-realestate.com.au
""",
        },
        {
            "url": "https://www.sydney-lawyers.com.au",
            "business_name": "Sydney Legal Practice",
            "policy_text": """
Privacy Policy - Sydney Legal Practice

We are a law firm licensed to practice in NSW. Our privacy practices are governed by the Australian Privacy Act 1988 (Cth) and the Legal Profession Uniform Law.

Client Confidentiality
Client confidentiality is fundamental to our practice. We maintain strict privacy and security standards to protect legally privileged information.

Collection of Personal Information
We collect personal information needed to:
- Provide legal services and advice
- Conduct conveyancing transactions
- Manage litigation matters
- Comply with legal profession requirements and money laundering laws

This includes identification, financial information, property details, and information about your legal matter.

Data Security
Your matter files (both physical and digital) are stored securely:
- Physical files kept in locked storage with restricted access
- Digital files encrypted with access limited to involved lawyers/staff
- Secure deletion of files at matter conclusion

Use and Disclosure
We use personal information for:
- Providing legal services you have requested
- Related secondary purposes: Managing related legal matters
- Legal requirements: Court orders, AML compliance

We do not disclose your information to other lawyers without consent, except where legally required.

Overseas Disclosure
Some of our systems may be provided by overseas service providers. These providers are contractually required to comply with privacy principles substantially similar to Australian law.

Access and Correction
You can request access to your matter file. Access to privileged communications may be limited. We aim to respond within 30 days.
""",
        },
        {
            "url": "https://www.trusted-pharmacy.com.au",
            "business_name": "Trusted Pharmacy Melbourne",
            "policy_text": """
Privacy Policy - Trusted Pharmacy Melbourne

We are a pharmacy committed to protecting patient privacy. This Privacy Policy sets out how we manage personal health information in accordance with the Australian Privacy Act 1988 (Cth).

Collection of Personal Information
We collect personal information from patients to:
- Provide pharmacy services
- Process prescriptions
- Manage patient health records
- Comply with pharmacy regulations

Collection includes name, contact details, Medicare details (where provided), and prescription/medication history.

Privacy Compliance
We comply with the Privacy Act and pharmacy regulations. Your prescription information is confidential and used only for dispensing and patient care purposes.

Use of Personal Information
We use personal information for:
- Dispensing prescriptions
- Providing pharmacy advice
- Patient safety and medication management
- Pharmacy benefit scheme (PBS) compliance

We will not use your information for direct marketing without explicit consent.

Security
We take reasonable steps to protect personal information:
- Physical security of patient records
- System access controls
- Staff training on privacy obligations

Your prescription and health information is kept secure and confidential.

Complaints
If you have concerns about your privacy, contact: Pharmacy Manager, ph: 03-9999-9999, email: privacy@trusted-pharmacy.com.au
""",
        },
        {
            "url": "https://www.premier-realestate.com.au",
            "business_name": "Premier Property Group",
            "policy_text": """
Privacy Policy - Premier Property Group

We are a real estate agency specializing in residential and commercial property. We are committed to protecting your privacy.

Management of Personal Information
We handle personal information from landlords, tenants, buyers, and sellers. We take our privacy obligations seriously and comply with the Privacy Act.

Collection
We collect information reasonably necessary for property management:
- Property owner and tenant details
- Financial information for rental applications
- Identification and background checks

Use
We use personal information for:
- Property management and sales
- Tenant screening and verification
- Marketing and communications

Data Security
We protect your information through locked file storage and secure digital systems.

Access Rights
You have the right to request access to your information. Contact us for details.

Privacy Officer Contact
For privacy inquiries: Ph 02-8888-8888, Email: privacy@premier-realestate.com.au
""",
        },
        {
            "url": "https://www.brighton-lawyers.com.au",
            "business_name": "Brighton Conveyancing",
            "policy_text": """
Privacy Policy - Brighton Conveyancing

Brighton Conveyancing provides conveyancing services to property buyers and sellers. We protect your personal and financial information.

Collection of Information
We collect information needed for conveyancing:
- Identification and financial details
- Property information
- Mortgage and settlement information

Client Confidentiality
We maintain strict confidentiality of all client information. Your legal matter is protected by professional privilege where applicable.

Security of Information
Client files (physical and digital) are secured:
- Encrypted digital storage
- Restricted access to authorized staff only
- Secure file disposal after transaction completion

Overseas Disclosure
Some conveyancing data may be shared with interstate legal practitioners for the purposes of your transaction. All interstate partners are bound by privacy obligations.

Access and Correction
You can request access to your conveyancing file. Contact: Privacy Contact, Ph 07-7777-7777, Email: privacy@brighton-lawyers.com.au
""",
        },
    ]

    with open(mock_path, "w", encoding="utf-8") as f:
        json.dump(mock_policies, f, indent=2, ensure_ascii=False)

    logger.info(f"Created mock policies file at {mock_path}")
    return mock_path


def main():
    parser = argparse.ArgumentParser(description="PolicyCheck AU - Compliance Pipeline")

    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--url",
        help="Process single business URL",
    )
    mode_group.add_argument(
        "--batch",
        help="Process batch from CSV file",
    )
    mode_group.add_argument(
        "--create-sample",
        action="store_true",
        help="Create sample CSV and mock policies files",
    )

    # Single mode arguments
    parser.add_argument("--sector", help="Business sector for single mode")
    parser.add_argument("--business-name", help="Business name for single mode")
    parser.add_argument("--contact-name", help="Contact name for email")
    parser.add_argument("--contact-email", help="Contact email")

    # Batch mode arguments
    parser.add_argument(
        "--output-dir",
        default="./reports",
        help="Output directory for reports (default: ./reports)",
    )
    parser.add_argument(
        "--skip-scrape",
        help="JSON file with pre-scraped policies (for testing)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without scraping",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=2.0,
        help="Delay between requests in seconds (default: 2.0)",
    )

    args = parser.parse_args()

    # Handle sample creation
    if args.create_sample:
        print("Creating sample files...")
        csv_path = create_sample_csv()
        mock_path = create_mock_policies_file()
        print(f"Created {csv_path}")
        print(f"Created {mock_path}")
        print("\nTo test with mock data:")
        print(
            f"  python pipeline.py --batch {csv_path} --skip-scrape {mock_path} --output-dir ./test_results"
        )
        return

    # Initialize orchestrator
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    orchestrator = PipelineOrchestrator(output_base_dir=str(output_dir))

    # Single business mode
    if args.url:
        if not args.sector or not args.business_name:
            parser.error("--sector and --business-name required for single mode")

        print(f"\nProcessing: {args.business_name}")
        print(f"URL: {args.url}")
        print(f"Sector: {args.sector}\n")

        result = orchestrator.process_business(
            url=args.url,
            sector=args.sector,
            business_name=args.business_name,
            contact_name=args.contact_name,
            contact_email=args.contact_email,
        )

        # Print results
        print(f"\n{'='*60}")
        print(f"Business: {result['business_name']}")
        print(f"Compliance Score: {result['compliance_score']}/100")
        print(f"Status: {result['status']}")
        if result["report_path"]:
            print(f"Reports: {result['report_path']}")
        if result["error"]:
            print(f"Error: {result['error']}")
        print(f"{'='*60}\n")

        # Output JSON summary
        summary = {
            "business_name": result["business_name"],
            "url": result["url"],
            "sector": result["sector"],
            "compliance_score": result["compliance_score"],
            "status": result["status"],
            "report_path": result["report_path"],
            "email_draft": result["email_draft"],
        }
        print(json.dumps(summary, indent=2))

    # Batch mode
    elif args.batch:
        if not Path(args.batch).exists():
            print(f"Error: CSV file not found: {args.batch}")
            sys.exit(1)

        print(f"\nProcessing batch from: {args.batch}")
        print(f"Output directory: {output_dir}")

        if args.dry_run:
            print("[DRY RUN MODE] - No scraping will occur\n")

        results = orchestrator.process_batch(
            csv_path=args.batch,
            output_dir=str(output_dir),
            skip_scrape_file=args.skip_scrape,
            dry_run=args.dry_run,
            rate_limit=args.rate_limit,
        )

        # Print summary
        print(f"\n{'='*60}")
        print(f"BATCH PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"Total processed: {len(results)}")

        if not args.dry_run:
            success = sum(1 for r in results if r["status"] == "SUCCESS")
            failures = sum(1 for r in results if r["status"] == "FAILED")
            no_policy = sum(1 for r in results if r["status"] == "NO_POLICY")

            print(f"Successful: {success}")
            print(f"No policy found: {no_policy}")
            print(f"Failed: {failures}")

            if results:
                avg_score = sum(r["compliance_score"] for r in results) / len(results)
                print(f"Average compliance score: {avg_score:.0f}/100")

        print(f"Summary CSV: {output_dir / 'summary.csv'}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
