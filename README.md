# CSO AI Banking Assistant

This project implements a banking assistant  that can classify user intents, execute banking actions (like checking balance or blocking a card), and generate customer-friendly responses using Azure OpenAI.  

Two implementations are included:

---

## 1. LangChain Implementation

- Uses **LangChain agents** and tools to handle user intents.
- Tools:
  - `IntentClassifier` – classifies user queries into intents (`transaction`, `card`, `unsupported`).
  - `CheckBalance` – returns account balance.
  - `report_card_issue` – simulates card blocking.
- LLM: `AzureChatOpenAI` deployed on Azure.
- Entry point: `main.py`
- Features:
  - Agent automatically routes the query to the correct tool.
  - Generates responses using the Azure LLM.

---

## 2. Manual Implementation (No LangChain)

* Directly calls the **custom classifier** (`classify_intent`) and **Azure LLM**.
* Implements the same tool logic (`check_balance`, `report_card_issues`, `unsupported`) manually.
* Handles user input in a continuous interactive loop:

  * Extracts account numbers from user queries.
  * Maps intents to tools manually.
  * Calls Azure LLM to generate the final response.
* Entry point: `manual-test.py`
* Advantages:

  * Lightweight, no LangChain dependency.
  * Full control over the flow of intent classification and tool execution.

**Example Interaction:**

```
Ask a question: I lost my ATM card. My account number is 002
Classifying intent...
Intent: card
 Running tool: report_card_issues on account 002 ...
 Building prompt for LLM...
--- Assistant reply ---
Your card for account 002 has been blocked. Next step: Collect a new card in 48 hours.
```

---

## Environment Variables

Ensure a `.env` file exists with:

```
azure_resource_endpoint=<Your Azure Endpoint>
azure_resource_key=<Your Azure API Key>
model_endpoint=<Your Custom Model Endpoint>
model_api_key=<Your Custom Model Key>
```

---

## Accounts (for testing)

Sample accounts are hardcoded in both implementations:

```python
accounts = {
    "001": {"name": "Ini", "balance": 200000},
    "002": {"name": "Bolu", "balance": 420000},
    "003": {"name": "Ebuks", "balance": 3000000},
    "004": {"name": "Daniel", "balance": 250000},
}
```

---

## How It Works (Both Versions)

1. User enters a query.
2. Intent is classified (`transaction`, `card`, or `unsupported`).
3. Appropriate tool is called based on the intent:

   * `transaction` → check balance.
   * `card` → block card.
   * `unsupported` → fallback response.
4. Response is generated using Azure LLM and displayed to the user.

---

## Dependencies

* Python 3.10+
* `requests`
* `python-dotenv`
* `azure-cognitiveservices-speech`
* `langchain_openai` (for LangChain version)
* `langchain_classic` (for LangChain version)

---

Both versions achieve the same functional flow; the manual one removes the LangChain abstraction for simpler control and easier debugging.

```
