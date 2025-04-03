from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from services.openaiService import OpenAIService
from services.geminiService import GeminiService

# .env-Variablen laden
load_dotenv()

# Init Flask App
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enhanced CORS settings

# Factory-Methode zur Auswahl des Modells
def get_model(model_name: str):
    if model_name == "openai":
        return OpenAIService()
    elif model_name == "gemini":
        return GeminiService()
    else:
        raise ValueError("Ungültiges Modell")

@app.route("/api/retrieve", methods=["POST"])
def retrieve_price():
    data = request.get_json()
    book_name = data.get("book_name")
    format_type = data.get("format_type", "hardcover")  # Default to hardcover if not specified
    model_name = data.get("model", "openai")  # Default to openai if not specified

    if not book_name:
        return jsonify({"error": "Bitte 'book_name' als Parameter angeben"}), 400

    try:
        ai_service = get_model(model_name)
        # For the real application, use the model to retrieve the price
        # If using the mock, we will provide the mocked data as fallback.
        if model_name in ["openai", "gemini"]:  # Replace this with actual API calls when implemented
            price, sources = ai_service.get_price(book_name, format_type)
            response = {
                "success": price is not None,
                "price": price if price is not None else "15.00",  # Default price if None
                "sources": sources,
                "model": model_name
            }
        else:
            # For demo purposes, return a mocked price
            mock_prices = {
                "hardcover": "24.99",
                "paperback": "14.99",
                "ebook": "9.99",
                "audiobook": "19.99"
            }
            price = mock_prices.get(format_type, "15.00")
            response = {
                "price": price,
                "book_name": book_name,
                "model_used": model_name
            }

        return jsonify(response)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
