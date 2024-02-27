import autogen

# Function to generate follow-up questions based on the last response
def generate_follow_up_question(response):
    # Implement logic to analyze the response and generate a follow-up question.
    # This is a placeholder logic. You need a more sophisticated NLP model to generate meaningful follow-up questions.
    keywords = ["features", "privacy", "user experience", "technology"]
    questions = {
        "features": "Can you elaborate on the specific features that stand out?",
        "privacy": "How does Apple Vision ensure user privacy and data security?",
        "user experience": "What makes the user experience with Apple Vision unique?",
        "technology": "Can you tell us more about the technology behind Apple Vision?",
    }
    for keyword in keywords:
        if keyword in response.lower():
            return questions[keyword]
    return "Can you provide more details?"

# Set up your configuration
config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")

# Create the agents
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 41,
        "config_list": config_list,
    },
    response_processor=lambda x: generate_follow_up_question(x["content"]),
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "use_docker": False
    },
)

# Hardcoded topic for demonstration
topic = """
Please provide your opinion on the following product: Introducing the new Apple Vision - a revolutionary device that redefines the way you interact with your digital life.
"""

# Function to simulate the interview process
def simulate_interview():
    response = None
    for _ in range(5):  # Limit to 5 questions for this example
        if response:
            question = assistant.process_response({"content": response})
        else:
            question = "What are your initial thoughts on Apple Vision?"
        print(f"Assistant asks: {question}")
        response = input("User Proxy responds: ")  # In real scenario, this would be the user_proxy generating a response.
        if "TERMINATE" in response:
            break

# Example usage
simulate_interview()
