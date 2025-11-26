"""
配置管理模块
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """应用配置类"""
    
    # AiHubMix LLM配置
    AIHUBMIX_API_KEY: str = ""
    AIHUBMIX_BASE_URL: str = "https://aihubmix.com/v1"
    AIHUBMIX_MODEL_RECOMMEND: str = "gpt-4o-mini"
    AIHUBMIX_MODEL_EXTRACT: str = "gpt-4o-mini"
    AIHUBMIX_TIMEOUT: int = 30
    AIHUBMIX_MAX_RETRIES: int = 3
    
    # 应用配置
    APP_NAME: str = "AI信息图生成系统"
    APP_VERSION: str = "1.0.0"
    DEBUG_MODE: bool = False
    
    # CORS配置
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://localhost:3000"
    
    # API配置
    API_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """获取允许的CORS来源列表"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


def get_settings() -> Settings:
    """获取配置单例 - 每次重新加载以支持热更新"""
    return Settings()
