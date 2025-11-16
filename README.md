# AI-Driven Phishing Email Detection System

A sophisticated web application that uses Support Vector Machine (SVM) machine learning algorithms to detect phishing emails in real-time. This system provides users with detailed explanations of why emails are classified as phishing or safe, promoting cybersecurity awareness.

## 🚀 Features

- **AI-Powered Detection**: Uses advanced SVM machine learning for accurate phishing detection
- **Real-time Analysis**: Instant email classification with confidence scores
- **Detailed Explanations**: Clear reasoning for each classification decision
- **Modern Web Interface**: Responsive design with dark/light mode support
- **Educational Content**: Learn about phishing detection through explanations
- **RESTful API**: Complete backend API for integration with other applications

## 🛠️ Technology Stack

### Machine Learning
- **Algorithm**: Support Vector Machine (SVM) with Linear kernel
- **Feature Extraction**: TF-IDF Vectorization
- **Text Processing**: Custom preprocessing pipeline
- **Training Data**: Curated dataset of phishing and legitimate emails

### Backend
- **Framework**: Flask (Python)
- **API**: RESTful endpoints with JSON responses
- **Model**: Serialized SVM model with pickle
- **Cross-Origin**: CORS enabled for web interface

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with CSS Variables for theming
- **Icons**: Font Awesome 6.0
- **Responsive**: Mobile-first design approach
- **Animations**: Smooth transitions and loading states

## 📁 Project Structure

```
workspace/
├── index.html              # Main web interface
├── styles.css              # Complete styling with dark mode
├── script.js               # Frontend JavaScript functionality
├── api.py                  # Flask REST API
├── working_phishing_detector.py  # ML model implementation
├── svm_phishing_model.pkl  # Trained model (auto-generated)
├── demo.py                 # API testing script
├── start_server.sh         # Server startup script
└── README.md               # This file
```

## 🚦 Getting Started

### Prerequisites
- Python 3.8+
- Required Python packages (automatically installed)

### Installation & Setup

1. **Clone/Download the project**:
   ```bash
   # All files are ready in the workspace
   cd /workspace
   ```

2. **Install dependencies**:
   ```bash
   # Dependencies are already installed:
   # - scikit-learn (ML algorithms)
   # - pandas (data processing)
   # - numpy (numerical computing)
   # - flask (web framework)
   # - flask-cors (cross-origin support)
   ```

3. **Train the model** (if not already trained):
   ```bash
   python working_phishing_detector.py
   ```

4. **Start the server**:
   ```bash
   # Method 1: Using the startup script
   chmod +x start_server.sh
   ./start_server.sh
   
   # Method 2: Direct Python execution
   python api.py
   ```

5. **Access the application**:
   - Web Interface: http://localhost:5000
   - API Endpoints: http://localhost:5000/api/*

## 🔌 API Endpoints

### Health Check
```http
GET /api/health
```
Returns the API status and model loading state.

### Model Information
```http
GET /api/model-info
```
Provides details about the trained model and algorithm.

### Email Prediction
```http
POST /api/predict
Content-Type: application/json

{
  "email_text": "Your email content here..."
}
```
Returns prediction, confidence scores, and detailed explanation.

### Detailed Explanation
```http
POST /api/explain
Content-Type: application/json

{
  "email_text": "Your email content here..."
}
```
Returns only the detailed explanation for the classification.

## 🧪 Testing the API

### Using the Demo Script
```bash
# Test API functionality
python demo.py

# Run comprehensive demo with sample emails
python demo.py demo
```

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test prediction endpoint
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"email_text": "Congratulations! You won a prize! Click here now!"}'
```

## 💻 Web Interface Usage

1. **Enter Email**: Paste or type the email content you want to analyze
2. **Analyze**: Click the "Analyze Email" button or press Ctrl+Enter
3. **View Results**: See the classification, confidence scores, and detailed explanation
4. **Dark Mode**: Toggle between light and dark themes using the moon/sun icon

### Keyboard Shortcuts
- `Ctrl + Enter`: Analyze email
- `Escape`: Clear input
- `Alt + 1`: Load phishing sample
- `Alt + 2`: Load safe sample

## 🧠 How It Works

### Machine Learning Pipeline

1. **Text Preprocessing**:
   - Lowercase conversion
   - Special character handling
   - URL and email address normalization
   - Whitespace cleanup

2. **Feature Extraction**:
   - TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
   - N-gram analysis (1-2 grams)
   - Stop word removal

3. **Classification**:
   - Support Vector Machine with linear kernel
   - Probability estimation for confidence scoring
   - Binary classification (Safe/Phishing)

4. **Explanation Generation**:
   - Pattern matching for phishing indicators
   - Content analysis for suspicious elements
   - Language pattern recognition

### Detection Features

The system identifies various phishing indicators:

**Phishing Indicators**:
- Urgency language ("urgent", "immediately", "now")
- Financial incentives ("free", "win", "prize", "money")
- Account-related threats ("suspended", "verify", "compromised")
- Call-to-action phrases ("click", "visit", "link")
- Unrealistic offers ("congratulations", "winner")

**Safe Indicators**:
- Business communication patterns
- Professional language ("thank", "please", "appreciate")
- Document references ("attached", "report", "feedback")
- Formal structure and proper formatting

## 🎨 Customization

### Styling
- Modify `styles.css` to change colors, fonts, and layout
- CSS variables support easy theme customization
- Responsive breakpoints for mobile optimization

### Model Training
- Update `working_phishing_detector.py` to retrain with new data
- Modify sample data in `create_sample_data()` method
- Adjust SVM parameters for different performance characteristics

### API Extensions
- Add new endpoints in `api.py`
- Implement additional analysis features
- Integrate with external email services

## 🔧 Troubleshooting

### Common Issues

1. **Model not found**:
   ```bash
   # Retrain the model
   python working_phishing_detector.py
   ```

2. **API connection failed**:
   - Ensure Flask server is running on port 5000
   - Check firewall settings
   - Verify CORS configuration

3. **Import errors**:
   ```bash
   # Reinstall dependencies
   uv add scikit-learn pandas numpy flask flask-cors
   ```

4. **Port already in use**:
   ```bash
   # Find and kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

## 📊 Performance

### Model Metrics
- **Algorithm**: Linear SVM
- **Features**: TF-IDF vectors (max 300 features)
- **Training Time**: < 10 seconds on sample data
- **Inference Time**: < 100ms per email
- **Accuracy**: High accuracy on sample data

### System Requirements
- **Memory**: < 100MB for model and application
- **CPU**: Minimal processing requirements
- **Storage**: < 50MB for complete application

## 🔒 Security Features

- **Input Validation**: Comprehensive email content validation
- **Error Handling**: Graceful error responses
- **CORS Configuration**: Secure cross-origin requests
- **No Data Storage**: Emails are processed in-memory only

## 🚀 Future Enhancements

- **Multi-language Support**: Extend to other languages
- **Advanced Features**: URL analysis, attachment scanning
- **Real-time Integration**: Email client plugins
- **Enhanced ML**: Deep learning models for better accuracy
- **Dashboard**: Analytics and reporting features

## 📝 License

This project is developed for educational and demonstration purposes. Feel free to use and modify according to your needs.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Model accuracy enhancement
- UI/UX improvements
- Additional detection features
- Performance optimizations

## 📞 Support

For technical support or questions about the implementation:
1. Check the troubleshooting section
2. Review the API documentation
3. Test with the provided demo script
4. Examine the source code comments

---

**Built with ❤️ for email security awareness using Machine Learning**