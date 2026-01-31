"""
Atoms: LLM Connector.
原子能力：LLM 连接器。
"""
import json
import os
import urllib.request
from typing import Optional, Dict, Any

def call_llm(prompt: str, system_prompt: str = "You are a helpful assistant.") -> Optional[str]:
    """
    Generic LLM call via environment variables.
    Supports: OPENAI_API_KEY, GEMINI_API_KEY (via Google AI API), DEEPSEEK_API_KEY.
    """
    # 1. Try DeepSeek (Commonly used in China)
    if os.getenv("DEEPSEEK_API_KEY"):
        return _call_openai_compatible(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            prompt=prompt,
            system_prompt=system_prompt
        )
    
    # 2. Try OpenAI
    if os.getenv("OPENAI_API_KEY"):
        return _call_openai_compatible(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1",
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            prompt=prompt,
            system_prompt=system_prompt
        )

    # 3. Try Gemini (Google AI Studio)
    if os.getenv("GEMINI_API_KEY"):
        return _call_gemini(
            api_key=os.getenv("GEMINI_API_KEY"),
            prompt=prompt,
            system_prompt=system_prompt
        )

    print("❌ Error: No LLM API key found (DEEPSEEK_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY).")
    return None

def _call_openai_compatible(api_key: str, base_url: str, model: str, prompt: str, system_prompt: str) -> Optional[str]:
    url = f"{base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ LLM Call Failed: {e}")
        return None

def _call_gemini(api_key: str, prompt: str, system_prompt: str) -> Optional[str]:
    # Gemini API format is slightly different
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # Combine system prompt and user prompt for Gemini if needed, 
    # though 1.5 supports system_instruction.
    data = {
        "system_instruction": {"parts": {"text": system_prompt}},
        "contents": {"parts": {"text": prompt}}
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"❌ Gemini Call Failed: {e}")
        return None
