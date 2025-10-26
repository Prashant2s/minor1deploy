"""
Application constants for the certificate verifier system.
"""

# File Upload Constants
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'bmp', 'webp'}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = [
    'application/pdf',
    'image/jpeg',
    'image/png',
    'image/tiff',
    'image/bmp',
    'image/webp'
]

# Certificate Status
class CertificateStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# User Types
class UserType:
    STUDENT = "student"
    UNIVERSITY = "university"
    ADMIN = "admin"

# API Response Messages
class ResponseMessages:
    # Success messages
    UPLOAD_SUCCESS = "Certificate uploaded successfully"
    LOGIN_SUCCESS = "Login successful"
    REGISTRATION_SUCCESS = "User registered successfully"
    UPDATE_SUCCESS = "Updated successfully"
    DELETE_SUCCESS = "Deleted successfully"
    
    # Error messages
    UPLOAD_FAILED = "Failed to upload certificate"
    LOGIN_FAILED = "Invalid credentials"
    UNAUTHORIZED = "Unauthorized access"
    NOT_FOUND = "Resource not found"
    INVALID_FILE = "Invalid file type"
    FILE_TOO_LARGE = "File size exceeds limit"
    MISSING_FIELD = "Missing required field"
    DUPLICATE_ENTRY = "Entry already exists"
    PROCESSING_FAILED = "Processing failed"

# HTTP Status Codes (for clarity)
class StatusCode:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_ERROR = 500

# OpenAI Configuration
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.1
OPENAI_MAX_TOKENS = 1500

# Database Configuration
DB_ECHO = False  # Set to True for SQL query logging
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20

# University Portal
UNIVERSITY_PORTAL_TIMEOUT = 10  # seconds
