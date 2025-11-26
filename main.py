from utils import *
from tools import tools

if __name__ == "__main__":
    accounts = {
        "001": {"name": "Ini", "balance": 200000},
        "002": {"name": "Bolu", "balance": 420000},
        "003": {"name": "Ebuks", "balance": 3000000},
        "004": {"name": "Daniel", "balance": 250000},
    }

    llm = azure_llm()
    tools = tools

    prompt_agent = """
        You are banking assistant. You MUST follow these steps:
        1. First, ALWAYS use the IntentClassifier tool to understand the user's intent
        2. Then, based on the classified intent, use the appropriate tool
        3. If the user does not provide an account number, ask them to
        User query: {input}
        Let's think step by step:
    """

    agent = ZeroShotAgent.from_llm_and_tools(
        llm=llm,
        tools=tools,
        prefix=prompt_agent   
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_erros=True,
    )

    result = agent_executor.invoke({"input":"I lost my ATM card. My account is 001. Please block it"})

    print(result["output"])