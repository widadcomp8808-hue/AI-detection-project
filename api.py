from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import sys
import os

# Import our phishing detector
from working_phishing_detector import detector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
def load_model():
    try:
        with open('svm_phishing_model.pkl', 'rb') as f:
            detector.pipeline = pickle.load(f)
        detector.is_trained = True
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

# Load model on startup
model_loaded = load_model()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'message': 'Phishing Detection API is running'
    })

@app.route('/api/predict', methods=['POST'])
def predict_email():
    """Predict if an email is phishing or safe"""
    try:
        if not model_loaded:
            return jsonify({
                'error': 'Model not loaded',
                'status': 'error'
            }), 500
        
        # Get email text from request
        data = request.get_json()
        if not data or 'email_text' not in data:
            return jsonify({
                'error': 'Missing email_text in request',
                'status': 'error'
            }), 400
        
        email_text = data['email_text']
        if not email_text or email_text.strip() == '':
            return jsonify({
                'error': 'Email text cannot be empty',
                'status': 'error'
            }), 400
        
        # Make prediction
        result = detector.predict_email(email_text)
        explanation = detector.generate_detailed_explanation(email_text)
        
        return jsonify({
            'status': 'success',
            'prediction': result,
            'explanation': explanation
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/explain', methods=['POST'])
def explain_prediction():
    """Get detailed explanation for email classification"""
    try:
        if not model_loaded:
            return jsonify({
                'error': 'Model not loaded',
                'status': 'error'
            }), 500
        
        # Get email text from request
        data = request.get_json()
        if not data or 'email_text' not in data:
            return jsonify({
                'error': 'Missing email_text in request',
                'status': 'error'
            }), 400
        
        email_text = data['email_text']
        if not email_text or email_text.strip() == '':
            return jsonify({
                'error': 'Email text cannot be empty',
                'status': 'error'
            }), 400
        
        # Generate explanation
        explanation = detector.generate_detailed_explanation(email_text)
        
        return jsonify({
            'status': 'success',
            'explanation': explanation
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about the trained model"""
    try:
        if not model_loaded:
            return jsonify({
                'error': 'Model not loaded',
                'status': 'error'
            }), 500
        
        return jsonify({
            'status': 'success',
            'model_type': 'Support Vector Machine (SVM)',
            'algorithm': 'Linear SVM with TF-IDF Vectorization',
            'training_method': 'Sample dataset with phishing and safe emails',
            'features': 'TF-IDF vectorization of email text',
            'description': 'AI-Driven Awareness Program for Phishing Email Detection using SVM'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    print("Starting Phishing Detection API...")
    print(f"Model loaded: {model_loaded}")
    
    if model_loaded:
        print("API is ready to accept requests!")
        print("Endpoints:")
        print("  GET  /api/health - Health check")
        print("  GET  /api/model-info - Model information")
        print("  POST /api/predict - Predict email classification")
        print("  POST /api/explain - Get detailed explanation")
    
    # Run the Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)