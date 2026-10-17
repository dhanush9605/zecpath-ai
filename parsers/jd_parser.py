"""Job Description Parsing System for Zecpath AI (Day 6).

Converts raw employer job descriptions into structured, AI-ready JobProfile
and JobRequirements objects with automated skill synonym resolution,
seniority inference, and salary range extraction.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

from parsers.cleaner import clean_whitespace, normalize_bullets, normalize_unicode
from parsers.models.entities import (
    EmploymentType,
    LocationObject,
    SkillObject,
    WorkplaceType,
)
from parsers.models.job import JobProfile, JobRequirements, PayPeriod, SalaryRange
from parsers.taxonomy import (
    SKILL_TAXONOMY,
    detect_education_level,
    detect_role_type,
    detect_seniority,
    resolve_skill_synonym,
)


class JobDescriptionParser:
    """Production parser extracting structured AI job profiles from unstructured text."""

    def __init__(self) -> None:
        # Precompile skill search regex patterns for fast extraction
        self._skill_patterns: list[tuple[re.Pattern, str]] = []
        for skill_def in SKILL_TAXONOMY:
            # Pattern matching canonical name and all synonyms with word boundaries
            terms = [re.escape(skill_def.canonical_name)] + [re.escape(s) for s in skill_def.synonyms]
            pattern = re.compile(r"\b(?:" + "|".join(terms) + r")\b", re.IGNORECASE)
            self._skill_patterns.append((pattern, skill_def.canonical_name))

    def parse_text(self, raw_text: str, job_id: str | None = None) -> JobProfile:
        """Parse raw job description text into a validated JobProfile object."""
        cleaned = self._clean_jd_text(raw_text)
        sections = self._segment_sections(cleaned)

        # 1. Header extraction (Title, Company, Location, Department)
        title, company, department, loc_obj, workplace_type = self._extract_header_metadata(
            sections.get("HEADER", "") or cleaned
        )

        # 2. Experience extraction
        req_text = sections.get("REQUIREMENTS", "") + "\n" + sections.get("OVERVIEW", "")
        min_exp = self._extract_experience_years(req_text)

        # 3. Role type and Seniority inference
        role_type = detect_role_type(title)
        seniority = detect_seniority(title, min_exp)

        # 4. Education level extraction
        min_edu = detect_education_level(req_text)

        # 5. Skills extraction & Partitioning (Required vs Preferred)
        required_skills = self._extract_skills(sections.get("REQUIREMENTS", ""))
        preferred_skills = self._extract_skills(sections.get("PREFERRED", ""))

        # If no preferred section, partition or fallback
        if not required_skills and sections.get("OVERVIEW"):
            required_skills = self._extract_skills(sections.get("OVERVIEW", ""))

        # 6. Responsibilities extraction
        responsibilities = self._extract_bullet_items(sections.get("RESPONSIBILITIES", ""))

        # 7. Benefits & Salary extraction
        salary = self._extract_salary(sections.get("COMPENSATION", "")) or self._extract_salary(cleaned)
        raw_benefits = self._extract_bullet_items(
            sections.get("BENEFITS", "") or sections.get("COMPENSATION", "")
        )
        benefits = [b for b in raw_benefits if not re.search(r"\$\s*\d+", b)]

        # Ensure unique job_id
        if not job_id:
            safe_title = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
            job_id = f"job-{safe_title[:24]}-{int(min_exp)}y"

        requirements = JobRequirements(
            minimum_experience_years=min_exp,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            minimum_education_level=min_edu,
            required_certifications=self._extract_certifications(req_text),
        )

        summary_text = sections.get("OVERVIEW", "").strip()
        if not summary_text:
            summary_text = f"{company} is hiring a {title} in {department}."

        return JobProfile(
            job_id=job_id,
            title=title,
            company_name=company,
            department=department,
            role_type=role_type,
            seniority_level=seniority,
            employment_type=EmploymentType.FULL_TIME,
            workplace_type=workplace_type,
            location=loc_obj,
            salary_range=salary,
            summary=summary_text,
            responsibilities=responsibilities,
            requirements=requirements,
            benefits=benefits,
            created_at=datetime.now(UTC).strftime("%Y-%m-%d"),
            is_active=True,
        )

    def parse_file(self, file_path: str | Path, job_id: str | None = None) -> JobProfile:
        """Parse job description from file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Job description file not found: {path}")

        raw_text = path.read_text(encoding="utf-8")
        jid = job_id or f"job-{path.stem.replace('jd_', '').replace('_', '-')}"
        return self.parse_text(raw_text, job_id=jid)

    def parse_and_save(
        self,
        file_path: str | Path,
        output_dir: str | Path | None = None,
    ) -> tuple[Path, JobProfile]:
        """Parse JD file and save structured JSON conforming to schema."""
        path = Path(file_path)
        job_profile = self.parse_file(path)

        out_dir = Path(output_dir) if output_dir else path.parent.parent / "structured" / "job_descriptions"
        out_dir.mkdir(parents=True, exist_ok=True)

        json_path = out_dir / f"{path.stem}.json"
        json_path.write_text(job_profile.model_dump_json(indent=2), encoding="utf-8")

        return json_path, job_profile

    # -------------------------------------------------------------------------
    # Helper Extraction Routines
    # -------------------------------------------------------------------------

    def _clean_jd_text(self, text: str) -> str:
        """Sanitize unicode and standardize bullet formats."""
        t = normalize_unicode(text)
        t = normalize_bullets(t)
        return clean_whitespace(t)

    def _segment_sections(self, text: str) -> dict[str, str]:
        """Segment raw text into semantic sections using header heuristics."""
        section_regexes = {
            "RESPONSIBILITIES": re.compile(
                r"^\s*(responsibilities|what you'?ll do|core responsibilities|duties|key deliverables)\b[:\s]*",
                re.IGNORECASE,
            ),
            "REQUIREMENTS": re.compile(
                r"^\s*(requirements|what you need|qualifications|minimum qualifications|basic qualifications)\b[:\s]*",
                re.IGNORECASE,
            ),
            "PREFERRED": re.compile(
                r"^\s*(preferred qualifications|nice to have|bonus points|preferred skills)\b[:\s]*",
                re.IGNORECASE,
            ),
            "COMPENSATION": re.compile(
                r"^\s*(compensation & benefits|compensation|salary range|remuneration|salary)\b[:\s]*",
                re.IGNORECASE,
            ),
            "BENEFITS": re.compile(
                r"^\s*(benefits|perks|what we offer)\b[:\s]*",
                re.IGNORECASE,
            ),
            "OVERVIEW": re.compile(
                r"^\s*(about the role|overview|summary|role description|the mission)\b[:\s]*",
                re.IGNORECASE,
            ),
        }

        lines = text.splitlines()
        sections: dict[str, list[str]] = {"HEADER": []}
        current_section = "HEADER"

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Check if this line triggers a new section (bullets cannot be headers)
            matched_sec = None
            if len(line_str) <= 60 and not line_str.startswith(("-", "*", "•", "►", "o ")):
                for sec_name, pattern in section_regexes.items():
                    if pattern.search(line_str):
                        matched_sec = sec_name
                        break

            if matched_sec:
                current_section = matched_sec
                if current_section not in sections:
                    sections[current_section] = []
            else:
                sections[current_section].append(line)

        return {k: "\n".join(v).strip() for k, v in sections.items()}

    def _extract_header_metadata(
        self, header_text: str
    ) -> tuple[str, str, str, LocationObject, WorkplaceType]:
        """Extract Title, Company, Department, and Location from header text."""
        title = "Software Engineer"
        company = "Technology Corp"
        department = "Engineering"
        city = "San Francisco"
        country = "USA"
        workplace_type = WorkplaceType.HYBRID

        # Role / Title extraction
        title_match = re.search(r"(?:JOB REQUISITION|JOB TITLE|POSITION|ROLE):\s*(.+)", header_text, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).split("\n")[0].strip()
        else:
            first_line = header_text.splitlines()[0] if header_text.splitlines() else ""
            if 5 < len(first_line) < 70:
                title = first_line.strip()

        # Company extraction
        company_match = re.search(r"Company:\s*(.+)", header_text, re.IGNORECASE)
        if company_match:
            company = company_match.group(1).split("\n")[0].strip()

        # Department extraction
        dept_match = re.search(r"Department:\s*(.+)", header_text, re.IGNORECASE)
        if dept_match:
            department = dept_match.group(1).split("\n")[0].strip()
        elif "engineering" in title.lower() or "systems" in title.lower():
            department = "Core Engineering"
        elif "talent" in title.lower() or "recruiter" in title.lower():
            department = "People & Talent Operations"
        elif "financial" in title.lower() or "fp&a" in title.lower():
            department = "Corporate Finance"

        # Location extraction
        loc_match = re.search(r"Location:\s*(.+)", header_text, re.IGNORECASE)
        if loc_match:
            loc_str = loc_match.group(1).split("\n")[0].strip()
            if "remote" in loc_str.lower():
                workplace_type = WorkplaceType.REMOTE
            elif "hybrid" in loc_str.lower():
                workplace_type = WorkplaceType.HYBRID
            elif "onsite" in loc_str.lower():
                workplace_type = WorkplaceType.ONSITE

            # Extract city if present
            city_match = re.match(r"^([^,(]+)", loc_str)
            if city_match:
                city = city_match.group(1).strip()

        location_obj = LocationObject(
            city=city,
            state_or_province=None,
            country=country,
            is_remote=(workplace_type == WorkplaceType.REMOTE),
        )

        return title, company, department, location_obj, workplace_type

    def _extract_experience_years(self, text: str) -> float:
        """Extract minimum years of required experience using pattern matching."""
        # Matches '5+ years', 'minimum 5 years', 'at least 3-5 years', '6+ yrs'
        patterns = [
            r"(\d+(?:\.\d+)?)\s*\+?\s*(?:-\s*\d+\s*)?(?:years|yrs)",
            r"(?:minimum|at least)\s*(\d+(?:\.\d+)?)\s*(?:years|yrs)?",
        ]
        for pat in patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                try:
                    val = float(match.group(1))
                    if 0.5 <= val <= 30.0:
                        return val
                except ValueError:
                    continue
        return 3.0

    def _extract_skills(self, text: str) -> list[SkillObject]:
        """Extract and resolve skills from text using taxonomy synonyms."""
        found_skills: dict[str, SkillObject] = {}

        for pattern, canonical_name in self._skill_patterns:
            if pattern.search(text):
                canonical_def = resolve_skill_synonym(canonical_name)
                if canonical_def and canonical_def.canonical_name not in found_skills:
                    found_skills[canonical_def.canonical_name] = SkillObject(
                        name=canonical_def.canonical_name,
                        category=canonical_def.category,
                        proficiency=canonical_def.default_proficiency,
                        years_of_experience=None,
                        last_used_year=None,
                        verified=False,
                    )

        return list(found_skills.values())

    def _extract_salary(self, text: str) -> SalaryRange | None:
        """Extract compensation brackets from text."""
        # Matches '$165,000 - $210,000' or '$110,000 - $140,000'
        match = re.search(
            r"\$\s*(\d{1,3}(?:,\d{3})+|\d+k?)\s*(?:-|to)\s*\$\s*(\d{1,3}(?:,\d{3})+|\d+k?)",
            text,
            re.IGNORECASE,
        )
        if match:
            raw_min = match.group(1).replace(",", "").lower()
            raw_max = match.group(2).replace(",", "").lower()
            min_val = float(raw_min.replace("k", "000"))
            max_val = float(raw_max.replace("k", "000"))
            return SalaryRange(
                currency="USD",
                min_amount=min_val,
                max_amount=max_val,
                pay_period=PayPeriod.ANNUAL,
            )
        return None

    def _extract_bullet_items(self, text: str) -> list[str]:
        """Extract individual bullet items or lines from a text block."""
        items: list[str] = []
        for line in text.splitlines():
            clean = line.strip().lstrip("•-*►o ").strip()
            if len(clean) >= 10:
                items.append(clean)
        return items

    def _extract_certifications(self, text: str) -> list[str]:
        """Detect standard professional certifications mentioned in JD."""
        certs = []
        cert_names = ["AWS Certified", "CFA", "CPA", "CISSP", "PMP", "SHRM-CP", "CKA", "Terraform Associate"]
        for cert in cert_names:
            if cert.lower() in text.lower():
                certs.append(cert)
        return certs
