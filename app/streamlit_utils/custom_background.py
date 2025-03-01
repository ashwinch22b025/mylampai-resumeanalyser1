import streamlit as st

class Background():

    def __init__(self) -> None:
        pass

    def background_img_md(self):
        page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://i.postimg.cc/4xgNnkfX/Untitled-design.png");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: local;
        }}

        </style>

        """

        return page_bg_img