"""
Main application module for a simple Flask REST API.

This module provides a basic Flask application with health check
and calculator endpoints for demonstration purposes.
"""

import os
from flask import Flask, jsonify, request
from src.calculator import Calculator
from src.utils import validate_number


app = Flask(__name__)
calc = Calculator()


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.

    Returns:
        JSON response with status and version information
    """
    return jsonify({
        'status': 'healthy',
        'service': 'python-sample-app',
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development')
    }), 200


@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with API information.

    Returns:
        JSON response with available endpoints
    """
    return jsonify({
        'message': 'Welcome to Python Sample API',
        'endpoints': {
            'health': '/health',
            'add': '/add',
            'subtract': '/subtract',
            'multiply': '/multiply',
            'divide': '/divide'
        }
    }), 200


@app.route('/add', methods=['POST'])
def add():
    """
    Addition endpoint.

    Expected JSON body:
        {
            "a": number,
            "b": number
        }

    Returns:
        JSON response with the sum
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        a = data.get('a')
        b = data.get('b')

        if not validate_number(a) or not validate_number(b):
            return jsonify({'error': 'Invalid input: both a and b must be numbers'}), 400

        result = calc.add(float(a), float(b))
        return jsonify({
            'operation': 'addition',
            'a': a,
            'b': b,
            'result': result
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/subtract', methods=['POST'])
def subtract():
    """
    Subtraction endpoint.

    Expected JSON body:
        {
            "a": number,
            "b": number
        }

    Returns:
        JSON response with the difference
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        a = data.get('a')
        b = data.get('b')

        if not validate_number(a) or not validate_number(b):
            return jsonify({'error': 'Invalid input: both a and b must be numbers'}), 400

        result = calc.subtract(float(a), float(b))
        return jsonify({
            'operation': 'subtraction',
            'a': a,
            'b': b,
            'result': result
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/multiply', methods=['POST'])
def multiply():
    """
    Multiplication endpoint.

    Expected JSON body:
        {
            "a": number,
            "b": number
        }

    Returns:
        JSON response with the product
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        a = data.get('a')
        b = data.get('b')

        if not validate_number(a) or not validate_number(b):
            return jsonify({'error': 'Invalid input: both a and b must be numbers'}), 400

        result = calc.multiply(float(a), float(b))
        return jsonify({
            'operation': 'multiplication',
            'a': a,
            'b': b,
            'result': result
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/divide', methods=['POST'])
def divide():
    """
    Division endpoint.

    Expected JSON body:
        {
            "a": number,
            "b": number
        }

    Returns:
        JSON response with the quotient
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        a = data.get('a')
        b = data.get('b')

        if not validate_number(a) or not validate_number(b):
            return jsonify({'error': 'Invalid input: both a and b must be numbers'}), 400

        if float(b) == 0:
            return jsonify({'error': 'Division by zero is not allowed'}), 400

        result = calc.divide(float(a), float(b))
        return jsonify({
            'operation': 'division',
            'a': a,
            'b': b,
            'result': result
        }), 200

    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero is not allowed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('ENVIRONMENT', 'production') != 'production'

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
