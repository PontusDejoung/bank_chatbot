import ollama
import re
import json
from prompts import get_intent_from_llm, get_info_about_company, get_loan_application_prompt, get_money_tranfer_prompt
from bank_duckdb import get_total_balance

def ask_llm(prompt):
    """Ask the Llama model for a response."""
    try:
        response = ollama.chat(model='deepseek-r1:1.5b', messages=[{'role': 'user', 'content': prompt}])
        response_without_think_process = re.sub(r"<think>.*?</think>", "", response['message']['content'], flags=re.DOTALL)
        json_match = re.search(r"\{.*?\}", response_without_think_process, flags=re.DOTALL)

        if json_match:
            return json.loads(json_match.group(0))
        return {"intent": "unknown", "reason": "Unable to parse valid JSON"}
    
    except json.JSONDecodeError:
       pass
    except Exception as e:
        print(f"Error in ask_llama: {e}")
        return None
    

user_input = "Hola amigo, I want to see my balance"
prompt = get_intent_from_llm(user_input)
answer = ask_llm(prompt)
print(answer)

if 'reason' in answer and answer['reason'] == "Unable to parse valid JSON":
    while answer['reason'] == "Unable to parse valid JSON":
        answer = ask_llm(prompt)
        print(answer)
if answer['intent'] == "get_company_info":
    prompt = get_info_about_company(user_input)
if answer['intent'] == "start_loan_application":
    prompt = get_loan_application_prompt()
if answer['intent'] == "transfer_between_accounts":
    prompt = get_money_tranfer_prompt()
if answer['intent'] == "get_balance":
    total_balance = get_total_balance("1")
    print(f"Your total balance across all your accounts is: {total_balance} $\nCan I assist you with anything else?")
print(ask_llm(prompt))