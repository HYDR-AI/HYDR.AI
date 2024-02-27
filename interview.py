import autogen

class ProductInterview:
    def __init__(self, age, income, products_to_test):
        # Interviewee parameters
        self.age = age
        self.income = income
        
        # Interview parameters
        self.products_to_test = products_to_test
        
        # Config setup
        self.config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
        self.llm_config = {"config_list": self.config_list}
        
        # Define interviewer and interviewee as instance attributes
        self.interviewer = None
        self.interviewee = None
        self.interview_chat = None
        self.interview_manager = None
        self.setup_interview_environment()

    def setup_interview_environment(self):
        self.interviewer = autogen.AssistantAgent(
            name="Interviewer",
            system_message="You ask follow-up questions based on the interviewee responses and personal opinions for the product.",
            llm_config=self.llm_config,
            code_execution_config=False,
        )

        self.interviewee = autogen.AssistantAgent(
            name="Interviewee",
            system_message="You are a person that came to test a product and give your personal opinion about it.",
            llm_config=self.llm_config,
            code_execution_config=False,
        )

        self.interview_chat = autogen.GroupChat(
            agents=[self.interviewer, self.interviewee],
            messages=[],
            speaker_selection_method="round_robin",
            allow_repeat_speaker=False,
            max_round=10,  # Each question and answer counts as a round.
        )

        self.interview_manager = autogen.GroupChatManager(
            groupchat=self.interview_chat,
            code_execution_config={
                "work_dir": "interview",
                "use_docker": False,
            },
            is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
            llm_config=self.llm_config,
        )

    def initiate_interview(self):
        for product in self.products_to_test:
            self.interview_manager.initiate_chat(self.interviewee, message=product, max_turns=12)

    def get_conversation_logs(self):
        return self.interview_chat.messages

if __name__ == "__main__":
    products = [
        "Give your opinion about coca colas with strawberry flavour.",
        "Give your opinion about the new apple vision pro",
    ]
    interview = ProductInterview(age=30, income=50000, products_to_test=products)
    interview.initiate_interview()
    
    print(f"#################### LOGS ####################")
    logs = interview.get_conversation_logs()
    print(logs)
