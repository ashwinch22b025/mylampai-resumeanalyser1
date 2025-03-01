import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import *
import json

def structure_jd(text_to_check):
    jd_prompt = """
    You will be provided with text that is either a job description or a job profile. Your task is to:

        Carefully analyze the provided text.
        Determine whether it's a job description or a job profile.
        Generate a JSON output based on the following criteria:

        If it's a job profile:

        Create a JSON object with the following keys: "HARD SKILLS", "SOFT SKILLS", "EXPERIENCE", and "EDUCATION".
        Generate appropriate values for each key based on the profile.
        Set "EXPERIENCE" as "Fresher" and "EDUCATION" as "Bachelor's degree in any domain".
        Infer and generate suitable "HARD SKILLS" and "SOFT SKILLS" based on the profile.

        If it's a job description:

        Create a JSON object with the same keys: "HARD SKILLS", "SOFT SKILLS", "EXPERIENCE", and "EDUCATION".
        Extract and populate the values for each key directly from the provided job description.

        In both cases:

        The Output must start with "```json" and trail with "```".
        List skills as arrays of strings.
        Keep the output concise and relevant.

        Here's the structure for your response:
        The JSON output in the specified format.
        Example output format:
        ```json{
        "CATEGORY" : "Specify Whether it is a Job Description or Job Profile",
        "PROFILE" : "Mention THe Profile for which the job is",
        "HARD SKILLS": ["Skill 1", "Skill 2", "Skill 3"],
        "SOFT SKILLS": ["Skill 1", "Skill 2", "Skill 3"],
        "EXPERIENCE": "Relevant experience information",
        "EDUCATION": "Required education information"
        }```
    """
    bot_quatify = Agent(jd_prompt)
    bot_quatify_resp = bot_quatify(str(text_to_check))
    print(bot_quatify_resp)
    json_file = json.loads(bot_quatify_resp.strip().strip("```json").strip("```"))
    print(json_file)
    return json_file

def calculate_score_llm(cv_text, job_text):
    score_prompt = """
       You will be provided with a job description (JD) and a resume. Your task is to analyze the resume against the JD requirements, assign scores in four categories, and provide detailed reasons for each score. Follow these guidelines strictly:

        1. Hard Skills Matching (0-100 points):
            Identify all hard skills mentioned in the JD.
            Assign weights to each skill (higher for mandatory skills, lower for preferred skills).
            Check for each skill's presence in the resume, considering only exact matches or very close synonyms.
            Calculate the score as: (Sum of weights of matched skills / Total sum of weights) * 100
            Apply a 20% penalty if any mandatory skills are missing.
            Round the result to the nearest integer.

        2. Soft Skills Matching (0-100 points):

            List all soft skills mentioned in the JD.
            For each soft skill, search for explicit mentions in the resume. Do not infer soft skills from general descriptions.
            Assign 100 / (total number of soft skills) points for each exact match.
            Apply a 50% reduction to the final score if less than half of the required soft skills are explicitly mentioned.
            Sum the points and round to the nearest integer.

        3. Experience Matching (0-100 points):
            a) If JD specifies required years of experience or specific roles/projects:

            Identify the required years of experience or specific roles/projects mentioned in the JD.
            Review each project mentioned in the RESUME.
            Award (100 / number of required roles/projects) points for each relevant project exactly matching JD requirements.
            Subtract (50 / number of required roles/projects) points for each irrelevant project mentioned in the RESUME.
            Apply a 25% penalty if the total years of experience are less than required.
            Ensure the final score doesn't go below 0 or above 100.

            b) If JD only specifies "Fresher" or doesn't provide specific experience requirements:

            Review each project and its bullet points mentioned in the RESUME.
            For each project:

            Assess relevance to specific entry-level skills mentioned in the JD.
            Award up to 15 points based on the project's direct relevance to the job requirements.


            For each bullet point within projects:

            Award 1 point for relevant skills or achievements explicitly mentioned in the JD.
            Maximum 5 points per project from bullet points.


            Sum all points from projects and bullet points.
            If total exceeds 100, cap the final score at 100.

            c) For both scenarios:

            Sum the points and round to the nearest integer.
            Provide a brief justification for the score, highlighting key matching experiences or skills and noting any significant gaps.
        4. Education Matching (0-100 points):

            Identify the required education level and field in the JD.
            Compare with the resume's education section:
            Award 100 points for an exact match in both level and field.
            Award 75 points for matching level but slightly different field.
            Award 50 points for matching field but lower level.
            Award 25 points for related field and level.
            Award 0 points for unrelated education.
            Apply a 50% penalty if the education is incomplete or in progress.
            
        Provide your output as a JSON object starting with '```json' and trailing with '```' with the following structure:

        ```json
        {
        "HARD_SKILLS_SCORE": {
        "score": <integer_value>,
        "reason": "<detailed explanation of the score, including matched and missing skills>"
        },
        "SOFT_SKILLS_SCORE": {
        "score": <integer_value>,
        "reason": "<detailed explanation of the score, listing matched soft skills and any notable absences>"
        },
        "EXPERIENCE_SCORE": {
        "score": <integer_value>,
        "reason": "<detailed explanation of the score, comparing required experience with the candidate's experience>"
        },
        "EDUCATION_SCORE": {
        "score": <integer_value>,
        "reason": "<detailed explanation of the score, comparing required education with the candidate's qualifications>"
        }
        }```
    """
    bot_quatify = Agent(score_prompt)
    bot_quatify_resp = bot_quatify(str(f"### RESUME TEXT {cv_text}, ### JOB {job_text}"))
    print(bot_quatify_resp)
    json_file = json.loads(bot_quatify_resp.strip().strip("```json").strip("```"))
    print(json_file)
    return json_file

resume_text = """HARSH BHATT | 23CH10030
Indian Institute of Technology Kharagpur
Education
Program Institution %/CGPA Year
B.Tech, Chemical Engineering Indian Institute of Technology Kharagpur 8.94 2024
Class XII, CBSE Kota 90 2023
Class X, CBSE Kota 89 2021
Scholastic Achievements
○ Secured All India Rank of 4944 in JEE Advanced 2024(out of 1,72,000 candidates).
○ Secured All India Rank of 1804 in JEE Mains 2024(out of 12,00,000 candidates).
○ Secured 1st position in Inter-IIT Street Play Competition.
○ Secured 1st position in Spring Fest Street Play Competition.
○ Secured 2nd position in Open-IIT Stand-up Competition.
○ Secured 3rd position in Open-IIT Monologue Competition.
Projects
Tech Intern at Renew Heat
○ Developed a website for aggregating thrifting stores across India, enhancing accessibility and visibility for sustainable shopping
options.
○ Demonstrated profi ciency in web development and front-end development, utilizing technologies such as HTML, CSS, JavaScript, and
frameworks like React.js and Next.js to create a user-friendly interface.
○ Integrated APIs to provide real-time updates and information on store inventories and locations.
Stock Price Prediction
○ ○ Developed a machine learning algorithm to predict stock market actions (Buy/Sell/Hold) for investors.
○ Implemented data preprocessing and feature engineering techniques to prepare historical stock price data for modeling.
○ Evaluated model performance using metrics like accuracy, precision, and F1-score to ensure robust predictions.
○ Enhanced the model by incorporating technical indicators and sentiment analysis for more accurate decision-making support.
○ Project available on Colab: {https://colab.research.google.com/drive/101Qvgqy5osrxz-p6Qm7GS3G4QNZJRHZ8?usp=sharing}
Bank Customer Churn Prediction
○ ○ Collaborated with Profs to develop a machine learning algorithm for predicting customer churn in the banking sector.
○ Applied and fi ne-tuned multiple machine learning models, including Logistic Regression, Random Forest, and Gradient Boosting, to
achieve optimal prediction accuracy.
○ Evaluated model performance using metrics such as accuracy, precision, recall, and the ROC-AUC curve.
○ Project available on Kaggle: { https://www.kaggle.com/code/iharshbhatt/bank-customer-churn-prediction }
Hexagonal Game of Life Simulation
○ ○ Developed a Python-based simulation of Conway's Game of Life using a hexagonal grid structure.
○ Implemented custom rules for cell resurrection and natural survival, adding complexity to the classic cellular automaton.
○ Employed matplotlib.animation.FuncAnimation to create an animated display of the evolving grid over multiple generations.
○ Project available on Colab : { https://colab.research.google.com/drive/1XYG7HfvtbbISdP6oPD6kpmqpuc506sgt?usp=sharing }
Course Work
○ Deep Learning ○ Blockchain Technology
○ Machine Learning ○ Artifi cial Intelligence
○ Programming and Data structures ○ Quantitative Finance
Skills
○ Programming Languages: Python, C++, C, JavaScript, HTML, CSS
○ Frameworks and Libraries: Pandas, Numpy, Matplot, Seaborn, Scikit-Learn, Bootstrap,React.js, Node.js, Next.js, Express
Extra - Curricular Activities
○ AI Geek at the Institute ML/AI Society (Spark4AI)
○ Member of the Institute Blockchain Society (Kharagpur Blockchain Society)
○ Quant Trainee at the Institute Quantitative Finance Club (Quant Club)
○ Part of the Institute Dramatics Society (Pravah)
○ Part of the institute Comedy Club (TCC)"""

job_profile = """"HARD SKILLS": ["HTML", "CSS", "JavaScript", "Node.js", "React", "Angular", "Vue.js"],
    "SOFT SKILLS": ["Problem-solving", "Teamwork", "Time management", "Communication"],
    "EXPERIENCE": "Fresher",
    "EDUCATION": "Bachelor's degree in any domain"""
if __name__ == "__main__":
    #structure_jd("Full Stack WEb Developer")
    calculate_score_llm(resume_text,job_profile)