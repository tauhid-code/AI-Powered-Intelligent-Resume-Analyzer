"""
This file is responsible for computing the ATS compatibility score between a resume and job description.
Implements keyword match scoring, semantic similarity via sentence-transformers, and section-based scoring,
then combines them into a single weighted ATS score on a 0–100 scale.

Formula:
    ATS Score = (0.50 × keyword_match_score)
              + (0.25 × semantic_similarity_score)
              + (0.25 × section_score)
"""
import logging 
from dataclasses import dataclass, field
from typing import Optional 

import numpy as np 
from src.utils import (
    cosine_similarity_sklearn,
    cosine_similarity_numpy,
    compute_keyword_scoring,
    detect_sections,
)
from src.preprocessing import preprocess_text, tokenize 
from src.skills_extractor import extract_skills
logger = logging.getLogger(__name__)

##scoring weights 
WEIGHT_KEYWORD: float = 0.50
WEIGHT_SEMANTIC: float = 0.30
WEIGHT_SECTION: float = 0.20

##Scored Sections 
SCORED_SECTIONS : list[str]= ['skills', 'experience', 'projects']

_embedding_model = None 

# Result dataclass
@dataclass 
class ATSResult: 
    ats_score: float 
    keyword_score: float 
    semantic_score: float 
    section_score: float 
    matched_skills: list[str] = field(default_factory = list)
    missing_skills: list[str] = field(default_factory=list)
    sections_found: dict[str,bool] = field(default_factory=dict)
     

## Model Loader 
def load_embedding_model():
    """Lazy loader for the sentence-transformers embedding model."""
    global _embedding_model
    if _embedding_model is None:
        try: 
            from sentence_transformers import SentenceTransformer 
            logger.info("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
            _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Model loaded successfully.")
        except ImportError as e: 
            raise ImportError("sentence-transformers library is not installed. Please install it using 'pip install sentence-transformers'.") from e
    return _embedding_model


## SUB_SCORERS 
def compute_keyword_score(resume_text: str, jd_text: str) -> float:
    resume_data = extract_skills(resume_text)
    jd_data = extract_skills(jd_text)

    resume_skills = resume_data.skill_set
    jd_skills = jd_data.skill_set

    if not jd_skills:
        return 0.0

    matched = resume_skills.intersection(jd_skills)
    score = len(matched) / len(jd_skills)

    logger.debug(
        f"Keyword score: {score:.4f} "
        f"({len(matched)} of {len(jd_skills)} JD skills matched)"
    )

    return score

def compute_semantic_score(resume_text: str, jd_text: str) -> float:
    """
    Compute semantic similarity between resume and JD using sentence embeddings.
    Score is clamped to [0.0, 1.0].
    """
    model = load_embedding_model()

    # Truncate to stay within the model's token window
    embeddings = model.encode(
        [resume_text[:3000], jd_text[:3000]],
        convert_to_numpy=True,
    )

    try:
        score = cosine_similarity_sklearn(embeddings[0], embeddings[1])
    except Exception:
        score = cosine_similarity_numpy(embeddings[0], embeddings[1])

    score = max(0.0, min(1.0, score))
    logger.debug(f"Semantic similarity score: {score:.4f}")
    return score


def compute_section_score(resume_text: str) -> tuple[float, dict[str, bool]]:
    """
    Score the resume based on the presence of key structural sections
    (skills, experience, projects). Each detected section contributes equally.
    """
    all_sections = detect_sections(resume_text)
    scored_count = sum(1 for sec in SCORED_SECTIONS if all_sections.get(sec, False))
    score = scored_count / len(SCORED_SECTIONS) if SCORED_SECTIONS else 0.0

    logger.debug(
        f"Section score: {score:.4f} "
        f"({scored_count} of {len(SCORED_SECTIONS)} required sections found)"
    )
    return score, all_sections

##--------Main pipeline function-----------

def compute_ats_score(
    resume_text: str,
    jd_text: str,
    matched_skills: list[str],
    missing_skills: list[str],
) -> ATSResult:
    """
    Run the complete ATS scoring pipeline and return a structured result.
    Computes keyword, semantic, and section sub-scores then combines them
    into a final weighted ATS score on a 0–100 scale.
    """
    logger.info("Starting ATS scoring pipeline...")

    kw_score = compute_keyword_score(resume_text, jd_text)

    try:
        sem_score = compute_semantic_score(resume_text, jd_text)
    except Exception as e:
        logger.warning(f"Semantic scoring failed: {e}. Defaulting semantic score to 0.")
        sem_score = 0.0

    sec_score, sections_found = compute_section_score(resume_text)

    ats_score = round(
        (WEIGHT_KEYWORD * kw_score + WEIGHT_SEMANTIC * sem_score + WEIGHT_SECTION * sec_score) * 100,
        2,
    )

    logger.info(
        f"ATS Score: {ats_score:.1f} | "
        f"Keyword: {kw_score:.2f}  Semantic: {sem_score:.2f}  Section: {sec_score:.2f}"
    )

    return ATSResult(
        ats_score=ats_score,
        keyword_score=kw_score,
        semantic_score=sem_score,
        section_score=sec_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        sections_found=sections_found,
    )
