import base64
from dotenv import load_dotenv

load_dotenv()
import openai
client = openai.Client()
from population import Population


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

class Survey:
    """
    A class to represent a survey about an ad campaign.
    
    Attributes:
        assets (list): List of images to be used in the campaign in base64 format.
        text (str): Text to be used in the campaign.
        target_audience (Population): An instance of the Population class representing the target audience.
        survey_questions (list): List of strings describing the survey questions.
        survey_responses (list): List of strings describing the survey responses.
    """
    
    def __init__(self, assets, campaign_description, target_audience:Population, campaign_intent=None, survey_questions=[]):
        """
        Constructs all the necessary attributes for the survey object.
        
        Parameters:
            assets (list): List of images to be used in the campaign.
            campaign_description (str): Text to be used in the campaign.
            campaign_intent (str): The intent of the campaign.
            target_audience (Population): An instance of the Population class.
            survey_questions (list): List of strings describing the survey questions.
        """
        self.assets = assets
        self.campaign_description = campaign_description
        self.campaign_intent = campaign_intent
        self.target_audience = target_audience
        self.survey_questions = self.create_survey()
        self.survey_responses = []  # Initialize as empty; will be filled out by responses
    
    def create_survey(self):
        """
        Creates a survey based on the specified attributes.
        This method could prepare and format the survey for presentation to the target audience.
        """
        # Use Gpt3.5 if there are no assets
        model = "gpt-3.5-turbo" if not self.assets else "gpt-4-vision-preview"
        system_prompt = f"""
        Please create a list of 10 questions to be given to respondants to assess how suitable an ad 
        campaign or product is. We will give you info about the campaign, as the description and if 
        needed images, as well as a description of the population and the intent. Only create questions 
        about the images and their content if provided amongst this text.
        {{
        "campaign_description": "{self.campaign_description}",
        "campaign_intent": "{self.campaign_intent}",
        "population_description": "{self.target_audience.get_population_description()}",
        }}
        Respond on a List format, without any other text. no intro or headers. Separate questions with a -.
        """
        try:
            content = [{"type": "text", "text": system_prompt}]
            for asset in self.assets:
                content.append({
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{asset}"
                })
            messages = [{"role": "system", "content": content}]
            response = client.chat.completions.create(model=model, messages=messages, max_tokens=1000)
        except Exception as e:
            # Log the exception
            print(f"An error occurred: {e}")
            # Optionally, you can log additional details about the error, if available
            if hasattr(e, 'response'):
                print("Error details:", e.response.text)
        raw_questions = response.choices[0].message.content
        # Split the raw questions into a list of questions detect by -
        questions = raw_questions.split("-")
        # Remove empty strings or strings with less than 5 characters
        questions = [question.strip() for question in questions if question.strip() and len(question.strip()) > 5]
        return questions
        
    def get_questions(self):
        """
        Returns the list of survey questions.
        
        Returns:
            list: The list of survey questions.
        """
        return self.survey_questions
    def save_survey(self):
        # Save a dictionary with the info
        survey = {
            "assets": self.assets,
            "campaign_description": self.campaign_description,
            "campaign_intent": self.campaign_intent,
            "target_audience": self.target_audience,
            "survey_questions": self.survey_questions,
            "survey_responses": self.survey_responses
        }
        return survey
# Main function to test the Survey class
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
    my_population = Population(ages, incomes, gender_distribution, interests, locations, 5)
    target_audience = my_population
    # Create a survey
    survey = Survey(assets, campaign_description, target_audience,campaign_intent)
    
    # Print survey questions
    print("Survey Questions:")
    for i, question in enumerate(survey.get_questions(), start=1):
        print(f"Question {i}: {question}")
