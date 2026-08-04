from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.schemas.voice import (
    StartVoiceResponse,
    StopVoiceResponse,
    VoiceSettingsResponse,
    VoiceSettingsUpdateRequest,
    VoiceSpeakRequest,
    VoiceTranscribeRequest,
    VoiceTranscribeResponse,
)
from app.voice.manager import voice_manager

router = APIRouter()


@router.post("/start", response_model=StartVoiceResponse)
def start_voice(current_user=Depends(get_current_user)) -> StartVoiceResponse:
    state = voice_manager.start()
    return StartVoiceResponse(**state)


@router.post("/stop", response_model=StopVoiceResponse)
def stop_voice(current_user=Depends(get_current_user)) -> StopVoiceResponse:
    state = voice_manager.stop()
    return StopVoiceResponse(**state)


@router.post("/transcribe", response_model=VoiceTranscribeResponse)
def transcribe_voice(payload: VoiceTranscribeRequest, current_user=Depends(get_current_user)) -> VoiceTranscribeResponse:
    try:
        response = voice_manager.transcribe(
            text=payload.text,
            audio_data=None,
            language=payload.language,
        )
        handle = voice_manager.handle_transcript(
            transcript=response["transcript"],
            conversation_id=payload.conversation_id,
            execute_command=payload.execute_command,
        )
        return VoiceTranscribeResponse(
            transcript=response["transcript"],
            wake_word_active=response["wake_word_active"],
            command_text=handle.get("command_text"),
            plan=handle.get("plan"),
            result=handle.get("result"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/speak")
def speak_voice(payload: VoiceSpeakRequest, current_user=Depends(get_current_user)) -> dict[str, str]:
    try:
        return voice_manager.speak(
            text=payload.text,
            voice=payload.voice,
            language=payload.language,
            speed=payload.speed,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/settings", response_model=VoiceSettingsResponse)
def get_voice_settings(current_user=Depends(get_current_user)) -> VoiceSettingsResponse:
    return VoiceSettingsResponse(**voice_manager.get_settings())


@router.patch("/settings", response_model=VoiceSettingsResponse)
def update_voice_settings(payload: VoiceSettingsUpdateRequest, current_user=Depends(get_current_user)) -> VoiceSettingsResponse:
    updates = payload.model_dump(exclude_none=True)
    try:
        settings = voice_manager.update_settings(updates)
        return VoiceSettingsResponse(**settings)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
