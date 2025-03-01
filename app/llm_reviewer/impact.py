import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import *
import json
import spacy
from spacy.matcher import Matcher
# def quantification(text_to_check):
#     quantify_prompt = """
#     You are a Hiring Manager of a Fortune 500 Company. Your role is to help candidates curate and improve their CVs to create maximum impact on recruiters.

#     Step #1: Objective
#     - Categorize the given bullet points as "Quantify" or "Not Quantify".
#     - Output the result as a JSON object starting with '```json' and ending with '```'.
#     - The JSON object should have two keys:"Quantify" and "Not Quantify", each containing a list of appropriately categorized bullet points.

#     Step #2: Instructions
#     - Carefully analyze each bullet point, ensuring a thorough understanding of its content.
#     - Categorization criteria:
#     a) "Quantify": The bullet point MUST contain at least one relevant numeric value. Acceptable formats include:
#         - Integers (e.g., 5, 100, 1000)
#         - Decimals (e.g., 3.14, 2.5)
#         - Percentages (e.g., 25%, 99.9%)
#         - Currency values (e.g., $1000, €50)
#         - Fractions (e.g., 3/4, 1/2)
#     b) "Not Quantify": Any bullet point that does not meet the above criteria.

#     Step #3: Validation
#     - Review your categorization meticulously.
#     - Repeat the categorization process at least twice to ensure accuracy.
#     - Verify that ONLY bullet points containing numeric values as specified above are categorized as "Quantify".

#     Step #4: Output
#     - Provide the final JSON output to the candidate, strictly adhering to the format specified in Step #1.

#     Important Notes:
#     - Numeric words (e.g., "five", "twenty") do NOT qualify for the "Quantify" category.
#     - Ordinal numbers (e.g., "1st", "2nd", "third") do NOT qualify for the "Quantify" category.
#     - Time periods without specific numeric values (e.g., "annually", "monthly") do NOT qualify for the "Quantify" category.
#     - Be extremely strict in your categorization. When in doubt, categorize as "Not Quantify".
# """.strip()
#     bot_quatify = Agent(quantify_prompt)
#     bot_quatify_resp = bot_quatify(str(text_to_check))
#     json_file = json.loads(bot_quatify_resp.strip().strip("```json").strip("```"))
#     quant_weight = 2  # You can adjust this weight based on importance
#     nquant_weight = 1 
#     quant_score = len(json_file['Quantify']) * quant_weight
#     nquant_score = len(json_file['Not Quantify']) * nquant_weight
#     total_points = quant_score+nquant_score
#     max_possible_score = (total_points * quant_weight) + (total_points * nquant_weight)
#     final_score = int((quant_score + nquant_score) / max_possible_score * 100)
#     json_file["score"] = final_score
#     return json_file


def quantification(text_to_check):
    print(text_to_check)
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    
    # Define a pattern that matches any token that is a digit or contains a digit
    pattern = [{"TEXT": {"REGEX": r"\b(\d+(\.\d+)?(/\d+)?%?|rs\.?|Rs\.?|yen|¥|\$|€|£)\d+\b"}}]
    matcher.add("QUANTIFY", [pattern])
    
    quantify = []
    not_quantify = []
    
    for sentence in text_to_check:
        doc = nlp(sentence)
        matches = matcher(doc)
        if matches:
            quantify.append(sentence)
        else:
            not_quantify.append(sentence)
    
    dicti = {"Quantify": quantify, "Not Quantify": not_quantify}
    json_file = json.dumps(dicti, indent=4)
    return json_file

def repetition(text_to_check,length):

    repetition_prompt = """
    ### TASK ###
    As an AI assistant, your role is to analyze a list of sentences from a CV to identify and group semantically similar concepts or phrases. Your objective is to improve the CV by highlighting repetitive content that could negatively impact a recruiter's assessment.

    Instructions:
    1. Carefully analyze the provided list of sentences.
    2. Identify phrases or concepts that are semantically similar across different sentences, even if they don't use identical wording.
    3. When determining similarity, disregard specific names of:
    - Companies
    - Technologies
    - Libraries
    - Frameworks related to web development, data science, DevOps, cybersecurity, machine learning, etc.
    4. Only include entries in the JSON object if there are at least two semantically similar sentences for each key.

    ### OUTPUT ###
    Present the final, refined JSON object using the following format:
    ```json
    {
    "Similar phrase between all these sentences": {
        "text": ["Sentence 1", "Sentence 2", ...],
        "reason": "Explanation of the semantic similarity between these sentences."
    },
    "Similar phrase between all these sentences": {
        "text": ["Sentence A", "Sentence B", ...],
        "reason": "Explanation of the semantic similarity between these sentences."
    }
    // Additional entries as needed...
    }```
    """.strip()
    repeat_bot = Agent(repetition_prompt)
    repeat_bot_resp = repeat_bot(text_to_check)
    json_file = json.loads(repeat_bot_resp.strip().strip("```json").strip("```"))
    total_points = length
    good_points = total_points - len(json_file.keys())
    score = int((good_points/total_points) *100)
    json_file["score"] = score
    return json_file



def weak_verb_checker(text_to_check):
    weak_verbs_prompt = """
    You are an expert resume consultant with years of experience in optimizing resumes for maximum impact. Your task is to analyze resume content and suggest powerful improvements to weak language.

    ### OBJECTIVE ###
    Enhance the impact and effectiveness of resume bullet points by replacing weak verbs with strong, action-oriented alternatives.

    ### INSTRUCTIONS ###
    1. Carefully review each line of the provided resume content.
    2. Identify weak or generic verbs that could be replaced with more impactful alternatives.
    3. Generate a JSON object where:
    - Keys are the identified weak verbs
    - Values are lists of 2-3 strong, context-appropriate alternative verbs

    4. Evaluate your output based on these criteria:
    - Relevance: Do the alternatives fit the original context?
    - Impact: Do they significantly strengthen the resume?
    - Variety: Are the suggestions diverse and non-repetitive?

    5. Refine your output until you're confident it meets all criteria.

    ### OUTPUT FORMAT ###
    Provide the final JSON object in this format:

    ```json
    {
    "weak_verb1": ["strong_alternative1", "strong_alternative2"],
    "weak_verb2": ["strong_alternative1", "strong_alternative2", "strong_alternative3"]
    }

    GUIDELINES

    Focus on verbs that begin bullet points or describe key achievements
    Ensure alternatives maintain the original meaning while increasing impact
    Prefer verbs that quantify achievements or demonstrate concrete results
    Consider industry-specific terminology where appropriate
    Avoid overly complex or uncommon words that might confuse readers

    STRONG VERB CATEGORIES
    Consider verbs from these categories:

    Accomplishment-driven (e.g., Achieved, Improved, Increased)
    Leadership (e.g., Spearheaded, Led, Directed)
    Problem-solving (e.g., Resolved, Streamlined, Optimized)
    Innovation (e.g., Pioneered, Developed, Implemented)
    Communication (e.g., Negotiated, Presented, Collaborated)

    FINAL CHECK
    Before submitting:

    Ensure no weak verb is left without strong alternatives
    Verify that alternatives are varied and not repetitive
    Confirm that each suggestion would genuinely improve the resume's impact

    Only provide your output if you're highly confident (8+ on a scale of 1-10) in its quality and effectiveness.
    Ensure your response begins with "```json" and ends with "```" to properly format the JSON output.

    """.strip()
    weak_verbs_bot = Agent(weak_verbs_prompt)
    weak_verbs_bot_resp = weak_verbs_bot(text_to_check)
    json_file = json.loads(weak_verbs_bot_resp.strip().strip("```json").strip("```"))
    return json_file
    


def responsibility(text_to_check):
    responsibility_prompt = """
    ### CONTEXT ###
    Hiring managers seek specific, impactful language in resumes. Many job seekers unknowingly use generic or overused phrases that can negatively impact their candidacy. Additionally, even without these clichés, some bullet points may still benefit from optimization to better showcase a candidate's value.
    
    ### INSTRUCTIONS ###
    a.) Carefully review each line of the provided resume text.
    b.) Identify and flag:
        i.) Instances of generic or overused phrases
    c.) Generate a JSON object with the following structure:
        Keys: The original phrase or bullet point
        Values: An object containing:
            i.) "correction": Improved phrase or bullet point without altering the overall meaning
            ii.) "reason": Brief explanation of the suggested change

    ### OUTPUT ###
    Provide the final, refined JSON object using the following format starting with '```json' and trailing with '```':
    ```json
    {
    "Original phrase or bullet point 1": {
        "correction": "Improved phrase or bullet point 1",
        "reason": "Explanation of the improvement 1"
    },
    "Original phrase or bullet point 2": {
        "correction": "Improved phrase or bullet point 2",
        "reason": "Explanation of the improvement 2"
    }
    }```

    """.strip()
    responsibility_prompt_bot = Agent(responsibility_prompt)
    responsibility_prompt_bot_resp = responsibility_prompt_bot(text_to_check)
    json_file = json.loads(responsibility_prompt_bot_resp.strip().strip("```json").strip("```"))
    if json_file:
        return json_file
    return {"Result":"Every Thing Looks Good for This Section."}

def text_analyzer(text_to_check):
    merged_prompt = """
    ### CONTEXT ###
        A resume is often the first impression potential employers have of a candidate. Every word matters, and using incorrect verb tenses or having spelling errors can make applicants appear unprofessional or careless to hiring managers. Proper tense usage and correct spelling are crucial for presenting a polished and competent image.    
    ### INSTRUCTIONS ###
        1. Carefully review each line of the provided resume text.
        2. Analyze the text for two types of errors:
            a) Verb tense issues
            b) Spelling errors
        3. For verb tense issues:
            Identify and flag any instances of incorrect verb tense usage that could negatively impact the candidate's perception by employers.
            Generate a JSON object with the following structure:
            Keys: The original bullet points with incorrect tense
            Values: An object containing:
                a) "correction": The revised bullet point with correct tense
                b) "reason": A brief explanation of why the change was made
                c) "impact": Point out the change you made
        4. For spelling errors:
            Use a comprehensive dictionary and context-aware spell-checking algorithm to identify misspelled words.
            For each misspelled word, create an object with:
                a) The misspelled word itself
                b) The word's context (a few words before and after)
                c) Suggested corrections
        5. Calculate a score based on the number and severity of mistakes:
            Start with a perfect score of 100
            Deduct points for each mistake:
                Minor mistakes (e.g., simple tense inconsistencies or minor spelling errors): -5 points
                Moderate mistakes (e.g., using past tense for current job or noticeable spelling errors): -10 points
                Severe mistakes (e.g., mixing tenses within a single bullet point or critical spelling errors): -15 points
        The final score should be between 0 and 100
    THINK DEEPLY AND SMARTLY
    ### OUTPUT ###
    Provide the final, refined JSON object starting with '```json' and trailing with '```' using the following format:
        {
    "verb_tense_mistakes": {
        "Original bullet point with incorrect tense": {
        "correction": "Revised bullet point with correct tense",
        "reason": "Explanation of the tense correction",
        "impact": "Point out the change you made"
        }
        // Additional entries...
    },
    "spelling_errors": [
        {
        "word": "misspelled_word",
        "context": "This is the misspelled_word in context.",
        "suggestions": ["correction1", "correction2", "correction3"]
        }
        // Additional entries...
    ],
    "score": 85
    }
    If no errors are found in either category, the respective section should be an empty object or array.
 """.strip()

    text_analyzer_bot = Agent(merged_prompt)
    analyzer_response = text_analyzer_bot(text_to_check)
    json_result = json.loads(analyzer_response.strip().strip('```json').strip('```'))
    return json_result



def spelling_checker(text_to_check):
    spelling_checker_prompt = """
    1. Analyze the input text for spelling errors using a comprehensive dictionary and context-aware spell-checking algorithm.
    2. Create a JSON object with the following structure:
        A "Result" key containing an array of misspelled words.
        For each misspelled word, include an object with:
            a. The misspelled word itself
            b. The word's context (a few words before and after)
            c. Suggested corrections


    3.If no errors are found, the "Result" array should be empty.
    4, Include a "Statistics" object in the JSON with:

            Total word count
            Number of unique words
            Number of misspellings found

    5.Format the output as a JSON string, starting with json and ending with .
    6.Ensure the JSON is properly formatted and escaped for easy parsing.
    7. Format the output as a JSON string, starting with ```json and ending with ```.

    Example output format:
    ```json
        {
    "Result": [
        {
        "word": "misspeled",
        "context": "This is a misspeled word in a sentence.",
        "suggestions": ["misspelled", "misspell", "dispelled"]
        },
        {
        "word": "errur",
        "context": "There is an errur in this text.",
        "suggestions": ["error", "errand", "erase"]
        }
    ],
    "Statistics": {
        "totalWords": 150,
        "uniqueWords": 120,
        "misspellings": 2
    }
    }```
    Please review the text and provide the results in the specified JSON format.""".strip()
    spelling_checker_bot = Agent(spelling_checker_prompt)
    spelling_checker_bot_res = spelling_checker_bot(text_to_check)
    json_file = json.loads(spelling_checker_bot_res.strip().strip('```json').strip('```'))
    misspellings = json_file["Statistics"]["misspellings"]
    score = max(0, 100 - (misspellings * 5))
    json_file["Score"] = score
    return json_file

def verb_tense(text_to_check):
    verb_tense_prompt = """
    ### CONTEXT ###
    A resume is often the first impression potential employers have of a candidate. Every word matters, and using incorrect verb tenses can make applicants appear unprofessional or careless to hiring managers. Proper tense usage is crucial for presenting a polished and competent image.
    ### INSTRUCTIONS ###
    1. Carefully review each line of the provided resume text.
    2. Identify and flag any instances of incorrect verb tense usage that could negatively impact the candidate's perception by employers.
    3. Generate a JSON object with the following structure:
    - Keys: The original bullet points with incorrect tense
    - Values: An object containing:
        a) "correction": The revised bullet point with correct tense
        b) "reason": A brief explanation of why the change was made
        c) "impact": Point Out to Change You made
    4. Repeat steps 1-3 up to 3 times, refining the corrections and explanations each time.
    5. Calculate a score based on the number and severity of mistakes:

        Start with a perfect score of 100
        Deduct points for each mistake:
        Minor mistakes (e.g., simple tense inconsistencies): -5 points
        Moderate mistakes (e.g., using past tense for current job): -10 points
        Severe mistakes (e.g., mixing tenses within a single bullet point): -15 points
        The final score should be between 0 and 100
    ### OUTPUT ###
    Provide the final, refined JSON object using the following format:
    ```json
    {
        "mistakes":{
        "Original bullet point with incorrect tense": {
            "correction": "Revised bullet point with correct tense",
            "reason": "Explanation of the tense correction",
            "impact": "Point Out to Change You made"
        }
        // Additional entries...
        },
        "score": 85
    }```    
""".strip()
    
    verb_tense_bot = Agent(verb_tense_prompt)
    verb_tense_bot_resp = verb_tense_bot(text_to_check)
    json_file = json.loads(verb_tense_bot_resp.strip().strip("```json").strip("```"))

    if json_file:
        return json_file
    return {"Result":"NO CORRECTION NEEDED"}