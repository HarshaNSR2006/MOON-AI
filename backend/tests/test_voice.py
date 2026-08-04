from app.voice.manager import voice_manager
from app.voice.settings import voice_settings


def test_voice_settings_defaults() -> None:
    assert voice_settings.wake_word == "moon"
    assert voice_settings.language == "en"
    assert voice_settings.voice_name == "default"
    assert voice_settings.speed == 1.0
    assert voice_settings.stt_engine == "placeholder"
    assert voice_settings.tts_engine == "placeholder"
    assert voice_settings.streaming is True


def test_voice_manager_start_and_stop() -> None:
    state = voice_manager.start()
    assert state["listening"] is True
    assert state["speaking"] is False

    stopped = voice_manager.stop()
    assert stopped["listening"] is False
    assert stopped["speaking"] is False
    assert stopped["wake_word_active"] is False


def test_voice_manager_transcribe_and_handle_transcript_without_execution() -> None:
    transcript = "Hey Moon open VS Code"
    response = voice_manager.transcribe(text=transcript)

    assert response["transcript"] == transcript
    assert response["wake_word_active"] is True

    result = voice_manager.handle_transcript(response["transcript"], execute_command=False)
    assert result["transcript"] == transcript
    assert result["command_text"] == "open vs code"
    assert result["plan"] is None
    assert result["result"] is None
