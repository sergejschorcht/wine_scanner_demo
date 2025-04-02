from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

# init flask app
app = Flask(__name__)


@app.route('/api/retrieve', methods=['POST'])
def retrieve_wine():
    wine = {}

    # TODO: wrap with try/except and handle sucess=False (400er response)
    # TODO: implement business logic

    return jsonify({"success": True, "wine": wine}), 500