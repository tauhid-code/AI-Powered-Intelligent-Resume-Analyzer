"""
This file serves as the main entry point for the AI Resume Intelligence Platform.
Orchestrates the full pipeline: PDF parsing → skill extraction → ATS scoring → report output.
Accepts a resume PDF path and optional job description file via CLI arguments.

Usage:
    python app.py --resume path/to/resume.pdf --jd path/to/jd.txt
    python app.py --resume path/to/resume.pdf   # uses built-in example JD
    python app.py --demo                         # runs with mock text, no PDF needed
"""

import argparse 
from ast import arg
import logging 
import sys 

from pathlib import Path 
from typing import Optional  


from src.parser import parse_resume 
from src.scorer import compute_ats_score 
from src.skills_extractor import extract_skills, compare_skills 
from src.utils import set_logging, format_score_report 

## Build In JD Example 
EXAMPLE_JD = """
We are looking for a Senior Machine Learning Engineer to join our AI team.

Responsibilities:
- Design, build, and deploy machine learning and deep learning models at scale.
- Collaborate with data engineers to build robust data pipelines using Apache Spark
  and Apache Airflow.
- Develop RESTful APIs using FastAPI to serve ML models in production.
- Implement MLOps best practices using MLflow, Docker, and Kubernetes.
- Work closely with cross-functional teams using Agile and Scrum methodologies.
- Maintain and optimize models deployed on AWS SageMaker and Azure ML.

Requirements:
- 4+ years of experience with Python, including scikit-learn, TensorFlow, and PyTorch.
- Strong knowledge of NLP, transformer architectures (BERT, GPT), and Hugging Face.
- Experience with SQL, PostgreSQL, and NoSQL databases (MongoDB, Redis).
- Proficiency with Git, GitHub Actions, CI/CD pipelines, Docker, and Kubernetes.
- Hands-on experience with AWS (S3, EC2, Lambda, SageMaker) or GCP (Vertex AI).
- Excellent communication, leadership, and problem-solving skills.
- Experience with data visualization tools such as Tableau or Power BI is a plus.
"""

## Build In Demo Resume 
DEMO_RESUME_TEXT = """
John Doe
Senior Software Engineer | john.doe@email.com | github.com/johndoe

SUMMARY
Results-driven ML Engineer with 5+ years of experience building and deploying
machine learning solutions. Passionate about NLP, deep learning, and scalable
data pipelines.

SKILLS
Programming Languages: Python, Java, Scala, SQL, Bash
Frameworks & Libraries: PyTorch, TensorFlow, scikit-learn, FastAPI, Flask, Pandas, NumPy, Spark
Cloud & DevOps: AWS (S3, EC2, SageMaker, Lambda), Docker, Kubernetes, GitHub Actions, Airflow, MLflow
Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
NLP: Hugging Face Transformers, BERT, GPT, LangChain, RAG

EXPERIENCE
Machine Learning Engineer — TechCorp Inc. (2021–Present)
- Built and deployed NLP classification models using PyTorch and Hugging Face Transformers.
- Designed ETL pipelines with Apache Airflow and PySpark on AWS.
- Containerised services using Docker and orchestrated via Kubernetes.
- Developed internal model serving API using FastAPI with CI/CD via GitHub Actions.
- Collaborated in an Agile/Scrum team environment, leading sprint planning for ML features.

Software Engineer — DataSoft Ltd. (2019–2021)
- Developed RESTful APIs using Flask and FastAPI backed by PostgreSQL and Redis.
- Implemented A/B testing framework to evaluate recommendation system models.
- Migrated legacy SQL pipelines to distributed PySpark jobs on AWS EMR.

PROJECTS
Resume Intelligence Platform (Personal)
- Built an ATS scoring system using sentence-transformers and cosine similarity.
- Tech stack: Python, FastAPI, Docker, scikit-learn, PostgreSQL.

Sentiment Analysis API
- Fine-tuned BERT on a custom dataset using Hugging Face Transformers.
- Deployed on AWS SageMaker with a FastAPI gateway.

EDUCATION
B.Tech in Computer Science — IIT Delhi (2019)
"""

## PIPELINE 

def run_ats_pipeline(resume_text: str , jd_text: str) -> str:
      """
    Execute the full ATS evaluation pipeline on provided texts and print the report.
    """
      logger = logging.getLogger(__name__)
      logger.info("Extracting skills from resume...")
      resume_skills = extract_skills(resume_text)

      logger.info("Extracting skills from job description...")
      jd_skills = extract_skills(jd_text)

      matched_skills, missing_skills = compare_skills(resume_skills, jd_skills)
      logger.info(f'Matched Skills:{len(matched_skills)}| Missing Skills:{len(missing_skills)}')

      result = compute_ats_score(
        resume_text=resume_text,
        jd_text=jd_text,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )
      report = format_score_report(
        ats_score=result.ats_score,
        keyword_score=result.keyword_score,
        semantic_score=result.semantic_score,
        section_score=result.section_score,
        matched_skills=result.matched_skills,
        missing_skills=result.missing_skills,
        sections_found=result.sections_found,
    )
      print(report)
      recommendations = generate_recommendations(
        result.missing_skills,
        result.sections_found
    )

      print("Recommendations:")
      for rec in recommendations:
        print(f"- {rec}")

## CLI 
def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
         prog="app.py",
         description="AI Resume Intelligence Platform - ATS Scoring",
         formatter_class=argparse.RawDescriptionHelpFormatter,
         epilog=(
            "Examples:\n"
            "  python app.py --demo\n"
            "  python app.py --resume resume.pdf\n"
            "  python app.py --resume resume.pdf --jd job_description.txt\n"
        ),
     )
    parser.add_argument(
         "--resume",
          metavar="RESUME_PATH",
          type=str,
          help="Path to the resume PDF file")
    
    parser.add_argument(
         "--jd", 
         metavar="JD_PATH",
         type=str,
           help="Path to the job description text file (optional)")
    
    parser.add_argument(
         "--demo--",
         type = str,
         choices = ["pymupdf", "pdfplumber"],
         default="pymupdf",
         help = "Preferred PDF parser (default: pymupdf). Falls back to the other if unavailable."
    )

    parser.add_argument(
         "--demo",
         action="store_true",
         help="Run with built-in demo resume and JD")
    
    parser.add_argument(
         "--debug",
         action = "store_true",
         help="Enable verbose debug logging.",
    )
    return parser

def main() -> None:
    """
    Main entry point. Parses CLI arguments and runs the ATS pipeline.
    """
    arg_parser = build_arg_parser()
    args = arg_parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    set_logging(log_level)
    logger = logging.getLogger(__name__)

    if args.demo:
        logger.info("Running in DEMO mode with built-in resume and JD.")
        resume_text = DEMO_RESUME_TEXT
        jd_text = EXAMPLE_JD

    elif args.resume:
        resume_path = Path(args.resume)
        if not resume_path.exists():
            logger.error(f"Resume file not found: {resume_path}")
            sys.exit(1)

        logger.info(f"Parsing resume: {resume_path.name}")
        resume_text = parse_resume(str(resume_path), preferred_parser=args.parser)

        if args.jd:
            jd_path = Path(args.jd)
            if not jd_path.exists():
                logger.error(f"JD file not found: {jd_path}")
                sys.exit(1)
            jd_text = jd_path.read_text(encoding="utf-8")
            logger.info(f"Loaded JD from: {jd_path.name}")
        else:
            logger.info("No JD file provided — using built-in example JD.")
            jd_text = EXAMPLE_JD

    else:
        arg_parser.print_help()
        sys.exit(0)

    run_ats_pipeline(resume_text=resume_text, jd_text=jd_text)

## GENERATE RECOMMENDATIONS 

def generate_recommendations(missing_skills, sections_found):
    recommendations = []

    missing_sections = [sec for sec, present in sections_found.items() if not present]

    if missing_sections:
        recommendations.append(f"Add missing sections: {', '.join(missing_sections)}")

    if missing_skills:
        recommendations.append(f"Consider adding skills: {', '.join(missing_skills[:5])}")

    if "communication" in missing_skills:
        recommendations.append("Highlight soft skills like communication and leadership")

    if "power bi" in missing_skills or "tableau" in missing_skills:
        recommendations.append("Add BI tools like Power BI or Tableau")

    return recommendations


if __name__ == "__main__":
    main()



