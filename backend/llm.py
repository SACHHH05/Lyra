import requests

class LLM:
    def __init__(self, model="deepseek-coder-v2:16b"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def ask(self, prompt, system_prompt=None, temperature=0.7):
        print("Lyra is thinking...")

        # clean prompt formatting
        if system_prompt:
            full_prompt = f"""System: {system_prompt}

User: {prompt}

Assistant:"""
        else:
            full_prompt = prompt

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=60
            )

            response.raise_for_status()
            data = response.json()

            return data.get("response", "").strip()

        except requests.exceptions.RequestException as e:
            return f"LLM error: {str(e)}"