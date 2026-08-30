from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..schemas.chat import ChatRequest, ChatResponse, ChatStatusResponse
from ..services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["AI Agricultural Chatbot"])
chat_service = ChatService()


@router.get("/status", response_model=ChatStatusResponse)
def get_chat_engine_status() -> ChatStatusResponse:
    """Returns the live status, active local ML model specs, and zero-API confirmation."""
    return chat_service.get_engine_status()


@router.post("", response_model=ChatResponse)
def chat_with_agri_bot(payload: ChatRequest) -> ChatResponse:
    """Conversational text interface for Sinhala, English, and Tamil agricultural queries."""
    return chat_service.generate_response(
        query=payload.message,
        forced_lang=payload.language,
        session_id=payload.session_id
    )


@router.post("/upload", response_model=ChatResponse)
async def upload_soil_report(
    file: UploadFile = File(...),
    message: Optional[str] = Form("Please analyze this soil report and recommend the best high-yielding crops."),
    language: Optional[str] = Form("auto"),
    session_id: Optional[str] = Form(None)
) -> ChatResponse:
    """
    Ingests and parses laboratory soil test sheets (PDF, CSV, TXT),
    extracts N, P, K, pH parameters, and evaluates them with the trained ML classifier.
    """
    try:
        content_bytes = await file.read()
        return chat_service.process_file_upload(
            file_bytes=content_bytes,
            filename=file.filename or "uploaded_report",
            user_prompt=message,
            session_id=session_id,
            language=language or "auto"
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to process file {file.filename}: {str(exc)}") from exc
