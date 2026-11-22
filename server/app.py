from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Mac Style Calculator API",
        "status": "running"
    })


@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON data required"}), 400

        a = float(data["a"])
        b = float(data["b"])
        operation = data["operation"]

        if operation == "add":
            result = a + b

        elif operation == "subtract":
            result = a - b

        elif operation == "multiply":
            result = a * b

        elif operation == "divide":
            if b == 0:
                return jsonify({"error": "Cannot divide by zero"}), 400
            result = a / b

        else:
            return jsonify({"error": "Invalid operation"}), 400

        return jsonify({
            "a": a,
            "b": b,
            "operation": operation,
            "result": result
        })

    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
