"""
Australian Privacy Principles (APPs) Requirements and Compliance Criteria

This module defines the 13 APPs and the specific requirements that a privacy policy
must address for compliance. Used by the compliance engine to assess policy adequacy.

Reference: Privacy Act 1988 (Cth), as amended 1 July 2026
"""

from enum import Enum
from typing import Dict, List


class ComplianceStatus(Enum):
    """Compliance status classification"""
    COMPLIANT = "COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    NOT_ADDRESSED = "NOT_ADDRESSED"


class APPRequirements:
    """Detailed requirements for each Australian Privacy Principle"""

    APP_DEFINITIONS = {
        1: {
            "name": "Open and transparent management of personal information",
            "short_name": "Openness",
            "key_requirements": [
                "Clear, up-to-date privacy policy available to public",
                "Policy describes personal information handling practices",
                "Details about identity and contact info of privacy officer/contact",
                "Explains how to lodge complaints",
                "Explains how to request access or correction",
                "Available in accessible format",
                "Clearly sets out management practices",
            ],
            "critical_phrases": [
                "privacy policy",
                "personal information",
                "privacy officer",
                "privacy contact",
                "privacy complaint",
                "accessible format",
                "management practices",
            ],
            "sector_notes": {
                "real_estate": "Must disclose property agent's privacy practices and client money handling",
                "accountant": "Must disclose how client financial information is protected",
                "lawyer": "Must disclose client confidentiality practices and file security",
                "jeweller": "Must disclose insurance information and high-value item handling",
                "licensed_venue": "Must disclose security and CCTV practices",
                "car_dealer": "Must disclose trade-in inspection and valuation processes",
            }
        },

        2: {
            "name": "Anonymity and pseudonymity",
            "short_name": "Anonymity",
            "key_requirements": [
                "Identifies whether individuals can deal anonymously",
                "Identifies which dealings cannot be anonymous",
                "Explains why anonymity is not practicable for certain dealings",
            ],
            "critical_phrases": [
                "anonymous",
                "pseudonymous",
                "anonymity not practical",
                "without identifying",
                "identity required",
            ],
            "sector_notes": {
                "real_estate": "Cannot deal anonymously - property identification requires personal details",
                "accountant": "Cannot deal anonymously - tax compliance requires identification",
                "lawyer": "Cannot deal anonymously - professional relationship requires identity",
                "jeweller": "Cannot deal anonymously - anti-money laundering requires ID",
                "licensed_venue": "Cannot deal anonymously - RSA/gaming laws require identification",
                "car_dealer": "Cannot deal anonymously - registration requires identification",
            }
        },

        3: {
            "name": "Collection of solicited personal information",
            "short_name": "Solicited Collection",
            "key_requirements": [
                "Only collects information reasonably necessary for functions/activities",
                "Takes reasonable steps to ensure accuracy, up-to-dateness, completeness",
                "Privacy notice provided at/before collection (unless APP 5 applies)",
                "Explains collection purposes",
                "Identifies whether disclosure is required by law",
            ],
            "critical_phrases": [
                "collect",
                "collection",
                "necessary information",
                "accurate",
                "complete",
                "reasonably necessary",
                "collection notice",
            ],
            "sector_notes": {
                "real_estate": "Must limit collection to property details, financial info, and identification",
                "accountant": "Must limit collection to financial records needed for tax compliance",
                "lawyer": "Must limit collection to information needed for legal matter",
                "jeweller": "Must collect identification for AML compliance",
                "licensed_venue": "Must collect ID for age verification and gaming compliance",
                "car_dealer": "Must collect ID and financial info for registration and financing",
            }
        },

        4: {
            "name": "Dealing with unsolicited personal information",
            "short_name": "Unsolicited Collection",
            "key_requirements": [
                "Must determine whether information would have been collected if solicited",
                "Must check whether it is practicable to notify about this APP",
                "Must destroy or de-identify unsolicited information where practicable",
                "Privacy notice provided if information is retained",
            ],
            "critical_phrases": [
                "unsolicited",
                "received information",
                "destroy",
                "de-identify",
                "not requested",
            ],
            "sector_notes": {
                "real_estate": "May receive unsolicited property history or tenant information",
                "accountant": "May receive unsolicited financial documents",
                "lawyer": "May receive unsolicited case materials",
                "jeweller": "May receive unsolicited item appraisals",
                "licensed_venue": "May receive unsolicited guest information",
                "car_dealer": "May receive unsolicited vehicle history reports",
            }
        },

        5: {
            "name": "Notification of the collection of personal information",
            "short_name": "Collection Notice",
            "key_requirements": [
                "Collection notice provided at or before collection",
                "Notice identifies entity and privacy contact details",
                "Notice explains collection purposes",
                "Notice explains intended disclosures",
                "Notice explains whether disclosure to overseas entities is intended",
                "Notice explains how to access/correct information",
                "Notice explains how to lodge complaint",
                "Notice explains whether law requires collection",
                "Notice is in clear, plain language",
            ],
            "critical_phrases": [
                "collection notice",
                "why we collect",
                "how we use",
                "who we share with",
                "overseas",
                "access",
                "correct",
                "complaint",
            ],
            "sector_notes": {
                "real_estate": "Must explain use of information for property marketing, tenant screening",
                "accountant": "Must explain use of information for tax, audit, regulatory reporting",
                "lawyer": "Must explain confidentiality limitations for legal matters",
                "jeweller": "Must explain AML/AUSTRAC reporting obligations",
                "licensed_venue": "Must explain use for age verification and gaming/RSA compliance",
                "car_dealer": "Must explain use for registration, financing, recalls",
            }
        },

        6: {
            "name": "Use or disclosure of personal information",
            "short_name": "Use & Disclosure",
            "key_requirements": [
                "Only uses/discloses information for primary purpose or related secondary purpose",
                "Secondary purpose allowed if related and individual would reasonably expect",
                "Secondary purpose allowed if required by law or to lessen serious harm",
                "Must not use/disclose for direct marketing without consent (with exceptions)",
                "Notifies of use/disclosure of personal information if reasonably practicable",
            ],
            "critical_phrases": [
                "use",
                "disclosure",
                "secondary purpose",
                "related purpose",
                "direct marketing",
                "consent",
                "share",
                "third party",
            ],
            "sector_notes": {
                "real_estate": "Cannot share tenant info with other landlords without consent",
                "accountant": "Cannot disclose client info to other clients",
                "lawyer": "Cannot disclose case details beyond legal team",
                "jeweller": "Must disclose AML reporting to AUSTRAC",
                "licensed_venue": "Cannot share customer info with competing venues",
                "car_dealer": "Can share with lenders but not competitors",
            }
        },

        7: {
            "name": "Direct marketing",
            "short_name": "Marketing",
            "key_requirements": [
                "Provides honest, accurate information in marketing",
                "Identifies marketing material as marketing",
                "Provides clear unsubscribe mechanism",
                "Honors unsubscribe requests quickly",
                "Does not use government identifiers for marketing",
                "Respects privacy preferences (if known)",
            ],
            "critical_phrases": [
                "direct marketing",
                "marketing",
                "opt-out",
                "unsubscribe",
                "promotional",
                "marketing preferences",
                "email marketing",
                "sms marketing",
            ],
            "sector_notes": {
                "real_estate": "Must respect Do Not Contact lists from tenants",
                "accountant": "Must respect client preferences for service updates",
                "lawyer": "Must respect client preferences for case updates",
                "jeweller": "Must respect preferences for product announcements",
                "licensed_venue": "Must respect VIP/member marketing preferences",
                "car_dealer": "Must respect preferences for vehicle updates",
            }
        },

        8: {
            "name": "Cross-border disclosure of personal information",
            "short_name": "Overseas Disclosure",
            "key_requirements": [
                "Must not disclose to overseas entity unless reasonable steps taken",
                "Reasonable steps mean ensuring recipient bound by substantially similar obligations",
                "Must take reasonable steps to ensure compliance even overseas",
                "Some countries are declared adequate (EU, NZ, etc.)",
                "Must notify individual of overseas disclosure",
            ],
            "critical_phrases": [
                "overseas",
                "international",
                "cross-border",
                "international transfer",
                "foreign",
                "abroad",
                "outside Australia",
            ],
            "sector_notes": {
                "real_estate": "May disclose to international property networks - ensure contracts",
                "accountant": "May use overseas cloud services - ensure encryption/contracts",
                "lawyer": "May work with international co-counsel - ensure confidentiality",
                "jeweller": "May use overseas valuers - ensure confidentiality agreements",
                "licensed_venue": "May disclose to international gaming bodies - ensure standards",
                "car_dealer": "May use overseas parts suppliers - ensure data protection",
            }
        },

        9: {
            "name": "Adoption, use or disclosure of government related identifiers",
            "short_name": "Government ID",
            "key_requirements": [
                "Must not adopt government identifier as identifier for individuals",
                "Cannot use ABN, ACN, TFN, driver's license number, Medicare number as primary ID",
                "Can use in limited circumstances: required by law, or reasonable business practice",
                "Must take reasonable steps to protect government identifiers",
                "Cannot disclose government identifiers unless authorized",
            ],
            "critical_phrases": [
                "TFN",
                "tax file number",
                "ABN",
                "ACN",
                "driver's license",
                "Medicare",
                "government identifier",
                "unique identifier",
            ],
            "sector_notes": {
                "real_estate": "Cannot use TFN as tenant ID - use lease reference",
                "accountant": "Must collect TFN for tax compliance but cannot use as primary ID",
                "lawyer": "Can collect ID numbers but should use matter reference",
                "jeweller": "Must collect ID for AML but not use as primary identifier",
                "licensed_venue": "Can verify driver's license for RSA but use member number as ID",
                "car_dealer": "Can use driver's license for registration but not as primary ID",
            }
        },

        10: {
            "name": "Quality of personal information",
            "short_name": "Data Quality",
            "key_requirements": [
                "Personal information must be accurate, up-to-date, complete, relevant",
                "Must take reasonable steps to ensure accuracy at collection",
                "Must take reasonable steps to ensure completeness at use/disclosure",
                "Must ensure information is relevant to purposes",
                "Must not retain information longer than necessary",
            ],
            "critical_phrases": [
                "accurate",
                "up-to-date",
                "current",
                "complete",
                "relevant",
                "retention",
                "data quality",
            ],
            "sector_notes": {
                "real_estate": "Must update tenant contact information regularly",
                "accountant": "Must verify financial data accuracy for tax compliance",
                "lawyer": "Must maintain accurate case files and client contact details",
                "jeweller": "Must keep current valuations and item descriptions",
                "licensed_venue": "Must update member details and preferences",
                "car_dealer": "Must maintain accurate vehicle condition and pricing data",
            }
        },

        11: {
            "name": "Security of personal information",
            "short_name": "Security",
            "key_requirements": [
                "Must take reasonable steps to protect from misuse, loss, unauthorized access, modification",
                "Must take reasonable steps to destroy/de-identify when no longer needed",
                "Security measures appropriate to sensitivity of information",
                "Must address physical, technical, and organizational security",
                "Must have incident response/breach notification procedures",
            ],
            "critical_phrases": [
                "security",
                "encrypt",
                "protected",
                "access control",
                "password",
                "firewall",
                "breach",
                "data breach",
                "secure",
            ],
            "sector_notes": {
                "real_estate": "Must secure rental applications with personal financial info",
                "accountant": "Must encrypt tax files with sensitive financial data",
                "lawyer": "Must secure case files with privileged information",
                "jeweller": "Must protect insurance valuations and customer financial info",
                "licensed_venue": "Must secure customer data and gaming records",
                "car_dealer": "Must protect customer financing and personal details",
            }
        },

        12: {
            "name": "Access to personal information",
            "short_name": "Access Rights",
            "key_requirements": [
                "Individual can request access to personal information held",
                "Must provide access unless reasonable grounds to deny",
                "Must provide in requested form if practicable",
                "Can charge reasonable fees for access",
                "Must respond within 30 days (can extend to 90 days)",
                "Must explain reason for denial",
            ],
            "critical_phrases": [
                "access",
                "request",
                "subject access",
                "access request",
                "individual access",
                "30 days",
                "reasonable fee",
            ],
            "sector_notes": {
                "real_estate": "Must provide copies of rental applications and references",
                "accountant": "Must provide copies of tax documents prepared",
                "lawyer": "Must provide case files (subject to privilege)",
                "jeweller": "Must provide appraisal records and valuations",
                "licensed_venue": "Must provide customer records and transaction history",
                "car_dealer": "Must provide service records and warranty documents",
            }
        },

        13: {
            "name": "Correction of personal information",
            "short_name": "Correction",
            "key_requirements": [
                "Individual can request correction if information is inaccurate/out-of-date",
                "Must take reasonable steps to correct after request",
                "If correct information is not practicable, must append statement",
                "Cannot charge fees for correction",
                "Must respond within 30 days (can extend to 90 days)",
                "If deny correction, must explain reasons",
            ],
            "critical_phrases": [
                "correct",
                "correction",
                "update",
                "inaccurate",
                "amend",
                "amendment",
                "rectify",
            ],
            "sector_notes": {
                "real_estate": "Must correct tenant details, reference inaccuracies",
                "accountant": "Must correct client financial records, income details",
                "lawyer": "Must correct case details, client contact information",
                "jeweller": "Must correct item descriptions, valuation records",
                "licensed_venue": "Must correct member details, transaction records",
                "car_dealer": "Must correct vehicle details, service records",
            }
        },
    }

    # New requirement from December 2026
    ADM_TRANSPARENCY_REQUIREMENT = {
        "effective_date": "10 December 2026",
        "name": "Automated Decision-Making Transparency",
        "requirement": "Must disclose when automated decision-making is used that has legal effect or similar significant effect",
        "key_elements": [
            "Identify use of ADM",
            "Explain how ADM works",
            "Describe personal information used",
            "Explain significant effects",
            "Provide mechanism to request human review",
            "Provide mechanism to object",
        ],
        "examples": [
            "Credit scoring systems",
            "Automated rental application rejection",
            "Automated insurance claim decisions",
            "Algorithmic content filtering",
            "Automated pricing decisions",
        ],
        "critical_phrases": [
            "automated decision",
            "algorithm",
            "automated system",
            "machine learning",
            "automated scoring",
        ],
    }

    # Human-readable gap descriptions keyed by (app_number, phrase)
    GAP_DESCRIPTIONS = {
        # APP 1: Openness
        (1, "privacy policy"): "No clearly published privacy policy found",
        (1, "personal information"): "Policy doesn't explain what personal information is collected",
        (1, "privacy officer"): "No privacy officer or contact person identified",
        (1, "privacy contact"): "No privacy contact details provided",
        (1, "privacy complaint"): "No process for making a privacy complaint",
        (1, "accessible format"): "Policy not available in an accessible format",
        (1, "management practices"): "Policy doesn't describe information management practices",
        # APP 2: Anonymity
        (2, "anonymous"): "No statement on whether individuals can deal anonymously",
        (2, "pseudonymous"): "No option to use a pseudonym where practical",
        (2, "anonymity not practical"): "Doesn't explain why anonymity isn't practical (if applicable)",
        (2, "without identifying"): "No mention of dealing without identifying yourself",
        (2, "identity required"): "Doesn't explain when identity verification is required",
        # APP 3: Collection
        (3, "collect"): "No description of what information is collected",
        (3, "collection"): "No description of collection practices",
        (3, "necessary information"): "Doesn't explain why collection is reasonably necessary",
        (3, "accurate"): "No commitment to collecting accurate information",
        (3, "complete"): "No commitment to collecting complete information",
        (3, "reasonably necessary"): "Doesn't limit collection to what's reasonably necessary",
        (3, "collection notice"): "No collection notice provided at time of collection",
        # APP 4: Unsolicited information
        (4, "unsolicited"): "No process for handling unsolicited personal information",
        (4, "received information"): "No policy on information received without request",
        (4, "destroy"): "No commitment to destroy information that shouldn't have been collected",
        (4, "de-identify"): "No process for de-identifying unnecessary information",
        (4, "not requested"): "No policy on unrequested personal information",
        # APP 5: Collection notice
        (5, "collection notice"): "No collection notice at or before time of collection",
        (5, "why we collect"): "Doesn't explain why personal information is collected",
        (5, "how we use"): "Doesn't explain how personal information is used",
        (5, "who we share with"): "Doesn't disclose who information is shared with",
        (5, "overseas"): "Doesn't disclose if information is sent overseas",
        (5, "access"): "Doesn't explain how to request access to your information",
        (5, "correct"): "Doesn't explain how to request corrections",
        (5, "complaint"): "Doesn't explain how to make a complaint",
        # APP 6: Use & disclosure
        (6, "use"): "Doesn't explain how personal information is used",
        (6, "disclosure"): "Doesn't describe disclosure practices",
        (6, "secondary purpose"): "No statement on secondary use of information",
        (6, "related purpose"): "Doesn't explain related purposes for information use",
        (6, "direct marketing"): "No direct marketing disclosure",
        (6, "consent"): "No mention of consent for information use",
        (6, "share"): "Doesn't explain information sharing practices",
        (6, "third party"): "No disclosure of third-party information sharing",
        # APP 7: Direct marketing
        (7, "direct marketing"): "No direct marketing policy",
        (7, "marketing"): "No explanation of marketing practices",
        (7, "opt-out"): "No opt-out mechanism for marketing communications",
        (7, "unsubscribe"): "No unsubscribe option for marketing",
        (7, "promotional"): "No policy on promotional communications",
        (7, "marketing preferences"): "No way to manage marketing preferences",
        (7, "email marketing"): "No email marketing policy",
        (7, "sms marketing"): "No SMS marketing policy",
        # APP 8: Cross-border disclosure
        (8, "overseas"): "No disclosure about overseas data transfers",
        (8, "international"): "No policy on international data sharing",
        (8, "cross-border"): "No cross-border data transfer policy",
        (8, "international transfer"): "No international transfer safeguards described",
        (8, "foreign"): "No mention of foreign data recipients",
        (8, "abroad"): "No policy on sending data abroad",
        (8, "outside Australia"): "Doesn't disclose if data is sent outside Australia",
        # APP 9: Government identifiers
        (9, "TFN"): "No policy on handling Tax File Numbers",
        (9, "tax file number"): "No Tax File Number handling policy",
        (9, "ABN"): "No policy on business number handling",
        (9, "ACN"): "No policy on company number handling",
        (9, "driver's license"): "No policy on driver's licence data handling",
        (9, "Medicare"): "No policy on Medicare number handling",
        (9, "government identifier"): "No government identifier handling policy",
        (9, "unique identifier"): "No policy on unique identifiers",
        # APP 10: Data quality
        (10, "accurate"): "No commitment to keeping information accurate",
        (10, "up-to-date"): "No commitment to keeping information up-to-date",
        (10, "current"): "No process for keeping records current",
        (10, "complete"): "No commitment to data completeness",
        (10, "relevant"): "No commitment to keeping only relevant information",
        (10, "retention"): "No data retention or deletion policy",
        (10, "data quality"): "No data quality standards described",
        # APP 11: Security
        (11, "security"): "No description of security measures",
        (11, "encrypt"): "No mention of encryption for data protection",
        (11, "protected"): "No description of how data is protected",
        (11, "access control"): "No access control measures described",
        (11, "password"): "No password or authentication policies",
        (11, "firewall"): "No network security measures described",
        (11, "breach"): "No data breach response plan",
        (11, "data breach"): "No data breach notification process",
        (11, "secure"): "No commitment to secure data handling",
        # APP 12: Access
        (12, "access"): "No process for individuals to access their information",
        (12, "request"): "No access request mechanism described",
        (12, "subject access"): "No subject access request process",
        (12, "access request"): "No access request procedure explained",
        (12, "individual access"): "No individual access rights described",
        (12, "30 days"): "No response timeframe for access requests",
        (12, "reasonable fee"): "No information about access request fees",
        # APP 13: Correction
        (13, "correct"): "No process for correcting inaccurate information",
        (13, "correction"): "No correction request procedure",
        (13, "update"): "No process for updating personal information",
        (13, "inaccurate"): "No policy on handling inaccurate information",
        (13, "amend"): "No amendment process for records",
        (13, "amendment"): "No amendment procedure described",
        (13, "rectify"): "No rectification process available",
    }

    @classmethod
    def get_gap_description(cls, app_number: int, phrase: str) -> str:
        """Get human-readable gap description for a missing phrase"""
        return cls.GAP_DESCRIPTIONS.get(
            (app_number, phrase),
            f"Policy doesn't address: {phrase}"
        )

    @classmethod
    def get_app(cls, app_number: int) -> Dict:
        """Get requirements for a specific APP"""
        return cls.APP_DEFINITIONS.get(app_number, {})

    @classmethod
    def get_all_apps(cls) -> Dict:
        """Get all APP requirements"""
        return cls.APP_DEFINITIONS

    @classmethod
    def get_critical_phrases_for_app(cls, app_number: int) -> List[str]:
        """Get key phrases used for rule-based analysis of an APP"""
        app_def = cls.get_app(app_number)
        return app_def.get("critical_phrases", [])

    @classmethod
    def get_sector_note(cls, app_number: int, sector: str) -> str:
        """Get sector-specific note for an APP"""
        app_def = cls.get_app(app_number)
        sector_notes = app_def.get("sector_notes", {})
        sector_key = sector.lower().replace(" ", "_")
        return sector_notes.get(sector_key, "")


class ComplianceScoringRules:
    """Rules for calculating compliance scores"""

    # Score weights for different statuses
    # Partially compliant gets generous credit (they're making an effort)
    # Non-compliant gets some credit if the topic is at least mentioned
    STATUS_WEIGHTS = {
        ComplianceStatus.COMPLIANT: 100,
        ComplianceStatus.PARTIALLY_COMPLIANT: 65,
        ComplianceStatus.NON_COMPLIANT: 15,
        ComplianceStatus.NOT_ADDRESSED: 0,
    }

    # Priority mapping for gaps
    PRIORITY_LEVELS = {
        "CRITICAL": {
            "color": "red",
            "apps": [1, 5, 11],  # Openness, Collection Notice, Security
            "description": "Essential for basic Privacy Act compliance"
        },
        "HIGH": {
            "color": "orange",
            "apps": [3, 6, 12, 13],  # Collection, Use/Disclosure, Access, Correction
            "description": "Important for customer rights and management"
        },
        "MEDIUM": {
            "color": "yellow",
            "apps": [2, 4, 7, 8, 9],  # Anonymity, Unsolicited, Marketing, Overseas, Gov ID
            "description": "Important for specific circumstances"
        },
        "LOW": {
            "color": "green",
            "apps": [10],  # Data Quality
            "description": "Operational best practice"
        },
    }

    @classmethod
    def get_priority_for_app(cls, app_number: int) -> str:
        """Determine priority level for non-compliance with an APP"""
        for priority, config in cls.PRIORITY_LEVELS.items():
            if app_number in config["apps"]:
                return priority
        return "MEDIUM"

    @classmethod
    def calculate_overall_score(cls, app_statuses: Dict[int, ComplianceStatus]) -> int:
        """Calculate overall compliance score from individual APP statuses"""
        if not app_statuses:
            return 0

        total_weight = sum(
            cls.STATUS_WEIGHTS.get(status, 0)
            for status in app_statuses.values()
        )

        max_weight = len(app_statuses) * 100
        score = int((total_weight / max_weight) * 100) if max_weight > 0 else 0
        return score

    @classmethod
    def calculate_overall_status(cls, score: int) -> str:
        """Determine overall risk level from score.
        70+ = low risk (compliant), 40-69 = moderate risk, <40 = high risk.
        """
        if score >= 70:
            return ComplianceStatus.COMPLIANT.value
        elif score >= 40:
            return ComplianceStatus.PARTIALLY_COMPLIANT.value
        else:
            return ComplianceStatus.NON_COMPLIANT.value


class SectorSpecificGuidance:
    """Sector-specific compliance guidance"""

    SECTORS = {
        "real_estate_agencies": {
            "display_name": "Real Estate Agencies",
            "priority_apps": [1, 5, 11, 12],
            "highest_risk": [
                "Tenant/buyer personal information exposure",
                "Inadequate security of financial data",
                "Lack of transparency about information use",
                "Failure to provide access to files on request",
            ],
            "common_issues": [
                "Privacy policy focuses on 'our privacy' rather than tenant/buyer rights",
                "No clear process for access requests",
                "Inadequate security practices for sensitive financial information",
                "Marketing lists without consent",
            ],
        },
        "accountants_tax_agents": {
            "display_name": "Accountants & Tax Agents",
            "priority_apps": [1, 5, 11, 12, 9],
            "highest_risk": [
                "Tax file number misuse",
                "Client financial data breaches",
                "Overseas disclosure without safeguards",
                "Inadequate encryption of sensitive documents",
            ],
            "common_issues": [
                "Collecting TFN without privacy notice",
                "Using cloud storage without privacy agreements",
                "Lack of clear data retention policies",
                "No mechanism for client correction requests",
            ],
        },
        "lawyers_conveyancers": {
            "display_name": "Lawyers & Conveyancers",
            "priority_apps": [1, 5, 11, 12, 13],
            "highest_risk": [
                "Breach of client privilege through inadequate security",
                "Unauthorized disclosure of confidential information",
                "Inadequate security of financial transaction details",
                "Third-party information mishandling",
            ],
            "common_issues": [
                "Privacy policy unclear about attorney-client privilege limits",
                "No clear process for correcting file errors",
                "Inadequate security for digital matter files",
                "Unclear processes for handling opposing party information",
            ],
        },
        "jewellers_high_value_dealers": {
            "display_name": "Jewellers & High-Value Goods Dealers",
            "priority_apps": [1, 5, 9, 11, 12],
            "highest_risk": [
                "AML/AUSTRAC compliance failures",
                "Inadequate security of high-value appraisals",
                "Government identifier misuse",
                "Customer information exposure",
            ],
            "common_issues": [
                "AML requirements not mentioned in privacy policy",
                "Insufficient explanation of why ID collection required",
                "No disclosure of AUSTRAC reporting obligations",
                "Inadequate insurance and security procedures",
            ],
        },
        "licensed_venues": {
            "display_name": "Licensed Venues (Pubs, Clubs)",
            "priority_apps": [1, 5, 11, 12, 7],
            "highest_risk": [
                "Inadequate security of customer/member information",
                "Gaming machine data mishandling",
                "CCTV footage management issues",
                "Undisclosed marketing use of customer data",
            ],
            "common_issues": [
                "No privacy policy available at venue",
                "Inadequate explanation of CCTV use",
                "Gaming/RSA compliance obligations not disclosed",
                "Member data used for marketing without consent",
            ],
        },
        "car_dealers": {
            "display_name": "Car Dealers",
            "priority_apps": [1, 5, 11, 12, 6],
            "highest_risk": [
                "Customer financial information exposure",
                "Third-party financing information disclosure",
                "Inadequate security of registration details",
                "Recall information management",
            ],
            "common_issues": [
                "No clear privacy policy for finance customers",
                "Inadequate disclosure of third-party lender sharing",
                "No process for accessing purchase records",
                "Marketing to customers without consent",
            ],
        },
    }

    @classmethod
    def get_guidance(cls, sector: str) -> Dict:
        """Get sector-specific guidance"""
        sector_key = sector.lower().replace(" ", "_")
        return cls.SECTORS.get(sector_key, {})

    @classmethod
    def get_all_sectors(cls) -> List[str]:
        """Get list of all supported sectors"""
        return [info["display_name"] for info in cls.SECTORS.values()]
