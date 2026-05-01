from sys import platform
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL")

    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash", env="GEMINI_MODEL")

    platform: str = Field(default="github", env="PLATFORM")

    github_token: Optional[str] = Field(default=None, env="GITHUB_TOKEN")
    github_webhook_secret: Optional[str] = Field(default=None, env="GITHUB_WEBHOOK_SECRET")

    gitlab_token: Optional[str] = Field(default=None, env="GITLAB_TOKEN")
    gitlab_url: str = Field(default="https://gitlab.com", env="GITLAB_URL")
    gitlab_webhook_secret: Optional[str] = Field(default=None, env="GITLAB_WEBHOOK_SECRET")

    agent_name: str = Field(default="PR-Reviewer-Bot", env="AGENT_NAME")
    max_files_to_review: int = Field(default=10, env="MAX_FILES_TO_REVIEW")
    max_diff_lines: int = Field(default=500, env="MAX_DIFF_LINES")
    
    allowed_repos_str: str = Field(default="", env="ALLOWED_REPOS")

    @property
    def allowed_repos(self) -> set[str]:
        if not self.allowed_repos_str:
            return set()
        return {repo.strip() for repo in self.allowed_repos_str.split(",") if repo.strip()}

    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    
    class Config:
        env_file = ".env"

settings = Settings()
if settings.google_api_key:
    print(f"DEBUG: Loaded Google API key prefix: {settings.google_api_key[:10]}... (length: {len(settings.google_api_key)})")
else:
    print("DEBUG: Google API key NOT loaded")