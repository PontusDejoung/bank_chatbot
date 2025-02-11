# AI-Powered Banking Chatbot

## Overview
This project is an AI-powered virtual banking assistant that processes user input, identifies intents, and responds accordingly. The chatbot is integrated with an LLM (Large Language Model) and supports various banking-related queries, including account balance inquiries, loan applications, and money transfers.

## Features
- **Intent Recognition**: Determines the user's intent from predefined categories.
- **Entity Recognition**: Extracts important details such as account types and services.
- **API Integration**: Connects with banking services and a DuckDB-based database.
- **Strict JSON Response Formatting**: Ensures all responses are formatted correctly in JSON.
- **Flask API**: Provides an endpoint to interact with the chatbot.

---

## Project Structure
```
.
├── prompts.py             # Prompt engineering for LLM interactions
├── start_interface.py     # Flask app serving UI components
├── llm_integration.py     # Main backend for chatbot responses
├── bank_duckdb.py         # Database handling with DuckDB
├── js/                    # Javascript for the front
├── css/                   # Frontend Style (CSS)
└── templates/             # HTML template
```

---

## How It Works
### 1️⃣ **Intent Detection**
User input is analyzed to match predefined intents such as:
- `get_balance` – Check account balance
- `make_deposit` – Deposit money
- `start_loan_application` – Begin a loan application
- `transfer_between_accounts` – Transfer money
- `get_company_info` – Provide bank details
- `greet_customer` – Handle greetings
- `support_errand` – Offer assistance

### 2️⃣ **LLM Processing**
Prompts are structured in `prompts.py` to ensure structured responses. The LLM processes user input and generates intent-specific JSON output.

### 3️⃣ **Flask API**
The `llm_integration.py` file hosts the Flask API, which:
- Receives user input
- Calls `ask_llm()` for response generation
- Fetches account details from the database when necessary
- Returns JSON responses

### 4️⃣ **Database Handling**
`bank_duckdb.py` manages customer data using **DuckDB**. It stores and retrieves account balances, transaction histories, and customer details.

---

## 🛠 Installation & Setup
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/PontusDejoung/bank_chatbot
cd chatbot-banking
```

### 2️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 3️⃣ **Run the Application**
```sh
python llm_integration.py
```
The server will run on `http://localhost:8000`.

### 4️⃣ **Run the Database**
If running for the first time, initialize the database:
```sh
python bank_duckdb.py
```

---

## 🛠 Technologies Used
- **Python** (Flask, DuckDB, Requests, JSON)
- **Ollama** for LLM processing
- **DuckDB** for fast and efficient data queries
- **Flask-CORS** to enable cross-origin requests

---

## 📝 Notes
- The chatbot is designed to strictly follow JSON response formats.
- Intent recognition can be improved by adding more training examples and refine existing ones.
- Database seeding can be run from `bank_duckdb.py`.
