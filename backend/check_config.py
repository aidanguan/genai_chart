"""检查配置加载"""
from app.config import get_settings

settings = get_settings()
print(f"API KEY: {settings.AIHUBMIX_API_KEY[:25]}...")
print(f"Base URL: {settings.AIHUBMIX_BASE_URL}")
print(f"Model Recommend: {settings.AIHUBMIX_MODEL_RECOMMEND}")
print(f"Model Extract: {settings.AIHUBMIX_MODEL_EXTRACT}")
print(f"ALLOWED_ORIGINS: {settings.ALLOWED_ORIGINS}")
print(f"allowed_origins_list: {settings.allowed_origins_list}")
