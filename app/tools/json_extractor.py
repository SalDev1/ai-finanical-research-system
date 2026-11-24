import json
import re

def extract_json(response: str) -> str:
    response = response.strip()
    if response.startswith("```"):
        match = re.search(
            r"```(?:json)?\s*(.*?)\s*```",
            response,
            re.DOTALL | re.IGNORECASE,
        )
        if not match:
            raise ValueError(
                "LLM returned an incomplete JSON code block."
            )
        response = match.group(1).strip()
    try:
        json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid JSON: {exc}"
        ) from exc

    return response