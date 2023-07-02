import streamlit as st

APP_TITLE = 'Test'

class MainWebsite:
    def __init__(self):
        pass

    def get_html_site(self):
        st.set_page_config(APP_TITLE)

        st.title(APP_TITLE)


site = MainWebsite()

site.get_html_site()