from typing import Dict

def validate_request(request: Dict) -> bool:
    request_data = request.json

    expected_fields = {"messages", "temperature"}
    extra_fields = set(request_data.keys()) - expected_fields
    if extra_fields:
        raise ValueError(f"Request contains unexpected fields: {', '.join(extra_fields)}")

    if "messages" not in request_data:
        raise ValueError("Request must contain 'messages' field")

    if not isinstance(request_data["messages"], list):
        raise ValueError("'messages' field must be a list")

    for message in request_data["messages"]:
        if "role" not in message:
            raise ValueError("Each message must contain 'role' field")
        if "content" not in message:
            raise ValueError("Each message must contain 'content' field")
        if not isinstance(message["role"], str):
            raise ValueError("'role' field must be a string")
        if not isinstance(message["content"], str):
            raise ValueError("'content' field must be a string")
    
    if "temperature" in request_data:
        if not isinstance(request_data["temperature"], (int, float)):
            raise ValueError("'temperature' field must be a number")
        if request_data["temperature"] <= 0 or request_data["temperature"] > 1:
            raise ValueError("'temperature' field must be between 0 and 1")
    
    return request_data