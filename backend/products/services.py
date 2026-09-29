"""OpenRouter tool calling and the product search workflow."""

import json

import requests
from django.conf import settings

from .catalog import search_products

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_products",
        "description": "Search the sample catalog for products matching the user's requirements.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["laptop", "mobile"]},
                "brand": {"type": "string", "description": "Brand name, for example Lenovo or Samsung."},
                "max_price": {"type": "number", "description": "Maximum price in Indian rupees."},
                "min_price": {"type": "number", "description": "Minimum price in Indian rupees."},
                "ram": {"type": "string", "description": "RAM size, for example 8GB."},
                "storage": {"type": "string", "description": "Storage size, for example 512GB."},
                "color": {"type": "string", "description": "Preferred product color."},
            },
            "required": [],
        },
    },
}


def ask_openrouter(messages, tools=None, tool_choice=None):
    """Send a chat request to OpenRouter and return the assistant message."""
    if not settings.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing. Add it to backend/.env.")

    request_body = {
        "model": settings.OPENROUTER_MODEL,
        "messages": messages,
        "temperature": 0.2,
    }
    if tools:
        request_body["tools"] = tools
        request_body["tool_choice"] = tool_choice

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "AI Product Finder",
        },
        json=request_body,
        timeout=45,
    )

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter returned HTTP {response.status_code}.")

    return response.json()["choices"][0]["message"]


def run_product_search(message):
    """Ask the model to search, execute its tool request, then ask for a summary."""
    messages = [
        {
            "role": "system",
            "content": (
                "You help users find products in a small sample catalog. "
                "Always call search_products for the user's request. Extract every explicit requirement, "
                "including category, brand, price limits, RAM, storage, and color. "
                "Do not omit the brand when the user names one. "
                "Use only the returned matches as product facts and give one short final answer."
            ),
        },
        {"role": "user", "content": message},
    ]

    tool_message = ask_openrouter(messages, tools=[SEARCH_TOOL], tool_choice="required")
    tool_calls = tool_message.get("tool_calls", [])
    if not tool_calls:
        raise RuntimeError("The selected model did not return a product search tool call.")

    messages.append(tool_message)
    products = []
    for tool_call in tool_calls:
        if tool_call["function"]["name"] != "search_products":
            continue
        arguments = json.loads(tool_call["function"].get("arguments", "{}"))
        products = search_products(**arguments)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": json.dumps(products),
            }
        )

    if not any(call["function"]["name"] == "search_products" for call in tool_calls):
        raise RuntimeError("The model requested an unknown tool.")

    final_message = ask_openrouter(messages)
    answer = final_message.get("content") or "I searched the catalog and found these matching products."
    return {"message": answer, "products": products}