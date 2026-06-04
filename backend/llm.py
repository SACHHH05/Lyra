import requests
import json

class LLM:
    def __init__(self, model="deepseek-coder-v2:16b"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def ask(self, prompt, system_prompt=None):
        """
        Sends prompt to local LLM (Ollama)
        """

        print("Lyra is thinking...")

        full_prompt = prompt

        
        if system_prompt:
            full_prompt = f"""
System: {system_prompt}
we 
User: {prompt}

Assistant:
"""

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=60
            )

            response.raise_for_status()

            return response.json().get("response", "").strip()

        except requests.exceptions.RequestException as e:
            return f"LLM error: {str(e)}"

def ask_llm(prompt):
    llm = LLM()
    return llm.ask(prompt)