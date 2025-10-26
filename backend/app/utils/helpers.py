"""
Helper utilities for the certificate verifier application.
"""
from flask import jsonify
from typing import Any, Dict, Optional
from app.core.constants import StatusCode


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = StatusCode.OK
) -> tuple:
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        "success": True,
        "message": message
    }
    
    if data is not None:
        if isinstance(data, dict):
            response.update(data)
        else:
            response["data"] = data
    
    return jsonify(response), status_code


def error_response(
    message: str = "An error occurred",
    error_details: Optional[str] = None,
    status_code: int = StatusCode.BAD_REQUEST
) -> tuple:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        error_details: Additional error details
        status_code: HTTP status code
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        "success": False,
        "error": message
    }
    
    if error_details:
        response["details"] = error_details
    
    return jsonify(response), status_code


def validate_required_fields(data: Dict, required_fields: list) -> Optional[str]:
    """
    Validate that all required fields are present in the data.
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        
    Returns:
        str or None: Error message if validation fails, None if success
    """
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return f"Missing required field(s): {', '.join(missing_fields)}"
    
    return None


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        str: Formatted file size (e.g., "5.2 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing potentially dangerous characters.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    import re
    # Remove any non-alphanumeric characters except dots, dashes, and underscores
    return re.sub(r'[^\w\s.-]', '', filename).strip()


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def is_valid_enrollment_number(enrollment_number: str) -> bool:
    """
    Validate enrollment number format.
    
    Args:
        enrollment_number: Enrollment number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not enrollment_number:
        return False
    
    # Basic validation: alphanumeric, 4-20 characters
    import re
    return bool(re.match(r'^[A-Za-z0-9]{4,20}$', enrollment_number.strip()))


def extract_field_safely(data: Dict, key: str, default: Any = None) -> Any:
    """
    Safely extract a field from dictionary with default value.
    
    Args:
        data: Dictionary
        key: Key to extract
        default: Default value if key not found
        
    Returns:
        Any: Value from dictionary or default
    """
    value = data.get(key, default)
    
    # Convert empty strings to None
    if isinstance(value, str) and value.strip() == "":
        return default
    
    return value
