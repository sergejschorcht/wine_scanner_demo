from unittest.mock import patch
from api.index import app
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_retrieve_price_success(client):
    with patch('api.services.openaiService.OpenAIService.get_price', return_value=(12.5, ['http://example.com'])):
        resp = client.post('/api/retrieve', json={'book_name': 'test book', 'model': 'openai'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['price'] == 12.5
        assert data['sources'] == ['http://example.com']
        assert data['success'] is True


def test_retrieve_price_missing_payload(client):
    resp = client.post('/api/retrieve')
    assert resp.status_code == 400
    assert 'error' in resp.get_json()


def test_retrieve_price_missing_book_name(client):
    resp = client.post('/api/retrieve', json={})
    assert resp.status_code == 400
    assert 'error' in resp.get_json()


def test_retrieve_price_invalid_model(client):
    resp = client.post('/api/retrieve', json={'book_name': 'X', 'model': 'bad'})
    assert resp.status_code == 400
    assert 'error' in resp.get_json()
