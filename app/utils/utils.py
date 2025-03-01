import streamlit as st
import PyPDF2
from llm_reviewer.agent import *
import json
import sys
import os
import fitz
import tempfile
import io
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def extract_structured_data(text):
    structured_prompt_2 = """
   Read the following CV text 100 times and deeply understand it. Then, convert the CV text into a JSON data structure with the following keys and specifications:

    1. "Personal Information": The value should be a dictionary containing all personal information related to the individual given in the CV text (e.g., name, contact details, location, date of birth, gender).
    2. "Description": The value should be a list of all bullet points found anywhere in the CV, including but not limited to:
        - Achievements
        - Awards
        - International exposure
        - Work experience responsibilities
        - Project details
        - Any other bullet-pointed information throughout the CV

    3. "Skills": The value should be a dictionary with the following sub-keys:
        "HARD" (technical skills, tools, programming languages, etc.): The value should be a list of all HARD SKILLS from the CV.
        "SOFT" (communication, leadership, etc.): The value should be a list of all SOFT SKILLS from the CV. Each skill should be listed individually.

    4. "Education": The value should be a list of dictionaries, each containing information about educational qualifications (degree, institution, year, etc.).
    5. "Sections": The value should be a list of all distinct section headings actually present in the CV. This may include, but is not limited to: "Profile Summary", "Education", "Work Experience", "Skills", "Projects", "Achievements", "Awards", "International Exposure", "Extra Curricular Activities", "Languages", "Interests", etc. Only include sections that are explicitly mentioned as headings in the CV.

    Finally, check the whole CV data and JSON structure. If there is anything missing, add it.
    The final output should start with '```json' and end with '```'.
    Additionally, please ensure that the JSON structure is valid and accurately represents the information in the CV text.
        """.strip()
    bot2 = Agent(structured_prompt_2)
    res = bot2(text)
    text_to = res.strip().strip('```').strip('```json')
    json_file = json.loads(text_to)
    return json_file

def perform_analysis(analysis_name, analysis_function):
    if analysis_name not in st.session_state.analysis_results:
        try:
            result = analysis_function()
            st.session_state.analysis_results[analysis_name] = result
        except Exception as e:
            st.error(f"An error occurred during {analysis_name}: {str(e)}")
            return
    
    st.subheader(analysis_name)
    #st.json(st.session_state.analysis_results[analysis_name])
    return result


def highlight(document,texts_to_highlight,colour):

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        
        for text in texts_to_highlight:
            if len(text) <= 2:
                continue
            text_instances = page.search_for(text)
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=colour)
                highlight.update()

def highlight_common(pdf_file, color, data, data2 = [], color2=(0.847, 0.988, 0.882),two_sections = False):
    pdf_bytes = pdf_file.getvalue()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    highlight(document,data,color)
    
    if two_sections:
        highlight(document,data2,color2)
    
    output_buffer = io.BytesIO()
    document.save(output_buffer)
    document.close()
    output_buffer.seek(0)
    return output_buffer


# BREVITY SHOW
def show_box_brevity(result):
    text = result["Result"]
    st.markdown(f"### {text}")

def show_bullet_point_improver(result):
    if result:
        bullet_dicts = result["bulletPoints"]
        for bullet_dict in bullet_dicts:
            exp = st.expander(bullet_dict["original"])
            exp.write("IMPROVED VERSION: " + bullet_dict["improved"])

def show_big_bullet_points(result):
    if result:
        list = result["Result"]
        if list:
            for point in list:
                cont = st.container()
                cont.write(point)
        else:
            st.write("Good No Big Bullet Points Here")

# SHOW STYLE
def show_personal_info(result):
    if result:
        keys = result.keys()
        for key in keys:
            exp = st.expander(key)
            exp.write("REASON: " + result[key])

def show_skill_checker(result):
    if result:
        hard_skills = result["HARD"]
        soft_skills = result["SOFT"]

        st.markdown("### HARD SKILLS THAT CAN BE ADDED")
        for skill in hard_skills:
            st.markdown("- " + skill)

        st.markdown("### SOFT SKILLS THAT CAN BE ADDED")
        for skill in soft_skills:
            st.markdown("- " + skill)

def show_repetition(result):
    if result:
        keys = result.keys()
        for key in keys:
            exp = st.expander(key)
            exp.markdown("** SIMILAR PHRASES **")
            for phrase in result[key]["text"]:
                exp.write(phrase)
            exp.markdown("** REASON **")
            exp.write(result[key]["reason"])

def show_weak_verb(result):
    if result:
        keys = list(result.keys())
        col1, col2 = st.columns(2)
        for i, key in enumerate(keys):
            with col1 if i % 2 == 0 else col2:
                exp = st.expander(key)
                exp.write(str(result[key]))

def show_verb_tense(result):
    if result:
        keys = result.keys()
        if "Result" in keys:
            st.markdown(f"### {result['Result']}")
        for key in keys:
            if key != "Result":
                exp = st.expander(key)
                exp.write("Correction: " + result[key]["correction"])
                exp.write("Reason: " + result[key]["reason"])
                exp.write("Impact: " + result[key]["impact"])

def show_responsibility(result):
    if result:
        keys = result.keys()
        if "Result" in keys:
            st.markdown(f"### {result['Result']}")
        for key in keys:
            if key != "Result":
                exp = st.expander(key)
                exp.write("Correction: " + result[key]["correction"])
                exp.write("Reason: " + result[key]["reason"])

def show_spell_checker(result):
    if result:
        if isinstance(result["Result"], str):
            st.markdown(f"### {result['Result']}")
        else:
            list = result["Result"]
            if not list:
                st.write("No Error In Spelling")
            for item in list:
                st.markdown("- " + item)

























def highlight_quantification(pdf_file,analysis_name,result):
    pdf_bytes = pdf_file.getvalue()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    colour_green = (0.847, 0.988, 0.882) # Green
    colour_blue = (0.49,0.961,0.902) # blue

    quant = result["Quantify"]
    nquant = result["Not Quantify"]

    highlight(document,quant,colour_green)
    highlight(document,nquant,colour_blue)
    
    
    output_buffer = io.BytesIO()
    document.save(output_buffer)
    document.close()
    output_buffer.seek(0)
    return output_buffer

def highlight_repetition(pdf_file,result):
    pdf_bytes = pdf_file.getvalue()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    colour_green = (1, 0.894, 0.698) # Green
    colour_blue = (0.49,0.961,0.902) # blue

    exact_matches_list = [item for key, items in result.items() for item in items["text"]]

    highlight(document,exact_matches_list,colour_green)
    
    
    output_buffer = io.BytesIO()
    document.save(output_buffer)
    document.close()
    output_buffer.seek(0)
    return output_buffer




def highlight_bullet_point_improved(pdf_file,result):
    pdf_bytes = pdf_file.getvalue()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    colour_green = (1, 0.698, 0.698) # Green
    colour_blue = (0.49,0.961,0.902) # blue

    exact_matches_list = [item["original"] for key, items in result.items() for item in items]

    highlight(document,exact_matches_list,colour_green)
    
    
    output_buffer = io.BytesIO()
    document.save(output_buffer)
    document.close()
    output_buffer.seek(0)
    return output_buffer

def highlight_weak_verbs(pdf_file,result):
    pdf_bytes = pdf_file.getvalue()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    colour_green = (1, 0.894, 0.698) # Green
    colour_blue = (0.49,0.961,0.902) # blue

    exact_matches_list = result.keys()

    highlight(document,exact_matches_list,colour_green)
    
    
    output_buffer = io.BytesIO()
    document.save(output_buffer)
    document.close()
    output_buffer.seek(0)
    return output_buffer

def highlight_big_bullet_points(pdf_file,result):
    pdf_bytes = pdf_file.getvalue()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    colour_green = (0.725, 0.71, 0.988) # Green
    colour_blue = (0.49,0.961,0.902) # blue

    exact_matches_list = result["Result"]

    highlight(document,exact_matches_list,colour_green)
    
    
    output_buffer = io.BytesIO()
    document.save(output_buffer)
    document.close()
    output_buffer.seek(0)
    return output_buffer



