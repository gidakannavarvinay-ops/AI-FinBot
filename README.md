# 💰 FinBot - AI Financial Assistant

**FinBot** is an intelligent, localhost personal finance web application built using **Python**, **Streamlit**, and the **Google Gemini API** (`google-generativeai`) using `gemini-2.5-flash`.

It is tailored specifically for the **Indian financial landscape (₹ INR)**, offering contextualized guidance on budgeting, savings, investments, loan EMI calculations, and long-term financial planning.

---

## ✨ Features

1. **💬 Interactive Chat Interface with Multi-turn History**:
   - Preserves session chat context across questions.
   - Clean chat avatars (👤 User, 💰 FinBot) and Markdown formatting for tables, lists, and bold highlights.
   - One-click **Clear Chat History** button to start fresh.

2. **🧠 Guardrailed Finance Persona & Indian Context**:
   - **India Context**: Values, currency, and instruments formatted in Indian Rupees (**₹**), **Lakhs**, and **Crores**.
   - **Covers**: Budgeting (50/30/20), Emergency Funds, SIPs, Mutual Funds, Stocks, PPF, EPF, NPS, FDs/RDs, Sovereign Gold Bonds, and Insurance (Term vs ULIP).
   - **Guardrails**: Politely refuses non-financial questions (e.g., cooking, programming, pop culture) and steers users back to personal money management.
   - **Mandatory Disclaimer**: Every response concludes with a clear educational note distinguishing the bot from certified SEBI-registered financial advisory.

3. **👤 Dynamic Sidebar Financial Profile**:
   - Customizable fields for:
     - **Monthly In-Hand Income (₹)**
     - **Monthly Expenses (₹)**
     - **Primary Savings Goal / Target**
     - **Investment Risk Appetite** (Conservative, Moderate, Aggressive)
     - **Investment Horizon** (Short, Medium, Long term)
   - **Live Financial Snapshot**: Automatically calculates your **Monthly Net Surplus** and **Savings Rate %** with health indicators (Healthy, Moderate, Needs Boost).
   - Shows ideal **50/30/20 budget allocations** for your entered income.
   - Injected live into the system prompt for tailored, personalized advice.

4. **🧮 Dual EMI Calculator Tool (Function Calling + UI Widget)**:
   - **AI Function Calling Tool**: The chatbot connects directly to a Python `calculate_emi` function via Gemini Tool Calling (`tools=[calculate_emi]`) to compute accurate loan figures (Principal, Monthly EMI, Total Interest, Total Payment).
   - **Standalone Interactive Widget**: An expandable loan calculator tool right in the UI to test loan amounts, interest rates, and tenures with instant metric cards and a button to submit the scenario to FinBot for affordability analysis.

5. **⚡ Quick-Question Buttons**:
   - Instant-action prompt chips for frequent financial questions:
     - 💡 *How to build an emergency fund?*
     - 🎯 *Explain 50/30/20 Budgeting Rule*
     - 📈 *Explain SIP & Compounding*
     - ⚖️ *PPF vs Equity Mutual Funds*
     - 💰 *Calculate EMI for ₹5 Lakh at 10%*
     - 🛡️ *Term Insurance vs ULIP*

6. **🎨 Clean, Modern Dark-Themed UI**:
   - Styled with modern cards, responsive metrics, badge indicators, and high contrast typography.

---

## 📁 Project Structure

```
AI chatbot/
│
├── app.py              # Main Streamlit web application
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment configuration template
├── .env                # Local environment file for GEMINI_API_KEY
└── README.md           # Documentation and run instructions
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- A **Google Gemini API Key** (Free tier available at [Google AI Studio](https://aistudio.google.com/app/apikey)).

### 2. Clone or Navigate to the Project Directory
```bash
cd "c:\Users\VINAY G\OneDrive\Documents\GitHub\CIA-2 AI FOR FINANCE\AI chatbot"
```

### 3. (Optional) Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Your Gemini API Key
The API key is securely loaded on the server from the `.env` file and is never exposed in the UI or committed to version control.

Open `.env` (or copy from `.env.example`) and paste your Gemini API key:
```env
GEMINI_API_KEY=AIzaSyYourActualGeminiAPIKeyHere
```
*(The `.env` file is excluded from git tracking in `.gitignore` to keep credentials secure).*

### 6. Run the Streamlit Application
```bash
streamlit run app.py
```

The app will launch in your default web browser at:
```
http://localhost:8501
```

---

## 💡 Example Prompts to Try

- *"Based on my monthly surplus of ₹30,000, how should I allocate between an emergency fund and an equity SIP?"*
- *"I want to buy a car for ₹8,00,000 with a down payment of ₹2,00,000 and loan at 9.5% for 5 years. What is my EMI and can I afford it?"*
- *"Should I choose the Old Tax Regime or the New Tax Regime if I earn ₹12 Lakh per year?"*
- *"What's the best way to make Biryani?"* *(Watch FinBot politely refuse and guide you back to finance!)*

---

## 🛡️ Disclaimer

*FinBot is an AI-powered conversational educational tool created for academic and personal financial literacy purposes. It is not an authorized, licensed, or SEBI-registered financial advisor. Do not make high-stakes investment, borrowing, or financial commitments without consulting a certified financial planner (CFP) or financial professional.*

