import os
import sys
import types
import pytest

# Stub out missing google.genai dependency for tests
google_module = types.ModuleType("google")

genai_module = types.ModuleType("genai")
# create nested types submodule with placeholder classes
types_module = types.ModuleType("types")
class Tool: ...
class GenerateContentConfig: ...
class GoogleSearch: ...
setattr(types_module, "Tool", Tool)
setattr(types_module, "GenerateContentConfig", GenerateContentConfig)
setattr(types_module, "GoogleSearch", GoogleSearch)
setattr(genai_module, "types", types_module)

google_module.genai = genai_module

sys.modules.setdefault("google", google_module)
sys.modules.setdefault("google.genai", genai_module)
sys.modules.setdefault("google.genai.types", types_module)

# Add the api directory to sys.path so that 'index' can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))
from index import app

@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client

def test_missing_book_name(client):
    response = client.post('/api/retrieve', json={})
    assert response.status_code == 400
    assert "book_name" in response.get_json().get("error", "")

def test_invalid_model(client):
    response = client.post('/api/retrieve', json={"book_name": "X", "model": "bad"})
    assert response.status_code == 400
    assert "Ung\u00fcltiges Modell" in response.get_json().get("error", "")
