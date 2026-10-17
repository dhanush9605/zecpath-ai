"""Text cleaning and normalization pipeline for resume extraction (Day 5).

Handles unicode sanitization, non-printable character removal, ligature fixing,
bullet point standardization, heading normalization, and whitespace cleanup.
"""

from __future__ import annotations

import re
import unicodedata

# Canonical standard headings mapped from common variations
CANONICAL_HEADINGS: dict[str, list[str]] = {
    "PROFESSIONAL SUMMARY": [
        "summary",
        "professional summary",
        "summary of qualifications",
        "career summary",
        "career objective",
        "objective",
        "profile",
        "about me",
        "executive summary",
    ],
    "WORK EXPERIENCE": [
        "experience",
        "work experience",
        "employment history",
        "work history",
        "professional experience",
        "career history",
        "relevant experience",
        "job history",
    ],
    "TECHNICAL SKILLS": [
        "skills",
        "technical skills",
        "key skills",
        "core competencies",
        "technical expertise",
        "technologies",
        "skills & competencies",
        "technical proficiency",
        "tools & technologies",
    ],
    "EDUCATION": [
        "education",
        "academic background",
        "academic history",
        "education & training",
        "educational qualifications",
        "academic credentials",
        "qualifications",
    ],
    "CERTIFICATIONS": [
        "certifications",
        "licenses",
        "licenses & certifications",
        "certificates",
        "professional certifications",
        "accreditations",
    ],
    "PROJECTS": [
        "projects",
        "key projects",
        "notable projects",
        "personal projects",
        "academic projects",
        "portfolio",
    ],
    "LANGUAGES": [
        "languages",
        "languages known",
        "language proficiencies",
        "language skills",
    ],
}

# Unicode Ligature replacements
LIGATURE_MAP = {
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb03": "ffi",
    "\ufb04": "ffl",
    "\ufb05": "ft",
    "\ufb06": "st",
}

# Varied bullet points across PDF/Word documents
BULLET_PATTERNS = re.compile(
    r"^[\t ]*(?:[\u2022\u2023\u25E6\u2043\u2219\u25AA\u25AB\u25CF\u25CB\u25A0\u25A1\u25BA\u27A4\u2713\u2714\u2605\u2726\u2212\u2013\u2014*+\-]|o(?=\s+))\s+",
    re.MULTILINE,
)


def normalize_unicode(text: str) -> str:
    """Normalize unicode characters to NFKC and resolve typographic symbols."""
    # Replace known ligatures
    for lig, rep in LIGATURE_MAP.items():
        text = text.replace(lig, rep)

    # Normalize unicode composition
    text = unicodedata.normalize("NFKC", text)

    # Normalize curly quotes and apostrophes to standard ASCII
    quote_map = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": " - ",
        "\u00a0": " ",  # Non-breaking space
        "\ufeff": "",   # Zero-width no-break space (BOM)
        "\u200b": "",   # Zero-width space
    }
    for orig, rep in quote_map.items():
        text = text.replace(orig, rep)

    return text


def remove_unprintable_artifacts(text: str) -> str:
    """Remove control characters and binary artifacts while preserving newlines and tabs."""
    # Retain \t (\x09) and \n (\x0a), remove other control characters
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)


def fix_hyphenated_line_breaks(text: str) -> str:
    """Recombine words split across line breaks by hyphens (e.g. 'micro-\nservices' -> 'microservices')."""
    return re.sub(r"(\b[a-zA-Z]{2,})-\n\s*([a-zA-Z]{2,}\b)", r"\1\2", text)


def normalize_bullets(text: str) -> str:
    """Standardize disparate bullet characters to canonical bullet marker ('• ')."""
    return BULLET_PATTERNS.sub("• ", text)


def normalize_section_headings(text: str) -> tuple[str, list[str]]:
    """Detect and normalize standard resume section headers into clear uppercase headers.

    Returns the transformed text and the list of detected canonical section headings.
    """
    detected_headings: list[str] = []
    lines = text.split("\n")
    normalized_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        # Clean potential decorative markdown/ASCII surrounding header (e.g. === Skills === or -- Work --)
        cleaned_cand = re.sub(r"^[=\-_#*:\s]+|[=\-_#*:\s]+$", "", stripped).strip().lower()

        matched_canonical = None
        for canonical, variations in CANONICAL_HEADINGS.items():
            if cleaned_cand in variations:
                matched_canonical = canonical
                break

        if matched_canonical and len(stripped) <= 45:
            normalized_lines.append(f"\n{matched_canonical}\n" + ("-" * len(matched_canonical)))
            if matched_canonical not in detected_headings:
                detected_headings.append(matched_canonical)
        else:
            normalized_lines.append(line)

    result_text = "\n".join(normalized_lines)
    return result_text, detected_headings


def clean_whitespace(text: str) -> str:
    """Remove trailing whitespace, collapse multi-spaces and excessive newlines."""
    # Collapse 3 or more spaces on a single line into 2 spaces (preserve indentation intent)
    text = re.sub(r"[ \t]{3,}", "  ", text)

    # Trim trailing whitespace on each line
    lines = [line.rstrip() for line in text.split("\n")]
    text = "\n".join(lines)

    # Collapse 3 or more consecutive newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_resume_text(raw_text: str) -> tuple[str, dict]:
    """Execute full end-to-end cleaning and normalization pipeline on raw resume text.

    Returns:
        (cleaned_text, stats_dict)
    """
    if not raw_text:
        return "", {"original_length": 0, "cleaned_length": 0, "detected_sections": []}

    orig_len = len(raw_text)

    # 1. Unicode & Ligature normalization
    step1 = normalize_unicode(raw_text)

    # 2. Control characters and unprintable symbols
    step2 = remove_unprintable_artifacts(step1)

    # 3. Rejoin hyphenated line breaks
    step3 = fix_hyphenated_line_breaks(step2)

    # 4. Standardize bullet markers
    step4 = normalize_bullets(step3)

    # 5. Normalize section headers
    step5, detected_sections = normalize_section_headings(step4)

    # 6. Final whitespace normalization
    cleaned = clean_whitespace(step5)

    stats = {
        "original_length": orig_len,
        "cleaned_length": len(cleaned),
        "characters_removed": max(0, orig_len - len(cleaned)),
        "detected_sections": detected_sections,
        "word_count": len(cleaned.split()),
        "lines_count": len(cleaned.splitlines()),
    }

    return cleaned, stats
