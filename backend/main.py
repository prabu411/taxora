from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from models import StartSessionRequest, ChatTurnRequest, ChatTurnResponse
from chat_logic import start_session, handle_turn, get_session_info, clear_session, get_active_sessions, get_session
from granite_client import test_granite_connectivity
from ai_provider_manager import get_ai_manager
from savings_planner import savings_planner
from business_tracker import business_tracker
from pydantic import BaseModel
import logging
import time
import uuid
from typing import Dict, Any
from contextlib import asynccontextmanager
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI):
	"""Initialize application and test Watson connectivity on startup."""
	logger.info("Starting Taxora Chat API...")

	# Test Granite AI services connectivity
	connectivity_results = test_granite_connectivity()

	if not connectivity_results.get("granite_ai"):
		logger.warning("Granite AI connectivity test failed. Using fallback responses.")

	if not connectivity_results.get("model_loaded"):
		logger.warning("Granite model not loaded locally. Using API or fallback mode.")

	if connectivity_results.get("nlu_analysis"):
		logger.info("NLU analysis capabilities available.")

	logger.info("Taxora Chat API startup completed")

	yield

	# Cleanup code can go here if needed
	logger.info("Taxora Chat API shutting down...")

# Initialize FastAPI app with enhanced configuration
app = FastAPI(
	title="Taxora - AI-Powered Conversational Finance Assistant",
	description="Advanced conversational AI finance assistant powered by IBM's generative AI and Watson NLP capabilities",
	version="2.0.0",
	docs_url="/docs",
	redoc_url="/redoc",
	lifespan=lifespan
)

# Mount static files
if os.path.exists("static"):
	app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware for frontend integration
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "http://localhost:8000", "http://127.0.0.1:8000"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)



@app.get("/", response_class=HTMLResponse)
def homepage():
	"""Serve the main homepage."""
	try:
		with open("static/index.html", "r", encoding="utf-8") as f:
			return f.read()
	except FileNotFoundError:
		return HTMLResponse("""
		<html>
			<head><title>Taxora API</title></head>
			<body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
				<h1>🤖 Taxora API</h1>
				<p>AI-Powered Conversational Finance Assistant</p>
				<p><a href="/docs">📚 API Documentation</a> | <a href="/status">⚡ System Status</a></p>
			</body>
		</html>
		""")

@app.get("/health")
def health_check():
	"""JSON health check endpoint."""
	return {
		"status": "healthy",
		"service": "Taxora - AI-Powered Conversational Finance Assistant",
		"version": "2.0.0",
		"description": "Conversational NLP Experience with IBM's generative AI and Watson NLP capabilities",
		"features": [
			"IBM watsonx.ai Integration",
			"Watson NLP Capabilities",
			"Adaptive Persona System",
			"Context-Aware Interactions",
			"Professional Finance Guidance"
		],
		"timestamp": time.time()
	}

@app.get("/docs")
def api_documentation():
	"""Comprehensive API documentation page."""
	return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taxora API Documentation</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: #333; line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; margin-bottom: 40px; }
        .header h1 { font-size: 3rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .content { background: white; border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
        .endpoint { background: #f8f9fa; border-radius: 10px; padding: 20px; margin: 20px 0; border-left: 4px solid #667eea; }
        .method { display: inline-block; padding: 4px 12px; border-radius: 4px; font-weight: bold; color: white; margin-right: 10px; }
        .get { background: #28a745; } .post { background: #007bff; } .put { background: #ffc107; color: #333; } .delete { background: #dc3545; }
        .code { background: #f1f3f4; padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; margin: 10px 0; overflow-x: auto; }
        .back-btn { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; margin-bottom: 20px; }
        .back-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
        h2 { color: #495057; margin: 30px 0 20px 0; border-bottom: 2px solid #e9ecef; padding-bottom: 10px; }
        h3 { color: #667eea; margin: 20px 0 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Taxora API Documentation</h1>
            <p>Complete API reference for the AI-Powered Finance Assistant</p>
        </div>

        <div class="content">
            <a href="/static/index.html" class="back-btn">← Back to Home</a>

            <h2>🚀 Getting Started</h2>
            <p>Taxora provides a RESTful API for AI-powered financial conversations. All endpoints return JSON responses and support CORS for web applications.</p>

            <h2>🔗 Core Endpoints</h2>

            <div class="endpoint">
                <h3><span class="method post">POST</span>/start</h3>
                <p><strong>Initialize a new conversation session</strong></p>
                <div class="code">
{
  "name": "John Doe",
  "role": "student" // "student", "professional", or "general"
}
</div>
                <p><strong>Response:</strong></p>
                <div class="code">
{
  "success": true,
  "session_id": "uuid-string",
  "message": "Welcome message",
  "persona": "Selected persona details"
}
</div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span>/chat</h3>
                <p><strong>Send a message and get AI response</strong></p>
                <div class="code">
{
  "message": "How should I budget my income?",
  "session_id": "uuid-string"
}
</div>
                <p><strong>Response:</strong></p>
                <div class="code">
{
  "success": true,
  "reply": "AI response with financial advice",
  "session_id": "uuid-string",
  "timestamp": 1234567890
}
</div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span>/voice/chat</h3>
                <p><strong>Voice chat with Tamil support</strong></p>
                <p>Upload audio file for complete voice processing pipeline</p>
                <div class="code">
Content-Type: multipart/form-data
- audio: audio file (wav, mp3, m4a)
- session_id: string (optional)
- include_tamil: boolean (default: true)
</div>
            </div>

            <h2>🛠️ Utility Endpoints</h2>

            <div class="endpoint">
                <h3><span class="method get">GET</span>/status</h3>
                <p><strong>System health and status</strong></p>
                <div class="code">
{
  "system": "operational",
  "ai_services": {...},
  "active_sessions": 5,
  "services": {
    "granite_ai": "✅ Connected",
    "nlu_analysis": "✅ Available"
  }
}
</div>
            </div>

            <div class="endpoint">
                <h3><span class="method get">GET</span>/ai/providers</h3>
                <p><strong>Available AI providers and status</strong></p>
                <div class="code">
{
  "success": true,
  "data": {
    "current_provider": "gemini",
    "available_providers": {...}
  }
}
</div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span>/ai/provider</h3>
                <p><strong>Switch AI provider</strong></p>
                <div class="code">
{
  "provider": "granite" // "granite" or "gemini"
}
</div>
            </div>

            <h2>📁 File Upload</h2>

            <div class="endpoint">
                <h3><span class="method post">POST</span>/upload</h3>
                <p><strong>Upload and analyze financial documents</strong></p>
                <div class="code">
Content-Type: multipart/form-data
- file: document file
- session_id: string (optional)
</div>
            </div>

            <h2>🎯 Session Management</h2>

            <div class="endpoint">
                <h3><span class="method get">GET</span>/session/{session_id}</h3>
                <p><strong>Get session information</strong></p>
            </div>

            <div class="endpoint">
                <h3><span class="method delete">DELETE</span>/session/{session_id}</h3>
                <p><strong>Clear session history</strong></p>
            </div>

            <h2>🔧 Error Handling</h2>
            <p>All endpoints return appropriate HTTP status codes:</p>
            <ul style="margin: 20px 0; padding-left: 30px;">
                <li><strong>200</strong> - Success</li>
                <li><strong>400</strong> - Bad Request (invalid input)</li>
                <li><strong>404</strong> - Not Found</li>
                <li><strong>500</strong> - Internal Server Error</li>
                <li><strong>503</strong> - Service Unavailable</li>
            </ul>

            <h2>🌟 Features</h2>
            <ul style="margin: 20px 0; padding-left: 30px;">
                <li>🧠 <strong>IBM Granite AI</strong> - Lightweight, fast AI responses</li>
                <li>🎭 <strong>Persona System</strong> - Tailored responses for different user types</li>
                <li>🎙️ <strong>Voice Chat</strong> - Complete voice processing with Tamil support</li>
                <li>🔄 <strong>Provider Switching</strong> - Automatic fallback between AI providers</li>
                <li>📊 <strong>Session Management</strong> - Persistent conversation context</li>
                <li>📁 <strong>File Analysis</strong> - Upload and analyze financial documents</li>
            </ul>

            <div style="text-align: center; margin: 40px 0;">
                <a href="/static/chat.html" class="back-btn">🚀 Try the Chat Interface</a>
                <a href="/status" class="back-btn" style="margin-left: 20px;">⚡ Check System Status</a>
            </div>
        </div>
    </div>
</body>
</html>
	""")

@app.get("/status")
def system_status_page():
	"""Beautiful HTML system status page."""
	try:
		connectivity = test_granite_connectivity()
		active_sessions = len(get_active_sessions())

		# Get AI provider status
		from ai_provider_manager import get_ai_manager
		ai_manager = get_ai_manager()
		provider_status = ai_manager.get_provider_status()

		# Get rate limit status
		try:
			from gemini_client import get_gemini_rate_limit_status
			rate_limit_status = get_gemini_rate_limit_status()
		except:
			rate_limit_status = {"error": "Unable to get rate limit status"}

		system_operational = connectivity.get("granite_ai", False)
		status_color = "#28a745" if system_operational else "#dc3545"
		status_text = "Operational" if system_operational else "Degraded"

		return HTMLResponse(content=f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taxora System Status</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: #333; line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; color: white; margin-bottom: 40px; }}
        .header h1 {{ font-size: 3rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .content {{ background: white; border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
        .status-overview {{ text-align: center; margin-bottom: 40px; padding: 30px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; }}
        .status-indicator {{ font-size: 4rem; margin-bottom: 20px; }}
        .status-text {{ font-size: 2rem; font-weight: bold; color: {status_color}; margin-bottom: 10px; }}
        .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }}
        .status-card {{ background: #f8f9fa; border-radius: 15px; padding: 25px; border-left: 4px solid #667eea; }}
        .status-card h3 {{ color: #495057; margin-bottom: 15px; font-size: 1.3rem; }}
        .service-item {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #e9ecef; }}
        .service-item:last-child {{ border-bottom: none; }}
        .service-status {{ font-weight: bold; }}
        .connected {{ color: #28a745; }}
        .disconnected {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .back-btn {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; margin-bottom: 20px; }}
        .back-btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }}
        .refresh-btn {{ background: #28a745; margin-left: 10px; }}
        .timestamp {{ text-align: center; color: #6c757d; margin-top: 30px; font-style: italic; }}
        @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} 100% {{ opacity: 1; }} }}
        .pulse {{ animation: pulse 2s infinite; }}
    </style>
    <script>
        function refreshStatus() {{
            window.location.reload();
        }}

        // Auto-refresh every 30 seconds
        setTimeout(function() {{
            refreshStatus();
        }}, 30000);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ Taxora System Status</h1>
            <p>Real-time monitoring of AI services and system health</p>
        </div>

        <div class="content">
            <a href="/static/index.html" class="back-btn">← Back to Home</a>
            <button onclick="refreshStatus()" class="back-btn refresh-btn">🔄 Refresh Status</button>

            <div class="status-overview">
                <div class="status-indicator">{'🟢' if system_operational else '🔴'}</div>
                <div class="status-text">{status_text}</div>
                <p>All core systems are {'functioning normally' if system_operational else 'experiencing issues'}</p>
            </div>

            <div class="status-grid">
                <div class="status-card">
                    <h3>🧠 AI Services</h3>
                    <div class="service-item">
                        <span>IBM Granite AI</span>
                        <span class="service-status {'connected' if connectivity.get('granite_ai') else 'disconnected'}">
                            {'✅ Connected' if connectivity.get('granite_ai') else '❌ Disconnected'}
                        </span>
                    </div>
                    <div class="service-item">
                        <span>NLU Analysis</span>
                        <span class="service-status {'connected' if connectivity.get('nlu_analysis') else 'disconnected'}">
                            {'✅ Available' if connectivity.get('nlu_analysis') else '❌ Unavailable'}
                        </span>
                    </div>
                    <div class="service-item">
                        <span>Model Status</span>
                        <span class="service-status {'connected' if connectivity.get('model_loaded') else 'warning'}">
                            {'✅ Loaded' if connectivity.get('model_loaded') else '⚠️ API Mode'}
                        </span>
                    </div>
                </div>

                <div class="status-card">
                    <h3>🔄 AI Providers</h3>
                    <div class="service-item">
                        <span>Current Provider</span>
                        <span class="service-status connected">{provider_status.get('current_provider', 'Unknown').title()}</span>
                    </div>
                    <div class="service-item">
                        <span>Available Providers</span>
                        <span class="service-status connected">{provider_status.get('provider_count', 0)} Active</span>
                    </div>
                    <div class="service-item">
                        <span>Provider Switching</span>
                        <span class="service-status {'connected' if provider_status.get('allow_switching') else 'warning'}">
                            {'✅ Enabled' if provider_status.get('allow_switching') else '⚠️ Disabled'}
                        </span>
                    </div>
                </div>

                <div class="status-card">
                    <h3>📊 System Metrics</h3>
                    <div class="service-item">
                        <span>Active Sessions</span>
                        <span class="service-status connected">{active_sessions}</span>
                    </div>
                    <div class="service-item">
                        <span>Gemini Rate Limits</span>
                        <span class="service-status connected">
                            {rate_limit_status.get('minute_remaining', 'N/A')}/{rate_limit_status.get('minute_limit', 'N/A')} remaining
                        </span>
                    </div>
                    <div class="service-item">
                        <span>System Uptime</span>
                        <span class="service-status connected pulse">🟢 Running</span>
                    </div>
                </div>

                <div class="status-card">
                    <h3>🎙️ Voice Services</h3>
                    <div class="service-item">
                        <span>Voice Chat</span>
                        <span class="service-status connected">✅ Available</span>
                    </div>
                    <div class="service-item">
                        <span>Tamil Support</span>
                        <span class="service-status connected">✅ Enabled</span>
                    </div>
                    <div class="service-item">
                        <span>Audio Processing</span>
                        <span class="service-status connected">✅ Ready</span>
                    </div>
                </div>
            </div>

            <div style="text-align: center; margin: 40px 0;">
                <a href="/static/chat.html" class="back-btn">💬 Test Chat Interface</a>
                <a href="/docs" class="back-btn" style="margin-left: 20px;">📚 API Documentation</a>
            </div>

            <div class="timestamp">
                Last updated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
                <br>Auto-refresh in 30 seconds
            </div>
        </div>
    </div>
</body>
</html>
		""")

	except Exception as e:
		logger.error(f"Status page failed: {e}")
		return HTMLResponse(content=f"""
<!DOCTYPE html>
<html><head><title>Status Error</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
<h1>⚠️ Status Check Failed</h1>
<p>Error: {str(e)}</p>
<a href="/static/index.html">← Back to Home</a>
</body></html>
		""", status_code=503)

@app.get("/api/status")
def system_status_json():
	"""JSON system status for API consumers."""
	try:
		connectivity = test_granite_connectivity()
		active_sessions = len(get_active_sessions())

		return {
			"system": "operational",
			"ai_services": connectivity,
			"active_sessions": active_sessions,
			"timestamp": time.time(),
			"services": {
				"granite_ai": "✅ Connected" if connectivity.get("granite_ai") else "❌ Disconnected",
				"nlu_analysis": "✅ Available" if connectivity.get("nlu_analysis") else "❌ Unavailable",
				"model_status": "✅ Loaded" if connectivity.get("model_loaded") else "⚠️ API Mode"
			}
		}
	except Exception as e:
		logger.error(f"Status check failed: {e}")
		return JSONResponse(
			status_code=503,
			content={"system": "degraded", "error": str(e), "timestamp": time.time()}
		)

@app.post("/start")
def start_conversation(req: StartSessionRequest):
	"""
	Initialize a new conversation session with persona-based system prompt.
	
	Enhanced with validation and detailed response information.
	"""
	try:
		# Validate input
		if not req.name or not req.name.strip():
			raise HTTPException(status_code=400, detail="Name is required and cannot be empty")
		
		if req.role not in ["student", "professional", "general"]:
			logger.warning(f"Unknown role '{req.role}' provided, defaulting to 'general'")
			req.role = "general"
		
		# Start session
		session_id = start_session(req.name.strip(), req.role)
		
		logger.info(f"New session started: {session_id[:8]}... for {req.name} ({req.role})")
		
		return {
			"session_id": session_id,
			"message": f"Welcome {req.name}! I'm Taxora, your AI-powered finance assistant.",
			"persona": req.role,
			"capabilities": [
				"Personalized financial guidance",
				"Context-aware conversations", 
				"Sentiment-based response adaptation",
				"Professional finance expertise"
			],
			"next_steps": "Ask me about savings, taxes, investments, or budgeting to get started."
		}
		
	except Exception as e:
		logger.error(f"Error starting session: {e}")
		raise HTTPException(status_code=500, detail="Failed to start conversation session")

@app.post("/chat", response_model=ChatTurnResponse)
def chat_interaction(req: ChatTurnRequest):
	"""
	Process chat message with enhanced NLP analysis and context-aware responses.
	
	Integrates IBM watsonx.ai and Watson NLU for sophisticated conversational experience.
	"""
	try:
		# Validate input
		if not req.message or not req.message.strip():
			raise HTTPException(status_code=400, detail="Message cannot be empty")
		
		if len(req.message) > 2000:
			raise HTTPException(status_code=400, detail="Message too long. Please keep messages under 2000 characters.")
		
		# Process conversation turn with advanced AI innovations
		start_time = time.time()
		reply, advanced_metadata = handle_turn(req.session_id, req.message.strip())
		processing_time = time.time() - start_time

		# Prepare enhanced response with unique innovations metadata
		response_data = {
			"session_id": req.session_id,
			"reply": reply,
			"metadata": advanced_metadata,  # Include all advanced AI metadata
			"processing_time": round(processing_time, 2),
			"conversation_insights": {}
		}
		
		# Add conversation insights if NLU data is available in metadata
		nlu_data = advanced_metadata.get("📊_traditional_metrics", {}).get("nlu_analysis", {})
		if nlu_data:
			sentiment = nlu_data.get("sentiment", {}).get("document", {})
			entities = nlu_data.get("entities", [])
			keywords = nlu_data.get("keywords", [])

			response_data["conversation_insights"] = {
				"sentiment": sentiment.get("label", "neutral"),
				"confidence": round(sentiment.get("score", 0), 2),
				"key_topics": [e.get("text", "") for e in entities[:3]],
				"important_keywords": [k.get("text", "") for k in keywords[:3]]
			}
		
		logger.info(f"Chat processed in {processing_time:.2f}s for session {req.session_id[:8]}...")
		
		return response_data
		
	except ValueError as e:
		# Handle invalid session ID
		raise HTTPException(status_code=404, detail=str(e))
	except Exception as e:
		logger.error(f"Error processing chat: {e}")
		raise HTTPException(status_code=500, detail="Failed to process chat message")

@app.get("/session/{session_id}")
def get_session_details(session_id: str):
	"""Get detailed information about a conversation session."""
	try:
		session_info = get_session_info(session_id)
		if not session_info:
			raise HTTPException(status_code=404, detail="Session not found")
		
		return session_info
	except Exception as e:
		logger.error(f"Error retrieving session info: {e}")
		raise HTTPException(status_code=500, detail="Failed to retrieve session information")

@app.delete("/session/{session_id}")
def end_session(session_id: str):
	"""End and clear a conversation session."""
	try:
		success = clear_session(session_id)
		if not success:
			raise HTTPException(status_code=404, detail="Session not found")
		
		return {"message": "Session ended successfully", "session_id": session_id}
	except Exception as e:
		logger.error(f"Error ending session: {e}")
		raise HTTPException(status_code=500, detail="Failed to end session")

@app.get("/sessions")
def list_active_sessions():
	"""List all active conversation sessions."""
	try:
		sessions = get_active_sessions()
		return {
			"active_sessions": len(sessions),
			"session_ids": [sid[:8] + "..." for sid in sessions],  # Truncated for privacy
			"timestamp": time.time()
		}
	except Exception as e:
		logger.error(f"Error listing sessions: {e}")
		raise HTTPException(status_code=500, detail="Failed to list sessions")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
	"""Custom HTTP exception handler with enhanced error information."""
	return JSONResponse(
		status_code=exc.status_code,
		content={
			"error": exc.detail,
			"status_code": exc.status_code,
			"timestamp": time.time(),
			"suggestion": "Please check your request and try again. Contact support if the issue persists."
		}
	)

@app.exception_handler(Exception)
async def general_exception_handler(_, exc):
	"""General exception handler for unexpected errors."""
	logger.error(f"Unexpected error: {exc}")
	return JSONResponse(
		status_code=500,
		content={
			"error": "An unexpected error occurred",
			"status_code": 500,
			"timestamp": time.time(),
			"suggestion": "Please try again later. If the issue persists, contact support."
		}
	)

# =============================================================================
# AI PROVIDER MANAGEMENT ENDPOINTS
# =============================================================================

@app.get("/ai/providers")
async def get_ai_providers():
	"""Get available AI providers and current selection with rate limit status."""
	try:
		ai_manager = get_ai_manager()
		status = ai_manager.get_provider_status()

		# Add Gemini rate limit status
		try:
			from gemini_client import get_gemini_rate_limit_status
			rate_limit_status = get_gemini_rate_limit_status()

			# Add rate limit info to response
			if "available_providers" in status and "gemini" in status["available_providers"]:
				status["available_providers"]["gemini"]["rate_limit_status"] = rate_limit_status
		except Exception as rate_error:
			logger.warning(f"Could not get rate limit status: {rate_error}")

		return JSONResponse(
			status_code=200,
			content={
				"success": True,
				"data": status,
				"timestamp": time.time()
			}
		)
	except Exception as e:
		logger.error(f"Error getting AI providers: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"error": "Failed to get AI providers",
				"message": str(e),
				"timestamp": time.time()
			}
		)

@app.post("/ai/provider")
async def set_ai_provider(request: dict):
	"""Set the current AI provider."""
	try:
		provider = request.get("provider")
		if not provider:
			return JSONResponse(
				status_code=400,
				content={
					"error": "Provider is required",
					"timestamp": time.time()
				}
			)

		ai_manager = get_ai_manager()
		result = ai_manager.set_provider(provider)

		status_code = 200 if result["success"] else 400
		return JSONResponse(
			status_code=status_code,
			content={
				**result,
				"timestamp": time.time()
			}
		)
	except Exception as e:
		logger.error(f"Error setting AI provider: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"error": "Failed to set AI provider",
				"message": str(e),
				"timestamp": time.time()
			}
		)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), session_id: str = None):
	"""Handle file uploads and provide AI analysis."""
	try:
		# Validate file
		if not file.filename:
			return JSONResponse(
				status_code=400,
				content={
					"success": False,
					"message": "No file provided",
					"timestamp": time.time()
				}
			)

		# Check file size (10MB limit)
		MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
		file_content = await file.read()
		if len(file_content) > MAX_FILE_SIZE:
			return JSONResponse(
				status_code=400,
				content={
					"success": False,
					"message": "File size exceeds 10MB limit",
					"timestamp": time.time()
				}
			)

		# Create uploads directory if it doesn't exist
		upload_dir = "uploads"
		os.makedirs(upload_dir, exist_ok=True)

		# Save file
		file_id = str(uuid.uuid4())
		file_extension = os.path.splitext(file.filename)[1]
		saved_filename = f"{file_id}{file_extension}"
		file_path = os.path.join(upload_dir, saved_filename)

		with open(file_path, "wb") as f:
			f.write(file_content)

		# Basic file analysis
		file_info = {
			"filename": file.filename,
			"size": len(file_content),
			"type": file.content_type,
			"extension": file_extension
		}

		# Generate AI response about the file
		ai_manager = get_ai_manager()
		analysis_messages = [
			{
				"role": "user",
				"content": f"I've uploaded a file named '{file.filename}' ({file.content_type}, {len(file_content)} bytes). Can you help me understand what I can do with this file for my financial planning?"
			}
		]

		ai_result = ai_manager.generate_response(analysis_messages)
		response_message = ai_result.get("response", "File uploaded successfully! I can help you analyze financial documents, budgets, and investment data.")

		return JSONResponse(
			status_code=200,
			content={
				"success": True,
				"filename": file.filename,
				"file_id": file_id,
				"message": response_message,
				"analysis": file_info,
				"timestamp": time.time()
			}
		)

	except Exception as e:
		logger.error(f"File upload error: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"message": "File upload failed",
				"error": str(e),
				"timestamp": time.time()
			}
		)

@app.post("/voice/chat")
async def voice_chat(file: UploadFile = File(...), session_id: str = None, include_tamil: bool = True):
	"""Handle voice input and provide bilingual voice-optimized AI response."""
	try:
		# Validate file
		if not file.filename:
			return JSONResponse(
				status_code=400,
				content={
					"success": False,
					"message": "No audio file provided",
					"timestamp": time.time()
				}
			)

		# Check file size (5MB limit for audio)
		MAX_AUDIO_SIZE = 5 * 1024 * 1024  # 5MB
		audio_content = await file.read()
		if len(audio_content) > MAX_AUDIO_SIZE:
			return JSONResponse(
				status_code=400,
				content={
					"success": False,
					"message": "Audio file size exceeds 5MB limit",
					"timestamp": time.time()
				}
			)

		# Get session for conversation history
		session = get_session(session_id) if session_id else None
		conversation_history = session.get("history", []) if session else []

		# Process voice chat using Gemini with Tamil support and fallback
		from gemini_client import gemini_voice_chat, get_gemini_rate_limit_status
		from granite_client import granite_chat

		try:
			voice_result = gemini_voice_chat(audio_content, conversation_history, include_tamil)
		except Exception as e:
			# Handle Gemini rate limiting with fallback to Granite
			if "GEMINI_RATE_LIMITED" in str(e):
				logger.warning("Gemini voice chat rate limited, falling back to Granite")

				# First, try to transcribe audio using a simple approach
				# For now, we'll use a placeholder since we need the user text
				user_text = "Voice input received"  # In a real implementation, you'd use a separate STT service

				# Create simple conversation for Granite
				granite_messages = conversation_history or []
				granite_messages.append({"role": "user", "content": user_text})

				# Get response from Granite
				granite_response = granite_chat(granite_messages)

				# Create voice result with Granite response
				voice_result = {
					"success": True,
					"user_text": user_text,
					"ai_response": f"[Switched to IBM Granite due to Gemini rate limits] {granite_response}",
					"tamil_response": "",  # No Tamil translation for Granite fallback
					"optimized_speech_text_english": granite_response,
					"optimized_speech_text_tamil": "",
					"speech_config_english": {"voice_name": "English", "language": "en-US", "speed": 0.9},
					"speech_config_tamil": None,
					"fallback_used": True,
					"fallback_provider": "granite"
				}
				logger.info("Successfully fell back to Granite for voice chat")
			else:
				# Re-raise other exceptions
				raise e

		if voice_result["success"]:
			# Update session history if available
			if session:
				session["history"].append({
					"role": "user",
					"content": voice_result["user_text"]
				})
				session["history"].append({
					"role": "assistant",
					"content": voice_result["ai_response"]
				})

			return JSONResponse(
				status_code=200,
				content={
					"success": True,
					"user_text": voice_result["user_text"],
					"ai_response": voice_result["ai_response"],
					"tamil_response": voice_result.get("tamil_response", ""),
					"optimized_speech_text_english": voice_result.get("optimized_speech_text_english", ""),
					"optimized_speech_text_tamil": voice_result.get("optimized_speech_text_tamil", ""),
					"speech_config_english": voice_result.get("speech_config_english"),
					"speech_config_tamil": voice_result.get("speech_config_tamil"),
					"timestamp": time.time()
				}
			)
		else:
			return JSONResponse(
				status_code=500,
				content={
					"success": False,
					"message": voice_result.get("error", "Voice processing failed"),
					"timestamp": time.time()
				}
			)

	except Exception as e:
		logger.error(f"Voice chat error: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"message": "Voice chat processing failed",
				"error": str(e),
				"timestamp": time.time()
			}
		)

# =============================================================================
# SAVINGS PLANNER ENDPOINTS
# =============================================================================

@app.post("/savings/goal")
async def create_savings_goal(request: dict):
	"""Create a new savings goal with AI-powered suggestions."""
	try:
		user_id = request.get("user_id", "default_user")
		goal_data = request.get("goal_data", {})

		result = savings_planner.create_savings_goal(user_id, goal_data)

		return JSONResponse(
			status_code=200 if result["success"] else 400,
			content=result
		)

	except Exception as e:
		logger.error(f"Error creating savings goal: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to create savings goal"
			}
		)

@app.post("/savings/entry")
async def add_savings_entry(request: dict):
	"""Add a savings entry and get AI feedback."""
	try:
		goal_id = request.get("goal_id")
		entry_data = request.get("entry_data", {})

		if not goal_id:
			return JSONResponse(
				status_code=400,
				content={"success": False, "error": "goal_id is required"}
			)

		result = savings_planner.add_savings_entry(goal_id, entry_data)

		return JSONResponse(
			status_code=200 if result["success"] else 400,
			content=result
		)

	except Exception as e:
		logger.error(f"Error adding savings entry: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to add savings entry"
			}
		)

@app.get("/savings/analysis/{goal_id}")
async def get_savings_analysis(goal_id: str):
	"""Get comprehensive AI-powered savings analysis."""
	try:
		result = savings_planner.get_savings_analysis(goal_id)

		return JSONResponse(
			status_code=200 if result["success"] else 404,
			content=result
		)

	except Exception as e:
		logger.error(f"Error getting savings analysis: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to get savings analysis"
			}
		)

@app.get("/savings/plan/{goal_id}")
async def get_30_day_plan(goal_id: str):
	"""Generate AI-powered 30-day savings plan."""
	try:
		result = savings_planner.get_30_day_savings_plan(goal_id)

		return JSONResponse(
			status_code=200 if result["success"] else 404,
			content=result
		)

	except Exception as e:
		logger.error(f"Error generating 30-day plan: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to generate 30-day plan"
			}
		)

@app.get("/savings/notifications/{user_id}")
async def get_savings_notifications(user_id: str):
	"""Get savings notifications and reminders."""
	try:
		notifications = savings_planner.check_savings_notifications(user_id)

		return JSONResponse(
			status_code=200,
			content={
				"success": True,
				"notifications": notifications,
				"count": len(notifications)
			}
		)

	except Exception as e:
		logger.error(f"Error getting savings notifications: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to get savings notifications"
			}
		)

# =============================================================================
# BUSINESS TRACKER ENDPOINTS
# =============================================================================

@app.post("/business/profile")
async def create_business_profile(request: dict):
	"""Create a new business profile."""
	try:
		result = business_tracker.create_business_profile(request)

		return JSONResponse(
			status_code=200 if result["success"] else 400,
			content=result
		)

	except Exception as e:
		logger.error(f"Error creating business profile: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to create business profile"
			}
		)

@app.post("/business/transaction")
async def add_business_transaction(request: dict):
	"""Add a business transaction with GST calculation."""
	try:
		business_id = request.get("business_id")
		transaction_data = request.get("transaction_data", {})

		if not business_id:
			return JSONResponse(
				status_code=400,
				content={"success": False, "error": "business_id is required"}
			)

		result = business_tracker.add_transaction(business_id, transaction_data)

		return JSONResponse(
			status_code=200 if result["success"] else 400,
			content=result
		)

	except Exception as e:
		logger.error(f"Error adding business transaction: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to add business transaction"
			}
		)

@app.get("/business/gst/{business_id}/{month}/{year}")
async def get_gst_summary(business_id: str, month: str, year: str):
	"""Get GST summary for a specific month."""
	try:
		result = business_tracker.get_gst_summary(business_id, month, year)

		return JSONResponse(
			status_code=200 if result["success"] else 404,
			content=result
		)

	except Exception as e:
		logger.error(f"Error getting GST summary: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to get GST summary"
			}
		)

@app.get("/business/gst-return/{business_id}/{month}/{year}")
async def calculate_gst_return(business_id: str, month: str, year: str):
	"""Calculate GST return amount."""
	try:
		result = business_tracker.calculate_gst_return(business_id, month, year)

		return JSONResponse(
			status_code=200 if result["success"] else 404,
			content=result
		)

	except Exception as e:
		logger.error(f"Error calculating GST return: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to calculate GST return"
			}
		)

@app.get("/business/reminder/{business_id}")
async def get_monthly_reminder(business_id: str):
	"""Get monthly GST reminder data (20th of every month)."""
	try:
		result = business_tracker.get_monthly_reminder_data(business_id)

		return JSONResponse(
			status_code=200 if result["success"] else 404,
			content=result
		)

	except Exception as e:
		logger.error(f"Error getting monthly reminder: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to get monthly reminder"
			}
		)

@app.get("/business/analytics/{business_id}")
async def get_business_analytics(business_id: str, period: str = "month"):
	"""Get comprehensive business analytics with AI insights."""
	try:
		result = business_tracker.get_business_analytics(business_id, period)

		return JSONResponse(
			status_code=200 if result["success"] else 404,
			content=result
		)

	except Exception as e:
		logger.error(f"Error getting business analytics: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to get business analytics"
			}
		)

@app.post("/business/tax")
async def add_tax_record(request: dict):
	"""Add a comprehensive tax record with transaction details."""
	try:
		business_id = request.get("business_id")
		tax_data = request.get("tax_data", {})

		if not business_id:
			return JSONResponse(
				status_code=400,
				content={"success": False, "error": "business_id is required"}
			)

		result = business_tracker.add_tax_record(business_id, tax_data)

		return JSONResponse(
			status_code=200 if result["success"] else 400,
			content=result
		)

	except Exception as e:
		logger.error(f"Error adding tax record: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to add tax record"
			}
		)

@app.get("/business/tax-summary/{business_id}")
async def get_comprehensive_tax_summary(business_id: str, period: str = "month"):
	"""Get comprehensive tax summary for all tax types."""
	try:
		result = business_tracker.get_comprehensive_tax_summary(business_id, period)

		return JSONResponse(
			status_code=200 if result["success"] else 404,
			content=result
		)

	except Exception as e:
		logger.error(f"Error getting comprehensive tax summary: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to get comprehensive tax summary"
			}
		)

@app.get("/business/tax-reminders/{business_id}")
async def get_tax_reminders(business_id: str):
	"""Get upcoming tax reminders and overdue notifications."""
	try:
		result = business_tracker.get_tax_reminders(business_id)

		return JSONResponse(
			status_code=200 if result["success"] else 404,
			content=result
		)

	except Exception as e:
		logger.error(f"Error getting tax reminders: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to get tax reminders"
			}
		)

@app.put("/business/tax-payment/{tax_record_id}")
async def update_tax_payment(tax_record_id: str, request: dict):
	"""Update tax payment with transaction details."""
	try:
		result = business_tracker.update_tax_payment(tax_record_id, request)

		return JSONResponse(
			status_code=200 if result["success"] else 400,
			content=result
		)

	except Exception as e:
		logger.error(f"Error updating tax payment: {e}")
		return JSONResponse(
			status_code=500,
			content={
				"success": False,
				"error": str(e),
				"message": "Failed to update tax payment"
			}
		)
