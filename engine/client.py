import os
from openai import OpenAI
from google import genai

class ResilientAIEngine:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")

        # Initialize Groq client
        self.groq_client = (
            OpenAI(base_url="https://api.groq.com/openai/v1", api_key=self.groq_key)
            if self.groq_key else None
        )

        # Initialize Google GenAI client
        self.gemini_client = (
            genai.Client(api_key=self.gemini_key)
            if self.gemini_key else None
        )

    def execute_prompt(self, system_prompt: str, user_prompt: str, max_tokens: int = 1024) -> str:
        # Route 1: Try Groq first for ultra-fast response
        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.2
                )
                print("[Provider: Groq (qwen3.8-27b)]")
                return response.choices[0].message.content
            except Exception as e:
                print(f"[Warning] Groq failed: {e}. Failing over to Gemini...")

        # Route 2: Fallback to Google Gemini
        if self.gemini_client:
            try:
                full_content = f"System: {system_prompt}\n\nTask:\n{user_prompt}"
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_content
                )
                print("[Provider: Google Gemini (gemini-2.5-flash)]")
                return response.text
            except Exception as e:
                raise RuntimeError(f"All model providers failed. Gemini error: {e}")

        raise ValueError("No active API keys found in your Codespaces environment.")
