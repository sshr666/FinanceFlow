import json
import requests
import pandas as pd
from analytics.translator import translate

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:latest"
TIMEOUT = 180


def generate_transaction_summary(txns):
    df = pd.DataFrame(txns)
    if df.empty:
        return None

    df["amount"] = pd.to_numeric(df["amount"])
    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expenses = df[df["type"] == "expense"]["amount"].sum()

    expense_by_cat = df[df["type"] == "expense"].groupby("category")["amount"].sum()
    income_by_cat = df[df["type"] == "income"].groupby("category")["amount"].sum()

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")
    monthly_expenses = df[df["type"] == "expense"].groupby("month")["amount"].sum()
    monthly_income = df[df["type"] == "income"].groupby("month")["amount"].sum()

    summary = f"""Personal Finance Summary:
- Total Income: ${total_income:,.2f}
- Total Expenses: ${total_expenses:,.2f}
- Net Savings: ${total_income - total_expenses:,.2f}
- Number of Transactions: {len(df)}

Top Expense Categories:
{chr(10).join(f"  - {cat}: ${amt:,.2f}" for cat, amt in expense_by_cat.sort_values(ascending=False).head(5).items())}

Top Income Categories:
{chr(10).join(f"  - {cat}: ${amt:,.2f}" for cat, amt in income_by_cat.sort_values(ascending=False).head(5).items())}

Monthly Expense Trend:
{chr(10).join(f"  - {month}: ${amt:,.2f}" for month, amt in monthly_expenses.items())}

Monthly Income Trend:
{chr(10).join(f"  - {month}: ${amt:,.2f}" for month, amt in monthly_income.items())}

Average Monthly Expense: ${monthly_expenses.mean():,.2f}
Average Monthly Income: ${monthly_income.mean():,.2f}
"""
    return summary


def get_ai_insights(txns, lang="en"):
    summary = generate_transaction_summary(txns)
    if summary is None:
        return None, "No transaction data available to generate insights."

    prompt = f"""You are a financial advisor. Based on the following transaction data, provide concise and actionable financial insights. Cover:

1. Spending trends and patterns
2. Savings observations
3. Budget warnings (if any)
4. Specific actionable recommendations

Keep the response brief, friendly, and under 200 words. Do not use markdown formatting.

{summary}"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=TIMEOUT,
        )
        result = response.json()
        if "error" in result:
            return None, f"Ollama error: {result['error']}"
        response.raise_for_status()
        text = result.get("response", "").strip()
        if not text:
            return None, "Ollama returned an empty response."
    except requests.exceptions.ConnectionError:
        return (
            None,
            "Could not connect to Ollama. Make sure Ollama is running locally (http://localhost:11434).",
        )
    except requests.exceptions.Timeout:
        return None, "Ollama request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return None, f"Ollama request failed: {e}"
    except (json.JSONDecodeError, KeyError) as e:
        return None, f"Failed to parse Ollama response: {e}"

    if lang != "en":
        translated, _ = translate(text, lang)
        if translated:
            return translated, None

    return text, None
