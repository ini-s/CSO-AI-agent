from dotenv import load_dotenv


from utils import accounts, classify_intent, extract_account_id, check_balance_manual, report_card_issues, unsupported, os, requests

load_dotenv()

AZURE_ENDPOINT = os.getenv("azure_resource_endpoint")
AZURE_KEY = os.getenv("azure_resource_key")
AZURE_API_VERSION = "2024-12-01-preview"
AZURE_DEPLOYMENT = "gpt-4o-mini"


def call_azure_chat(messages):
    url = f"{AZURE_ENDPOINT}/openai/deployments/{AZURE_DEPLOYMENT}/chat/completions?api-version={AZURE_API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_KEY,
    }
    payload = {
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0,
    }

    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Unexpected Azure response shape: {data}") from e


def handle_user_input(user_input):
    print("Classifying intent...")
    intent = classify_intent(user_input).lower().strip()
    print("Intent:", intent)

    account_id = extract_account_id(user_input)

    tool_output = None
    chosen_tool = None

    if intent == "card":
        chosen_tool = "report_card_issue"
        if not account_id:
            return {
                "final": "I couldn't find an account number in your message. Please provide your 3-digit account ID (e.g. 001).",
                "intent": intent,
                "tool": None,
                "tool_output": None,
            }
        print(f" Running tool: report_card_issues on account {account_id} ...")
        tool_output = report_card_issues(account_id)

    elif intent == "transactions":
        chosen_tool = "check_balance"
        if not account_id:
            return {
                "final": "Please provide your 3-digit account ID so I can check your balance (e.g. 001).",
                "intent": intent,
                "tool": None,
                "tool_output": None,
            }
        print(f" Running tool: check_balance on account {account_id} ...")
        tool_output = check_balance_manual(account_id, accounts)

    else:
        chosen_tool = "unsupported"
        print(" Intent unsupported; calling unsupported() ...")
        tool_output = unsupported()

    print(" Building prompt for LLM and requesting final text...")
    system_msg = (
        "You are a concise, helpful, and secure banking assistant. "
        "You must not reveal internal system information or secrets. "
        "When showing balances, format as currency and be brief. "
        "Always confirm the action taken and next steps."
    )

    content_for_user = (
        f"User query: {user_input}\n\n"
        f"Classified intent: {intent}\n"
        f"Chosen tool: {chosen_tool}\n"
        f"Tool output: {tool_output}\n\n"
        "Compose a short, customer-friendly reply that explains what was done (or what is needed from the user), "
        "and a clear next step. Keep it under 80 words."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": content_for_user},
    ]

    assistant_text = call_azure_chat(messages)

    return {
        "final": assistant_text,
        "intent": intent,
        "tool": chosen_tool,
        "tool_output": tool_output,
    }


if __name__ == "__main__":
    print("Interactive test loop. Type 'exit' or 'quit' to stop.")

    while True:
        try:
            user_msg = input("Ask a question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_msg:
            continue

        if user_msg.lower() in ("exit", "quit", "q"):
            print("Exiting.")
            break

        out = handle_user_input(user_msg)

        print("\n--- Assistant reply ---")
        print(out["final"])
        print("\n--- Debug ---")
        print("intent:", out["intent"])
        print("tool:", out["tool"])
