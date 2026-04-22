# 💎 SpendSage — Smart Expense Tracker

Ultra-advanced AI-powered expense tracker built with Streamlit + Google Gemini 2.5 Flash + Groq.

## 📁 Project Structure

```
expenses_tracker/
├── app.py                    ← Main Streamlit UI (all 4 pages)
├── suchat.py                 ← AI Agent (Gemini 2.5 Flash + Groq fallback)
├── requirements.txt          ← Python dependencies
└── .streamlit/
    └── secrets.toml          ← API keys (local only, never commit!)
```

## 🚀 Features

| Feature | Details |
|---|---|
| 🏠 Dashboard | Welcome banner, metric cards, charts, recent txns, AI insight |
| 💳 Transactions | Add/filter/delete transactions, AI assistant tab |
| 📊 Analytics | Treemap, trend lines, savings chart, monthly breakdown |
| 🤖 AI Assistant | Full-page chatbot with suggested prompts |
| 💬 Inline Chatbot | On Dashboard + Transactions page simultaneously |
| 🌙 Dark Theme | Ultra premium dark UI with Syne + Inter fonts |

## ⚙️ Local Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Streamlit Cloud Deployment

1. Push code to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file** as `app.py`
5. Go to **App Settings → Secrets** and add:

```toml
GOOGLE_API_KEY = "your-gemini-api-key"
GROQ_API_KEY   = "your-groq-api-key"
```

### Get API Keys
- **Google Gemini**: https://aistudio.google.com/app/apikey (Free tier available)
- **Groq**: https://console.groq.com/keys (Free tier, very fast)

## 🤖 AI Models Used

| Model | Role | Provider |
|---|---|---|
| `gemini-2.5-flash-preview-05-20` | Primary AI | Google AI Studio |
| `llama-3.3-70b-versatile` | Fallback AI | Groq |

The app automatically falls back to Groq if Gemini is unavailable.

## 🔒 Security Notes

- **Never commit** `.streamlit/secrets.toml` to GitHub
- Add `.streamlit/secrets.toml` to your `.gitignore`
- All API keys are read via `st.secrets` (safe for Streamlit Cloud)
