import streamlit as st


st.set_page_config(page_title="Campaign Panel", layout="wide")


def intro():
    st.write("Welcome to the Campaign Panel!")


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

    if st.button("Submit"):
        st.write("Campaign Description:", campaign_description)
        st.write("Uploaded Files:", images_content_videos)
        st.write("List of Questions:", list_of_questions)
        st.write("Age:", age)
        st.write("Income:", income)
        st.write("Other Attributes:", other_attributes)
        st.write("Number of Agents:", number_of_agents)
        st.write("Attachments:", attachments)


def output_results():
    st.title("Analytics Output")
    col1, col2, col3 = st.columns(3)

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
