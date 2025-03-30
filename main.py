from flask import Flask, Response, request, jsonify
from validations.validate_chat import validate_request
from agent.graph import run_graph

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat_response():
    try:
        request_data = validate_request(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"response": run_graph(**request_data)['messages'][-1].content})

@app.route("/", methods=["GET"])
def healthy_check():
    return Response(status=200)