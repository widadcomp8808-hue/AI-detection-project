from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import sys
import os
import traceback

# Import our phishing detector
from working_phishing_detector import detector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global model loading status
model_loaded = False

def load_model():
    """Enhanced model loading with detailed logging"""
    global model_loaded
    
    print("=== Starting model loading process ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
    
    # Try multiple paths and strategies
    possible_paths = [
        'svm_phishing_model.pkl',
        './svm_phishing_model.pkl',
        '/svm_phishing_model.pkl',
        'working_phishing_detector.py',  # Check if detector exists
        './working_phishing_detector.py'
    ]
    
    # Try to load model
    for i, path in enumerate(possible_paths):
        try:
            print(f"Trying path {i+1}: {path}")
            if os.path.exists(path):
                print(f"Path exists! Loading...")
                with open(path, 'rb') as f:
                    model_data = pickle.load(f)
                
                # Try to assign the model
                if hasattr(model_data, 'predict'):
                    detector.pipeline = model_data
                elif isinstance(model_data, dict) and 'pipeline' in model_data:
                    detector.pipeline = model_data['pipeline']
                else:
                    print(f"Model format not recognized: {type(model_data)}")
                    continue
                    
                detector.is_trained = True
                model_loaded = True
                print(f"✅ Model loaded successfully from: {path}")
                return True
            else:
                print(f"Path {path} does not exist")
                
        except Exception as e:
            print(f"❌ Error loading from {path}: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            continue
    
    # If we reach here, no model was found
    print("❌ Could not load model from any path")
    model_loaded = False
    return False

# Load model on startup
try:
    print("=== Initializing Flask API ===")
    load_model()
    print(f"Final model_loaded status: {model_loaded}")
except Exception as e:
    print(f"❌ Critical error during initialization: {str(e)}")
    print(f"Traceback: {traceback.format_exc()}")
    model_loaded = False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Enhanced health check with detailed diagnostics"""
    try:
        files_in_dir = []
        if os.path.exists('.'):
            files_in_dir = os.listdir('.')
            
        # Check if detector is properly imported
        detector_status = "available"
        if not hasattr(detector, 'is_trained'):
            detector_status = "malformed"
        elif detector.is_trained:
            detector_status = "trained"
        else:
            detector_status = "untrained"
        
        return jsonify({
            'status': 'healthy' if model_loaded else 'unhealthy',
            'model_loaded': model_loaded,
            'detector_status': detector_status,
            'message': 'Phishing Detection API is running',
            'working_dir': os.getcwd(),
            'files_count': len(files_in_dir),
            'python_version': sys.version,
            'available_files': files_in_dir[:10]  # First 10 files only
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'model_loaded': model_loaded,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/test', methods=['GET'])
def test_basic():
    """Basic test endpoint to verify Flask is working"""
    return jsonify({
        'status': 'success',
        'message': 'Flask is working!',
        'model_loaded': model_loaded,
        'detector_available': hasattr(detector, 'is_trained')
    })

@app.route('/api/predict', methods=['POST'])
def predict_email():
    """Predict if an email is phishing or safe"""
    try:
        if not model_loaded:
            return jsonify({
                'error': 'Model not loaded',
                'status': 'error',
                'available_files': os.listdir('.') if os.path.exists('.') else []
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
            'status': 'error',
            'traceback': traceback.format_exc()
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
        'status': 'error',
        'available_endpoints': [
            '/api/health',
            '/api/test', 
            '/api/predict',
            '/api/model-info'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error',
        'traceback': traceback.format_exc()
    }), 500

if __name__ == '__main__':
    print("=== Starting Phishing Detection API ===")
    print(f"Model loaded: {model_loaded}")
    
    if model_loaded:
        print("✅ API is ready to accept requests!")
        print("Available endpoints:")
        print("  GET  /api/health - Health check with diagnostics")
        print("  GET  /api/test - Basic Flask test")
        print("  GET  /api/model-info - Model information")
        print("  POST /api/predict - Predict email classification")
    else:
        print("❌ API cannot start - model not loaded")
    
    # Run the Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)
