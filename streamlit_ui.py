import streamlit as st
import re
import pandas as pd
from scraper import scrapeEpsilon, ConditionData, Condition
from gptbot import formatIntoMarkdown
import urllib
from mock_data import mock_data

def mock_condition_data():
    return [
        ConditionData(
            gene="HLA-B27",
            conditions=[
                Condition(
                    name="Ankylosing Spondylitis",
                    description="Ankylosing spondylitis is a type of arthritis that affects the spine. It causes inflammation between your vertebrae, which are the bones that make up your spine, and in the joints between your spine and pelvis."
                ),
                Condition(
                    name="Reactive Arthritis",
                    description="Reactive arthritis is a type of arthritis that occurs as a reaction to an infection in the body. The infection that triggers reactive arthritis is typically a sexually transmitted infection or a gastrointestinal infection."
                )
            ],
            condition_references=[
                "https://www.healthline.com/health/ankylosing-spondylitis",
                "https://www.healthline.com/health/reactive-arthritis"
            ],
            suppliments=[
                Condition(
                    name="Vitamin D",
                    description="Vitamin D is a fat-soluble vitamin that helps your body absorb calcium and phosphorus. Having the right amount of vitamin D, calcium, and phosphorus is important for building and keeping strong bones."
                ),
                Condition(
                    name="Omega-3 Fatty Acids",
                    description="Omega-3 fatty acids are incredibly important for your body and brain. They have many powerful health benefits for your body and brain."
                )
            ],
            suppliment_references=[
                "https://www.healthline.com/nutrition/vitamin-d-deficiency-symptoms",
                "https://www.healthline.com/nutrition/17-health-benefits-of-omega-3"
            ]
        )
    ]

def supplement_link(supplement: str):
    encoded_supplement = urllib.parse.quote(supplement)
    url = f"https://www.amazon.com/s?k={encoded_supplement}"
    return f"[{supplement}]({url})"

def render_condition_component(condition_data: ConditionData):
    st.header(f"Gene: {condition_data.gene}")
    
    st.subheader("Associated Conditions")
    for condition in condition_data.conditions:
        st.write(f"**{condition.name}**: {condition.description}")
    
    with st.expander("Condition References", expanded=False):
        for i, ref in enumerate(condition_data.condition_references, 1):
            st.write(f"[{i}] {ref}")
    
    st.subheader("Recommended Supplements")
    for supplement in condition_data.suppliments:
        st.write(f"**{supplement_link(supplement.name)}**: {supplement.description}")
        # supplement_link(supplement.name)
    
    with st.expander("Supplement References", expanded=False):
        for i, ref in enumerate(condition_data.suppliment_references, 1):
            st.write(f"[{i}] {ref}")

def run_streamlit(scrape_provider):
    st.set_page_config(
        page_title="HealthAssess @ AiTX Hack",
        page_icon="🧬",
        layout="wide"
    )
    st.title("Welcome to HealthAssess @ AiTX Hack")
    st.header("About")
    st.write("This is a section about something interesting.")

    with st.form("upload_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        uploaded_file = st.file_uploader("Upload DNA csv", type="csv")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if name and email and uploaded_file:
            # Process the uploaded file
            df = pd.read_csv(uploaded_file)
            st.success(f"Thank you, {name}! Your DNA data has been uploaded successfully.")
            st.write("Preview of your uploaded data:")
            st.dataframe(df.head())
            
            data = scrape_provider()
            for condition_data in data:
                render_condition_component(condition_data)
        else:
            st.error("Please fill in all fields and upload a CSV file.")

    st.markdown("---")
    st.markdown("© 2024 . All rights reserved.")

def main():
    run_streamlit(scrapeEpsilon)
    


def main_test():
    run_streamlit(mock_condition_data)


if __name__ == "__main__":
    main()
    # main_test()