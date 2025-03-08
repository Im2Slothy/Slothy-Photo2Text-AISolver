import os
import json
import requests
import time

# Try to load API keys from config/api_keys.json, fall back to None if not found
try:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root_dir, 'config', 'api_keys.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
        OPENAI_API_KEY = config.get("openai_api_key")
        GROK_API_KEY = config.get("grok_api_key")
except FileNotFoundError:
    OPENAI_API_KEY = None
    GROK_API_KEY = None

# Temporarily comment out query_gpt4 since you don't have OpenAI credits
'''
def query_gpt4(question):
    try:
        if not OPENAI_API_KEY:
            return {"model": "GPT-4", "answer": "No API key provided (simulated)", "time": 0.01}
        
        start_time = time.time()
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": question}],
                "max_tokens": 100
            }
        )
        elapsed_time = time.time() - start_time
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"].strip()
            return {"model": "GPT-4", "answer": answer, "time": elapsed_time}
        else:
            return {"model": "GPT-4", "answer": f"Error: {response.status_code}", "time": elapsed_time}
    except Exception as e:
        return {"model": "GPT-4", "answer": f"Failed - {str(e)}", "time": time.time() - start_time}
'''

def query_grok(question):
    try:
        if not GROK_API_KEY:
            return {"model": "Grok", "answer": "No API key provided (simulated)", "time": 0.01}
        
        start_time = time.time()
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-2-latest",
                "messages": [
                    {"role": "system", "content": "Try to answer the question as simple as possible in cases where yes/no may work please do that otherwise keep word count as little as possible but ensure the question is answered. "},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 25,  
                "stream": False,
                "temperature": 0
            }
        )
        elapsed_time = time.time() - start_time
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"].strip()
            return {"model": "Grok", "answer": answer, "time": elapsed_time}
        else:
            return {"model": "Grok", "answer": f"Error: {response.status_code}", "time": elapsed_time}
    except Exception as e:
        return {"model": "Grok", "answer": f"Failed - {str(e)}", "time": time.time() - start_time}