import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { PythonShell } from 'python-shell';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

let modelReady = false;
let pythonReady = false;

const initializePython = async () => {
  return new Promise((resolve) => {
    const script = `
import sys
sys.path.insert(0, '.')
from working_phishing_detector import detector

print("Python environment ready")
print(f"Detector loaded: {hasattr(detector, 'is_trained')}")
`.trim();

    const options = {
      mode: 'text',
      pythonOptions: ['-u'],
      cwd: __dirname,
    };

    PythonShell.runString(script, options, (err, results) => {
      if (err) {
        console.error('❌ Python initialization error:', err);
        pythonReady = false;
      } else {
        console.log('✅ Python environment initialized');
        console.log(results);
        pythonReady = true;
        modelReady = true;
      }
      resolve();
    });
  });
};

app.get('/api/health', (req, res) => {
  res.json({
    status: pythonReady ? 'healthy' : 'initializing',
    model_loaded: modelReady,
    python_ready: pythonReady,
    message: 'Phishing Detection API is running'
  });
});

app.get('/api/test', (req, res) => {
  res.json({
    status: 'success',
    message: 'Server is running!',
    model_loaded: modelReady,
    python_ready: pythonReady
  });
});

app.post('/api/predict', async (req, res) => {
  try {
    if (!modelReady) {
      return res.status(503).json({
        status: 'error',
        error: 'Model is still initializing. Please try again in a moment.'
      });
    }

    const { email_text } = req.body;

    if (!email_text || email_text.trim() === '') {
      return res.status(400).json({
        status: 'error',
        error: 'Email text cannot be empty'
      });
    }

    const script = `
import sys
sys.path.insert(0, '.')
from working_phishing_detector import detector
import json

email_text = """${email_text.replace(/"/g, '\\"')}"""

try:
    result = detector.predict_email(email_text)
    explanation = detector.generate_detailed_explanation(email_text)

    response = {
        "status": "success",
        "prediction": result,
        "explanation": explanation
    }
    print(json.dumps(response))
except Exception as e:
    error_response = {
        "status": "error",
        "error": str(e)
    }
    print(json.dumps(error_response))
`.trim();

    const options = {
      mode: 'text',
      pythonOptions: ['-u'],
      cwd: __dirname,
    };

    PythonShell.runString(script, options, (err, results) => {
      if (err) {
        console.error('❌ Prediction error:', err);
        return res.status(500).json({
          status: 'error',
          error: 'Failed to process email'
        });
      }

      try {
        const output = results[results.length - 1];
        const response = JSON.parse(output);
        res.json(response);
      } catch (parseErr) {
        console.error('❌ Parse error:', parseErr);
        res.status(500).json({
          status: 'error',
          error: 'Failed to parse prediction results'
        });
      }
    });
  } catch (error) {
    console.error('❌ Server error:', error);
    res.status(500).json({
      status: 'error',
      error: 'Internal server error'
    });
  }
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

const startServer = async () => {
  console.log('=== Initializing Phishing Detection API ===');

  await initializePython();

  app.listen(PORT, () => {
    console.log(`✅ Server running on port ${PORT}`);
    if (modelReady) {
      console.log('✅ Model is ready for predictions');
    } else {
      console.log('⚠️  Model still initializing...');
    }
  });
};

startServer();
