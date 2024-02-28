import json
# import random
# import autogen
# import requests

import openai
from population import Population

from survey import Survey
from dotenv import load_dotenv
load_dotenv()

client = openai.Client()
# class ProductInterview:
#     def __init__(self, age, income, products_to_test):
#         self.age = age
#         self.income = income
#         self.products_to_test = products_to_test
#         self.config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
#         self.llm_config = {"config_list": self.config_list}
#         self.interviewer = None
#         self.interviewee = None
#         self.interview_chat = None
#         self.interview_manager = None
#         self.setup_interview_environment()

#     def setup_interview_environment(self):
#         self.interviewer = autogen.AssistantAgent(
#             name="Interviewer",
#             system_message="You ask follow-up questions based on the interviewee responses and personal opinions for the product.",
#             llm_config=self.llm_config,
#             code_execution_config=False,
#         )
#         self.interviewee = autogen.AssistantAgent(
#             name="Interviewee",
#             system_message="You are a person that came to test a product and give your personal opinion about it.",
#             llm_config=self.llm_config,
#             code_execution_config=False,
#         )
#         self.interview_chat = autogen.GroupChat(
#             agents=[self.interviewer, self.interviewee],
#             messages=[],
#             speaker_selection_method="round_robin",
#             allow_repeat_speaker=False,
#             max_round=10,
#         )
#         self.interview_manager = autogen.GroupChatManager(
#             groupchat=self.interview_chat,
#             code_execution_config={
#                 "work_dir": "interview",
#                 "use_docker": False,
#             },
#             is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
#             llm_config=self.llm_config,
#         )

#     def initiate_interview(self):
#         for product in self.products_to_test:
#             self.interview_manager.initiate_chat(self.interviewee, message=product, max_turns=12)

#     def get_conversation_logs(self):
#         return self.interview_chat.messages

class InterviewV2:
    def __init__(self, survey:Survey):
        self.survey = survey
        self.population = survey.target_audience
        self.answers = {question: {user: "" for user in survey.target_audience.get_population()} for question in survey.get_questions()}
    def interview_user(self, individual):
        memory = []  # This will store past Q&A pairs
        for question in self.survey.survey_questions:
            # Convert past Q&As into a format that can be included in the prompt
            past_interactions = "\n\n".join(memory)

            model = "gpt-3.5-turbo" if not self.survey.assets else "gpt-4-vision-preview"
            system_prompt = f"""
            We are conducting an interview with a participant for a focus group survey. We will ask 
            the participant to give their opinion about the ad campaign or product. We have
            a 50-word description of them as background information about them,
            which gives us insights about how they think.
            This is today's participant:
            ```
            {individual}
            ```
            The individual is shown the ad campaign or product and asked to give their opinion, 
            this might include images that should be looked very closely. We will take 
            into consideration this information very seriously, and will always give genuine feedback.
            {{
                "ad_campaign": "{self.survey.campaign_description}",
                "intent": "{self.survey.campaign_intent}",
            }}
            
            Interviewer: "Hello, nice to meet you! Thank you for participating in our survey.
            We will now begin the interview."
            Respondent: "Hello, thank you for having me."
            Interviewer: "My pleasure. Please respond, with your true thoughts, don't hesitate to be honest.
            Your opinion is very important to us."
            Respondent: "Of course, I will be honest, and give short and honest feedback based on who I am."
            Interviewer: "Great! Let's start with the questions."
            
            {past_interactions}  

            Interviewer: "{question}"
            Respondent: "
            """
            try:
                content = [{"type": "text", "text": system_prompt}]
                if self.survey.assets:
                    for asset in self.survey.assets:
                        content.append({
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{asset}"  # Ensure this is correct; it might be asset.image_url or similar
                        })
                messages = [{"role": "system", "content": content}]
                response = client.chat.completions.create(model=model, messages=messages, max_tokens=1000)
                print(f"Question: {question}")
                print(f"Response: {response.choices[0].message.content}")
                self.answers[question][individual] = response.choices[0].message.content
                # Add the current Q&A pair to memory for use in future questions
                memory.append(f"Interviewer: {question}\nRespondent: {response.choices[0].message.content.strip()}")  
            except Exception as e:
                # Log the exception
                print(f"An error occurred: {e}")
                # Optionally, you can log additional details about the error, if available
                if hasattr(e, 'response'):
                    print("Error details:", e.response.text)
    def mass_interview(self):
        for individual in self.population.get_population():
            self.interview_user(individual)
    def get_results(self):
        return self.answers
    def save_results(self):
        # Save a dictionary with the info
        interview = {
            "survey": self.survey,
            "population": self.population,
            "answers": self.answers
        }    
        with open("interview.json", "w") as file:
            file.write(json.dumps(interview))

    
if __name__ == "__main__":
        # Define assets (images)
    assets = [
        # encode_image("assets/valor.jpg")
    ]    
    # Define campaign description, intent, and target audience
    campaign_description = "Chocolates Valor presenta su gama de productos y sabores que van desde lo más tradicional a lo más innovador. Placer en estado puro."
    campaign_intent = "We want to evoke a premium and traditional feeling in the user"
    ages = [20, 25, 30, 35, 40, 45, 50]  # Example age range
    incomes = [30000, 40000, 50000, 60000, 70000]  # Example income brackets
    gender_distribution = 50  # Assuming a 50-50 gender split
    interests = ['sports', 'music', 'art', 'technology', 'cooking']  # Example interests
    locations = ['New York', 'California', 'Texas', 'Florida', 'Illinois']  # Example locations
    # Instantiate the Population class with the defined parameters
    print("Creating a population")
    my_population = Population(ages, incomes, gender_distribution, interests, locations, 5)
    target_audience = my_population
    print("Creating a survey")
    # Create a survey
    survey = Survey(assets, campaign_description, target_audience,campaign_intent)
    
    # Print survey questions
    print("Survey Questions:")
    for i, question in enumerate(survey.get_questions(), start=1):
        print(f"Question {i}: {question}")
    print("Conducting interview")
    interview = InterviewV2(survey)
    interview.mass_interview()