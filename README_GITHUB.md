# 🤖💰 Taxora AI Finance Assistant

A comprehensive AI-powered financial management system with multi-provider AI integration, savings planning, business tracking, and intelligent financial advice.

## 🌟 Features

### 🤖 **Multi-AI Provider Support**
- **IBM Granite** (Default) - Local AI with intelligent fallback system
- **Google Gemini** - Advanced AI with Gemini 2.0 Flash
- **Hugging Face** - Open source AI models
- Intelligent provider switching and fallback

### 💰 **Financial Management**
- **AI-Powered Savings Planning** - Personalized strategies and goal tracking
- **Business Expense Tracking** - Tax optimization and analytics
- **Investment Guidance** - AI-driven investment advice
- **Budget Management** - Smart budgeting tools
- **Compound Interest Calculator** - Financial planning tools

### 🎯 **Advanced Features**
- **Role-Based Onboarding** - Personalized user experience
- **Session Management** - Persistent conversation history
- **Voice Integration** - Gemini voice chat with Tamil support
- **Real-time Analytics** - Business insights and reporting
- **Professional UI** - Modern, responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/taxora-ai-finance.git
cd taxora-ai-finance
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the `backend` directory:
```env
# AI Provider Configuration
DEFAULT_AI_PROVIDER=granite
ALLOW_AI_SWITCHING=true

# Google Gemini API (Primary)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY_BACKUP=your_backup_gemini_key_here
GEMINI_MODEL=gemini-2.0-flash

# Hugging Face API
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
HUGGINGFACE_MODEL=gpt2

# IBM Granite Configuration (Local)
GRANITE_USE_LOCAL=true
GRANITE_MODEL_NAME=distilgpt2
GRANITE_DEVICE=cpu
```

### 4. Run the Application
```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Access the Application
- **Main Dashboard**: http://127.0.0.1:8000/static/index.html
- **AI Chat Interface**: http://127.0.0.1:8000/static/chat.html
- **Savings Planner**: http://127.0.0.1:8000/static/savings.html
- **Business Tracker**: http://127.0.0.1:8000/static/business.html

## 🔧 Getting API Keys

### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` file as `GEMINI_API_KEY`

### Hugging Face API
1. Visit [Hugging Face Tokens](https://huggingface.co/settings/tokens)
2. Create a new token
3. Add to `.env` file as `HUGGINGFACE_API_KEY`

## 📁 Project Structure
```
taxora-ai-finance/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── ai_provider_manager.py  # AI routing and management
│   ├── granite_client.py       # IBM Granite integration
│   ├── gemini_client.py        # Google Gemini integration
│   ├── huggingface_client.py   # Hugging Face integration
│   ├── static/                 # Frontend files
│   │   ├── index.html          # Main dashboard
│   │   ├── chat.html           # AI chat interface
│   │   ├── savings.html        # Savings planner
│   │   └── business.html       # Business tracker
│   └── .env                    # Environment configuration
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

## 🧪 Testing

### Verify Installation
```bash
# Test all AI providers
python backend/test_all_providers_final.py

# Test API keys
python backend/test_api_keys.py

# Check system status
curl http://127.0.0.1:8000/api/status
```

## 🚀 Deployment Options

### Local Development
```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Production Deployment
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Heroku Deployment
1. Create `Procfile`:
```
web: cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

## 🔒 Security Notes

- Never commit API keys to the repository
- Use environment variables for all sensitive data
- The `.env` file is included in `.gitignore`
- Consider using secrets management for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **GaneshPrabu** - Lead Developer
- **EswaraKumar** - AI Integration Specialist  
- **Akshya Nethra** - Frontend Developer

## 🙏 Acknowledgments

- IBM Granite for local AI processing
- Google Gemini for advanced AI capabilities
- Hugging Face for open source AI models
- FastAPI for the excellent web framework

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the test files for examples

---

**Built with ❤️ for better financial management through AI**
