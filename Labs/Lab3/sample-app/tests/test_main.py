"""
Unit tests for the main Flask application.

This module contains integration tests for all API endpoints.
"""

import pytest
import json
from src.main import app


@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns 200 and correct data."""
        response = client.get('/health')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'python-sample-app'
        assert 'version' in data
        assert 'environment' in data


class TestHomeEndpoint:
    """Tests for the home endpoint."""

    def test_home(self, client):
        """Test home endpoint returns API information."""
        response = client.get('/')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'message' in data
        assert 'endpoints' in data
        assert '/health' in str(data['endpoints'])


class TestAddEndpoint:
    """Tests for the addition endpoint."""

    def test_add_positive_numbers(self, client):
        """Test adding two positive numbers."""
        response = client.post('/add',
                               data=json.dumps({'a': 5, 'b': 3}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['operation'] == 'addition'
        assert data['result'] == 8.0

    def test_add_negative_numbers(self, client):
        """Test adding negative numbers."""
        response = client.post('/add',
                               data=json.dumps({'a': -5, 'b': -3}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['result'] == -8.0

    def test_add_with_zero(self, client):
        """Test adding with zero."""
        response = client.post('/add',
                               data=json.dumps({'a': 10, 'b': 0}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['result'] == 10.0

    def test_add_invalid_input(self, client):
        """Test addition with invalid input."""
        response = client.post('/add',
                               data=json.dumps({'a': 'abc', 'b': 3}),
                               content_type='application/json')
        assert response.status_code == 400

        data = json.loads(response.data)
        assert 'error' in data

    def test_add_missing_data(self, client):
        """Test addition with missing data."""
        response = client.post('/add',
                               data=json.dumps({'a': 5}),
                               content_type='application/json')
        assert response.status_code == 400

    def test_add_no_json(self, client):
        """Test addition without JSON data."""
        response = client.post('/add')
        assert response.status_code == 400

        data = json.loads(response.data)
        assert 'error' in data


class TestSubtractEndpoint:
    """Tests for the subtraction endpoint."""

    def test_subtract_positive_numbers(self, client):
        """Test subtracting positive numbers."""
        response = client.post('/subtract',
                               data=json.dumps({'a': 10, 'b': 3}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['operation'] == 'subtraction'
        assert data['result'] == 7.0

    def test_subtract_resulting_negative(self, client):
        """Test subtraction resulting in negative number."""
        response = client.post('/subtract',
                               data=json.dumps({'a': 3, 'b': 10}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['result'] == -7.0

    def test_subtract_invalid_input(self, client):
        """Test subtraction with invalid input."""
        response = client.post('/subtract',
                               data=json.dumps({'a': 10, 'b': 'xyz'}),
                               content_type='application/json')
        assert response.status_code == 400


class TestMultiplyEndpoint:
    """Tests for the multiplication endpoint."""

    def test_multiply_positive_numbers(self, client):
        """Test multiplying positive numbers."""
        response = client.post('/multiply',
                               data=json.dumps({'a': 4, 'b': 5}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['operation'] == 'multiplication'
        assert data['result'] == 20.0

    def test_multiply_by_zero(self, client):
        """Test multiplying by zero."""
        response = client.post('/multiply',
                               data=json.dumps({'a': 10, 'b': 0}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['result'] == 0.0

    def test_multiply_negative_numbers(self, client):
        """Test multiplying negative numbers."""
        response = client.post('/multiply',
                               data=json.dumps({'a': -4, 'b': -5}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['result'] == 20.0


class TestDivideEndpoint:
    """Tests for the division endpoint."""

    def test_divide_positive_numbers(self, client):
        """Test dividing positive numbers."""
        response = client.post('/divide',
                               data=json.dumps({'a': 10, 'b': 2}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['operation'] == 'division'
        assert data['result'] == 5.0

    def test_divide_by_zero(self, client):
        """Test division by zero."""
        response = client.post('/divide',
                               data=json.dumps({'a': 10, 'b': 0}),
                               content_type='application/json')
        assert response.status_code == 400

        data = json.loads(response.data)
        assert 'error' in data
        assert 'zero' in data['error'].lower()

    def test_divide_zero(self, client):
        """Test dividing zero."""
        response = client.post('/divide',
                               data=json.dumps({'a': 0, 'b': 5}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['result'] == 0.0

    def test_divide_negative_numbers(self, client):
        """Test dividing negative numbers."""
        response = client.post('/divide',
                               data=json.dumps({'a': -10, 'b': -2}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['result'] == 5.0


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_invalid_endpoint(self, client):
        """Test accessing invalid endpoint."""
        response = client.get('/invalid')
        assert response.status_code == 404

    def test_wrong_http_method(self, client):
        """Test using wrong HTTP method."""
        response = client.get('/add')
        assert response.status_code == 405

    def test_large_numbers(self, client):
        """Test with very large numbers."""
        response = client.post('/add',
                               data=json.dumps({'a': 1e10, 'b': 1e10}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['result'] == 2e10

    def test_floating_point_precision(self, client):
        """Test floating point arithmetic."""
        response = client.post('/add',
                               data=json.dumps({'a': 0.1, 'b': 0.2}),
                               content_type='application/json')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert abs(data['result'] - 0.3) < 1e-10
