"""
Sector-Specific Compliance Guidance for Australian Privacy Act

This module provides detailed, sector-specific recommendations for privacy policies.
Each sector has unique data handling requirements and regulatory obligations.

Reference: Privacy Act 1988 (Cth) and sector-specific regulations
"""

from typing import Dict, List, Tuple


class SectorSpecificLanguage:
    """Recommended privacy policy language templates for each sector"""

    # Real Estate Agencies
    REAL_ESTATE_LANGUAGE = {
        "about_us": """
We are a real estate agency licensed under [State] legislation. Our privacy practices are governed
by the Australian Privacy Act 1988 (Cth) and this Privacy Policy.

We collect personal information from property owners, tenants, buyers, sellers, and agents to:
- Manage property sales, lettings, and management
- Verify financial information and creditworthiness
- Conduct tenant/buyer screening
- Market properties and services
- Comply with legislation
""",

        "collection": """
We collect personal information that is reasonably necessary to:
- Process rental applications and sales
- Conduct due diligence checks
- Verify financial capacity
- Manage ongoing property management services
- Provide property marketing and communications

We collect information only at/before the point it is needed, and we explain what we're collecting
and why. For rental applications, this includes identification, financial references, and employment details.
""",

        "use": """
We use your personal information for:
- Primary purposes: The purpose you provided it for (rental application, sale, property management)
- Related secondary purposes: Marketing similar properties, providing improved service
- Legal requirements: Compliance with tenancy law, tax law, and AML regulations

We will not use your personal information for other purposes without your consent or unless required by law.
We respect that tenant and buyer information is sensitive and will not disclose it to other landlords
or agents without your consent.
""",

        "security": """
Personal information including rental applications and financial details are stored securely:
- Physical files kept in locked cabinets with restricted access
- Digital files encrypted and accessible only to authorized staff
- Access controls limiting staff to information needed for their role
- Secure disposal of information when no longer required
- No public display of photos/documents containing personal information
""",

        "access": """
You can request access to personal information we hold about you in your rental application,
reference checks, or transaction file. We aim to respond within 30 days. A reasonable
administration fee may apply. Contact our privacy contact at [details] to request access.
""",

        "correction": """
If you believe any personal information we hold is incorrect or out-of-date, you can request
correction. There is no fee for correction requests. We will make the correction or, if we
disagree that the information is inaccurate, add a note to your file explaining your position.
""",
    }

    # Accountants & Tax Agents
    ACCOUNTANT_LANGUAGE = {
        "about_us": """
We are a registered tax agent / BAS agent / accounting practice. Our privacy practices are
governed by the Australian Privacy Act 1988 (Cth) and this Privacy Policy.

We handle sensitive financial information from our clients and must protect it carefully. We also
must comply with tax law obligations and can only use client information for permitted purposes.
""",

        "collection": """
We collect personal information and business financial information that is reasonably necessary to:
- Prepare tax returns and financial statements
- Provide accounting and taxation advice
- Manage BAS/GST obligations
- Comply with Australian Taxation Office requirements
- Provide general business advice

This includes income details, financial statements, tax file numbers, employment information,
and other information you provide in relation to tax or financial matters. We explain why
we need each piece of information and keep it confidential.
""",

        "tax_file_number": """
We are authorized to collect and use your Tax File Number (TFN) for income tax purposes and to
identify you with the ATO. We cannot use your TFN as our unique identifier for you - we use your
client number instead. We protect your TFN carefully and only share it with the ATO when required.
""",

        "cloud_storage": """
Some of our files are stored using cloud-based systems. These services are bound by privacy
agreements that require them to protect your information. All cloud storage uses encryption
to prevent unauthorized access. You can request that files be kept locally if you prefer.
""",

        "use": """
We use your personal information for:
- Primary purposes: Providing taxation and accounting services
- Related secondary purposes: Providing related financial advice, superannuation advice
- Legal requirements: ATO compliance, accounting standards, legal obligations

We will not disclose your information to other accountants, bookkeepers, or advisors without
your consent except where we are legally required to do so or where we have a shared service arrangement
that is clearly disclosed to you.
""",

        "access": """
You can request access to any documentation or files we hold about you or your business.
We aim to respond within 30 days. A reasonable fee for copying may apply. Contact our
privacy contact at [details] to request access to your file.
""",

        "overseas": """
Some of our systems may be provided by overseas service providers, including cloud storage
companies. These providers are contractually required to comply with privacy principles
substantially similar to Australian law. All overseas transfer of information is secured
through encryption.
""",
    }

    # Lawyers & Conveyancers
    LAWYER_LANGUAGE = {
        "about_us": """
We are a law firm licensed to practice in [State]. Our privacy practices are governed by the
Australian Privacy Act 1988 (Cth), the Legal Profession Uniform Law, and this Privacy Policy.

Client confidentiality is fundamental to our practice. We maintain strict privacy and security
standards to protect legally privileged information.
""",

        "collection": """
We collect personal information needed to:
- Provide legal services and advice
- Conduct conveyancing transactions
- Manage litigation matters
- Comply with legal profession requirements
- Meet obligations under money laundering laws

This includes identification, financial information, property details, and information about
your legal matter. We explain what information we need and why before collecting it.
""",

        "confidentiality_limits": """
While we maintain strict confidentiality, there are limits:
- Legal professional privilege protects communications about your legal matter
- However, we must comply with legal obligations to disclose information
- Courts can order disclosure of our files
- We must comply with anti-money laundering laws
- We may be required to disclose information to other parties (courts, opposing counsel)

We will advise you of any required disclosure when we are legally permitted to do so.
""",

        "use": """
We use your personal information for:
- Primary purposes: Providing legal services you have requested
- Related secondary purposes: Managing related legal matters, providing improved service
- Legal requirements: Court orders, AML compliance, law society obligations

We do not disclose your information to other lawyers or law firms without your consent,
except where we are acting together on your matter or legally required to do so.
""",

        "third_party_information": """
If you provide us with information about third parties (witnesses, other parties to a matter),
we will protect that information with the same confidentiality standards we apply to your own
information. We will not disclose it except as necessary for your legal matter or as required by law.
""",

        "access": """
You can request access to your matter file and the information we hold about you. Access to
privileged communications may be limited. We aim to respond to access requests within 30 days.
A reasonable fee may apply. Contact our privacy contact at [details].
""",

        "security": """
Your matter files (both physical and digital) are stored securely:
- Physical files kept in locked storage with restricted access
- Digital files encrypted with access limited to involved lawyers/staff
- Secure deletion of files at matter conclusion or as legally permitted
- No disclosure of privileged information except to parties involved in the matter
""",
    }

    # Jewellers & High-Value Goods Dealers
    JEWELLER_LANGUAGE = {
        "about_us": """
We are a jeweller and high-value goods dealer. Our privacy practices are governed by the
Australian Privacy Act 1988 (Cth) and this Privacy Policy.

Due to the nature of our business (high-value items), we have additional regulatory requirements
including anti-money laundering obligations, which affect how we collect and use personal information.
""",

        "collection": """
We collect personal information needed to:
- Complete sales and valuations of high-value items
- Provide insurance valuations and documentation
- Comply with anti-money laundering legislation (AML Act)
- Manage warranty and service records
- Contact you about valuations or service

This includes your name, address, identification, and financial information. We explain why
we need identification before collecting it. AML laws require us to verify your identity
for transactions above certain values.
""",

        "aml_obligations": """
As a jeweller, we are required to comply with anti-money laundering laws. This means:
- We must verify customer identity for transactions above AUD 10,000
- We must keep records of high-value transactions
- We must report suspicious transactions to AUSTRAC (Australian Transaction Reports and
  Analysis Centre)

Your identification information is collected to comply with these legal requirements, not
for marketing purposes. We keep this information secure and separate from marketing information.
""",

        "use": """
We use your personal information for:
- Primary purposes: Completing the transaction or valuation you requested
- Related secondary purposes: Providing warranty service, insurance documentation
- Legal requirements: AML compliance, AUSTRAC reporting, law enforcement

We will not use your information for direct marketing without your consent. We respect that
information about high-value purchases is sensitive.
""",

        "access": """
You can request access to any appraisals, valuations, warranty records, or other information
we hold about you. We aim to respond within 30 days. A small fee for copying may apply.
Contact our privacy contact at [details].
""",

        "correction": """
If any valuation records or descriptions of your items are incorrect, you can request correction.
We will update our records or, if we disagree, add a note explaining your position.
""",
    }

    # Licensed Venues
    LICENSED_VENUE_LANGUAGE = {
        "about_us": """
We are a licensed venue [pub/club/bar] operating under [State] liquor licensing law. Our privacy
practices are governed by the Australian Privacy Act 1988 (Cth) and this Privacy Policy.

As a licensed venue, we have obligations under gaming and liquor laws that affect how we
collect and handle personal information.
""",

        "collection": """
We collect personal information from patrons and members to:
- Verify age for Responsible Service of Alcohol (RSA) compliance
- Manage gaming machine access and gaming compliance
- Provide member services and benefits
- Communicate with members
- Comply with licensing obligations

We collect identification details to verify age. We collect member details to provide
services and benefits to our regular patrons.
""",

        "rsa_gaming": """
For RSA compliance:
- We verify identification to confirm you are of legal drinking age
- We keep basic records to demonstrate compliance
- We may refuse service if you appear intoxicated
- Your identification information is kept confidential

For gaming compliance:
- We keep records of gaming machine use as required by gaming authorities
- We do not sell gaming data to marketing companies
- Self-exclusion information is kept strictly confidential
""",

        "cctv": """
We use CCTV systems for:
- Monitoring the licensed premises for safety and security
- Preventing theft and antisocial behavior
- Complying with licensing obligations

CCTV footage is retained for [X] days/weeks and then deleted. Footage is accessed only for
legitimate security purposes. Footage of individuals is not shared for purposes other than
security (e.g., not used for marketing or member identification).
""",

        "member_information": """
We collect information about our members including names, contact details, and preferences.
This information is used to provide member services and communicate about member events.

We will not market to members without their consent. We will not sell or share member
information with other venues or businesses without consent. If you wish to opt out of
member communications, contact us at [details].
""",

        "use": """
We use your personal information for:
- Primary purposes: Providing services, RSA/gaming compliance
- Related secondary purposes: Member communications (with consent), venue improvements
- Legal requirements: Licensing compliance, law enforcement

We will not use your information for direct marketing to other businesses without consent.
""",

        "access": """
You can request access to personal information we hold about you, including member records.
We aim to respond within 30 days. Contact our privacy contact at [details].
""",
    }

    # Car Dealers
    CAR_DEALER_LANGUAGE = {
        "about_us": """
We are a car dealer licensed under [State] legislation. Our privacy practices are governed by
the Australian Privacy Act 1988 (Cth) and this Privacy Policy.

As a car dealer, we handle sensitive customer information including identification, financial
information, and vehicle transaction details.
""",

        "collection": """
We collect personal information to:
- Process vehicle sales and trade-ins
- Arrange financing and insurance
- Conduct vehicle valuations and inspections
- Manage warranties and service
- Verify customer identification
- Comply with consumer protection and AML laws

This includes your name, address, identification, financial details, and vehicle information.
We explain what we're collecting and why at the point of collection.
""",

        "financing": """
When you purchase a vehicle through financing, we share your information with:
- Finance companies and banks to arrange the loan
- Insurance companies for mandatory vehicle insurance
- Statutory bodies for vehicle registration

We disclose to these parties the minimum information necessary to complete the transaction.
These parties are bound by privacy obligations. You authorize these disclosures as part of
accepting finance.
""",

        "use": """
We use your personal information for:
- Primary purposes: Vehicle sales, financing, registration
- Related secondary purposes: Service information, recall notifications, extended warranty offers
- Legal requirements: Consumer protection compliance, AML compliance

We will not use your information for marketing vehicles to other customers without your consent.
If you request not to be contacted about new vehicles, we will remove you from marketing lists.
""",

        "vehicle_history": """
When you trade in a vehicle or purchase a used vehicle, we obtain and store vehicle history reports.
These reports contain information about the vehicle's condition and history. This information is kept
confidential and used only for transaction purposes. We will not disclose it to other dealers
without authorization.
""",

        "access": """
You can request access to records we hold about your vehicle purchase, including finance
documents and service records. We aim to respond within 30 days. A reasonable fee for copying
may apply. Contact our privacy contact at [details].
""",

        "recall_information": """
We will contact you if a vehicle you have purchased from us is subject to a manufacturer recall.
This is a safety obligation. We use your contact details to notify you of important safety recalls.
""",
    }

    # Master language lookup
    SECTOR_LANGUAGE_TEMPLATES = {
        "real_estate_agencies": REAL_ESTATE_LANGUAGE,
        "accountants_tax_agents": ACCOUNTANT_LANGUAGE,
        "lawyers_conveyancers": LAWYER_LANGUAGE,
        "jewellers_high_value_dealers": JEWELLER_LANGUAGE,
        "licensed_venues": LICENSED_VENUE_LANGUAGE,
        "car_dealers": CAR_DEALER_LANGUAGE,
    }


class GAP_RECOMMENDATIONS:
    """Recommended language to fill specific gaps for each APP"""

    # APP 1: Openness
    OPENNESS_GAPS = {
        "no_privacy_policy": """
RECOMMENDED: "We are committed to protecting your privacy. This Privacy Policy sets out how
we collect, use, disclose, and manage personal information in accordance with the Australian
Privacy Act 1988 (Cth)."
""",
        "no_contact_details": """
RECOMMENDED: "If you have any questions about this Privacy Policy or our privacy practices,
please contact: [Name/Title], [Phone], [Email], [Physical Address]"
""",
        "no_complaint_process": """
RECOMMENDED: "If you believe we have breached the Australian Privacy Act or your privacy rights,
you can lodge a complaint with us. Complaints should be lodged with our Privacy Contact at
[contact details]. We aim to respond to complaints within 30 days. If you are not satisfied
with our response, you can lodge a complaint with the Office of the Australian Information
Commissioner (OAIC) at www.oaic.gov.au."
""",
        "unclear_practices": """
RECOMMENDED: "We collect personal information only when necessary. We explain what information
we collect and how we use it at the point of collection. Our staff are trained in privacy
principles. We review our privacy practices regularly to ensure they comply with the Privacy Act."
""",
    }

    # APP 2: Anonymity
    ANONYMITY_GAPS = {
        "no_anonymity_statement": """
RECOMMENDED FOR [SECTOR]: "In most cases, we cannot deal with you anonymously because [reason -
e.g., 'we must verify your identity for AML compliance' / 'the nature of our services requires
us to know who you are']. However, you can obtain general information about our services without
identifying yourself."
""",
    }

    # APP 3: Solicited Collection
    COLLECTION_GAPS = {
        "unclear_necessity": """
RECOMMENDED: "We collect personal information that is reasonably necessary for our functions.
We do not collect information you do not choose to provide. If you do not wish to provide
certain information, please advise us and we will discuss alternative arrangements."
""",
        "no_accuracy_measures": """
RECOMMENDED: "We take reasonable steps to ensure personal information is accurate, current,
and complete. We ask you to verify information we hold about you and to inform us of any
changes. If you believe any information is inaccurate, please contact us."
""",
    }

    # APP 5: Collection Notice
    COLLECTION_NOTICE_GAPS = {
        "incomplete_notice": """
RECOMMENDED: "At the time we collect your personal information, we will inform you of: (1) why
we are collecting it; (2) to whom we may disclose it; (3) whether disclosure overseas is
intended; (4) how to access or correct it; (5) how to lodge a complaint about privacy; and
(6) whether any information is legally required to be collected."
""",
    }

    # APP 6: Use & Disclosure
    USE_DISCLOSURE_GAPS = {
        "no_secondary_purpose_limit": """
RECOMMENDED: "We use personal information for the primary purpose you provided it for. We may
use it for related secondary purposes if you would reasonably expect this. We will not use
information for unrelated purposes without your consent, except where required by law."
""",
        "no_consent_process": """
RECOMMENDED: "Before we use your information for a secondary purpose, we will seek your consent
unless the purpose is closely related to the primary purpose or we are required by law to disclose.
You can withdraw consent at any time by contacting our Privacy Contact."
""",
        "unclear_third_party_sharing": """
RECOMMENDED: "We do not disclose personal information to third parties except: (1) to service
providers who help us provide services to you; (2) where you have consented; (3) where required
by law; or (4) where you would reasonably expect this. All service providers are bound by
confidentiality obligations."
""",
    }

    # APP 7: Marketing
    MARKETING_GAPS = {
        "no_opt_out": """
RECOMMENDED: "We may use your contact details to send you marketing communications about
products and services we think may interest you. You can opt out of marketing communications
at any time by contacting us at [contact details] or by clicking 'unsubscribe' on any marketing
email. We will stop marketing communications within 5 business days."
""",
        "no_unsubscribe": """
RECOMMENDED: "Each marketing email will include an 'unsubscribe' link. You can unsubscribe
immediately. We will honor unsubscribe requests within 5 business days."
""",
    }

    # APP 8: Overseas Disclosure
    OVERSEAS_GAPS = {
        "no_overseas_statement": """
RECOMMENDED: "We may disclose your information to overseas recipients [list countries/purposes if known].
Before we disclose, we take reasonable steps to ensure the recipient is bound by privacy
obligations substantially similar to Australian law. If you do not wish your information disclosed
overseas, please advise us."
""",
        "no_overseas_safeguards": """
RECOMMENDED: "When we disclose information overseas, we take steps to ensure it is protected.
This may include: (1) contractual privacy obligations; (2) encryption during transfer; (3)
verifying the recipient's privacy practices. Some countries have laws we consider substantially
similar to Australian privacy law (e.g., European Union, New Zealand)."
""",
    }

    # APP 9: Government ID
    GOVERNMENT_ID_GAPS = {
        "no_govt_id_statement": """
RECOMMENDED FOR [SECTOR]: "We collect [TFN/driver's license/other] to comply with [legal requirement -
e.g., 'tax law'/'AML requirements']. We do not use this as your unique identifier with us. We protect
this information securely and will not disclose it except as required by law."
""",
    }

    # APP 11: Security
    SECURITY_GAPS = {
        "no_security_measures": """
RECOMMENDED: "We take reasonable steps to protect personal information from misuse, loss,
unauthorized access, and modification. Our security measures include: (1) physical security
(locked storage); (2) access controls (passwords, system permissions); (3) encryption (of sensitive data);
(4) staff training (privacy obligations); and (5) regular security reviews."
""",
        "no_breach_response": """
RECOMMENDED: "If we become aware that personal information has been compromised, we will: (1) take steps
to secure the information; (2) investigate the breach; (3) notify individuals affected (unless the risk
is low); and (4) report to the Office of the Australian Information Commissioner where required."
""",
        "no_secure_deletion": """
RECOMMENDED: "When we no longer need personal information, we take reasonable steps to destroy it or
make it anonymous. This applies to both physical and digital information. Personal information is
retained only as long as necessary for our functions or as required by law."
""",
    }

    # APP 12: Access
    ACCESS_GAPS = {
        "no_access_statement": """
RECOMMENDED: "You have a right to request access to personal information we hold about you. To request
access, contact our Privacy Contact at [contact details]. We aim to respond within 30 days. We may
charge a reasonable administration fee. You do not have a right of access in limited circumstances
(e.g., legally privileged information)."
""",
    }

    # APP 13: Correction
    CORRECTION_GAPS = {
        "no_correction_statement": """
RECOMMENDED: "If you believe any personal information we hold is inaccurate, out-of-date, incomplete,
or misleading, you can request correction. There is no fee for correction requests. We will make the
correction or, if we believe the information is accurate, we will add a note to your file explaining
your position."
""",
    }

    # ADM Transparency
    ADM_GAPS = {
        "no_adm_disclosure": """
RECOMMENDED (from 10 December 2026): "Where we use automated decision-making systems that have a
legal effect or similarly significant effect on you, we will: (1) inform you that we are using an
automated system; (2) explain the personal information used; (3) describe the effect of the system;
(4) provide a mechanism to request human review; and (5) allow you to object to the decision."
""",
    }

    MASTER_GAPS = {
        "APP_1": OPENNESS_GAPS,
        "APP_2": ANONYMITY_GAPS,
        "APP_3": COLLECTION_GAPS,
        "APP_5": COLLECTION_NOTICE_GAPS,
        "APP_6": USE_DISCLOSURE_GAPS,
        "APP_7": MARKETING_GAPS,
        "APP_8": OVERSEAS_GAPS,
        "APP_9": GOVERNMENT_ID_GAPS,
        "APP_11": SECURITY_GAPS,
        "APP_12": ACCESS_GAPS,
        "APP_13": CORRECTION_GAPS,
        "ADM": ADM_GAPS,
    }

    @classmethod
    def get_gap_recommendation(cls, app_number: int, gap_type: str) -> str:
        """Get specific recommended language for a gap"""
        app_key = f"APP_{app_number}" if app_number <= 13 else "ADM"
        gaps = cls.MASTER_GAPS.get(app_key, {})
        return gaps.get(gap_type, "")


class SectorRiskAssessment:
    """Risk factors specific to each sector"""

    RISK_PROFILES = {
        "real_estate_agencies": {
            "data_sensitivity": "HIGH",
            "regulatory_complexity": "HIGH",
            "common_breaches": [
                "Sharing tenant details without consent",
                "Inadequate security of rental application information",
                "Marketing without consent",
                "Retaining information longer than necessary",
            ],
            "enforcement_history": "Moderate - multiple OAIC complaints about tenant privacy",
            "compliance_cost": "Low - mostly policy and process",
        },
        "accountants_tax_agents": {
            "data_sensitivity": "VERY_HIGH",
            "regulatory_complexity": "VERY_HIGH",
            "common_breaches": [
                "TFN misuse as identifier",
                "Cloud storage without adequate safeguards",
                "Overseas disclosure without contracts",
                "Inadequate security of financial records",
            ],
            "enforcement_history": "Active - OAIC has issued determinations",
            "compliance_cost": "Medium - requires secure systems and contracts",
        },
        "lawyers_conveyancers": {
            "data_sensitivity": "VERY_HIGH",
            "regulatory_complexity": "VERY_HIGH",
            "common_breaches": [
                "Inadequate security of privileged information",
                "Disclosure without appropriate authorization",
                "Inadequate retention/destruction practices",
                "Third-party information mishandling",
            ],
            "enforcement_history": "Active - professional bodies enforce standards",
            "compliance_cost": "Medium - secure systems required",
        },
        "jewellers_high_value_dealers": {
            "data_sensitivity": "HIGH",
            "regulatory_complexity": "VERY_HIGH",
            "common_breaches": [
                "AML/AUSTRAC obligation non-disclosure",
                "Government ID misuse",
                "Inadequate security of high-value item details",
                "Inadequate breach notification",
            ],
            "enforcement_history": "Active - AUSTRAC enforces AML obligations",
            "compliance_cost": "Medium - AML compliance required by law",
        },
        "licensed_venues": {
            "data_sensitivity": "MEDIUM",
            "regulatory_complexity": "HIGH",
            "common_breaches": [
                "No privacy policy available",
                "Inadequate CCTV disclosure",
                "Marketing without consent",
                "Gaming data mishandling",
            ],
            "enforcement_history": "Moderate - some OAIC complaints",
            "compliance_cost": "Low - mostly policy and signage",
        },
        "car_dealers": {
            "data_sensitivity": "HIGH",
            "regulatory_complexity": "MEDIUM",
            "common_breaches": [
                "Finance company disclosure not disclosed",
                "Marketing without consent",
                "Inadequate security of financial info",
                "Vehicle history information sharing",
            ],
            "enforcement_history": "Moderate - some consumer complaints",
            "compliance_cost": "Low to Medium - mostly policy and process",
        },
    }

    @classmethod
    def get_risk_profile(cls, sector: str) -> Dict:
        """Get risk profile for a sector"""
        sector_key = sector.lower().replace(" ", "_")
        return cls.RISK_PROFILES.get(sector_key, {})


# ADM Transparency Requirements (New from 10 December 2026)
ADM_TRANSPARENCY_DETAILS = {
    "effective_date": "10 December 2026",
    "applies_to": [
        "Decisions with legal effect (e.g., loan approval/rejection, credit scoring)",
        "Decisions with similarly significant effect (e.g., eligibility determination)",
        "Automated systems (including machine learning and AI)",
    ],
    "disclosure_requirements": [
        "Must inform individual automated decision-making is used",
        "Must explain how system works (in understandable terms)",
        "Must describe personal information used",
        "Must explain the significant effect on individual",
        "Must provide mechanism to request human review",
        "Must allow objection to decision",
    ],
    "sector_applications": {
        "car_dealers": "Finance eligibility decisions, pricing algorithms",
        "accountants": "Client suitability assessments, automated tax calculations",
        "real_estate": "Automated tenant scoring/screening",
        "jewellers": "Automated valuation systems, AML risk scoring",
        "licensed_venues": "Self-exclusion algorithms, automated member restrictions",
    },
}
