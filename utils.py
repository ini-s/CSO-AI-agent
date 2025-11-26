import os
import requests
import json
import re

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_classic.agents import AgentExecutor, Tool
from langchain_classic.prompts import PromptTemplate
import azure.cognitiveservices.speech as speech
from langchain_classic.agents.mrkl.base import ZeroShotAgent

load_dotenv()

accounts = {
    "001": {"name": "Ini", "balance": 200000},
    "002": {"name": "Bolu", "balance": 420000},
    "003": {"name": "Ebuks", "balance": 3000000},
    "004": {"name": "Daniel", "balance": 250000},
}


def classify_intent(text: str):
    model_api_endpoint = os.getenv("model_api_endpoint")
    model_api_key = os.getenv("model_api_key")
    response = requests.post(url=model_api_endpoint, json={"text": text}, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {model_api_key}"
    })
    data = dict(response.json())

    print(data["prediction"])
    return data["prediction"]


def azure_llm():
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("azure_resource_endpoint"),
        api_key=os.getenv("azure_resource_key"),
        api_version="2024-12-01-preview",
        max_tokens=4096,
        temperature=0,
        azure_deployment="gpt-4o-mini",
    )

    return llm


def extract_account_id(text: str):
    match = re.search(r'\b(\d{3})\b', text)
    return match.group(1) if match else None


def check_balance(account_id: str):
    acct = accounts.get(account_id, None)
    if not acct:
        return {'error': "Account not found"}
    return acct

def check_balance_manual(account_id: str, accounts: dict):
    acct = accounts.get(account_id, None)
    if not acct:
        return {'error': "Account not found"}
    return acct

def report_card_issues(account_id: str):
    # simulate blocking card
    return {"status": "blocked", "account_id": account_id, "next_step": "Collect new card in 48hrs"}


def unsupported():
    return {"status": "unsupported"}
