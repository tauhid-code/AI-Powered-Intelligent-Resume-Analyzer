"""
This file provides cosine similarity computation, resume section detection via regex, keyword scoring,
logging setup, and formatted report generation.
"""

import re 
import logging 
import sys 
from typing import Optional 

import numpy as np 

## Logging setup 

def set_logging( level: int = logging.INFO) -> None:
    logging.basicConfig(
        stream = sys.stdout,
        level = level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

## Cosine similarity 
def cosine_similarity_numpy(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0 
    
    return float(np.dot(vec_a,vec_b)/(norm_a*norm_b))

def cosine_similarity_sklearn(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    from sklearn.metrics.pairwise import cosine_similarity 
    score = cosine_similarity(vec_a.reshape(1,-1), vec_b.reshape(1,-1))[0][0]
    return float(score)

## Section detection via regex 
_SECTION_PATTERNS: dict[str, list[str]] = {
    "skills": [
        r"\bskills?\b",
        r"\btechnical skills?\b",
        r"\bcore competenc",
        r"\btechnologies\b",
        r"\btech stack\b",
        r"\bproficienc",
    ],
    "experience": [
        r"\bwork experience\b",
        r"\bprofessional experience\b",
        r"\bemployment history\b",
        r"\bwork history\b",
        r"\bexperience\b",
        r"\bjob history\b",
        r"\bcareer history\b",
    ],
    "projects": [
        r"\bprojects?\b",
        r"\bpersonal projects?\b",
        r"\bacademic projects?\b",
        r"\bkey projects?\b",
        r"\bside projects?\b",
        r"\bportfolio\b",
    ],
    "education": [
        r"\beducation\b",
        r"\bacademic background\b",
        r"\bqualifications?\b",
        r"\bdegree\b",
    ],
    "certifications": [
        r"\bcertifications?\b",
        r"\bcertificates?\b",
        r"\blicenses?\b",
        r"\baccreditations?\b",
    ],
    "summary": [
        r"\bsummary\b",
        r"\bprofile\b",
        r"\bobjective\b",
        r"\babout me\b",
        r"\bprofessional summary\b",
    ],
}
def detect_sections(text: str) -> dict[str, bool]:
    """
    Detect which standard resume sections are present in the given text.
    Returns a mapping of section name to a boolean presence flag.
    """
    lowered = text.lower()
    return {
        section: any(re.search(pat, lowered) for pat in patterns)
        for section, patterns in _SECTION_PATTERNS.items()
    }

## Keyword scoring 

def compute_keyword_scoring(resume_tokens: set[str], jd_tokens: set[str]) -> float:

    if not jd_tokens:
        return 0.0
    score = len(resume_tokens & jd_tokens) / len(jd_tokens)
    return float(score)

## Report formatting 

def format_score_report(
    ats_score: float,
    keyword_score: float,
    semantic_score: float,
    section_score: float,
    matched_skills: list[str],
    missing_skills: list[str],
    sections_found: dict[str, bool],
) -> str:
    """
    Build and return a human-readable ATS score report string with a progress bar,
    sub-score breakdown, section detection results, and skill gap analysis.
    """
    bar_length = 40 
    filled = int((ats_score/100)*bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)


    lines = [
        "",
        "=" * 60,
        "       AI RESUME INTELLIGENCE PLATFORM — ATS REPORT",
        "=" * 60,
        f"  ATS Score  : {ats_score:.1f} / 100",
        f"  [{bar}]",
        "",
        "  Score Breakdown:",
        f"    • Keyword Match Score     : {keyword_score * 100:.1f}%  (weight 50%)",
        f"    • Semantic Similarity     : {semantic_score * 100:.1f}%  (weight 30%)",
        f"    • Section Coverage Score  : {section_score * 100:.1f}%  (weight 20%)",
        "",
        "  Resume Sections Detected:",
    ]

    for section, present in sections_found.items():
        icon = "✔" if present else "✘"
        lines.append(f"    {icon}  {section.capitalize()}")

    lines += [
        "",
        f"  Matched Skills ({len(matched_skills)}):",
        "    " + (", ".join(matched_skills) if matched_skills else "None"),
        "",
        f"  Missing Skills ({len(missing_skills)}):",
        "    " + (", ".join(missing_skills) if missing_skills else "None — great match!"),
        "",
        "=" * 60,
        "",
    ]

    return "\n".join(lines)
