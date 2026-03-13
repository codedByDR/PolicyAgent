"""
Flask Web Application for Flexible Work & Life Balance Policy System
Main application with RAG, voice synthesis, and policy explanation
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from rag_engine import RAGEngine
from voice_synthesizer import VoiceSynthesizer

# Initialize Flask app
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')
CORS(app)

# Initialize RAG Engine and Voice Synthesizer
# IMPORTANT: Set your API key using environment variable GENAI_API_KEY
# Or replace the default value below with your GenAI Lab API key
API_KEY = os.environ.get("GENAI_API_KEY", "sk-T4AaQhdHdumu_fBjjE5nyg")

# Warn if using default/empty API key
if not API_KEY:
    print("=" * 60)
    print("WARNING: API key not configured!")
    print("Please set your GenAI Lab API key:")
    print("  - Set environment variable: export GENAI_API_KEY='your-api-key'")
    print("  - Or edit backend/app.py and set API_KEY directly")
    print("=" * 60)

rag_engine = RAGEngine(API_KEY)
voice_synthesizer = VoiceSynthesizer(output_dir="voice_outputs")

# Global variable to track if policy is loaded
policy_loaded = False


@app.before_request
def load_policy():
    """Load policy document on first request"""
    global policy_loaded
    
    if not policy_loaded:
        policy_file = Path(__file__).parent.parent / "documents" / "policy.txt"
        
        if policy_file.exists():
            success, message = rag_engine.load_policy_document(str(policy_file))
            if success:
                policy_loaded = True
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")


@app.route('/')
def index():
    """Serve main application page"""
    return render_template('index.html')


@app.route('/policy')
def view_policy():
    """Serve policy document"""
    policy_file = Path(__file__).parent.parent / "documents" / "policy.html"
    
    if policy_file.exists():
        with open(policy_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    return "<h1>Policy document not found</h1>", 404


@app.route('/api/policy-status')
def policy_status():
    """Check if policy document is loaded"""
    return jsonify({
        "loaded": policy_loaded,
        "status": "Policy document loaded successfully" if policy_loaded else "Policy document not loaded"
    })


@app.route('/api/health')
def health_check():
    """Check API configuration and connectivity"""
    api_key = os.getenv('GENAI_API_KEY', '')
    
    if not api_key:
        return jsonify({
            "status": "error",
            "message": "API key not configured. Please set GENAI_API_KEY environment variable.",
            "configured": False
        })
    
    # Test basic connectivity
    try:
        import requests
        response = requests.get(
            "https://genailab.tcs.in/health",
            verify=False,
            timeout=5
        )
        return jsonify({
            "status": "ok",
            "message": "API key configured",
            "configured": True,
            "endpoint_reachable": True
        })
    except Exception as e:
        return jsonify({
            "status": "warning",
            "message": f"API key configured but endpoint not reachable: {str(e)}",
            "configured": True,
            "endpoint_reachable": False
        })


@app.route('/api/explain', methods=['POST'])
def explain_policy():
    """Get policy explanation using RAG"""
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                "success": False,
                "explanation": "Please provide a question about the policy"
            }), 400
        
        if not policy_loaded:
            return jsonify({
                "success": False,
                "explanation": "Policy document is not loaded. Please refresh the page."
            }), 400
        
        result = rag_engine.explain_policy(question)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "explanation": f"Error: {str(e)}"
        }), 500


@app.route('/api/voice', methods=['POST'])
def generate_voice():
    """Generate voice note from text"""
    try:
        data = request.json
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({
                "success": False,
                "message": "Please provide text for voice generation"
            }), 400
        
        print(f"[Voice] Generating voice note for language: {language}, text length: {len(text)}")
        
        result = voice_synthesizer.synthesize_voice(text, language)
        
        print(f"[Voice] Generation result: {result.get('success')}")
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500


@app.route('/api/voice-status/<task_id>')
def get_voice_status(task_id):
    """Get status of voice synthesis task"""
    try:
        result = voice_synthesizer.get_task_status(task_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500


@app.route('/api/languages')
def get_languages():
    """Get supported languages for voice synthesis"""
    languages = voice_synthesizer.get_supported_languages()
    return jsonify(languages)


@app.route('/api/summary')
def get_summary():
    """Get policy document summary"""
    global policy_loaded
    
    try:
        # Try to load the policy if not loaded
        if not policy_loaded:
            policy_file = Path(__file__).parent.parent / "documents" / "policy.txt"
            print(f"[Summary] Checking policy file: {policy_file}")
            
            if policy_file.exists():
                success, message = rag_engine.load_policy_document(str(policy_file))
                print(f"[Summary] Load result: {success}, {message}")
                if success:
                    policy_loaded = True
                else:
                    return jsonify({
                        "success": False,
                        "summary": f"Error loading policy: {message}"
                    }), 500
            else:
                return jsonify({
                    "success": False,
                    "summary": f"Policy document file not found at {policy_file}"
                }), 404
        
        print("[Summary] Getting document summary...")
        result = rag_engine.get_document_summary()
        print(f"[Summary] Result: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"[Summary] Error: {str(e)}")
        return jsonify({
            "success": False,
            "summary": f"Error: {str(e)}"
        }), 500


@app.route('/api/pdf-list')
def get_pdf_list():
    """Get list of available PDF files"""
    pdf_dir = Path(__file__).parent.parent / "documents"
    pdfs = [f.name for f in pdf_dir.glob("*.pdf")]
    return jsonify({"pdfs": pdfs})


@app.route('/pdf/<filename>')
def download_pdf(filename):
    """Download a PDF file"""
    try:
        pdf_dir = Path(__file__).parent.parent / "documents"
        file_path = pdf_dir / filename
        
        if file_path.exists() and file_path.suffix.lower() == '.pdf':
            return send_file(
                str(file_path),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({"error": "PDF file not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


@app.route('/voice/<filename>')
def download_voice(filename):
    """Stream voice file for audio playback"""
    try:
        # Get the base directory (project root)
        base_dir = Path(__file__).parent.parent
        file_path = base_dir / "voice_outputs" / filename
        
        if file_path.exists():
            # Determine MIME type based on file extension
            if filename.endswith('.wav'):
                mimetype = 'audio/wav'
            elif filename.endswith('.mp3'):
                mimetype = 'audio/mpeg'
            else:
                mimetype = 'audio/mpeg'
            
            return send_file(
                str(file_path),
                mimetype=mimetype,
                as_attachment=False  # Stream instead of download
            )
        else:
            # Try alternative path (root level voice_outputs)
            alt_path = Path("voice_outputs") / filename
            if alt_path.exists():
                return send_file(
                    str(alt_path),
                    mimetype='audio/wav',
                    as_attachment=False
                )
            return jsonify({"error": "File not found"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Error serving voice file: {str(e)}"}), 500


@app.route('/api/request-flow')
def request_flow():
    """Get information about the request approval workflow"""
    workflow = {
        "steps": [
            {
                "step": 1,
                "name": "Request Initiation",
                "description": "Employee submits a flexible work arrangement request through the system",
                "duration": "Day 1"
            },
            {
                "step": 2,
                "name": "AI Justification Generation",
                "description": "AI generates professional justification and checks policy compliance",
                "duration": "Automatic"
            },
            {
                "step": 3,
                "name": "Automatic Routing",
                "description": "Request is routed to appropriate manager based on organizational hierarchy",
                "duration": "Automatic"
            },
            {
                "step": 4,
                "name": "Policy Review",
                "description": "Request is tagged with relevant policies and compliance verified",
                "duration": "Days 2-3"
            },
            {
                "step": 5,
                "name": "Manager Approval",
                "description": "Manager reviews and approves/denies the request with feedback",
                "duration": "Days 3-5"
            },
            {
                "step": 6,
                "name": "Outcome Monitoring",
                "description": "Approved arrangements are tracked and outcome analytics are provided",
                "duration": "Ongoing"
            }
        ],
        "approval_criteria": [
            "Compliance with company policies",
            "Business operational requirements",
            "Team resource availability",
            "Performance history and reliability"
        ]
    }
    
    return jsonify(workflow)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Flexible Work & Life Balance Policy System")
    print("=" * 60)
    print("Starting Flask application...")
    print("Open http://localhost:5000 in your browser")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
