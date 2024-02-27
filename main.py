import streamlit as st
from interview import ProductInterview  # Ensure this is a valid import in your project
from assets.homepage import homepage_html  # Ensure this is a valid import in your project

# Constants for easier maintenance and updates
HOME = 'Home'
INPUT_FORM = 'Input Form'
OUTPUT_RESULTS = 'Output Results'

# Set up the page
st.set_page_config(page_title="HYDR.AI", layout="wide", page_icon="assets/logo.png")

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = HOME

if 'page_history' not in st.session_state:
    st.session_state['page_history'] = [HOME]  

st.session_state['page_history'] = st.session_state.get('page_history', [HOME])
def go_back():
    """Go back to the previous page."""
    if len(st.session_state['page_history']) > 1:  # Ensure there is a previous page
        st.session_state['page_history'].pop()  # Remove current page
        st.session_state['current_page'] = st.session_state['page_history'][-1]  # Set to previous page
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

    col1, col2, col3 = st.columns([2.6,1,2])  # Adjust the ratio as needed for better centering
    with col2:  # This puts the button in the center column
        st.write('<br><br>', unsafe_allow_html=True)  # Add more <br> tags to move the button further down
        if st.button("Input Form"):
            st.session_state['current_page'] = INPUT_FORM
            st.session_state['page_history'].append(INPUT_FORM)
            st.experimental_rerun()

def input_form():
    """The input form page function."""
    cols = st.columns([1, 9])  # Adjust the ratio as needed
    with cols[0]:
        if st.button("Go Back", key='go_back_input'):
            go_back()
    
    with cols[1]:  # Main content starts here
        st.header("Product")
        # Define your form fields here
        # Example:
        campaign_description = st.text_area("Enter campaign description", height=150)
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
            with st.spinner('Please wait... Interview in progress'):
                try:
                    # Adjust the call to initiate_interview if it's supposed to take parameters
                          
                    products = [
                        "Give your opinion about coca colas with strawberry flavour.",
                        "Give your opinion about the new apple vision pro",
                    ]
                            
                    interview = ProductInterview(age=age, income=income, products_to_test=products)

                    st.success("Interview completed successfully.")
                    # Wait 2 seconds to simulate a process
                    
                    st.session_state['current_page'] = OUTPUT_RESULTS
                    st.session_state['page_history'].append(INPUT_FORM)
                    st.experimental_rerun() 
                    # Process the output as needed, for example:
                    # st.write(output)
                except Exception as e:
                    st.error(f"Failed to complete the interview: {str(e)}")


def output_results():
    """The results/output page function."""
    cols = st.columns([1, 9])  # Adjust the ratio as needed
    with cols[0]:
        if st.button("Go Back", key='go_back_output'):
            go_back()

    with cols[1]:  # Main content starts here
        st.title("Analytics Output")
        # Layout for output results, you can adjust as necessary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Survey Responses")
            # Display survey responses or other information
        with col2:
            st.header("Sentiment")
            # Display sentiment analysis results
        with col3:
            st.header("Risk")
            # Display risk assessment results

# Mapping of page names to their corresponding functions for easier navigation handling
page_names_to_funcs = {
    HOME: intro,
    INPUT_FORM: input_form,
    OUTPUT_RESULTS: output_results,
}

# Execute the function associated with the current page
if st.session_state['current_page'] in page_names_to_funcs:
    page_names_to_funcs[st.session_state['current_page']]()
