# backend/tests/test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    # Configura el cliente de prueba
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_ask_endpoint(client):
    # Simula una solicitud POST al endpoint /api/ask
    response = client.post('/api/ask', json={'question': 'What is the capital of France?'})
    
    # Verifica que la respuesta es 200 OK
    assert response.status_code == 200
    
    # Verifica que la respuesta es un JSON válido y contiene la respuesta
    data = response.get_json()
    assert 'answer' in data
    assert data['answer'] == 'The capital of France is Paris.'
