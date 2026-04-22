"""
suchat.py — SpendSage AI Agent
Google Gemini 2.5 Flash (primary) + Groq llama3 (fallback)
API keys via st.secrets
"""

import streamlit as st
import json
import pandas as pd

import google.generativeai as genai
from groq import Groq


SYSTEM_PROMPT = """
You are SpendSage AI — an intelligent, warm, and insightful personal finance assistant 
embedded inside an expense tracking app used by Indian users.

Your capabilities:
1. Deeply analyze income & expense data when provided in context.
2. Answer spending pattern questions with specific numbers and percentages.
3. Identify top spending categories and suggest where to cut costs.
4. Compare month-over-month or category-wise trends.
5. Give personalized savings tips based on actual data.
6. Help with budget planning and financial goals.
7. Respond fluently in Hindi, English, or Hinglish — match the user's language.

Response style:
- Be warm, friendly, never judgmental about spending habits.
- Use the rupee symbol (Rs. or INR), format numbers with Indian comma style.
- Use emojis sparingly for key points.
- Structure answers clearly — use bullet points for lists.
- Keep responses focused and actionable.
- If data exists, ALWAYS reference actual numbers from it.
- If no transactions exist, gently guide user to add some.
"""


def build_data_context(transactions: list) -> str:
    if not transactions:
        return "No transactions recorded yet. Ask the user to add some transactions first."

    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%b %Y")

    income_df  = df[df["type"] == "Income"]
    expense_df = df[df["type"] == "Expense"]

    total_income  = income_df["amount"].sum()  if not income_df.empty else 0
    total_expense = expense_df["amount"].sum() if not expense_df.empty else 0
    balance       = total_income - total_expense
    savings_rate  = ((total_income - total_expense) / total_income * 100) if total_income > 0 else 0

    exp_by_cat   = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False).to_dict() if not expense_df.empty else {}
    inc_by_cat   = income_df.groupby("category")["amount"].sum().sort_values(ascending=False).to_dict()  if not income_df.empty else {}
    exp_by_month = expense_df.groupby("month")["amount"].sum().to_dict() if not expense_df.empty else {}
    inc_by_month = income_df.groupby("month")["amount"].sum().to_dict()  if not income_df.empty else {}

    recent = df.sort_values("date", ascending=False).head(8)
    recent_lines = "\n".join(
        f"  - {row['date'].strftime('%d %b %Y')} | {row['type']} | {row['category']} | Rs.{row['amount']:,.0f}"
        + (f" | {row['note']}" if row.get("note") else "")
        for _, row in recent.iterrows()
    )
    top_expense = list(exp_by_cat.items())[0] if exp_by_cat else ("None", 0)

    return f"""
=== USER FINANCIAL DATA SUMMARY ===
Total Income   : Rs.{total_income:,.2f}
Total Expenses : Rs.{total_expense:,.2f}
Net Balance    : Rs.{balance:,.2f}
Savings Rate   : {savings_rate:.1f}%
Transactions   : {len(df)} total
Top Expense    : {top_expense[0]} (Rs.{top_expense[1]:,.2f})

EXPENSES BY CATEGORY:
{json.dumps({k: f'Rs.{v:,.2f}' for k,v in exp_by_cat.items()}, indent=2, ensure_ascii=False)}

INCOME BY CATEGORY:
{json.dumps({k: f'Rs.{v:,.2f}' for k,v in inc_by_cat.items()}, indent=2, ensure_ascii=False)}

MONTHLY EXPENSES:
{json.dumps({k: f'Rs.{v:,.2f}' for k,v in exp_by_month.items()}, indent=2, ensure_ascii=False)}

MONTHLY INCOME:
{json.dumps({k: f'Rs.{v:,.2f}' for k,v in inc_by_month.items()}, indent=2, ensure_ascii=False)}

RECENT TRANSACTIONS:
{recent_lines}

Date Range: {df['date'].min().strftime('%d %b %Y')} to {df['date'].max().strftime('%d %b %Y')}
===================================
"""


def _get_gemini():
    key = st.secrets.get("GOOGLE_API_KEY", "")
    if not key:
        return None
    try:
        genai.configure(api_key=key)
        return genai.GenerativeModel(
            model_name="gemini-2.5-flash-preview-05-20",
            system_instruction=SYSTEM_PROMPT,
        )
    except Exception:
        return None


def _get_groq():
    key = st.secrets.get("GROQ_API_KEY", "")
    if not key:
        return None
    try:
        return Groq(api_key=key)
    except Exception:
        return None


def chat_with_agent(user_message: str, chat_history: list, transactions: list) -> tuple:
    """
    Returns (response_text, model_used)
    chat_history: [{"role": "user"|"assistant", "content": "..."}]
    """
    context      = build_data_context(transactions)
    full_message = f"{context}\n\nUser: {user_message}"

    # ── Gemini 2.5 Flash ─────────────────────────────────────────────
    try:
        model = _get_gemini()
        if model:
            history = []
            for m in chat_history[-12:]:
                role = "user" if m["role"] == "user" else "model"
                history.append({"role": role, "parts": [m["content"]]})
            session  = model.start_chat(history=history)
            response = session.send_message(full_message)
            return response.text, "gemini-2.5-flash"
    except Exception:
        pass

    # ── Groq Llama 3.3 70B ───────────────────────────────────────────
    try:
        client = _get_groq()
        if client:
            msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
            for m in chat_history[-12:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            msgs.append({"role": "user", "content": full_message})
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=msgs,
                max_tokens=1024,
                temperature=0.7,
            )
            return resp.choices[0].message.content, "groq-llama-3.3-70b"
    except Exception:
        pass

    return (
        "AI service unavailable. Please check GOOGLE_API_KEY and GROQ_API_KEY in Streamlit secrets.",
        "error"
    )


def get_quick_insight(transactions: list) -> str:
    """One-line AI insight for dashboard."""
    if not transactions:
        return "Add your first transaction to get AI-powered insights!"
    text, _ = chat_with_agent(
        "Give ONE short specific actionable financial insight in 1-2 sentences with actual numbers. No preamble.",
        [], transactions
    )
    return text
