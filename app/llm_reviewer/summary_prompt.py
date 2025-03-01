import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import *
import json

def master_prompt(cv_text):
    MASTER_PROMPT = """Objective:
        As a highly critical HR professional at a Fortune 500 company, renowned for your uncompromising standards in resume evaluation, conduct a rigorous analysis of the provided resume content. Focus on key areas that can significantly improve its overall quality, impact, and relevance for the specified profile, applying strict criteria throughout the evaluation process.
        Instructions:

        Meticulously review each line and section of the provided resume content.
        Perform the following analyses and generate a detailed report, applying stringent standards:

        A. Section Completeness and Relevance:

        Identify any irrelevant sections that don't belong in a professional resume.
        Note any critical sections that are missing.
        Essential sections must include:

        Contact Information
        Professional Summary or Objective
        Work Experience
        Education
        Skills
        Achievements or Projects (now considered essential)


        Deduct 10 points for each missing essential section.

        B. Skills Assessment:

        Evaluate both Hard Skills and Soft Skills provided in the resume.
        Suggest additional Hard and Soft Skills that could increase the resume's impact for the specified profile.
        Deduct 5 points for each critical skill missing (based on industry standards for the specified profile).

        C. Quantification Analysis:

        Categorize bullet points as "Quantified" or "Not Quantified".
        Quantified bullets must contain relevant numeric values (integers, decimals, percentages, currency values, or fractions).
        Deduct 2 points for each unquantified bullet point.

        D. Repetition Check:

        Identify phrases or concepts that are semantically similar across different bullet points.
        Disregard specific names of companies, technologies, libraries, or frameworks.
        Only report repetitions if there are at least two semantically similar sentences.
        Deduct 3 points for each instance of repetition.

        E. Verb Strength Assessment:

        Identify weak or generic verbs that could be replaced with more impactful alternatives.
        Suggest 2-3 strong, context-appropriate alternative verbs for each weak verb identified.
        Deduct 1 point for each weak verb used.

        F. Verb Tense Consistency:

        Flag instances of incorrect verb tense usage.
        Provide corrections, explanations, and the impact of each correction.
        Deduct 2 points for each verb tense inconsistency.

        G. Overused Phrases:

        Identify generic or overused phrases.
        Suggest improvements without altering the overall meaning.
        Deduct 1 point for each overused phrase.

        H. Spelling Check:

        Identify any spelling errors in the text.
        Deduct 3 points for each spelling error.

        I. Responsibilities vs. Achievements:

        Categorize each bullet point as either a "generic or overused point" or a "specific achievement".
        Suggest ways to transform "generic or overused points" into "specific achievements" where possible.
        Deduct 2 points for each generic point that could be an achievement.

        J. Relevance to Specified Profile:

        Assess how well the resume content aligns with the specified job profile.
        Deduct up to 20 points based on the overall relevance (0 for perfect relevance, 20 for completely irrelevant).
    Output:
    Generate a JSON object starting with "```json" and trailing with "```", the following structure should be followed:

    ```json
    {
    "Section Analysis": {
        "All Section" : [],
        "Missing Sections": []
    },
    "Skills Assessment": {
        "Current Hard Skills": [],
        "Current Soft Skills": [],
        "Suggested Additional Hard Skills": [],
        "Suggested Additional Soft Skills": []
    },
    "Quantification": {
        "Quantified": [],
        "Not Quantified": []
    },
    "Repetition": {
        "Similar Concepts": {}
    },
    "Verb Strength": {
        "Weak Verbs": {}
    },
    "Verb Tense": {
        "Inconsistencies": {}
    },
    "Overused Phrases": {},
    "Spelling Errors": [],
    "Generic Points":[],
    "Summary": "",
    "Score":<integer_value_between_0-100_for the effectiveness of RESUME>
    }
    """
    bot_quatify = Agent(MASTER_PROMPT)
    bot_quatify_resp = bot_quatify(str(f"### RESUME TEXT {cv_text}"))
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


if __name__ == "__main__":
    print(master_prompt(resume_text))