from pydantic import BaseModel
from typing import Optional, Dict, List, Any

class StartSessionRequest(BaseModel):
	name: str
	role: str # "student" | "professional" | "other"

class ChatTurnRequest(BaseModel):
	session_id: str
	message: str

class ChatTurnResponse(BaseModel):
	session_id: str
	reply: str
	nlu: Optional[Dict] = None

# AI Provider Management Models
class AIProviderRequest(BaseModel):
	provider: str  # "granite" | "chatgpt"

class AIProviderResponse(BaseModel):
	success: bool
	message: str
	current_provider: str
	previous_provider: Optional[str] = None

class VoiceRequest(BaseModel):
	session_id: str
	audio_data: str  # Base64 encoded audio
	language: Optional[str] = "en-US"

class FileUploadResponse(BaseModel):
	success: bool
	filename: str
	file_id: str
	message: str
	analysis: Optional[Dict] = None
