from flask import Flask, request, jsonify
import ollama
import re
import json
from prompts import get_intent_from_llm_prompt, get_info_about_company, get_loan_application_prompt, get_money_transfer_prompt, get_deposit_money_prompt, get_greeting_prompt
from bank_duckdb import get_total_balance
from flask_cors import CORS

app = Flask(__name__)

def ask_llm(prompt):
    """Ask the Llama model for a response."""
    try:
        response = ollama.chat(model='llama3.1-8b-metal:latest', messages=[{'role': 'user', 'content': prompt}])
        response_without_think_process = re.sub(r"<think>.*?</think>", "", response['message']['content'], flags=re.DOTALL)
        json_match = re.search(r"\{.*?\}", response_without_think_process, flags=re.DOTALL)

        if json_match:
            return json.loads(json_match.group(0))
        return {"intent": "unknown", "reason": "Unable to parse valid JSON"}

    except json.JSONDecodeError:
        return {"intent": "unknown", "reason": "JSONDecodeError"}
    except Exception as e:
        print(f"Error in ask_llm: {e}")
        return {"intent": "unknown", "reason": str(e)}
    
def check_LLM_answer(answer, prompt):
    if answer and 'reason' in answer and answer['reason'] in ["Unable to parse valid JSON", "JSONDecodeError"]:
        while answer['intent'] == "unknown":
            answer = ask_llm(prompt)
            print(answer)
    return answer    

def fetch_and_validate_llm_response(prompt,column):
    answer = ask_llm(prompt)
    answer = check_LLM_answer(answer, prompt)
    response_content = json.dumps(answer[column])
    return response_content

@app.route('/get_response/', methods=['POST'])
def get_response():
    data = request.get_json()
    user_text = data.get('text', '')

    prompt = get_intent_from_llm_prompt(user_text)
    answer = ask_llm(prompt)
    answer = check_LLM_answer(answer, prompt)
    print(answer)
    check_LLM_answer(answer, prompt)

    intent = answer.get('intent', 'unknown')
    response_content = ""

    if intent == "get_company_info":
        prompt = get_info_about_company(user_text)
        response_content = fetch_and_validate_llm_response(prompt,"answer")

    elif intent == "start_loan_application":
        prompt = get_loan_application_prompt()
        response_content = fetch_and_validate_llm_response(prompt,"response")

    elif intent == "transfer_between_accounts":
        prompt = get_money_transfer_prompt()
        response_content = fetch_and_validate_llm_response(prompt,"response")
        print(response_content)

    elif intent == "get_balance":
        # This is just a example, therefore its hardcoded with number 1 
        total_balance = get_total_balance("1")
        response_content = f"Your total balance across all your accounts is: {total_balance} $\nCan I assist you with anything else?"

    elif intent == "make_deposit":
        prompt = get_deposit_money_prompt()
        response_content = fetch_and_validate_llm_response(prompt,"response")

    elif intent == "greet_customer":
        prompt = get_greeting_prompt(user_text)
        response_content = fetch_and_validate_llm_response(prompt,"response")

    elif intent == "support_errand":
        response_content = "I'll connect you with our support"

    else:
        response_content = "I'm not sure how to help with that. I can only help with bank related topics"
    
    if '"' in response_content or "'" in response_content:
        response_content = response_content.replace('"', '')

    return jsonify({"response": response_content})

if __name__ == '__main__':
    CORS(app) 
    app.run(port=8000, debug=True)
