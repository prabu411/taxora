# Taxora Setup Guide

## Quick Start

### For Windows Users
1. Double-click `start_taxora.bat`
2. Follow the prompts to configure your IBM Watson API keys
3. The application will start automatically

### For Linux/Mac Users
1. Make the script executable: `chmod +x start_taxora.sh`
2. Run: `./start_taxora.sh`
3. Follow the prompts to configure your IBM Watson API keys

## Manual Setup

### Prerequisites
- Python 3.8 or higher
- IBM Cloud account with watsonx.ai and Watson NLU services

### Step 1: IBM Cloud Setup

#### Create IBM Cloud Account
1. Go to [cloud.ibm.com](https://cloud.ibm.com)
2. Sign up for a free account or log in

#### Set up watsonx.ai
1. In IBM Cloud dashboard, go to "Catalog"
2. Search for "watsonx.ai"
3. Create a new service instance
4. Go to "Manage" → "Access (IAM)" → "API keys"
5. Create a new API key and save it
6. Note your Project ID from the watsonx.ai dashboard

#### Set up Watson NLU
1. In IBM Cloud dashboard, go to "Catalog"
2. Search for "Natural Language Understanding"
3. Create a new service instance
4. Go to service credentials and create new credentials
5. Note the API key and URL

### Step 2: Environment Configuration

1. Navigate to the `backend` directory
2. Copy `.env.example` to `.env`
3. Edit `.env` with your IBM credentials:

```env
# IBM watsonx.ai Configuration
WATSONX_APIKEY=your_actual_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_actual_project_id_here
WATSONX_MODEL_ID=ibm/granite-3-3-8b-instruct
WATSONX_API_VERSION=2024-10-10

# Watson NLU Configuration
NLU_APIKEY=your_actual_nlu_api_key_here
NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com
```

### Step 3: Install Dependencies

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
pip install -r requirements.txt
```

### Step 4: Run the Application

#### Start Backend (Terminal 1)
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend (Terminal 2)
```bash
cd frontend
streamlit run app.py --server.port 8501
```

### Step 5: Access the Application

- **Frontend Interface**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### "Connection refused" errors
- Ensure backend is running on port 8000
- Check firewall settings
- Verify IBM Watson credentials

#### IBM Watson API errors
- Verify API keys are correct
- Check service instance status in IBM Cloud
- Ensure you have sufficient service credits

#### Frontend not loading
- Check if Streamlit is installed: `pip install streamlit`
- Verify backend is running and accessible
- Clear browser cache

### Getting Help

1. Check the application logs in the terminal windows
2. Visit the API documentation at http://localhost:8000/docs
3. Verify your IBM Watson service status in IBM Cloud dashboard

## Features Overview

### Conversational NLP Experience
- **IBM watsonx.ai Integration**: Uses Granite foundation models for intelligent responses
- **Watson NLP Capabilities**: Advanced sentiment analysis and entity extraction
- **Adaptive Persona System**: Tailors communication based on user role
- **Context-Aware Interactions**: Maintains conversation history and context

### Professional Finance Guidance
- Personal budgeting and expense management
- Tax optimization strategies
- Investment planning and portfolio guidance
- Savings goal setting and tracking

### Technical Architecture
- **Backend**: FastAPI with IBM Watson services integration
- **Frontend**: Professional Streamlit interface with classic styling
- **AI Services**: IBM watsonx.ai + Watson NLU
- **Session Management**: Stateful conversation handling

## API Endpoints

### Core Endpoints
- `GET /` - Health check and system information
- `GET /status` - Comprehensive system status
- `POST /start` - Initialize conversation session
- `POST /chat` - Process chat messages with NLP analysis
- `GET /session/{session_id}` - Get session details
- `DELETE /session/{session_id}` - End session
- `GET /sessions` - List active sessions

### Example Usage

#### Start a conversation
```bash
curl -X POST "http://localhost:8000/start" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "role": "professional"}'
```

#### Send a message
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"session_id": "your-session-id", "message": "How can I optimize my taxes?"}'
```

## Security Considerations

- API keys are stored in environment variables
- Session IDs are UUIDs for security
- No sensitive data is logged
- CORS is configured for local development

## Performance Tips

- The system uses in-memory session storage (suitable for development)
- For production, consider implementing database-backed session storage
- Monitor IBM Watson service usage and quotas
- Consider implementing rate limiting for production deployments

## License

This project is licensed under the MIT License - see the LICENSE file for details.
