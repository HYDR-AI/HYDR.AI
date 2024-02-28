
import random
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()


class Population:
    """
    A class to represent a population group.

    Attributes:
        ages (list of int): List of ages of the individuals.
        incomes (list of int): List of incomes of the individuals.
        gender_distribution (int): Percentage of males in the population.
        interests (list of str): List of interests prevalent within the population.
        locations (list of str): List of locations from where the individuals are.
        population_size (int): Number of individuals in the population.
        individuals (list): Container for storing individual profiles.

    Methods:
        create_population(): Creates a population based on the specified attributes.
        create_individual(age, income, gender, interests, location): Creates and returns a dictionary representing an individual.
        get_population(): Returns the list of individuals in the population.
    """

    def __init__(self, ages: list, incomes: list, gender_distribution: int, interests: list, locations: list, population_size: int):
        """
        Constructs all the necessary attributes for the population object.

        Parameters:
            ages (list of int): List of possible ages for the individuals.
            incomes (list of int): List of possible incomes for the individuals.
            gender_distribution (int): The percentage representation of males in the population.
            interests (list of str): List of interests that the population may have.
            locations (list of str): List of possible locations of the individuals.
            population_size (int): The total number of individuals in the population.
        """
        self.ages = ages
        self.incomes = incomes
        self.gender_distribution = gender_distribution  # Assume this is the percentage of males in the population.
        self.interests = interests
        self.locations = locations
        self.population_size = population_size
        self.individuals = []
        self.create_population()

    def create_population(self):
        """
        Generates the population based on the initialized attributes.
        Each individual is randomly assigned attributes from the provided lists and added to the population.
        """
        for _ in range(self.population_size):
            age = random.choice(self.ages)
            income = random.choice(self.incomes)
            gender = 'Male' if random.randint(1, 100) <= self.gender_distribution else 'Female'
            interests = random.sample(self.interests, k=min(len(self.interests), 3))
            location = random.choice(self.locations) 
            self.individuals.append(self.create_individual(age, income, gender, interests, location))

    def create_individual(self, age: int, income: int, gender: str, interests: list, location: str):
        """
        Creates a dictionary representing an individual with specified characteristics.

        Parameters:
            age (int): The age of the individual.
            income (int): The income of the individual.
            gender (str): The gender of the individual.
            interests (list of str): The interests of the individual.
            location (str): The location of the individual.

        Returns:
            dict: A dictionary containing the individual's characteristics.
        """
        # Construct the system prompt
        system_prompt = f"""
            User
            We are playing a role-playing game. We are still creating the characters, I will provide you a JSON with the description of a participant for a focus group survey. You have to make a 50-word description of them as background information about them, which gives us insights about how they think. Description must include everything including name, answer must be plain text without introduction or formatting.
            {{
                "age": {age},
                "income": {income},
                "gender": "{gender}",
                "interests": {interests},
                "location": "{location}"
            }}
        """.strip()

        # Call the GPT-3.5 Turbo to generate the respondent
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                ],
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        # Append the generated description to the individuals list
        self.individuals.append(response.choices[0].message.content)

    def get_population(self):
        """
        Returns the list of individuals in the population.

        Returns:
            list: The list of individual dictionaries.
        """
        return self.individuals

# Main function to test the Population class
if __name__ == "__main__":
    ages = [20, 25, 30, 35, 40, 45, 50]  # Example age range
    incomes = [30000, 40000, 50000, 60000, 70000]  # Example income brackets
    gender_distribution = 50  # Assuming a 50-50 gender split
    interests = ['sports', 'music', 'art', 'technology', 'cooking']  # Example interests
    locations = ['New York', 'California', 'Texas', 'Florida', 'Illinois']  # Example locations
    # Instantiate the Population class with the defined parameters
    my_population = Population(ages, incomes, gender_distribution, interests, locations, 5)
    # Retrieve the generated population
    individuals = my_population.get_population()
    # Print the first few individuals to check
    for individual in individuals[:5]:  # Print the first five individuals
        print(individual)