import streamlit as st
import sys
import os
import tempfile
import base64
from streamlit_pdf_viewer import pdf_viewer

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from llm_reviewer.agent import *
from llm_reviewer.brevity import *
from llm_reviewer.style import *
from llm_reviewer.impact import *
from utils.utils import *
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from streamlit_utils.custom_background import Background
from database.database import Database
from dotenv import load_dotenv
from streamlit import session_state as ss

load_dotenv()
uri = os.getenv('URI')

colour_dict = {
    "green": (0.847, 0.988, 0.882),
    "blue": (0.725, 0.71, 0.988),
    "red": (1, 0.698, 0.698),
    "yellow": (1, 0.894, 0.698)
}
    
def inject_css():
    css = """
    <style>
    
    h1, h2, h3, h4 {
        color: #8c52ff;
    }
    .main p {
        color: #000000aa;
    }

    .main .e1e4pi9i0 p {
        color: white;
    }

    .stApp {
        background: #F1EAFF;
        color: #000000
    }
    #stDecoration {
        display: none;
    }
    .eczjsme18 {
        background: #f5f5f540;
        backdrop-filter: blur(10px);
        color: white;
        box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.1);
    }
    .e1nzilvr4 h2 {
        color: #8c52ff;
        text-transform: uppercase;
        text-align: center;
        font-size: 1.5em;
    }
    .st-emotion-cache-h4xjwg {
        background: #f1eaff;
        color: #f1eaff;
        position: relative;
    }
    .st-emotion-cache-mnu3yk.ef3psqc5 {
        opacity: 0;
        display: none;
    }
    .st-emotion-cache-1p1m4ay.e3g6aar0 {
        display: none;
    }
    header::before {
        content: "";
        position: absolute;
        top: 20%;
        left: 0;
        width: 150px;
        height: 60%;
        background: url('https://main--mylamp-ai.netlify.app/home/logo.svg') no-repeat center;
        background-size: contain;
    }
    .st-emotion-cache-19u4bdk.eczjsme5 .st-emotion-cache-yfhhig.ef3psqc4 {
        background-color: #8c52ff90 !important;
        color: white;
        border-radius: 100px;
        transform: translateY(calc(50vh - 50%));
    }
    .st-emotion-cache-a1dni5.eczjsme18 .st-emotion-cache-yfhhig {
        background-color: #8c52ff90 !important;
        color: white;
    }
    
    .st-emotion-cache-1i4v8s7.eczjsme18 .st-emotion-cache-yfhhig {
        background-color: #8c52ff90 !important;
        border-radius: 100px;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #F1EAFF;
    }
    .e1b2p2ww15 {
        background-color: #8c52ff;
        color: white;
    }
    .ef3psqc12 {
        background-color: #8c52ff !important;
        color: white !important;
        border: 1px solid rgb(250, 250, 250, 0.2) !important;
    }
    .stButton>button {
        background-color: #8c52ff !important;
        color: white !important;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        width: 100%;
        transition: all 0.15s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        color: white;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# def add_logo():
#     logo_path = "./logo.png"  # Update this with your logo's path
#     logo_html = f"""
#     <div class="header">
#         <img src="data:image/png;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}" class="logo">
#         <h1>Resume Analyzer</h1>
#     </div>
#     """
#     st.markdown(logo_html, unsafe_allow_html=True)


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def get_path(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name
    return temp_file_path

def show_pdf_from_bytes(pdf_bytes):
    pdf_viewer(pdf_bytes, render_text=True)

def main():
    inject_css()
    # add_logo()
    # bacground_img = Background()
    client = Database(uri)
    # st.markdown(bacground_img.background_img_md(), unsafe_allow_html=True)
    
    st.title("Resume Analyzer")
    uploaded_file = st.file_uploader("Upload your CV (PDF)", type="pdf")

    if 'last_uploaded_file' not in st.session_state or (uploaded_file and uploaded_file.name != st.session_state.last_uploaded_file):
        # Reset session state
        st.session_state.clear()
        st.session_state.last_uploaded_file = uploaded_file.name if uploaded_file else None
    
    if uploaded_file:
        pdf_bytes = uploaded_file.getvalue()

        if uploaded_file.size > 5 * 1024 * 1024:  # 5 MB limit in bytes
            st.error("File size exceeds 5 MB limit. Please upload a smaller PDF.")
        
        else:
            existing_doc = client.collection.find_one({'pdf': pdf_bytes})
            if existing_doc:
                st.session_state.analysis_results = existing_doc.get('analysis_results', {})
            else: 
                client.insert_data({'pdf': pdf_bytes,'analysis_results': {}})

        if 'cv_text' not in st.session_state:
            st.session_state.cv_text = extract_text_from_pdf(uploaded_file)

        if st.session_state.cv_text:
            st.success("CV uploaded successfully!")

            if 'structured_data' not in st.session_state:
                st.session_state.structured_data = extract_structured_data(st.session_state.cv_text)
            
            if 'analysis_results' not in st.session_state:
                st.session_state.analysis_results = {}

            if 'highlighted_pdfs' not in st.session_state:
                st.session_state.highlighted_pdfs = {}

            st.sidebar.header("Analysis Functions")

            analysis_functions = {
                "Quantification Checker": lambda: quantification("\n".join(st.session_state.structured_data["Description"])),
                "Resume Length": lambda: resume_length(st.session_state.cv_text),
                "Bullet Point Length": lambda: bullet_point_length(st.session_state.structured_data["Description"]),
                "Bullet Points Improver": lambda: bullet_points_improver("\n".join(st.session_state.structured_data["Description"])),
                "Total Bullet Points": lambda: total_bullet_list(st.session_state.structured_data["Description"]),
                "Verb Tense Checker": lambda: verb_tense("\n".join(st.session_state.structured_data["Description"])),
                "Weak Verb Checker": lambda: weak_verb_checker("\n".join(st.session_state.structured_data["Description"])),
                "Section Checker": lambda: section_checker(st.session_state.structured_data["Sections"]),
                "Skill Checker": lambda: skill_checker(st.session_state.structured_data["Skills"]["HARD"], st.session_state.structured_data["Skills"]["SOFT"]),
                "Repetition Checker": lambda: repetition("\n".join(st.session_state.structured_data["Description"])),
                "Responsibility In Words Checker": lambda: responsibility("\n".join(st.session_state.structured_data["Description"])),
                "Spelling Checker": lambda: spelling_checker("\n".join(st.session_state.structured_data["Description"]))
            }

            pdf_list = [
                "Bullet Point Length", "Bullet Points Improver", "Quantification Checker",
                "Weak Verb Checker", "Repetition Checker", "Verb Tense Checker",
                "Responsibility In Words Checker", 
            ]

            show_dict = {
                "Resume Length": show_box_brevity,
                "Bullet Point Length": show_big_bullet_points,
                "Total Bullet Points": show_box_brevity,
                "Bullet Points Improver": show_bullet_point_improver,
                "Section Checker": show_personal_info,
                "Skill Checker": show_skill_checker,
                "Repetition Checker": show_repetition,
                "Weak Verb Checker": show_weak_verb,
                "Verb Tense Checker": show_verb_tense,
                "Responsibility In Words Checker": show_responsibility,
                "Spelling Checker": show_spell_checker
            }

            for analysis_name, analysis_function in analysis_functions.items():
                if st.sidebar.button(analysis_name):
                    if analysis_name not in st.session_state.analysis_results:
                        result = perform_analysis(analysis_name, analysis_function)
                    else:
                        result = st.session_state.analysis_results[analysis_name]

                    if result:
                        st.session_state.analysis_results[analysis_name] = result
                        client.update_analysis_results(pdf_bytes, st.session_state.analysis_results)
                        if analysis_name in show_dict:
                            show_dict[analysis_name](result)

                        if analysis_name not in pdf_list:
                            show_pdf_from_bytes(uploaded_file.getvalue())

                        if analysis_name in pdf_list:
                            if analysis_name not in st.session_state.highlighted_pdfs:
                                highlighted_pdf_path = generate_highlighted_pdf(analysis_name, result, uploaded_file)
                                st.session_state.highlighted_pdfs[analysis_name] = highlighted_pdf_path.getvalue()

                            st.download_button(
                                label="Download Highlighted PDF",
                                data=st.session_state.highlighted_pdfs[analysis_name],
                                file_name=f"highlighted_{analysis_name}.pdf",
                                mime="application/pdf"
                            )
                            show_pdf_from_bytes(st.session_state.highlighted_pdfs[analysis_name])
                    else:
                        st.subheader("Everything Looks Pretty Good in This Section, Perfect!")
                        show_pdf_from_bytes(uploaded_file.getvalue())
        

                        
            st.markdown("[Early Access](https://docs.google.com/forms/d/e/1FAIpQLSd1vn8mLB5dXrxsimkfEJCH6-cxX_1gMUGVZDcfxM5eSYrrbA/viewform?usp=sf_link)")
            st.markdown("[Feedback](https://forms.gle/eAUHd2GpyRiZqvry9)")


def generate_highlighted_pdf(analysis_name, result, uploaded_file):
    if analysis_name == "Quantification Checker":
        return highlight_common(
            pdf_file=uploaded_file, color=colour_dict["green"],
            data=result["Quantify"], data2=result["Not Quantify"],
            color2=colour_dict["red"], two_sections=True
        )
    elif analysis_name == "Repetition Checker":
        exact_matches_list = [item for key, items in result.items() for item in items["text"]]
        return highlight_common(pdf_file=uploaded_file, color=colour_dict["yellow"], data=exact_matches_list)
    elif analysis_name == "Bullet Points Improver":
        exact_matches_list = [item["original"] for key, items in result.items() for item in items]
        return highlight_common(pdf_file=uploaded_file, color=colour_dict["blue"], data=exact_matches_list)
    elif analysis_name in ["Weak Verb Checker", "Verb Tense Checker", "Responsibility In Words Checker", "Personal Info"]:
        return highlight_common(pdf_file=uploaded_file, color=colour_dict["yellow"], data=result.keys())
    elif analysis_name == "Bullet Point Length":
        return highlight_common(pdf_file=uploaded_file, color=colour_dict["red"], data=result["Result"])
    else:
        return uploaded_file

if __name__ == "__main__":
    main()