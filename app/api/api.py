from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any
import io
import logging
import os
import sys
from app.llm_reviewer.agent import *
from app.llm_reviewer.brevity import *
from app.llm_reviewer.style import *
from app.llm_reviewer.impact import *
from app.utils.utils import *

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Pydantic models
class ResumeAnalysisRequest(BaseModel):
    text: str
    experience: str = "FRESHERS"

class TextList(BaseModel):
    points_to_check: List[str]

class TextInput(BaseModel):
    cv_text: str

class DictInput(BaseModel):
    data: Dict[str, Any]

class SkillCheckerRequest(BaseModel):
    hard_skills: List[str]
    soft_skills: List[str]
    profile: str = "Full Stack Web Development"

# Unified Request Model for Analysis

class UnifiedAnalysisRequest(BaseModel):
    action: str
    points_to_check: List[str] = None
    cv_text: str = None
    hard_skills: List[str] = None
    soft_skills: List[str] = None
    profile: str = "Full Stack Web Development"
    data: Dict[str, Any] = None
    experience: str = "FRESHERS"

# Endpoint to extract text from PDF
@app.post("/extract_text_from_pdf")
async def extract_pdf_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        pdf_data = extract_text_from_pdf(pdf_file)
        return {"message": pdf_data}
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=500, detail="Error extracting text from PDF")


# Endpoint to extract structured data from text
@app.post("/extract_structured_data")
async def extract_data(input: TextInput):
    try:
        return {"message": extract_structured_data(input.cv_text)}
    except Exception as e:
        logger.error(f"Error extracting structured data: {e}")
        raise HTTPException(status_code=500, detail="Error extracting structured data")

# Endpoint for quantification analysis
@app.post("/quantification")
async def analyze_quantification(data:DictInput):
    try:
        input = "\n".join(data["Description"])
        return {"message": quantification(input)}
    except Exception as e:
        logger.error(f"Error analyzing quantification: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing quantification")

# Endpoint for repetition analysis
@app.post("/repetition")
async def analyze_repetition(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": repetition(input)}
    except Exception as e:
        logger.error(f"Error analyzing repetition: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing repetition")

# Endpoint for weak verb checking
@app.post("/weak_verb_checker")
async def check_weak_verbs(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": weak_verb_checker(input)}
    except Exception as e:
        logger.error(f"Error checking weak verbs: {e}")
        raise HTTPException(status_code=500, detail="Error checking weak verbs")

# Endpoint for verb tense checking
@app.post("/verb_tense")
async def check_verb_tense(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": verb_tense(input)}
    except Exception as e:
        logger.error(f"Error checking verb tense: {e}")
        raise HTTPException(status_code=500, detail="Error checking verb tense")

# Endpoint for responsibility analysis
@app.post("/responsibility")
async def analyze_responsibility(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": responsibility(input)}
    except Exception as e:
        logger.error(f"Error analyzing responsibility: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing responsibility")

# Endpoint for spelling checking
@app.post("/spelling_checker")
async def check_spelling(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": spelling_checker(input)}
    except Exception as e:
        logger.error(f"Error checking spelling: {e}")
        raise HTTPException(status_code=500, detail="Error checking spelling")

# Endpoint for resume length analysis
@app.post("/resume_length")
async def analyze_resume_length(request: ResumeAnalysisRequest):
    try:
        return {"message": resume_length(request.text, request.experience)}
    except Exception as e:
        logger.error(f"Error analyzing resume length: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing resume length")

# Endpoint for bullet point length analysis
@app.post("/bullet_point_length")
async def analyze_bullet_point_length(data):
    try:
        return {"message": bullet_point_length(input.points_to_check)}
    except Exception as e:
        logger.error(f"Error analyzing bullet point length: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing bullet point length")

# Endpoint for total bullet list analysis
@app.post("/total_bullet_list")
async def analyze_total_bullet_list(cv_data,experience):
    try:
        return {"message": total_bullet_list(cv_data,experience)}
    except Exception as e:
        logger.error(f"Error analyzing total bullet list: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing total bullet list")

# Endpoint to improve bullet points
@app.post("/bullet_points_improver")
async def improve_bullet_points(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": bullet_points_improver(input)}
    except Exception as e:
        logger.error(f"Error improving bullet points: {e}")
        raise HTTPException(status_code=500, detail="Error improving bullet points")

# Endpoint for personal info checking
@app.post("/personal_info")
async def check_personal_info(data):
    try:
        input = "\n".join(data["Personal Information"])
        return {"message": personal_info(input)}
    except Exception as e:
        logger.error(f"Error checking personal info: {e}")
        raise HTTPException(status_code=500, detail="Error checking personal info")

# Endpoint for section checking
@app.post("/section_checker")
async def check_sections(data):
    try:
        input = "\n".join(data["Sections"])
        return {"message": section_checker(input)}
    except Exception as e:
        logger.error(f"Error checking sections: {e}")
        raise HTTPException(status_code=500, detail="Error checking sections")

# Endpoint for skill checking
@app.post("/skill_checker")
async def check_skills(data, profile):
    try:
        hard_skills = data["Skills"]["HARD"]
        soft_skills = data["Skills"]["SOFT"]
        profile = profile
        return {"message": skill_checker(hard_skills, soft_skills, profile)}
    except Exception as e:
        logger.error(f"Error checking skills: {e}")
        raise HTTPException(status_code=500, detail="Error checking skills")

@app.post("/analyze")
async def unified_analysis(request: UnifiedAnalysisRequest):
    try:
        # Action mapping
        action_map = {
            "quantification": lambda: quantification("\n".join(request.points_to_check or [])),
            "repetition": lambda: repetition("\n".join(request.points_to_check or [])),
            "weak_verb_checker": lambda: weak_verb_checker("\n".join(request.points_to_check or [])),
            "verb_tense": lambda: verb_tense("\n".join(request.points_to_check or [])),
            "responsibility": lambda: responsibility("\n".join(request.points_to_check or [])),
            "spelling_checker": lambda: spelling_checker("\n".join(request.points_to_check or [])),
            "resume_length": lambda: resume_length(request.cv_text, request.experience),
            "bullet_point_length": lambda: bullet_point_length(request.points_to_check),
            "total_bullet_list": lambda: total_bullet_list(request.cv_text.split("\n"), request.experience),
            "bullet_points_improver": lambda: bullet_points_improver("\n".join(request.points_to_check or [])),
            "personal_info": lambda: personal_info("\n".join(request.data.get("Personal Information", []))),
            "section_checker": lambda: section_checker("\n".join(request.data.get("Sections", []))),
            "skill_checker": lambda: skill_checker(request.hard_skills, request.soft_skills, request.profile),
        }

        if request.action not in action_map:
            raise HTTPException(status_code=400, detail=f"Invalid action '{request.action}'.")

        # Execute corresponding function
        result = action_map[request.action]()
        return {"message": result}
    except Exception as e:
        logger.error(f"Error performing analysis for action '{request.action}': {e}")
        raise HTTPException(status_code=500, detail=f"Error performing analysis: {str(e)}")