import autogen

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {"config_list": config_list}

# Define interview questions
products_to_test = [
    "Give your opinion about coca colas with strawberry flavour.",
    "Give your opinion about the new apple vision pro",
]

# Configure the interviewer - This should be an AssistantAgent with the role of asking questions.
interviewer = autogen.AssistantAgent(
    name="Interviewer",
    system_message="You ask follow-up questions based on the interviewee responses and personal opinions for the product.",
    llm_config={"config_list": config_list},
    code_execution_config=False,
)

interviewee = autogen.AssistantAgent(
    name="Interviewee",
    system_message=f"You are a person that came to test a product and give your personal opinion about it.",
    llm_config={"config_list": config_list},
    code_execution_config=False,
)

# Set up a GroupChat for the interview
interview_chat = autogen.GroupChat(
    agents=[interviewer, interviewee],
    messages=[],
    speaker_selection_method="round_robin",
    allow_repeat_speaker=False,
    max_round=10,  # Each question and answer counts as a round.
)

# Configure GroupChatManager for managing the interview process
interview_manager = autogen.GroupChatManager(
    groupchat=interview_chat,
    code_execution_config={
        "work_dir": "interview",
        "use_docker": False,
    },
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
)

def initiate_interview():
    for product in products_to_test:
        interview_manager.initiate_chat(interviewee, message=product, max_turns=12)

if __name__ == "__main__":
    initiate_interview()
