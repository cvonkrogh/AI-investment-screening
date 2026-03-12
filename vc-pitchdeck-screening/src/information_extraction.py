import json
import os
from typing import Any, Dict

from openai import OpenAI


EXPECTED_KEYS = [
    "value_proposition",
    "customer_segments",
    "product_technology",
    "revenue_model",
    "industry_market",
    "traction_signals",
]


def _empty_representation() -> Dict[str, Any]:
    return {key: "" for key in EXPECTED_KEYS}


def extract_startup_representation(text: str) -> Dict[str, Any]:
    """Extract a simplified startup representation from pitch deck text."""
    if not text.strip():
        return _empty_representation()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is missing. Add it to your environment or .env file.")

    prompt = f"""
You are helping a VC analyst structure a startup pitch deck.
Extract a concise Business Model Canvas-like representation from the text below.

Return STRICT JSON with exactly these keys:
- value_proposition
- customer_segments
- product_technology
- revenue_model
- industry_market
- traction_signals

Each value should be a short paragraph (1-3 sentences). If unknown, return an empty string.

Pitch deck text:
\"\"\"{text[:15000]}\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You return valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    parsed = json.loads(content)

    # Normalize missing keys for predictable downstream processing.
    result = _empty_representation()
    for key in EXPECTED_KEYS:
        value = parsed.get(key, "")
        result[key] = value if isinstance(value, str) else str(value)

    return result
