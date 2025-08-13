# Taxora - AI-Powered Conversational Finance Assistant

## Overview

Taxora is an advanced conversational AI finance assistant that leverages IBM's cutting-edge generative AI and Watson NLP capabilities to provide natural, fluid, and context-aware financial guidance. The system combines IBM watsonx.ai for intelligent response generation with Watson Natural Language Understanding (NLU) for sentiment analysis and entity extraction, creating a sophisticated conversational experience.

## Key Features

### Conversational NLP Experience
- **IBM watsonx.ai Integration**: Utilizes IBM's Granite foundation models for intelligent, context-aware responses
- **Watson NLP Capabilities**: Advanced sentiment analysis, entity extraction, and keyword identification
- **Adaptive Persona System**: Tailors communication style based on user role (student/professional)
- **Context-Aware Interactions**: Maintains conversation history and adapts responses based on user sentiment

### Professional Finance Guidance
- Personal budgeting and expense management
- Tax optimization strategies
- Investment planning and portfolio guidance
- Savings goal setting and tracking
- Real-time financial analysis and insights

### Technical Architecture
- **Backend**: FastAPI-based REST API with IBM Watson services integration
- **Frontend**: Classic, professional Streamlit interface with responsive design
- **AI Services**: IBM watsonx.ai (Granite models) + Watson NLU
- **Session Management**: Stateful conversation handling with persona adaptation

## Prerequisites

### IBM Cloud Account Setup
1. Create an IBM Cloud account at [cloud.ibm.com](https://cloud.ibm.com)
2. Set up the following services:
   - **IBM watsonx.ai**: For generative AI capabilities
   - **Watson Natural Language Understanding**: For NLP analysis

### Required API Keys and Configuration

#### IBM watsonx.ai Setup
1. Navigate to IBM watsonx.ai in your IBM Cloud dashboard
2. Create a new project or use an existing one
3. Note down your:
   - API Key
   - Project ID
   - Service URL (typically: `https://us-south.ml.cloud.ibm.com`)
   - Model ID (default: `ibm/granite-3-3-8b-instruct`)

#### Watson NLU Setup
1. Create a Watson Natural Language Understanding service instance
2. Generate service credentials
3. Note down your:
   - API Key
   - Service URL (typically: `https://api.us-south.natural-language-understanding.watson.cloud.ibm.com`)

## Installation & Setup

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd taxora

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Edit .env file with your IBM credentials
```

### 3. Configure Environment Variables

Edit the `.env` file with your IBM Cloud credentials:

```env
# IBM watsonx.ai Configuration
WATSONX_APIKEY=your_ibm_cloud_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_MODEL_ID=ibm/granite-3-3-8b-instruct
WATSONX_API_VERSION=2024-10-10

# Watson NLU Configuration
NLU_APIKEY=your_watson_nlu_api_key_here
NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

### Start Backend Server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Application
```bash
cd frontend
streamlit run app.py --server.port 8501
```

### Access the Application
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Endpoints

### Core Endpoints
- `GET /` - Health check
- `POST /start` - Initialize conversation session
- `POST /chat` - Process user messages with NLP analysis

### Request/Response Examples

#### Start Session
```json
POST /start
{
  "name": "John Doe",
  "role": "professional"
}

Response:
{
  "session_id": "uuid-string",
  "message": "Session started for John Doe (professional)."
}
```

#### Chat Interaction
```json
POST /chat
{
  "session_id": "uuid-string",
  "message": "How can I optimize my tax savings?"
}

Response:
{
  "session_id": "uuid-string",
  "reply": "Based on your professional profile, here are key tax optimization strategies...",
  "nlu": {
    "sentiment": {"document": {"label": "neutral"}},
    "entities": [...],
    "keywords": [...]
  }
}
```

## Architecture Overview

### System Components
1. **Frontend Layer**: Classic Streamlit interface with professional styling
2. **API Layer**: FastAPI REST endpoints with request validation
3. **Business Logic**: Session management and persona adaptation
4. **AI Integration**: IBM watsonx.ai and Watson NLU services
5. **Data Layer**: In-memory session storage (production: database)

### Conversation Flow
1. User initiates session with name and role
2. System creates persona-specific system prompt
3. User sends message → Watson NLU analyzes sentiment/entities
4. System updates context with NLP insights
5. IBM watsonx.ai generates contextual response
6. Response delivered with professional formatting

## Development Guidelines

### Code Structure
- `backend/main.py` - FastAPI application and endpoints
- `backend/chat_logic.py` - Conversation management and session handling
- `backend/ibm_clients.py` - IBM Watson service integrations
- `backend/models.py` - Pydantic data models
- `frontend/app.py` - Streamlit interface with classic styling

### Best Practices
- Environment variables for all sensitive configuration
- Proper error handling and logging
- Session-based conversation management
- Responsive, accessible UI design
- Professional tone and styling

## Troubleshooting

### Common Issues
1. **API Key Errors**: Verify IBM Cloud credentials and service access
2. **Connection Timeouts**: Check network connectivity and service URLs
3. **Model Access**: Ensure watsonx.ai project has model access permissions
4. **NLU Limits**: Monitor Watson NLU usage quotas

### Support
For technical support and feature requests, please refer to the IBM Watson documentation or contact your system administrator.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
