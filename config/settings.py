from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    alphavantage_api_key: str
    aws_region: str = "us-east-1"
    aws_profile: str | None = None
    model_id: str = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

    class Config:
        env_file = ".env"

settings = Settings()
