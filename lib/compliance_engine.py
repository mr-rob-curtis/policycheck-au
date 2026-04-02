"""
Australian Privacy Act Compliance Analysis Engine

Analyzes privacy policies against the 13 Australian Privacy Principles (APPs)
and produces a structured compliance report using rule-based keyword/pattern matching.

Usage:
    engine = ComplianceEngine()
    report = engine.analyze(policy_text, business_name, sector)
"""

import json
import re
from datetime import datetime
from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

from lib.app_requirements import (
    APPRequirements,
    ComplianceStatus,
    ComplianceScoringRules,
    SectorSpecificGuidance,
)
from lib.sector_notes import (
    SectorSpecificLanguage,
    GAP_RECOMMENDATIONS,
    SectorRiskAssessment,
    ADM_TRANSPARENCY_DETAILS,
)


@dataclass
class APPAnalysis:
    """Result of analyzing a single APP"""
    app_number: int
    app_name: str
    status: str  # COMPLIANT, PARTIALLY_COMPLIANT, NON_COMPLIANT, NOT_ADDRESSED
    findings: List[str]
    gaps: List[str]
    recommended_language: str
    priority: str
    confidence: float  # 0.0 to 1.0


@dataclass
class ADMAnalysis:
    """Result of analyzing ADM transparency requirement"""
    uses_adm: str  # YES, NO, UNKNOWN
    adm_disclosed: bool
    examples_found: List[str]
    recommendation: str


@dataclass
class ComplianceReport:
    """Complete compliance analysis report"""
    business_name: str
    sector: str
    analysis_date: str
    analysis_mode: str
    overall_score: int
    overall_status: str
    apps: List[Dict]
    adm_check: Dict
    summary: Dict
    sector_risk_profile: Dict
    next_steps: List[str]

    def to_json(self, indent: int = 2) -> str:
        """Convert report to JSON"""
        data = {
            "business_name": self.business_name,
            "sector": self.sector,
            "analysis_date": self.analysis_date,
            "analysis_mode": self.analysis_mode,
            "overall_score": self.overall_score,
            "overall_status": self.overall_status,
            "apps": self.apps,
            "adm_check": self.adm_check,
            "summary": self.summary,
            "sector_risk_profile": self.sector_risk_profile,
            "next_steps": self.next_steps,
        }
        return json.dumps(data, indent=indent)


class ComplianceEngine:
    """
    Core compliance analysis engine for Australian Privacy Act

    Analyzes privacy policies against 13 APPs and produces structured reports.
    Uses rule-based keyword/pattern matching for fast screening.
    """

    def __init__(self):
        self.app_requirements = APPRequirements()
        self.scoring_rules = ComplianceScoringRules()

    # ========================================================================================
    # PUBLIC API
    # ========================================================================================

    def analyze(
        self,
        policy_text: Optional[str],
        business_name: str,
        sector: str,
    ) -> ComplianceReport:
        """
        Analyze a privacy policy for compliance with Australian Privacy Act

        Args:
            policy_text: The privacy policy text to analyze (or None if no policy exists)
            business_name: Name of the business
            sector: Business sector (e.g., "Real Estate Agencies")

        Returns:
            ComplianceReport with detailed analysis
        """
        # Handle missing policy
        if not policy_text or policy_text.strip() == "":
            return self._analyze_missing_policy(business_name, sector)

        return self._analyze_rule_based(policy_text, business_name, sector)

    # ========================================================================================
    # RULE-BASED MODE - Keyword/Pattern Analysis
    # ========================================================================================

    def _analyze_rule_based(
        self,
        policy_text: str,
        business_name: str,
        sector: str,
    ) -> ComplianceReport:
        """
        Analyze using rule-based keyword/pattern matching
        Fast screening that checks for presence of key phrases with semantic expansion
        Applies scoring floor for policies that address multiple APPs substantively
        """
        app_analyses = {}
        app_statuses = {}

        for app_num in range(1, 14):
            analysis = self._analyze_app_rule_based(app_num, policy_text, sector)
            app_analyses[app_num] = analysis
            app_statuses[app_num] = ComplianceStatus[analysis.status]

        # Analyze ADM requirement
        adm_analysis = self._analyze_adm(policy_text, sector)

        # Calculate scores with potential floor application
        overall_score = self.scoring_rules.calculate_overall_score(app_statuses)

        # Apply scoring floor if policy exists and covers multiple APPs
        overall_score = self._apply_scoring_floor(
            overall_score, policy_text, app_statuses
        )

        overall_status = self.scoring_rules.calculate_overall_status(overall_score)

        # Build apps list
        apps_list = [
            {
                "app_number": analysis.app_number,
                "app_name": analysis.app_name,
                "status": analysis.status,
                "findings": analysis.findings,
                "gaps": analysis.gaps,
                "recommendations": [analysis.recommended_language] if analysis.recommended_language else [],
                "recommended_language": analysis.recommended_language,
                "priority": analysis.priority,
            }
            for analysis in app_analyses.values()
        ]

        # Get sector guidance
        sector_guidance = SectorSpecificGuidance.get_guidance(sector)
        sector_risk = SectorRiskAssessment.get_risk_profile(sector)

        # Build summary
        summary = {
            "compliant_count": sum(
                1 for s in app_statuses.values()
                if s == ComplianceStatus.COMPLIANT
            ),
            "partial_count": sum(
                1 for s in app_statuses.values()
                if s == ComplianceStatus.PARTIALLY_COMPLIANT
            ),
            "non_compliant_count": sum(
                1 for s in app_statuses.values()
                if s == ComplianceStatus.NON_COMPLIANT
            ),
            "not_addressed_count": sum(
                1 for s in app_statuses.values()
                if s == ComplianceStatus.NOT_ADDRESSED
            ),
        }

        # Generate next steps
        next_steps = self._generate_next_steps(
            overall_status, sector, app_statuses
        )

        return ComplianceReport(
            business_name=business_name,
            sector=sector,
            analysis_date=datetime.now().isoformat(),
            analysis_mode="rule_based",
            overall_score=overall_score,
            overall_status=overall_status,
            apps=apps_list,
            adm_check=asdict(adm_analysis),
            summary=summary,
            sector_risk_profile=sector_risk,
            next_steps=next_steps,
        )

    def _analyze_app_rule_based(
        self,
        app_num: int,
        policy_text: str,
        sector: str,
    ) -> APPAnalysis:
        """
        Analyze a single APP using rule-based keyword matching with semantic expansion.
        Includes partial credit logic for policies that address the spirit of an APP
        without using exact keywords.
        """
        app_def = self.app_requirements.get_app(app_num)
        app_name = app_def.get("name", "Unknown APP")

        # Get expanded keyword phrases (includes synonyms/alternatives)
        expanded_phrases = self._get_expanded_phrases_for_app(app_num)
        original_phrases = app_def.get("critical_phrases", [])

        # Count matches in policy using expanded phrases
        found_phrases = self._find_phrases_in_text(policy_text, expanded_phrases)
        phrase_match_count = len(found_phrases)
        expected_phrase_count = len(original_phrases)

        # Calculate coverage percentage based on expanded phrases
        # This gives partial credit if ANY expanded keyword is found for a requirement
        coverage_percentage = self._calculate_coverage_percentage(
            app_num, policy_text, found_phrases, expanded_phrases
        )

        # Determine status based on coverage with new thresholds
        if expected_phrase_count == 0:
            status = ComplianceStatus.NOT_ADDRESSED
            findings = ["No requirements defined for this APP"]
            gaps = []
        elif coverage_percentage >= 75:
            status = ComplianceStatus.COMPLIANT
            findings = [f"Found {phrase_match_count} key indicators addressing {int(coverage_percentage)}% of requirements"]
            gaps = []
        elif coverage_percentage >= 25:
            # PARTIALLY_COMPLIANT: covers 25-75% of requirements
            status = ComplianceStatus.PARTIALLY_COMPLIANT
            findings = [f"Found {phrase_match_count} key indicators addressing {int(coverage_percentage)}% of requirements"]
            gaps = self._identify_gaps(app_num, found_phrases, original_phrases)
        else:
            # Only NON_COMPLIANT if coverage is <25% AND no topic indicators found
            topic_detected = self._detect_topic_presence(app_num, policy_text)
            if topic_detected:
                status = ComplianceStatus.PARTIALLY_COMPLIANT
                findings = [f"Policy addresses topic of APP {app_num} but lacks specific requirement details ({int(coverage_percentage)}% coverage)"]
                gaps = self._identify_gaps(app_num, found_phrases, original_phrases)
            else:
                status = ComplianceStatus.NON_COMPLIANT
                findings = [f"Only {phrase_match_count} of {expected_phrase_count} key requirements found ({int(coverage_percentage)}% coverage)"]
                gaps = self._identify_gaps(app_num, found_phrases, original_phrases)

        # Get recommended language
        gap_type = self._determine_gap_type(app_num, gaps)
        recommended = GAP_RECOMMENDATIONS.get_gap_recommendation(app_num, gap_type)
        if not recommended:
            # Fallback recommendation
            recommended = f"Review APP {app_num} ({app_name}) requirements and update policy to address identified gaps."

        # Determine priority
        priority = self.scoring_rules.get_priority_for_app(app_num)

        # Calculate confidence (based on coverage percentage)
        confidence = min(1.0, max(0.0, coverage_percentage / 100.0))

        return APPAnalysis(
            app_number=app_num,
            app_name=app_name,
            status=status.value,
            findings=findings,
            gaps=gaps,
            recommended_language=recommended,
            priority=priority,
            confidence=confidence,
        )

    # ========================================================================================
    # MISSING POLICY ANALYSIS
    # ========================================================================================

    def _analyze_missing_policy(
        self,
        business_name: str,
        sector: str,
    ) -> ComplianceReport:
        """
        Analyze case where business has no privacy policy
        ALL APPs will be NOT_ADDRESSED
        """
        app_analyses = {}
        app_statuses = {}

        for app_num in range(1, 14):
            app_def = self.app_requirements.get_app(app_num)
            app_name = app_def.get("name", "Unknown")

            analysis = APPAnalysis(
                app_number=app_num,
                app_name=app_name,
                status=ComplianceStatus.NOT_ADDRESSED.value,
                findings=["No privacy policy exists"],
                gaps=["Entire APP not addressed"],
                recommended_language=GAP_RECOMMENDATIONS.get_gap_recommendation(
                    app_num, "no_privacy_policy"
                ),
                priority=self.scoring_rules.get_priority_for_app(app_num),
                confidence=1.0,
            )

            app_analyses[app_num] = analysis
            app_statuses[app_num] = ComplianceStatus.NOT_ADDRESSED

        # ADM check (also not addressed)
        adm_analysis = ADMAnalysis(
            uses_adm="UNKNOWN",
            adm_disclosed=False,
            examples_found=[],
            recommendation="A privacy policy must be created before ADM transparency can be assessed.",
        )

        # Build summary
        summary = {
            "compliant_count": 0,
            "partial_count": 0,
            "non_compliant_count": 0,
            "not_addressed_count": 13,
        }

        # Build apps list
        apps_list = [
            {
                "app_number": analysis.app_number,
                "app_name": analysis.app_name,
                "status": analysis.status,
                "findings": analysis.findings,
                "gaps": analysis.gaps,
                "recommendations": [analysis.recommended_language] if analysis.recommended_language else [],
                "recommended_language": analysis.recommended_language,
                "priority": analysis.priority,
            }
            for analysis in app_analyses.values()
        ]

        # Get sector guidance
        sector_risk = SectorRiskAssessment.get_risk_profile(sector)

        # Generate next steps
        next_steps = [
            "CRITICAL: Create a comprehensive privacy policy addressing all 13 APPs",
            "Refer to sector-specific guidance for priority requirements",
            "Include all required privacy notices and contact information",
            "Establish access and correction request procedures",
            "Implement security measures for personal information",
        ]

        return ComplianceReport(
            business_name=business_name,
            sector=sector,
            analysis_date=datetime.now().isoformat(),
            analysis_mode="rule_based",
            overall_score=0,
            overall_status=ComplianceStatus.NON_COMPLIANT.value,
            apps=apps_list,
            adm_check=asdict(adm_analysis),
            summary=summary,
            sector_risk_profile=sector_risk,
            next_steps=next_steps,
        )

    # ========================================================================================
    # ADM TRANSPARENCY ANALYSIS (NEW from 10 December 2026)
    # ========================================================================================

    def _analyze_adm(self, policy_text: str, sector: str) -> ADMAnalysis:
        """
        Analyze whether policy discloses automated decision-making
        New requirement from 10 December 2026
        """
        critical_phrases = [
            "automated decision",
            "automated decision-making",
            "adm",
            "algorithm",
            "algorithmic",
            "machine learning",
            "automated scoring",
            "automated system",
            "automated process",
            "human review",
            "object to",
        ]

        found_phrases = self._find_phrases_in_text(policy_text, critical_phrases)

        if len(found_phrases) == 0:
            uses_adm = "UNKNOWN"
            adm_disclosed = False
            examples = []
            recommendation = (
                "From 10 December 2026, if you use automated decision-making with legal or "
                "similarly significant effect (e.g., credit scoring, eligibility decisions), "
                "you must disclose: (1) the use of automated systems; (2) how they work; "
                "(3) personal information used; (4) the significant effect; (5) mechanism to "
                "request human review; and (6) right to object."
            )
        elif len(found_phrases) >= 3:
            uses_adm = "YES"
            adm_disclosed = True
            examples = found_phrases
            recommendation = "Your policy adequately discloses automated decision-making. Ensure you have processes for human review requests."
        else:
            uses_adm = "YES"
            adm_disclosed = False
            examples = found_phrases
            recommendation = (
                "Your policy mentions automated systems but does not fully comply with the "
                "10 December 2026 ADM transparency requirement. Add explicit disclosure of: "
                "how the system works, personal information used, significant effects, and "
                "mechanisms for human review and objection."
            )

        return ADMAnalysis(
            uses_adm=uses_adm,
            adm_disclosed=adm_disclosed,
            examples_found=examples,
            recommendation=recommendation,
        )

    # ========================================================================================
    # HELPER METHODS - SEMANTIC EXPANSION & PARTIAL CREDIT
    # ========================================================================================

    def _get_expanded_phrases_for_app(self, app_num: int) -> List[str]:
        """
        Get expanded keyword phrases for an APP including synonyms and alternative phrasings.
        This addresses Fix 2: Semantic Keyword Expansion
        """
        base_phrases = self.app_requirements.get_critical_phrases_for_app(app_num)

        # Semantic expansion mappings - add synonyms and alternative phrasings
        expansions = {
            1: [  # Open and transparent management
                "privacy contact", "data protection", "responsible for privacy",
                "privacy matters", "contact us about privacy", "privacy inquiries",
                "privacy issues", "how we handle", "our practices",
            ],
            2: [  # Anonymity and pseudonymity
                "without identifying", "not required to identify", "do not need to provide your name",
                "can remain anonymous", "identity not required", "provide your details",
            ],
            3: [  # Solicited collection
                "information we collect", "collect and retain", "gather", "what we collect",
                "collection of information",
            ],
            5: [  # Collection notice
                "why we collect", "how we use", "who we share with", "purposes of collection",
                "reasons for collecting",
            ],
            6: [  # Use or disclosure
                "share", "third party", "service providers", "software providers",
                "disclose information", "provide to", "send to",
            ],
            7: [  # Marketing
                "unsubscribe", "stop receiving", "remove from", "marketing preferences",
                "communication preferences", "email preferences", "opt out of",
            ],
            8: [  # Overseas disclosure
                "stored across the world", "international", "third party providers",
                "outside Australia", "other countries", "software providers",
                "cloud", "overseas", "global", "world",
            ],
            10: [  # Quality of personal information
                "reasonable steps", "ensure", "keep current", "up to date",
                "verify", "accurate information", "current information",
                "diligence",
            ],
            11: [  # Security
                "securely", "protected", "safeguard", "diligence", "safely",
                "take all diligence", "measures", "protection", "security measures",
            ],
            12: [  # Access request
                "request a copy", "obtain your information", "provide you with",
                "your right to access", "access to your", "get a copy",
                "give you access",
            ],
            13: [  # Correction
                "update your information", "amend", "change your details",
                "correct information", "put right", "inaccurate",
            ],
        }

        expanded = list(base_phrases)
        if app_num in expansions:
            expanded.extend(expansions[app_num])

        return expanded

    def _calculate_coverage_percentage(
        self,
        app_num: int,
        policy_text: str,
        found_phrases: List[str],
        expanded_phrases: List[str],
    ) -> float:
        """
        Calculate coverage percentage for an APP.
        Uses partial credit logic: if ANY expanded keyword is found for a requirement,
        that requirement gets credit.
        This addresses Fix 3: Partial Credit Logic
        """
        original_phrases = self.app_requirements.get_critical_phrases_for_app(app_num)

        if not original_phrases:
            return 100.0  # No requirements = full coverage

        # Group expanded phrases by their original requirement
        # For simplicity, we count how many original phrases have at least one match
        phrases_with_matches = set()

        for original_phrase in original_phrases:
            # Check if any expanded variant of this phrase was found
            for found_phrase in found_phrases:
                # Simple heuristic: if found phrase is similar to original or contains key words
                if self._is_related_to_phrase(found_phrase, original_phrase):
                    phrases_with_matches.add(original_phrase)
                    break

        # Calculate percentage: (matched requirements / total requirements) * 100
        coverage = (len(phrases_with_matches) / len(original_phrases)) * 100

        # Boost if we found any matches at all (minimum 25% for topic presence)
        if len(found_phrases) > 0 and coverage < 25:
            coverage = 25

        return coverage

    def _is_related_to_phrase(self, found_phrase: str, original_phrase: str) -> bool:
        """Check if a found phrase is related to the original requirement phrase"""
        found_lower = found_phrase.lower()
        original_lower = original_phrase.lower()

        # Exact match
        if found_lower == original_lower:
            return True

        # Substring match (found contains original or vice versa)
        if original_lower in found_lower or found_lower in original_lower:
            return True

        # Check if they share significant keywords
        found_words = set(found_lower.split())
        original_words = set(original_lower.split())

        # If more than 30% of words overlap, consider related
        if found_words & original_words:
            overlap = len(found_words & original_words)
            if overlap >= len(original_words) * 0.3:
                return True

        return False

    def _detect_topic_presence(self, app_num: int, policy_text: str) -> bool:
        """
        Detect if policy discusses the TOPIC of an APP even without exact keywords.
        This addresses Fix 3: Partial Credit Logic for topic-based presence.
        """
        policy_lower = policy_text.lower()

        # Topic keywords for each APP
        topic_keywords = {
            1: ["privacy", "personal information", "data"],
            2: ["anonymous", "identify", "identity"],
            3: ["collect", "gather", "receive", "obtain"],
            4: ["unsolicited", "receive", "receive information"],
            5: ["collection", "why we", "purposes"],
            6: ["share", "disclose", "provide", "use", "service provider"],
            7: ["marketing", "promotional", "communication", "contact"],
            8: ["overseas", "international", "cross-border", "provider", "world"],
            9: ["identifier", "tfn", "abn", "government", "unique"],
            10: ["accurate", "current", "up to date", "quality", "data"],
            11: ["security", "protect", "breach", "safe", "safeguard"],
            12: ["access", "request", "provide", "copy"],
            13: ["correct", "amend", "update", "inaccurate"],
        }

        topic_words = topic_keywords.get(app_num, [])

        # Count how many topic words are present
        matches = sum(1 for word in topic_words if word in policy_lower)

        # If at least 2 topic words found, consider topic detected
        return matches >= 2

    def _apply_scoring_floor(
        self,
        current_score: int,
        policy_text: str,
        app_statuses: Dict[int, ComplianceStatus],
    ) -> int:
        """
        Apply scoring floor: having a real privacy policy that addresses multiple
        APPs deserves meaningful credit. Floor scales with coverage breadth.

        Rationale: a business that has published a privacy policy and addresses
        several APPs is making a genuine effort. The score should reflect that
        effort, even if keyword coverage is imperfect.
        """
        # Check if policy is substantial (>500 characters)
        if not policy_text or len(policy_text.strip()) < 500:
            return current_score

        # Count APPs that are PARTIALLY_COMPLIANT or COMPLIANT (substantively addressed)
        substantive_apps = sum(
            1
            for status in app_statuses.values()
            if status in [ComplianceStatus.PARTIALLY_COMPLIANT, ComplianceStatus.COMPLIANT]
        )

        # Floor applies only if at least 2 APPs are addressed substantively
        if substantive_apps < 2:
            return current_score

        # Base floor: 30 for having a real policy covering 2+ APPs
        # Scales up by 2 points per additional APP covered, capped at 45
        floor = min(45, 30 + (substantive_apps - 2) * 2)

        # Apply floor: return max of current score or floor
        return max(current_score, int(floor))

    # ========================================================================================
    # HELPER METHODS
    # ========================================================================================

    def _find_phrases_in_text(
        self,
        text: str,
        phrases: List[str],
    ) -> List[str]:
        """
        Find phrases in text (case-insensitive, handles word boundaries)
        Returns list of phrases that were found
        """
        text_lower = text.lower()
        found = []

        for phrase in phrases:
            # Create word-boundary regex pattern
            pattern = r'\b' + re.escape(phrase.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found.append(phrase)

        return found

    def _identify_gaps(
        self,
        app_num: int,
        found_phrases: List[str],
        expected_phrases: List[str],
    ) -> List[str]:
        """
        Identify which expected phrases were not found,
        returning human-readable gap descriptions.
        """
        missing = [p for p in expected_phrases if p not in found_phrases]
        return [
            APPRequirements.get_gap_description(app_num, phrase)
            for phrase in missing[:3]
        ]

    def _determine_gap_type(self, app_num: int, gaps: List[str]) -> str:
        """
        Determine the type of gap to recommend language for
        """
        if not gaps:
            return "no_gap"

        # Map gap patterns to gap types
        gap_patterns = {
            "app_1": {
                "no_privacy_policy": "No privacy policy",
                "no_contact_details": "Privacy contact",
                "no_complaint_process": "Complaint",
                "unclear_practices": "Management",
            },
        }

        # Default to generic gap type
        return "no_privacy_policy"

    def _generate_next_steps(
        self,
        overall_status: str,
        sector: str,
        app_statuses: Dict[int, ComplianceStatus],
    ) -> List[str]:
        """
        Generate prioritized next steps based on compliance status
        """
        steps = []

        if overall_status == ComplianceStatus.NON_COMPLIANT.value:
            steps.append("CRITICAL: Conduct urgent privacy policy review and update")
            steps.append("Engage privacy consultant or lawyer with Privacy Act expertise")
            steps.append("Prioritize critical APPs: 1 (Openness), 5 (Collection Notice), 11 (Security)")
        elif overall_status == ComplianceStatus.PARTIALLY_COMPLIANT.value:
            steps.append("Update privacy policy to address identified gaps")
            steps.append("Prioritize gaps in high-risk APPs for your sector")
            steps.append("Implement missing security and access/correction procedures")
        else:
            steps.append("Monitor for changes in Privacy Act requirements")
            steps.append("Review policy annually for compliance with new obligations")

        # Add ADM requirement reminder
        steps.append("Prepare for 10 December 2026 ADM transparency requirement")

        # Add sector-specific steps
        sector_guidance = SectorSpecificGuidance.get_guidance(sector)
        if sector_guidance:
            steps.append(f"Review sector-specific guidance for {sector}")

        return steps

    # ========================================================================================
    # LLM PROMPT GENERATION - All 13 APPs + ADM
    # ========================================================================================

    @staticmethod
    def get_all_llm_prompts(
        policy_text: str,
        business_name: str,
        sector: str,
    ) -> Dict[str, str]:
        """
        Generate all LLM prompts that would be sent to Claude API
        Useful for understanding the analysis process and for testing
        """
        engine = ComplianceEngine(mode="llm")
        prompts = {}

        # Generate prompts for each APP
        for app_num in range(1, 14):
            app_def = APPRequirements.get_app(app_num)
            prompts[f"APP_{app_num}"] = engine._generate_llm_prompt_for_app(
                app_num, app_def, policy_text, sector
            )

        # Generate ADM prompt
        prompts["ADM_TRANSPARENCY"] = engine._generate_adm_llm_prompt(
            policy_text, sector
        )

        return prompts

    @staticmethod
    def _generate_adm_llm_prompt(
        policy_text: str,
        sector: str,
    ) -> str:
        """Generate LLM prompt for ADM transparency analysis"""
        prompt = f"""You are an expert in Australian Privacy Act compliance, particularly the new ADM transparency requirement (effective 10 December 2026).

PRIVACY POLICY:
{policy_text}

REQUIREMENT ANALYSIS:
From 10 December 2026, organizations must disclose when they use automated decision-making (ADM) that has:
- A legal effect, or
- A similarly significant effect on the individual (e.g., eligibility determination, credit decision)

REQUIRED DISCLOSURES:
1. That you use automated decision-making
2. How the system works (in understandable terms)
3. What personal information is used
4. The significant effect on the individual
5. A mechanism for the individual to request human review
6. A right for the individual to object to the decision

BUSINESS CONTEXT:
Sector: {sector}
Sector ADM examples: {ADM_TRANSPARENCY_DETAILS.get('sector_applications', {}).get(sector.lower().replace(' ', '_'), 'N/A')}

ANALYSIS TASK:
Determine whether the policy discloses ADM use and compliance.

For your response, provide JSON:
{{
    "uses_adm": "[YES|NO|UNKNOWN]",
    "adm_disclosed": true/false,
    "examples_found": ["list of ADM types mentioned"],
    "compliance_level": "[COMPLIANT|PARTIAL|NON_COMPLIANT|NOT_APPLICABLE]",
    "gaps": ["specific gaps in disclosure"],
    "recommendation": "what's needed to comply"
}}
"""
        return prompt


# ========================================================================================
# EXAMPLE USAGE & TESTING
# ========================================================================================

if __name__ == "__main__":
    # Example: Analyze a minimal privacy policy
    sample_policy = """
    Privacy Policy

    We collect personal information from customers. We take security seriously and protect
    your information. You can request access to your information. We may share information
    with third parties to provide our services.
    """

    # Rule-based analysis (fast)
    engine_rb = ComplianceEngine(mode="rule_based")
    report_rb = engine_rb.analyze(
        policy_text=sample_policy,
        business_name="Sample Business",
        sector="Real Estate Agencies",
    )

    print("=" * 80)
    print("RULE-BASED ANALYSIS REPORT")
    print("=" * 80)
    print(f"Business: {report_rb.business_name}")
    print(f"Sector: {report_rb.sector}")
    print(f"Overall Score: {report_rb.overall_score}/100")
    print(f"Overall Status: {report_rb.overall_status}")
    print(f"\nSummary:")
    print(f"  Compliant: {report_rb.summary['compliant_count']}")
    print(f"  Partially Compliant: {report_rb.summary['partial_count']}")
    print(f"  Non-Compliant: {report_rb.summary['non_compliant_count']}")
    print(f"  Not Addressed: {report_rb.summary['not_addressed_count']}")
    print(f"\nJSON Report:\n{report_rb.to_json()}")

    # LLM analysis (would use Claude API in production)
    print("\n" + "=" * 80)
    print("LLM MODE - PROMPT GENERATION")
    print("=" * 80)
    prompts = ComplianceEngine.get_all_llm_prompts(
        sample_policy,
        "Sample Business",
        "Real Estate Agencies",
    )
    print(f"Generated {len(prompts)} prompts for Claude API")
    print("\nFirst APP prompt (APP_1):")
    print(prompts["APP_1"][:500] + "...")
