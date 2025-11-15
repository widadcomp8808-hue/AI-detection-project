import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import pickle
import re
import warnings
warnings.filterwarnings('ignore')

class SimplePhishingDetector:
    def __init__(self):
        self.pipeline = None
        self.is_trained = False
        
    def preprocess_text(self, text):
        """Clean and preprocess email text"""
        if pd.isna(text) or text == '':
            return ''
        
        # Convert to string and lowercase
        text = str(text).lower()
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@.\-!?]', ' ', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' URL ', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' EMAIL ', text)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def create_sample_data(self):
        """Create sample phishing and safe emails for training"""
        phishing_emails = [
            "Congratulations! You have won $1000000! Click here to claim your prize immediately!",
            "URGENT: Your bank account will be suspended. Verify your identity now at this secure link!",
            "Limited time offer! Get a free iPhone 15! Click here and fill out the form!",
            "Dear user, we detected suspicious activity. Reset your password immediately to avoid account closure!",
            "You've been selected for a cash reward! Claim your money now by visiting this website!",
            "FREE vacation! You're the lucky winner! No purchase necessary. Click to claim your prize!",
            "Your PayPal account has been compromised. Login immediately to secure your account!",
            "Win a brand new car! Just click here and fill out the simple form to claim!",
            "CONGRATULATIONS! You won the lottery! Send us your bank details to receive your winnings!",
            "Important: Your email quota is full. Upgrade your account now to continue receiving emails!",
            "Act now! Your account expires in 24 hours. Click the link to save your data!",
            "Get rich quick! Make $5000 per day working from home! No experience needed!",
            "Security alert: Someone tried to access your account. Verify your identity immediately!"
        ]
        
        safe_emails = [
            "Hi John, I hope you're doing well. Can we schedule a meeting for next week?",
            "Thank you for your purchase. Your order confirmation is attached.",
            "Team meeting scheduled for Friday at 2 PM in conference room B.",
            "Please review the attached document and provide your feedback by Monday.",
            "Job application status update: We appreciate your interest in joining our team.",
            "Project deadline reminder: Please submit your reports by end of this week.",
            "Expense reimbursement request approved. Payment will be processed within 5 business days.",
            "Welcome to our newsletter! Here are this week's updates and news.",
            "Monthly report summary is ready for review. Please check the shared folder.",
            "Thank you for attending today's seminar. The presentation slides are attached.",
            "Meeting agenda for tomorrow's project discussion is now available.",
            "Please find attached the quarterly financial report for your review.",
            "New company policies document has been updated. Please read and acknowledge."
        ]
        
        # Create dataset
        emails = phishing_emails + safe_emails
        labels = ['Phishing'] * len(phishing_emails) + ['Safe'] * len(safe_emails)
        
        return emails, labels
    
    def train_model(self):
        """Train the phishing detection model with sample data"""
        print("Creating sample dataset...")
        emails, labels = self.create_sample_data()
        
        # Preprocess emails
        print("Preprocessing emails...")
        clean_emails = [self.preprocess_text(email) for email in emails]
        
        # Encode labels: Safe=0, Phishing=1
        y = [1 if label == 'Phishing' else 0 for label in labels]
        
        # Create and train pipeline
        print("Training SVM model...")
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=300,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=1.0
            )),
            ('classifier', SVC(
                kernel='linear',
                C=1.0,
                probability=True,
                random_state=42
            ))
        ])
        
        self.pipeline.fit(clean_emails, y)
        self.is_trained = True
        
        print("Model trained successfully!")
        
        # Save model
        with open('svm_phishing_model.pkl', 'wb') as f:
            pickle.dump(self.pipeline, f)
        print("Model saved as 'svm_phishing_model.pkl'")
        
        return True
    
    def predict_email(self, email_text):
        """Predict if an email is phishing or safe"""
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        # Preprocess the input text
        clean_text = self.preprocess_text(email_text)
        
        # Make prediction
        prediction = self.pipeline.predict([clean_text])[0]
        probabilities = self.pipeline.predict_proba([clean_text])[0]
        
        # Get confidence scores
        safe_prob = probabilities[0] * 100
        phishing_prob = probabilities[1] * 100
        
        result = {
            'prediction': 'Phishing' if prediction == 1 else 'Safe',
            'confidence': max(safe_prob, phishing_prob),
            'safe_probability': safe_prob,
            'phishing_probability': phishing_prob
        }
        
        return result
    
    def analyze_email_content(self, email_text):
        """Analyze email content for phishing indicators"""
        clean_text = email_text.lower()
        
        phishing_indicators = []
        safe_indicators = []
        
        # Phishing indicators
        phishing_patterns = {
            'urgent': ['urgent', 'immediately', 'now', 'instantly', 'asap'],
            'money': ['free', 'win', 'prize', 'money', 'cash', 'reward', 'lottery'],
            'account': ['account', 'verify', 'suspended', 'locked', 'compromised'],
            'action': ['click', 'click here', 'visit', 'link', 'button'],
            'offers': ['congratulations', 'selected', 'winner', 'limited time'],
            'threats': ['suspended', 'expired', 'closure', 'terminated']
        }
        
        # Safe indicators
        safe_patterns = {
            'business': ['meeting', 'schedule', 'agenda', 'document', 'report'],
            'courtesy': ['thank', 'appreciate', 'please', 'regards', 'sincerely'],
            'formal': ['attached', 'regarding', 'concerning', 'feedback', 'review'],
            'process': ['approved', 'processed', 'completed', 'updated', 'confirm']
        }
        
        # Check for phishing indicators
        for category, patterns in phishing_patterns.items():
            found_patterns = [p for p in patterns if p in clean_text]
            if found_patterns:
                phishing_indicators.extend(found_patterns)
        
        # Check for safe indicators
        for category, patterns in safe_patterns.items():
            found_patterns = [p for p in patterns if p in clean_text]
            if found_patterns:
                safe_indicators.extend(found_patterns)
        
        return {
            'phishing_indicators': list(set(phishing_indicators)),
            'safe_indicators': list(set(safe_indicators))
        }
    
    def generate_detailed_explanation(self, email_text):
        """Generate a detailed explanation of why an email is classified"""
        result = self.predict_email(email_text)
        analysis = self.analyze_email_content(email_text)
        
        explanation = {
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'safe_probability': result['safe_probability'],
            'phishing_probability': result['phishing_probability'],
            'reasoning': [],
            'indicators': analysis
        }
        
        if result['prediction'] == 'Phishing':
            explanation['reasoning'].append("This email shows characteristics typical of phishing attempts:")
            
            if analysis['phishing_indicators']:
                explanation['reasoning'].append(f"• Contains suspicious language: {', '.join(analysis['phishing_indicators'][:5])}")
            
            if any('click' in str(ind).lower() for ind in analysis['phishing_indicators']):
                explanation['reasoning'].append("• Contains urgent call-to-action language")
            
            if any(word in str(ind).lower() for ind in analysis['phishing_indicators'] for word in ['free', 'win', 'prize']):
                explanation['reasoning'].append("• Uses enticing offers or prizes to lure recipients")
            
            if any(word in str(ind).lower() for ind in analysis['phishing_indicators'] for word in ['urgent', 'immediately', 'suspended']):
                explanation['reasoning'].append("• Creates a sense of urgency to bypass critical thinking")
            
            if any(word in str(ind).lower() for ind in analysis['phishing_indicators'] for word in ['account', 'verify']):
                explanation['reasoning'].append("• Requests account verification or sensitive information")
            
            if len(explanation['reasoning']) == 1:  # Only the opening sentence
                explanation['reasoning'].append("• Contains suspicious language patterns commonly found in phishing emails")
        else:
            explanation['reasoning'].append("This email appears to be legitimate:")
            
            if analysis['safe_indicators']:
                explanation['reasoning'].append(f"• Contains professional language: {', '.join(analysis['safe_indicators'][:5])}")
            
            if any(word in str(ind).lower() for ind in analysis['safe_indicators'] for word in ['meeting', 'schedule']):
                explanation['reasoning'].append("• Contains normal business communication elements")
            
            if any(word in str(ind).lower() for ind in analysis['safe_indicators'] for word in ['thank', 'appreciate']):
                explanation['reasoning'].append("• Uses professional and courteous language")
            
            if any(word in str(ind).lower() for ind in analysis['safe_indicators'] for word in ['document', 'report', 'attached']):
                explanation['reasoning'].append("• Contains typical business document references")
            
            if len(explanation['reasoning']) == 1:  # Only the opening sentence
                explanation['reasoning'].append("• Does not contain typical phishing indicators")
        
        return explanation

# Global detector instance
detector = SimplePhishingDetector()

def main():
    """Main function to train the model"""
    detector.train_model()
    
    # Test with sample emails
    test_emails = [
        "Congratulations! You won a free iPhone! Click here to claim your prize now!",
        "Hi John, can we meet tomorrow to discuss the project details?",
        "URGENT: Your account will be suspended unless you verify immediately at this link",
        "Meeting scheduled for 2 PM tomorrow in conference room A"
    ]
    
    print("\n" + "="*60)
    print("TESTING SAMPLE EMAILS")
    print("="*60)
    
    for i, email in enumerate(test_emails, 1):
        result = detector.predict_email(email)
        print(f"\nEmail {i}: {email[:50]}...")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.1f}%")
        print(f"Safe: {result['safe_probability']:.1f}% | Phishing: {result['phishing_probability']:.1f}%")
        
        # Show detailed explanation
        explanation = detector.generate_detailed_explanation(email)
        print("Explanation:")
        for reason in explanation['reasoning']:
            print(f"  {reason}")

if __name__ == "__main__":
    main()