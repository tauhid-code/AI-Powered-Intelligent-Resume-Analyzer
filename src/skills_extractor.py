"""
This section extracts skills from resume and JD text using regex patttern and skill taxanomy.
Supports comparison between resume skills and JD requirements to surface matched and missing skills.
"""

from email.mime import text
import re 
import logging 
from typing import NamedTuple, Optional
from rapidfuzz import fuzz
logger = logging.getLogger(__name__)

## Skill Taxonomy --- 200+ skills across 13 categories 


SKILL_TAXONOMY: dict[str, list[str]] = {
    "programming_languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "c",
        "go", "golang", "rust", "kotlin", "swift", "scala", "r", "matlab",
        "perl", "ruby", "php", "bash", "shell", "powershell", "dart",
        "objective-c", "haskell", "elixir", "clojure", "fortran",
    ],
    "web_frameworks": [
        "react", "angular", "vue", "next.js", "nuxt", "svelte",
        "django", "flask", "fastapi", "spring", "spring boot", "express",
        "nestjs", "laravel", "rails", "ruby on rails", "asp.net", ".net",
        "node.js", "nodejs",
    ],
    "ml_ai": [
        "machine learning", "deep learning", "neural network", "nlp",
        "natural language processing", "computer vision", "reinforcement learning",
        "scikit-learn", "sklearn", "tensorflow", "keras", "pytorch", "torch",
        "xgboost", "lightgbm", "catboost", "hugging face", "transformers",
        "bert", "gpt", "llm", "large language model", "openai", "langchain",
        "rag", "retrieval augmented generation", "mlflow", "kubeflow",
        "feature engineering", "model deployment", "a/b testing",
        "time series", "recommendation system", "generative ai",
    ],
    "data_engineering": [
        "sql", "nosql", "pandas", "numpy", "spark", "pyspark",
        "hadoop", "hive", "kafka", "airflow", "dbt", "etl", "elt",
        "data pipeline", "data warehouse", "data lake", "databricks",
        "snowflake", "redshift", "bigquery", "dask", "polars",
    ],
    "cloud_platforms": [
        "aws", "azure", "gcp", "google cloud", "amazon web services",
        "s3", "ec2", "lambda", "sagemaker", "azure ml", "vertex ai",
        "cloud functions", "cloud run", "fargate", "ecs", "eks",
    ],
    "devops_mlops": [
        "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins",
        "github actions", "gitlab ci", "ci/cd", "devops", "mlops",
        "prometheus", "grafana", "helm", "argocd", "pulumi",
    ],
    "databases": [
        "postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis",
        "elasticsearch", "cassandra", "dynamodb", "neo4j", "oracle",
        "mssql", "sql server", "mariadb", "couchdb", "firebase",
        "supabase", "pinecone", "weaviate", "chroma",
    ],
    "data_visualization": [
        "tableau", "power bi", "looker", "matplotlib", "seaborn", "plotly",
        "d3.js", "grafana", "metabase", "superset",
    ],
    "version_control": [
        "git", "github", "gitlab", "bitbucket", "svn",
    ],
    "soft_skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "project management", "agile", "scrum",
        "kanban", "stakeholder management", "mentoring", "collaboration",
        "time management", "presentation",
    ],
    "methodologies": [
        "agile", "scrum", "kanban", "tdd", "test driven development",
        "bdd", "behavior driven development", "microservices",
        "rest", "restful", "graphql", "grpc", "api design",
        "system design", "object oriented programming", "oop",
        "functional programming", "design patterns",
    ],
    "testing": [
        "unit testing", "integration testing", "pytest", "junit",
        "selenium", "playwright", "cypress", "jest", "mocha",
        "load testing", "performance testing",
    ],
    "security": [
        "cybersecurity", "owasp", "penetration testing", "iam",
        "oauth", "jwt", "ssl", "tls", "encryption",
    ],
}


ALL_SKILLS : list[str] = sorted(
    { skill for skills in SKILL_TAXONOMY.values() for skill in skills},
    key = len,
    reverse = True,
)

# skills -> category mapping 

SKILL_TO_CATEGORY: dict[str, str] = {
    skill : cat 
    for cat, skills in SKILL_TAXONOMY.items()
    for skill in skills 
}


SKILL_PATTERN: re.Pattern = re.compile(
    r"\b(?:" + "|".join(re.escape(s) for s in ALL_SKILLS) + r")\b",
    re.IGNORECASE,
)

## RESULT TYPE

class SkillExtractionResult(NamedTuple):
    skills : list[str]
    skill_set : set[str]
    categories : dict[str,list[str]]


## PUBLIC FUNCTION 

def extract_skills(text: str) -> SkillExtractionResult:
    """
    Extract all recognized skills from the given text using regex pattern matching
    against the predefined skill taxonomy.
    """
    if not text or not text.strip():
        logger.warning("extract_skills received empty or blank text.")
        return SkillExtractionResult(skills=[], skill_set=set(), categories={})

    lowered = text.lower()
    raw_matches = SKILL_PATTERN.findall(lowered)

    # Deduplicate while preserving first-occurrence order
    seen: set[str] = set()
    ordered_skills: list[str] = []
    for match in raw_matches:
        normalized = match.lower()
        if normalized not in seen:
            seen.add(normalized)
            ordered_skills.append(normalized)

    # Group by category
    categories: dict[str, list[str]] = {}
    for skill in ordered_skills:
        cat = SKILL_TO_CATEGORY.get(skill, "other")
        categories.setdefault(cat, []).append(skill)

    logger.info(f"Extracted {len(ordered_skills)} unique skills from text.")
    return SkillExtractionResult(
        skills=ordered_skills,
        skill_set=set(ordered_skills),
        categories=categories,
    )
def fuzzy_match(skill: str, skill_set: set[str], threshold: int = 85) -> bool:
    for s in skill_set:
        if fuzz.partial_ratio(skill, s) >= threshold:
            return True
    return False


def compare_skills(
    resume_skills: SkillExtractionResult,
    jd_skills: SkillExtractionResult,
) -> tuple[list[str], list[str]]:
    """
    Compare resume skills against JD requirements and return matched and missing skill lists.
    """
    matched = []
    missing = []

    for jd_skill in jd_skills.skills:
        if jd_skill in resume_skills.skill_set or fuzzy_match(jd_skill, resume_skills.skill_set):
            matched.append(jd_skill)
        else:
            missing.append(jd_skill)

    logger.info(f"Compared skills: {len(matched)} matched, {len(missing)} missing.")
    return matched, missing


