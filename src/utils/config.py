from sys import platform
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPEN_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview")

    platform: str = Field(default="github", env="PLATFORM")

    # github settings
    github_token: Optional[str] = Field(default=None, env="GITHUB_TOKEN")
    github_webhook_secret: Optional[str] = Field(default=None, env="GITHUB_WEBHOOK_SECRET")

    agent_name: str = Field(default="PR-Reviewer-Bot", env="AGENT_NAME")
    max_files_to_review: int = Field(default=10, env="MAX_FILES_TO_REVIEW")
    max_diff_lines: int = Field(default=500, env="MAX_DIFF_LINES")
    
    # api Settings
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    
    class Config:
        env_file = ".env"

settings = Settings()