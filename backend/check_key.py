
from app.core.config import settings
print(f"GEMINI_KEY_PRESENT: {bool(settings.GEMINI_API_KEY)}")
if settings.GEMINI_API_KEY:
    print(f"GEMINI_KEY_Length: {len(settings.GEMINI_API_KEY)}")
