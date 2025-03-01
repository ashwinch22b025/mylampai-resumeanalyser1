from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any
import io
import logging
import os
import sys
# from llm_reviewer.agent import *
from llm_reviewer.brevity import *
from llm_reviewer.style import *
from llm_reviewer.impact import *
from llm_reviewer.jd import structure_jd,calculate_score_llm
from utils.utils import *
from llm_reviewer.summary_prompt import master_prompt
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize FastAPI app

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

class TextInputJob(BaseModel):
    job_text: str

class DictInput(BaseModel):
    extracted_data: Dict[str, Any]

class StyleInput(BaseModel):
    extracted_data: Dict[str, Any]
    profile:str =  "Full Stack Web Development"

class SkillCheckerRequest(BaseModel):
    hard_skills: List[str]
    soft_skills: List[str]
    profile: str = "Full Stack Web Development"

import re

def clean_text(text):
    # Remove single quotes
    text = re.sub(r"'", "", text)
    
    # Remove double quotes
    text = re.sub(r'"', '', text)
    
    return text

@app.post("/summary")
async def summary_resume(cv_text:TextInput):
    try:
        return {"message": master_prompt(clean_text(cv_text.cv_text))}
    except Exception as e:
        logger.error(f"Error extracting Summary data: {e}")
        raise HTTPException(status_code=500, detail="Error extracting Summary data")

@app.post("/style_check")
async def style_check(data: StyleInput):
    try:
        resp = style_checker(data.extracted_data,data.profile)
        return {"message":resp}
    except Exception as e:
        logger.error(f"Error extracting Style data: {e}")
        raise HTTPException(status_code=500, detail="Error extracting Style data")

@app.post("/spell_verb_checker")
async def spell_verb_checker(data:DictInput):
    try:
        input = "\n".join(data.extracted_data["Description"])
        return {"message": text_analyzer(input)}
    except Exception as e:
        logger.error(f"Error checking verb tense: {e}")
        raise HTTPException(status_code=500, detail="Error checking verb tense")
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

@app.post("/structure_job_description")
async def extract_job_description(input : TextInputJob):
    try:
        return {"message": structure_jd(input.job_text)}
    except Exception as e:
        logger.error(f"Error extracting structured data: {e}")
        raise HTTPException(status_code=500, detail="Error extracting structured data")
    
@app.post("/job_description_resume_score")
async def calculate_score(cv_text:TextInput, job_text : TextInputJob):
    try:
        scores = calculate_score_llm(clean_text(cv_text.cv_text),job_text.job_text)
        hard_skills_score = scores["HARD_SKILLS_SCORE"]['score']
        soft_skills_score = scores["SOFT_SKILLS_SCORE"]['score']
        experience_score = scores["EXPERIENCE_SCORE"]['score']
        education_score = scores["EDUCATION_SCORE"]['score']
        final_score = int((((0.4 * hard_skills_score) + (0.2 * experience_score) + (0.2 * education_score) + (0.2 * soft_skills_score))/175)*100)
        return {"message": {"FINAL_SCORE":final_score,"DETAILS":scores}}
    except Exception as e:
        logger.error(f"Error extracting structured data: {e}")
        raise HTTPException(status_code=500, detail="Error extracting structured data")
 

# Endpoint to extract structured data from text
@app.post("/extract_structured_data")
async def extract_data(input: TextInput):
    try:
        logger.info(f"Original text: {input.cv_text}")
        cleaned_text = clean_text(input.cv_text)
        logger.info(f"Cleaned text: {cleaned_text}")
        return {"message": extract_structured_data(cleaned_text)}
    except Exception as e:
        logger.error(f"Error extracting structured data: {e}")
        raise HTTPException(status_code=500, detail="Error extracting structured data")

# Endpoint for quantification analysis
@app.post("/quantification")
async def analyze_quantification(data:DictInput):
    try:
        input = data.extracted_data["Description"]
        return {"message": quantification(input)}
    except Exception as e:
        logger.error(f"Error analyzing quantification: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing quantification")

# Endpoint for repetition analysis
@app.post("/repetition")
async def analyze_repetition(data: DictInput):
    try:
        input = "\n".join(data.extracted_data["Description"])
        length = len(data.extracted_data["Description"])
        return {"message": repetition(input,length)}
    except Exception as e:
        logger.error(f"Error analyzing repetition: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing repetition")

# Endpoint for weak verb checking
@app.post("/weak_verb_checker")
async def check_weak_verbs(data: DictInput):
    try:
        input = "\n".join(data.extracted_data["Description"])
        return {"message": weak_verb_checker(input)}
    except Exception as e:
        logger.error(f"Error checking weak verbs: {e}")
        raise HTTPException(status_code=500, detail="Error checking weak verbs")

# Endpoint for verb tense checking
@app.post("/verb_tense")
async def check_verb_tense(data: DictInput):
    try:
        input = "\n".join(data.extracted_data["Description"])
        return {"message": verb_tense(input)}
    except Exception as e:
        logger.error(f"Error checking verb tense: {e}")
        raise HTTPException(status_code=500, detail="Error checking verb tense")

# Endpoint for responsibility analysis
@app.post("/responsibility")
async def analyze_responsibility(data: DictInput):
    try:
        input = "\n".join(data.extracted_data["Description"])
        print(inout)
        return {"message": responsibility(input)}
    except Exception as e:
        logger.error(f"Error analyzing responsibility: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing responsibility")

# Endpoint for spelling checking
@app.post("/spelling_checker")
async def check_spelling(data: DictInput):
    try:
        input = "\n".join(data.extracted_data["Description"])
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
async def analyze_bullet_point_length(data: DictInput):
    try:
        input = "\n".join(data.extracted_data["Description"])
        return {"message": bullet_point_length(input)}
    except Exception as e:
        logger.error(f"Error analyzing bullet point length: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing bullet point length")

# Endpoint for total bullet list analysis
@app.post("/total_bullet_list")
async def analyze_total_bullet_list(data:DictInput):
    try:
        input = "\n".join(data.extracted_data["Description"])
        return {"message": total_bullet_list(input)}
    except Exception as e:
        logger.error(f"Error analyzing total bullet list: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing total bullet list")

# Endpoint to improve bullet points
@app.post("/bullet_points_improver")
async def improve_bullet_points(data: DictInput):
    try:
        input = "\n".join(data.extracted_data["Description"])
        return {"message": bullet_points_improver(input)}
    except Exception as e:
        logger.error(f"Error improving bullet points: {e}")
        raise HTTPException(status_code=500, detail="Error improving bullet points")

# Endpoint for personal info checking
@app.post("/personal_info")
async def check_personal_info(data: DictInput):
    try:
        input = "\n".join(data.extracted_data["Personal Information"])
        return {"message": personal_info(input)}
    except Exception as e:
        logger.error(f"Error checking personal info: {e}")
        raise HTTPException(status_code=500, detail="Error checking personal info")

# Endpoint for section checking
@app.post("/section_checker")
async def check_sections(data: DictInput):
    try:
        input = "\n".join(data.extracted_data["Sections"])
        return {"message": section_checker(input)}
    except Exception as e:
        logger.error(f"Error checking sections: {e}")
        raise HTTPException(status_code=500, detail="Error checking sections")

# Endpoint for skill checking
@app.post("/skill_checker")
async def check_skills(data: DictInput, profile :str):
    try:
        hard_skills = data.extracted_data["Skills"]["HARD"]
        soft_skills = data.extracted_data["Skills"]["SOFT"]
        profile = profile
        return {"message": skill_checker(hard_skills, soft_skills, profile)}
    except Exception as e:
        logger.error(f"Error checking skills: {e}")
        raise HTTPException(status_code=500, detail="Error checking skills")

if __name__ == "__main__":
    uvicorn.run(app)