from flask import Flask, request, jsonify
from dotenv import load_dotenv
from services.openaiService import OpenAIService
from services.geminiService import GeminiService


# .env-Variablen laden
load_dotenv()

# Init Flask App
app = Flask(__name__)

# Factory-Methode zur Auswahl des Modells
def get_model(model_name: str):
    if model_name == "openai":
        return OpenAIService()
    elif model_name == "gemini":
        return GeminiService()
    else:
        raise ValueError("Ungültiges Modell")

@app.route('/api/retrieve', methods=['POST'])
def retrieve():
    data = request.get_json()
    book_name = data.get("book_name")
    format_type = data.get("format_type", "hardcover")  # Default to hardcover if not specified
    model_name = data.get("model", "openai")  # Default to openai if not specified

    if not book_name:
        return jsonify({"error": "Bitte 'book_name' als Parameter angeben"}), 400

    try:
        ai_service = get_model(model_name)
        price, sources = ai_service.get_price(book_name, format_type)
        
        response = {
            "success": price is not None,
            "price": price if price is not None else None,
            "sources": sources,
            "model": model_name
        }
        
        return jsonify(response)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
