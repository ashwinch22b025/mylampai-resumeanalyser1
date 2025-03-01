import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import *
import json

def resume_length(text, experience = "FRESHERS"):
    length = len(text)
    result = ""
    score = 0
    if experience=="FRESHERS":
        if length>450 and length<850:
            result = "This is Good Length For Your Resume"
        else:
            result =  "The Length could be little smaller"
    else:
        result = "This is Good Length For Your Resume"
    return {"Result":result} 

def bullet_point_length(text_list):
    big_points_list = [point for point in text_list if len(point)>140]
    return {"Result":big_points_list}

def total_bullet_list(text_list, experience = "FRESHERS"):
    result = ""
    if len(text_list)>15 and experience=="FRESHERS":
         result = "This Contains more Bullet Points than required"
    else:
        result = "This could contain more bullet points"
    return {"Result":result}


def bullet_points_improver(text_to_check):
    improver_prompt = """
    You are a professional resume writer with expertise in crafting impactful bullet points for job seekers in various industries. Your task is to analyze and enhance a list of resume bullet points.

    For each bullet point:

    1. Evaluate its effectiveness in showcasing the candidate's skills and achievements.
    2. If the bullet point is weak or ineffective, create an improved version that is:
    - Clear and concise
    - Results-oriented
    - Impactful and engaging

    When improving bullet points:
    - Use strong, specific action verbs
    - Quantify achievements with relevant metrics where possible
    - Highlight key skills and competencies
    - Remove unnecessary words or phrases that dilute the impact
    - Ensure relevance to the job or industry

    Provide your analysis in a JSON format as follows:
    Based on your analysis of everything, judge and provide a score between (0-100).Reach the score with proper reason and analysis. 
    {
    "score":<integer_score>,
    "bulletPoints": [
        {
        "original": "Original weak bullet point text",
        "improved": "Enhanced, more impactful version"
        },
        {
        "original": "Another weak bullet point",
        "improved": "Its improved, more detailed counterpart"
        }
    ]
    }

    Only include bullet points that require improvement. If a bullet point is already strong and effective, do not include it in the output.

    Examples of improvements:
    - Weak: "Responsible for managing team projects"
    Strong: "Led cross-functional team of 8 to complete 5 high-priority projects, resulting in 20% increase in departmental efficiency"
    - Weak: "Helped with customer service"
    Strong: "Resolved 50+ customer inquiries daily, maintaining a 98% satisfaction rate and reducing response time by 25%"

    Ensure your response begins with "```json" and ends with "```" to properly format the JSON output.

    Remember, your goal is to transform each weak bullet point into a powerful statement that effectively communicates the candidate's value to potential employers.
    """.strip()
    bulletpoint_improver_bot = Agent(improver_prompt)
    bulletpoint_improver_bot_res = bulletpoint_improver_bot(text_to_check)
    bulletpoint_improver_bot_res  = bulletpoint_improver_bot_res .strip().strip('```json').strip('```')
    json_file = json.loads(bulletpoint_improver_bot_res)
    return json_file


