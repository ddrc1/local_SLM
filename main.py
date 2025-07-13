from flask import Flask, Response, request, jsonify
from validations.validate_chat import validate_request
from graph.graph import compiled_graph

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat_response():
    try:
        request_data: list[dict] = validate_request(request) # type: ignore
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    response: str = compiled_graph.invoke(request_data)['answer'] # type: ignore

    return jsonify({"response": response})

@app.route("/", methods=["GET"])
def healthy_check():
    return Response(status=200)