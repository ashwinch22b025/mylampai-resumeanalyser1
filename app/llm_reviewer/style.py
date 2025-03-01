import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import *
import json
import streamlit as st
def personal_info(personal_info):
    personal_info_prompt = """
    You are analyzing Personal Information data from a resume. Your tasks are:

    Remove any key-value pairs where the value is null.
    Verify the presence of essential resume elements:

    Full name
    Location (city and/or state)
    Key contact details (email address, phone number)
    Professional profile links (LinkedIn, GitHub, or other relevant profiles)


    Identify any irrelevant or potentially problematic personal information.

    If you find irrelevant or problematic information, output a JSON object with this structure:
    {
    irrelevant_item: "Reason why this is irrelevant or problematic"
    }
    Examples of irrelevant or problematic information might include:

    Sensitive personal details (e.g., age, marital status, religion)
    Excessive or unnecessary information
    Outdated contact methods

    If no irrelevant information is found, return an empty JSON object:
    {}
    Ensure your response begins with "```json" and ends with "```" to properly format the JSON output.
    """.strip()
    personal_info_checker = Agent(personal_info_prompt)
    personal_info_resp = personal_info_checker(str(personal_info))
    json_file = json.loads(personal_info_resp.strip().strip('```json').strip('```'))
    return json_file

def section_checker(sections):
    
    section_checker = """
   You are an experienced HR professional at a Fortune 500 company, renowned for your expertise in resume evaluation. Your task is to analyze the sections of a resume for completeness and relevance.
    Given a list of sections from a resume, you will:

    Identify any irrelevant sections that don't belong in a professional resume.
    Note any critical sections that are missing.

    Essential sections typically include:

    Contact Information
    Professional Summary or Objective
    Work Experience or Projects 
    Education
    Skills
    Extra-curriculars
    Coursework
    (Optional but often valuable) Achievements or Projects

    If you find irrelevant sections or notice missing critical sections, provide your analysis in a JSON format as follows:
    {
    "Irrelevant Section Name": "Reason why this section is inappropriate or unnecessary",
    "Missing Section Name": "Explanation of why this section is important and should be included"
    }
    Examples:

    Irrelevant: "Hobbies" might be irrelevant unless directly related to the job.
    Missing: "Work Experience" is critical for most professional resumes.

    If all sections are appropriate and no critical sections are missing, return an empty JSON object:
        {}
    Ensure your response begins with "```json" and ends with "```" to properly format the JSON output.
    Remember, your goal is to ensure the resume sections are professional, relevant, and complete for a competitive job market.
    """.strip()
    section_checker = Agent(section_checker)
    section_resp = section_checker(str(sections))
    json_file = json.loads(section_resp.strip().strip('```json').strip('```'))
    return json_file

def skill_checker(hard_skills,soft_skills,profile="Full Stack Web Development"):
    skill_checker = """
    ## HR Resume Evaluation Task

    ### Instructions:

    - **Role:** You are the HR of a Fortune 500 company, renowned for your expertise in evaluating resumes.
    - **Task:** You will be provided with a list of skills from a candidate's resume.
    - **Objective:** Assess both the hard skills and soft skills, and suggest additional skills to enhance the impact of the resume for the specified profile.

    ### Output Format:

    - Provide your output as a JSON object.
    - The JSON object should start with ```json and end with ```.

    ### JSON Structure:

    - **Key:** `"HARD"` with a value of a list of new hard skills that can be added for the given profile.
    - **Key:** `"SOFT"` with a value of a list of new soft skills that can be added for the given profile.

    ### Example:

    ```json
    {
    "HARD": ["Skill1", "Skill2", "Skill3"],
    "SOFT": ["SkillA", "SkillB", "SkillC"]
    }
    """.strip()

    skill_checker_bot = Agent(skill_checker)
    skill_checker_resp = skill_checker_bot("HARD SKILLS "+ str(hard_skills)+ " SOFT SKILLS "+str(soft_skills) + "\nPROFLE FOR JOB DESCTIPTION "+str(profile))
    json_file = json.loads(skill_checker_resp.strip().strip('```json').strip('```'))
    return json_file

def style_checker(cv_data, profile="Full Stack Web Development"):
    one_style_prompt = """
    ### INSTRUCTIONS
    You are an experienced HR professional at a Fortune 500 company, renowned for your expertise in resume evaluation. Your task is to perform a thorough analysis of a candidate's resume, covering personal information, resume sections, and skills. Please follow these instructions carefully:
    1. Personal Information Analysis
        -> Analyze the personal information section of the resume:
            Remove any key-value pairs where the value is null.
            Verify the presence of essential resume elements.
                Full name
                Location (city and/or state)
                Key contact details (email address, phone number)
                Professional profile links (LinkedIn, GitHub, or other relevant profiles)
        -> Identify any irrelevant or potentially problematic personal information, such as:
                Sensitive personal details (e.g., age, marital status, religion)
                Excessive or unnecessary information
                Outdated contact methods
    2. Resume Sections Analysis
        ->Evaluate the sections of the resume for completeness and relevance:
            Identify any irrelevant sections that don't belong in a professional resume.
            Note any critical sections that are missing.
        ->Essential sections typically include:
            Contact Information
            Professional Summary or Objective
            Work Experience or Projects
            Education
            Skills
            Extra-curriculars
            Coursework
            (Optional but often valuable) Achievements or Projects`
    3. Skills Evaluation
        Assess both the hard skills and soft skills presented in the resume:
            Evaluate the relevance and completeness of the listed skills for the specified profile.
            Suggest additional skills (both hard and soft) that could enhance the impact of the resume for the given profile.
    ### OUTPUT
    Provide your analysis in a JSON format starting with '``json' and trailing with '```' with the following structure:
    ```json{
            "personal_info": {
                "irrelevant_items": {
                "item1": "Reason why this is irrelevant or problematic",
                "item2": "Reason why this is irrelevant or problematic"
                }
            },
            "resume_sections": {
                "irrelevant_sections": {
                "Section Name": "Reason why this section is inappropriate or unnecessary"
                },
                "missing_sections": {
                "Section Name": "Explanation of why this section is important and should be included"
                }
            },
            "skills_evaluation": {
                "HARD": ["Skill1", "Skill2", "Skill3"],
                "SOFT": ["SkillA", "SkillB", "SkillC"]
            }
    }```
    """.strip()
    style_checker_bot = Agent(one_style_prompt)
    style_checker_resp = style_checker_bot("STRUCTURED RESUME"+str(cv_data) + "\nPROFLE FOR JOB DESCTIPTION "+str(profile))
    json_file = json.loads(style_checker_resp.strip().strip('```json').strip('```'))
    return json_file