from app.core.config import settings


def test_settings_loads() -> None:
    assert settings.app_name == "MOON AI"
    assert settings.secret_key != ""
    assert settings.database_url.startswith("sqlite")
