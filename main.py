import math
import time
import numpy as np
import streamlit as st
from interview import InterviewV2
from population import Population
from assets.homepage import homepage_html
from survey import Survey
from analysis import analyze_results, compute_word_relevance, embedding_api, top_words
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from analysis import analyze_results, compute_word_relevance
import plotly.graph_objects as go
# Constants for easier maintenance and updates
HOME = "Home"
INPUT_FORM = "Input Form"
OUTPUT_RESULTS = "Output Results"
APPLE_DEMO = "Apple Demo"

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
        st.write('<br style="line-height: 6;"><br><br>', unsafe_allow_html=True)
        if st.button("New Study"):
            st.session_state["current_page"] = INPUT_FORM
            st.session_state["page_history"].append(INPUT_FORM)
            st.rerun()
        if st.button("Demo Apple"):
            st.session_state["current_page"] = APPLE_DEMO
            st.session_state["page_history"].append(APPLE_DEMO)
            st.rerun()

def input_form():
    """The input form page function."""
    cols = st.columns([1, 9])
    with cols[0]:
        if st.button("Go Back", key="go_back_input"):
            go_back()

    with cols[1]:
        st.header("Product")
        campaign_description = st.text_area("Enter campaign description", height=150, value="Chocolates Valor presents its range of products and flavors that range from the most traditional to the most innovative. Pure pleasure")
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
                        campaign_intent
                    )
                    # Print survey questions
                    print("Survey Questions:")
                    for i, question in enumerate(survey.get_questions(), start=1):
                        print(f"Question {i}: {question}")
                except Exception as e:
                    st.error(f"Failed to create survey questions: {str(e)}")
            with st.spinner("Please wait... Conducting interview"):
                # try:
                print("Conducting interview")
                interview = InterviewV2(survey)
                interview.mass_interview() 
                # except Exception as e:
                    # st.error(f"Failed to complete the interview: {str(e)}")

            st.session_state["interview_results"] = interview.get_results()
            
            st.success("Interview completed successfully.")
            st.session_state["current_page"] = OUTPUT_RESULTS
            st.session_state["page_history"].append(INPUT_FORM)
            st.rerun()



def output_results():
    """The results/output page function."""
    st.title("Analytics Output")
    st.markdown("---")

    if "interview_results" in st.session_state:
        interview_results = st.session_state["interview_results"]
        print(f"[DEBUG] interview_results: {interview_results}")

        with st.spinner("Analyzing results..."):
            insights = analyze_results(interview_results)
            st.balloons()
            # print(f"[DEBUG] INSIGHTS: {insights}")
        
        # Create two columns for the layout
        col1, col2 = st.columns([2, 3])  # Adjust the ratio as per your content size

        with col1:
            st.subheader("Questions insights")
            for insight in insights:
                for question_id, detail in insight.items():
                    with st.expander(f"Insight for Question {question_id.split('_')[-1]}"):
                        st.markdown("**Top Topics:** " + ', '.join(detail["topics"]))
                        st.markdown("**Positive Feedback:** " + ', '.join(detail["good"]))
                        st.markdown("**Areas for Improvement:** " + ', '.join(detail["bad"]))
        
        with col2:
            with st.spinner("Getting top words of the interview..."):
                topic = [value["topics"] for question in insights for key, value in question.items()]
                words = top_words(str(topic), 5)
            
            word_embedding = {}
            for word in words:
                word_embedding[word] = embedding_api(word)
            
            questions_embeding = [value["embeddings"] for question in insights for key, value in question.items()]
            relevance = []
            for key, value in word_embedding.items():
                word_em = np.array(value).flatten()
                sum_relevance = 0
                for question in questions_embeding:
                    question = np.array(question).flatten()
                    sum_relevance += np.dot(question, word_em) / (np.linalg.norm(question) * np.linalg.norm(word_em))
                relevance.append(sum_relevance)
            
            df = pd.DataFrame({'Words': words, 'Relevance': relevance})
            df = df.sort_values(by='Relevance', ascending=False)

            fig = go.Figure()
            categories = df['Words']
            r_values = df['Relevance'].tolist() + [df['Relevance'].iloc[0]]
            theta_values = categories + [categories[0]]
            fig.add_trace(go.Scatterpolar(
                r=r_values,
                theta=theta_values,
                line_color='rgb(202, 231, 22)',
                fillcolor='rgba(239, 247, 188,0.5)',
                fill='toself',
                line=dict(width=2, color='rgb(202, 231, 22)'),
    
                name='Top Words'
            ))
            fig.update_layout(
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, math.ceil(df['Relevance'].max())]
                )),
            showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            # Convert the structure to a DataFrame
        data = []
        for question, responses in st.session_state["interview_results"].items():
            for individual, response in responses.items():
                data.append([question, individual, response])

        # Create DataFrame
        df_all = pd.DataFrame(data, columns=['Question', 'Individual', 'Response'])
        st.dataframe(df_all)
    else:
        st.write("No interview results to display.")

def apple_output_results():
    """The results/output page function."""
    st.title("Analytics Output")
    st.markdown("---")

    # Load from results from file
    with open("results.txt", "r") as file:
        interview_results = file.read()
    interview_results = eval(interview_results)
    
    print(f"[DEBUG] interview_results: {interview_results}")

    with st.spinner("Analyzing results..."):
        insights = analyze_results(interview_results)
        st.balloons()
        # print(f"[DEBUG] INSIGHTS: {insights}")
    
    # Create two columns for the layout
    col1, col2 = st.columns([2, 3])  # Adjust the ratio as per your content size

    with col1:
        st.subheader("Questions insights")
        max_height_style = """
            <style>
                .scrollable-container {
                    overflow-y: auto;
                    max-height: 500px; /* Adjust the max-height as needed */
                }
            </style>
            """

        # Inject custom CSS with the above style
        st.markdown(max_height_style, unsafe_allow_html=True)

        # Wrap the content you want to be scrollable inside a div with the scrollable-div class
        
        for insight in insights:
            for question_id, detail in insight.items():
                with st.expander(f"Insight for Question {question_id.split('_')[-1]}"):
                    st.markdown("**Top Topics:** " + ', '.join(detail["topics"]))
                    st.markdown("**Positive Feedback:** " + ', '.join(detail["good"]))
                    st.markdown("**Areas for Improvement:** " + ', '.join(detail["bad"]))
        
       
    with col2:
        with st.spinner("Getting top words of the interview..."):
            topic = [value["topics"] for question in insights for key, value in question.items()]
            words = top_words(str(topic), 5)
        
        word_embedding = {}
        for word in words:
            word_embedding[word] = embedding_api(word)
        
        questions_embeding = [value["embeddings"] for question in insights for key, value in question.items()]
        relevance = []
        for key, value in word_embedding.items():
            word_em = np.array(value).flatten()
            sum_relevance = 0
            for question in questions_embeding:
                question = np.array(question).flatten()
                sum_relevance += np.dot(question, word_em) / (np.linalg.norm(question) * np.linalg.norm(word_em))
            relevance.append(sum_relevance)
        
        df = pd.DataFrame({'Words': words, 'Relevance': relevance})
        df = df.sort_values(by='Relevance', ascending=False)

        fig = go.Figure()
        categories = df['Words']
        r_values = df['Relevance'].tolist() + [df['Relevance'].iloc[0]]
        theta_values = categories + [categories[0]]
        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=theta_values,
            line_color='rgb(202, 231, 22)',
            fillcolor='rgba(239, 247, 188,0.5)',
            fill='toself',
            line=dict(width=2, color='rgb(202, 231, 22)'),

            name='Top Words'
        ))
        fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, math.ceil(df['Relevance'].max())]
            )),
        showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        # Convert the structure to a DataFrame
    data = []
    for question, responses in interview_results.items():
        for individual, response in responses.items():
            data.append([question, individual, response])

    # Create DataFrame
    df_all = pd.DataFrame(data, columns=['Question', 'Individual', 'Response'])
    st.dataframe(df_all)


# Mapping of page names to their corresponding functions for easier navigation handling
page_names_to_funcs = {
    HOME: intro,
    INPUT_FORM: input_form,
    OUTPUT_RESULTS: output_results,
    APPLE_DEMO: apple_output_results
}

# Execute the function associated with the current page
if st.session_state["current_page"] in page_names_to_funcs:
    page_names_to_funcs[st.session_state["current_page"]]()
