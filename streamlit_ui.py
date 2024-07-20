import os
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import streamlit as st
import re
import pandas as pd
from scraper import scrapeEpsilon, ConditionData, Condition
import urllib
from mock_data import mock_data
from dotenv import load_dotenv
load_dotenv()

def mock_condition_data(_):
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
    
    st.subheader(f'Based on your DNA, we have found you have the variant {condition_data.gene}. Here are the associated conditions:')
    for condition in condition_data.conditions:
        st.write(f"**{condition.name}**: {condition.description}")
    
    with st.expander("Condition References", expanded=False):
        for i, ref in enumerate(condition_data.condition_references, 1):
            st.write(f"[{i}] {ref}")
    
    st.subheader("Here are some supplements personalized for you to help modulate gene expression:")
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
    st.write("Welcome to HeathAssess, your personal chat assistant to help you reach your genetic potential.")

    # Initialize session state for data
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False

    with st.form("upload_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        uploaded_file = st.file_uploader("Upload DNA csv", type="csv")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if name and email and uploaded_file:
            # Process the uploaded file
            df = pd.read_csv(uploaded_file, header=None)
            st.success(f"Thank you, {name}! Your DNA data has been uploaded successfully.")
            st.write("Preview of your uploaded data:")
            st.dataframe(df)
            genes = df[0].values
            
            data = scrape_provider(genes)

            
            # Set the data_loaded flag to True
            st.session_state.data = data
            # st.rerun()  # Rerun the app to update the UI
        else:
            st.error("Please fill in all fields and upload a CSV file.")

    # Chat interface - only show when data is loaded
    if 'data' in st.session_state and st.session_state.data is not None:
        data = st.session_state.data
        for condition_data in data:
            render_condition_component(condition_data)
        st.header("AI Assistant")
        system_prompt = f"""
       You are an AI assistant specialized in helping users understand their genetic mutations and polymorphisms. Your primary goal is to provide clear, accurate, and personalized information to users about their genetic variations. Follow these guidelines in your interactions:

1. Use clear, non-technical language: Explain genetic concepts in simple terms that a layperson can understand. When you must use scientific terms, provide brief, clear definitions.

2. Scope of information: Focus on explaining the nature of specific genetic mutations or polymorphisms, their potential effects on health or traits, and their prevalence in the general population. Do not attempt to diagnose medical conditions or predict health outcomes.

3. Personalization: Ask users for specific genetic information they want to understand. Tailor your explanations to their particular mutations or polymorphisms.

4. Educational approach: Provide context for genetic variations. Explain basic concepts like genes, alleles, and how mutations occur. Use analogies to help users grasp complex ideas.

5. Empathy and sensitivity: Recognize that genetic information can be sensitive. Maintain a supportive and non-judgmental tone throughout your interactions.

6. Privacy and ethics: Emphasize the importance of genetic privacy. Remind users not to share personal genetic information in public forums. Do not store or remember any personal genetic data shared by users.

7. Limitations and disclaimers: Clearly state that you are an AI and not a medical professional. Encourage users to consult with genetic counselors or healthcare providers for medical advice or concerns.

8. Scientific accuracy: Base your information on current, peer-reviewed scientific research. If there's uncertainty or conflicting evidence about a particular genetic variation, communicate this clearly.

9. Resources: Provide reputable sources for further reading on genetics and specific mutations when appropriate.

10. Interactivity: Be prepared to answer follow-up questions and dive deeper into topics based on user interest.

Remember, your role is to inform and educate, not to diagnose or prescribe. Always prioritize scientific accuracy, user understanding, and ethical considerations in your responses.

        Here is the data the user {name} uploaded to base your responses on:
        {st.session_state.data}
        """

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                SystemMessage(content=system_prompt)
            ]

        # Display chat messages from history on app rerun
        for message in st.session_state.messages[1:]:  # Skip the system message
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)

        # Accept user input
        if prompt := st.chat_input("What is your question?"):
            openai_api_key = os.getenv('OPENAI_API_KEY')
            # Add user message to chat history
            st.session_state.messages.append(HumanMessage(content=prompt))
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Create ChatOpenAI instance
            chat = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key, model="gpt-4o")
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Generate assistant response
                for chunk in chat.stream(st.session_state.messages):
                    full_response += chunk.content
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append(AIMessage(content=full_response))

    # Footer
    st.markdown("---")
    st.markdown("© 2024 . All rights reserved.")

def main():
    run_streamlit(scrapeEpsilon)

def main_test():
    run_streamlit(mock_condition_data)

if __name__ == "__main__":
    main()