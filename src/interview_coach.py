"""
Hirelytics AI — Interview Coach Module

Generates structured, role-specific interview questions using the Groq API
(llama3-8b-8192), based on resume analysis data (matched skills, missing
skills, projects, ATS score).

Set your Groq API key in .env:
    GROQ_API_KEY=gsk_your_actual_key_here

Get a free key at: https://console.groq.com
"""

import os
import json
import logging
import re

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "gsk_placeholder_replace_with_your_key")
GROQ_MODEL   = os.getenv("GROQ_MODEL",   "llama-3.1-8b-instant")


# Master Prompt Template 
_PROMPT_TEMPLATE = """You are an expert technical interviewer and hiring manager.
Your task is to generate structured interview questions based on a candidate's resume, job description (JD), and ATS analysis.

CANDIDATE DATA:
Role: {role}
Matched Skills (skills present in resume AND JD): {matched_skills}
Missing Skills (skills present in JD but NOT in resume): {missing_skills}
Projects (from resume): {projects}
ATS Score: {ats_score}

STRICT INSTRUCTIONS:
1. Follow difficulty levels EXACTLY as defined below.
2. Do NOT generate generic or random questions.
3. Questions must be relevant to the role and skills.
4. Keep questions concise and interview-like.
5. Return ONLY valid JSON. No extra text, no explanation.

QUESTION GENERATION RULES:

1. TECHNICAL QUESTIONS (from Matched Skills):
   * Difficulty: MEDIUM to HARD
   * Test deep understanding
   * Include "why", "how", "compare", and scenario-based questions
   * Avoid basic definitions
   * Generate 5-6 questions
   * For EACH question also write a concise model answer (3-5 sentences, expert-level)

2. GAP QUESTIONS (from Missing Skills):
   * Difficulty: EASY to MEDIUM
   * Focus on fundamentals and basic understanding
   * DO NOT ask advanced or tricky questions
   * Generate 4-5 questions
   * For EACH question also write a simple, beginner-friendly answer (2-3 sentences)

3. PROJECT-BASED SECTION (NO answers needed — candidate answers from personal experience):
   For the most relevant project:
   A. Generate a professional summary:
      * 4-5 lines
      * Clear, strong, resume-quality explanation
      * Mention tech stack, purpose, and impact
   B. Generate 4 questions (NO answer field):
      * 1 EASY  (basic understanding)
      * 2 MEDIUM (implementation + logic)
      * 1 HARD  (real-world / scenario-based)

4. BEHAVIORAL QUESTIONS (NO answers needed — candidate answers from personal experience):
   * Generate 3 questions (NO answer field)
   * Focus on problem-solving, teamwork, and challenges

OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "technical_questions": [
    {{"question": "", "difficulty": "medium", "skill": "", "answer": ""}},
    {{"question": "", "difficulty": "hard",   "skill": "", "answer": ""}}
  ],
  "gap_questions": [
    {{"question": "", "difficulty": "easy",   "skill": "", "answer": ""}},
    {{"question": "", "difficulty": "medium", "skill": "", "answer": ""}}
  ],
  "project": {{
    "project_name": "",
    "summary": "",
    "questions": [
      {{"question": "", "difficulty": "easy"}},
      {{"question": "", "difficulty": "medium"}},
      {{"question": "", "difficulty": "medium"}},
      {{"question": "", "difficulty": "hard"}}
    ]
  }},
  "behavioral_questions": [
    {{"question": ""}},
    {{"question": ""}},
    {{"question": ""}}
  ]
}}

FINAL RULE: Return ONLY the JSON object above. No markdown fences, no explanations, no extra text."""


def build_prompt(
    role: str,
    matched_skills: list,
    missing_skills: list,
    projects: list,
    ats_score: float,
) -> str:
    """Fill the master prompt template with candidate data."""
    return _PROMPT_TEMPLATE.format(
        role           = role or "Software Engineer",
        matched_skills = ", ".join(matched_skills) if matched_skills else "None specified",
        missing_skills = ", ".join(missing_skills) if missing_skills else "None",
        projects       = ", ".join(projects)       if projects       else "Not specified",
        ats_score      = f"{ats_score:.0f}/100"    if ats_score      else "N/A",
    )


def extract_projects_from_text(resume_text: str) -> list:
    """
    Heuristic extraction of project names from raw resume text.
    Scans for a Projects section header then collects short title-like lines.
    Falls back to a generic label if none found.
    """
    projects = []
    lines = resume_text.split("\n")
    in_projects = False

    project_header = re.compile(
        r"^(projects?|personal projects?|academic projects?|key projects?|notable projects?)\s*[:\-]?\s*$",
        re.IGNORECASE,
    )
    section_header = re.compile(
        r"^(experience|work experience|education|skills?|certifications?|"
        r"awards?|publications?|summary|objective|profile)\s*[:\-]?\s*$",
        re.IGNORECASE,
    )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if project_header.match(stripped):
            in_projects = True
            continue
        if in_projects:
            if section_header.match(stripped):
                break
            if (
                len(stripped) < 90
                and not stripped.startswith(("•", "-", "*", "·"))
                and not stripped[0].islower()
            ):
                projects.append(stripped)
                if len(projects) >= 4:
                    break

    if not projects:
        for match in re.finditer(
            r"(?:project|system|app|tool|platform)[:\s]+([A-Z][^\n]{3,60})",
            resume_text, re.IGNORECASE
        ):
            candidate = match.group(1).strip(" .:-")
            if candidate and candidate not in projects:
                projects.append(candidate)
            if len(projects) >= 3:
                break

    return projects if projects else ["Primary project from resume"]


def _clean_json(raw: str) -> str:
    """Strip markdown fences and whitespace from LLM output."""
    cleaned = re.sub(r"```(?:json)?", "", raw, flags=re.IGNORECASE).strip()
    cleaned = cleaned.rstrip("`").strip()
    return cleaned


## Main public function to generate interview questions

def generate_interview_questions(
    role: str,
    matched_skills: list,
    missing_skills: list,
    projects: list,
    ats_score: float,
    timeout: int = 60,
) -> dict:
    """
    Call the Groq API using the official groq package and return a parsed dict.

    Raises:
        ValueError  — invalid API key, rate limit, or unparseable response
        Exception   — any other Groq / network error
    """
    prompt = build_prompt(role, matched_skills, missing_skills, projects, ats_score)

    logger.info("Calling Groq API: model=%s", GROQ_MODEL)

    client = Groq(api_key=GROQ_API_KEY)

    try:
        chat_completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert technical interviewer and hiring manager. "
                        "You MUST respond with valid JSON only. "
                        "No markdown, no code fences, no explanations — pure JSON object only."
                    ),
                },
                {
                    "role":    "user",
                    "content": prompt,
                },
            ],
            temperature=0.65,
            max_tokens=2048,
            top_p=0.90,
        )
    except Exception as e:
        err = str(e)
        if "401" in err or "invalid_api_key" in err.lower():
            raise ValueError(" Invalid Groq API key. Update GROQ_API_KEY in your .env file.")
        if "429" in err or "rate_limit" in err.lower():
            raise ValueError(" Groq rate limit hit. Wait a moment and try again.")
        raise

    raw_output = chat_completion.choices[0].message.content
    logger.debug("Groq raw output (first 400 chars): %s", raw_output[:400])

    # ── Parse JSON from response ──────────────────────────────────────────────
    cleaned = _clean_json(raw_output)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            raise ValueError(
                f"Could not parse JSON from Groq response.\n"
                f"First 500 chars:\n{raw_output[:500]}"
            )

    # ── Ensure all 4 keys exist ───────────────────────────────────────────────
    result.setdefault("technical_questions", [])
    result.setdefault("gap_questions", [])
    result.setdefault("project", {"project_name": "", "summary": "", "questions": []})
    result.setdefault("behavioral_questions", [])

    logger.info(
        "Questions generated — technical: %d  gap: %d  behavioral: %d",
        len(result["technical_questions"]),
        len(result["gap_questions"]),
        len(result["behavioral_questions"]),
    )

    return result
