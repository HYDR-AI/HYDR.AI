import streamlit as st
from interview import InterviewV2
from population import Population
from assets.homepage import homepage_html
from survey import Survey

# Constants for easier maintenance and updates
HOME = "Home"
INPUT_FORM = "Input Form"
OUTPUT_RESULTS = "Output Results"

# Set up the page
st.set_page_config(page_title="HYDR.AI", layout="wide", page_icon="assets/logo.png")

# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = HOME

if "page_history" not in st.session_state:
    st.session_state["page_history"] = [HOME]

st.session_state["page_history"] = st.session_state.get("page_history", [HOME])


def go_back():
    """Go back to the previous page."""
    if len(st.session_state["page_history"]) > 1:  # Ensure there is a previous page
        st.session_state["page_history"].pop()  # Remove current page
        st.session_state["current_page"] = st.session_state["page_history"][
            -1
        ]  # Set to previous page
        st.experimental_rerun()


def apply_custom_styles():
    """Apply custom CSS styles."""
    streamlit_style = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }
        </style>
    """
    st.markdown(streamlit_style, unsafe_allow_html=True)


def intro():
    """The homepage/intro page function."""
    if st.session_state.get("skip_intro"):
        return  # Skip the intro if applicable

    apply_custom_styles()  # Apply the custom CSS styles
    # No go back button needed on home page, but layout example included for consistency

    # Add svg
    st.markdown(homepage_html, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(
        [2.6, 1, 2]
    )  # Adjust the ratio as needed for better centering
    with col2:  # This puts the button in the center column
        st.write('<br style="line-height: 6;">', unsafe_allow_html=True)
        if st.button("Input Form"):
            st.session_state["current_page"] = INPUT_FORM
            st.session_state["page_history"].append(INPUT_FORM)
            st.experimental_rerun()


def input_form():
    """The input form page function."""
    cols = st.columns([1, 9])
    with cols[0]:
        if st.button("Go Back", key="go_back_input"):
            go_back()

    with cols[1]:
        st.header("Product")
        campaign_description = st.text_area("Enter campaign description", height=150, value="Chocolates Valor presenta su gama de productos y sabores que van desde lo más tradicional a lo más innovador. Placer en estado puro")
        campaign_intent = st.text_area("Enter campaign intent", height=80, value="We want to evoke a premium and traditional feeling in the user")
        images_content_videos = st.file_uploader(
            "Imágenes, contenido, videos",
            type=["jpg", "png", "mp4"],
            accept_multiple_files=True,
        )
        # list_of_questions = st.text_area("Lista de preguntas. (Opcional)", height=100)

        st.header("Información sobre el grupo a testar")
        age = st.slider("Edad", min_value=18, max_value=100, value=(30, 40), step=1)
        income = st.slider(
            "Income", min_value=0, max_value=100000, value=(10000, 50000), step=1000
        )
        gender_distribution = st.slider(
            "% Male", min_value=0, max_value=100, value=50, step=1
        )
        other_attributes = st.text_input("Other attributes", value="Sports")
        number_of_agents = st.number_input(
            "Number of agents", min_value=1, max_value=100, value=1
        )
        attachments = st.file_uploader(
            "Attachments", type=["pdf", "doc", "docx", "txt"]
        )
        locations = st.text_input("Locations", value="Madrid")

        if st.button("Submit"):
            with st.spinner("Please wait... Creating population"):
                try:
                    # Create population
                    my_population = Population(
                        ages=range(age[0], age[1], 5),
                        incomes=range(income[0], income[1], 10000),
                        gender_distribution=gender_distribution,
                        interests=[other_attributes],
                        locations=[locations],
                        population_size=number_of_agents,
                    )
                except Exception as e:
                    st.error(f"Failed to create population: {str(e)}")
                    
            with st.spinner("Please wait... Creating interview questions"):
                try:
                    # Create questions
                    survey = Survey(
                        attachments,
                        campaign_description,
                        my_population,
                        campaign_intent,
                        number_questions=1
                    )
                    # Print survey questions
                    print("Survey Questions:")
                    for i, question in enumerate(survey.get_questions(), start=1):
                        print(f"Question {i}: {question}")
                except Exception as e:
                    st.error(f"Failed to create survey questions: {str(e)}")
            with st.spinner("Please wait... Conducting interview"):
                try:
                    print("Conducting interview")
                    interview = InterviewV2(survey)
                    interview.mass_interview()
                except Exception as e:
                    st.error(f"Failed to complete the interview: {str(e)}")

            st.session_state["interview_results"] = interview.get_results()
            
            st.success("Interview completed successfully.")
            st.session_state["current_page"] = OUTPUT_RESULTS
            st.session_state["page_history"].append(INPUT_FORM)
            st.rerun()


def output_results():
    """The results/output page function."""
    cols = st.columns([1, 9])  # Adjust the ratio as needed
    with cols[0]:
        if st.button("Go Back", key="go_back_output"):
            go_back()

    with cols[1]:  # Main content starts here
        st.title("Analytics Output")
        # Check if interview results are available and display them
        if "interview_results" in st.session_state:
            interview_results = st.session_state["interview_results"]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.header("Survey Responses")
                st.write(interview_results)  # Assuming interview_results is in a displayable format
            with col2:
                st.header("Sentiment")
                # Display sentiment analysis results here, if applicable
            with col3:
                st.header("Risk")
                # Display risk assessment results here, if applicable
        else:
            st.write("No interview results to display.")

# Mapping of page names to their corresponding functions for easier navigation handling
page_names_to_funcs = {
    HOME: intro,
    INPUT_FORM: input_form,
    OUTPUT_RESULTS: output_results,
}

# Execute the function associated with the current page
if st.session_state["current_page"] in page_names_to_funcs:
    page_names_to_funcs[st.session_state["current_page"]]()
