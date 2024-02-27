import streamlit as st
import requests
from requests.exceptions import RequestException
from interview import ProductInterview

# Apply the custom theme
st.set_page_config(page_title="HYDR.AI", layout="wide", page_icon = "assets/logo.png")

if "current_page" not in st.session_state:
    st.session_state['current_page'] = 'Home'


def intro():

    st.write("# Welcome to HYDR.AI!")
    st.markdown("## *Many heads think better than one.*")

    # Create three columns
    col1, col2, col3 = st.columns([1,2,1])  # The middle column is twice as wide as the side columns

    # Use the middle column to display the logo, which will effectively center it
    with col2:
        st.image("assets/logo.png", caption="HYDR.AI Logo", width=400)  # Adjust the width as necessary

    # Welcome message and additional content below

    st.write("""
    HYDR.AI is a cutting-edge platform designed to revolutionize the way businesses conduct market research and 
    focus groups. By leveraging the power of synthetic intelligence, HYDR.AI provides insights and data analysis 
    at a scale and speed unmatched by traditional methods.
    """)
    st.write("""
    Our platform aims to empower companies to carry out comprehensive synthetic 
    focus groups and market studies efficiently. With HYDR.AI, businesses can quickly gather and analyze 
    feedback on products, services, or marketing campaigns from a diverse and extensive virtual panel, 
    simulating a wide range of consumer perspectives.
    """)
    
    st.write("Please select the 'Input Form' section to submit your campaign details.")
    st.write("Once you have submitted the campaign details, you can view the results in the 'Output Results' section.")
    st.write("You can also navigate to the 'Home' section to learn more about the application.")

    # Add a button to navigate to the Input Form section
    if st.button("Input Form"):
        st.session_state['current_page'] = 'input_form'


def input_form():
    st.header("Producto")
    campaign_description = st.text_area("Pon descripción de la campaña", height=150)
    images_content_videos = st.file_uploader(
        "Imágenes, contenido, videos",
        type=["jpg", "png", "mp4"],
        accept_multiple_files=True,
    )
    list_of_questions = st.text_area("Lista de preguntas. (Opcional)", height=100)

    st.header("Información sobre el grupo a testar")
    age = st.slider("Edad", min_value=18, max_value=100, value=30, step=1)
    income = st.slider("Income", min_value=0, max_value=100000, value=50000, step=1000)
    other_attributes = st.text_input("Other attributes")
    number_of_agents = st.number_input(
        "Number of agents", min_value=1, max_value=100, value=1
    )
    attachments = st.file_uploader("Attachments", type=["pdf", "doc", "docx", "txt"])


    # Send POST request to the API


    if st.button("Submit"):

    
        # Instead of sending a POST request, we call initiate_interview()
        with st.spinner('Please wait... Interview in progress'):
            try:
                # Adjust the call to initiate_interview if it's supposed to take parameters
                        
                products = [
                    "Give your opinion about coca colas with strawberry flavour.",
                    "Give your opinion about the new apple vision pro",
                ]
                        
                interview = ProductInterview(age=age, income=income, products_to_test=products)

                st.success("Interview completed successfully.")
                # Process the output as needed, for example:
                # st.write(output)
            except Exception as e:
                st.error(f"Failed to complete the interview: {str(e)}")

        

        



def output_results():
    st.title("Analytics Output")
    col1, col2, col3 = st.columns(3)
    row1, row2 = st.columns(2)

    with col1:
        st.header("Encuestas respuestas")
        survey_responses = st.text_area("Responses", height=300)

    with col2:
        st.header("Sentiment")
        sentiment_analysis = st.text_area("Sentiment Analysis", height=300)

    with col3:
        st.header("Risk")
        risk_assessment = st.text_area("Risk Assessment", height=300)


# Dictionary mapping page names to functions
page_names_to_funcs = {
    "Home": intro,
    "Input Form": input_form,
    "Output Results": output_results,
}

# Sidebar navigation
demo_name = st.sidebar.selectbox("Choose a section", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
