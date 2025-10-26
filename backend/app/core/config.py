import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    def __init__(self) -> None:
        self.DB_URL: str = os.environ.get("DB_URL", "sqlite:///./university.db")
        self.OPENAI_API_KEY: str | None = os.environ.get("OPENAI_API_KEY")
        # Optional: custom base URL for OpenAI-compatible APIs (e.g., OpenRouter)
        self.OPENAI_BASE_URL: str | None = os.environ.get("OPENAI_BASE_URL")
        self.UPLOAD_DIR: str = os.environ.get("UPLOAD_DIR", "./uploads")
        self.MAX_FILE_SIZE: int = int(os.environ.get("MAX_FILE_SIZE", "10485760"))  # 10MB
        self.LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
        self.CORS_ORIGIN: str = os.environ.get("CORS_ORIGIN", "*")
        self.JWT_SECRET: str = os.environ.get("JWT_SECRET", "default-secret-change-in-production")
        self.PORT: int = int(os.environ.get("PORT", "5000"))
        self.HOST: str = os.environ.get("HOST", "0.0.0.0")
        
        # Create upload directory
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        
        # Warn if using default JWT secret
        if self.JWT_SECRET == "default-secret-change-in-production":
            print("WARNING: Using default JWT secret. Set JWT_SECRET environment variable for security.")
        
        # Print AI functionality status
        if self.OPENAI_API_KEY:
            print("âœ“ OpenAI API key configured - AI features enabled")
            # Hint about base URL selection
            if (self.OPENAI_BASE_URL and 'openrouter.ai' in self.OPENAI_BASE_URL.lower()) or (
                isinstance(self.OPENAI_API_KEY, str) and self.OPENAI_API_KEY.startswith('sk-or-')
            ):
                print("Using OpenRouter-compatible base URL and model identifiers")
        else:
            print("âš  WARNING: OpenAI API key not configured - AI features will be disabled")
            print("  Set OPENAI_API_KEY environment variable to enable AI-powered certificate analysis")
    
    def validate(self) -> bool:
        if not self.DB_URL:
            raise ValueError("DB_URL is required")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for AI functionality")
        return True

    def validate_optional(self) -> bool:
        """Optional validation that doesn't require OpenAI API key for basic functionality"""
        if not self.DB_URL:
            raise ValueError("DB_URL is required")
        return True

settings = Settings()
# Only validate required settings, not OpenAI API key for local development
try:
    settings.validate_optional()
except Exception as e:
    print(f"Warning: Configuration validation failed: {e}")
    print("Continuing with basic configuration...")