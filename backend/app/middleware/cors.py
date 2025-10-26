"""
CORS (Cross-Origin Resource Sharing) middleware.
"""
from flask import request
from app.core.config import settings


def add_cors_headers(response):
    """
    Add CORS headers to response.
    
    In development, allows all origins.
    In production, should be configured with specific origins.
    
    Args:
        response: Flask response object
        
    Returns:
        response: Modified response with CORS headers
    """
    # Get allowed origins from settings
    allowed_origins = settings.CORS_ORIGIN
    
    # Get the origin from request
    origin = request.headers.get('Origin')
    
    # Set CORS headers
    if allowed_origins == '*':
        # Allow all origins (development only)
        response.headers['Access-Control-Allow-Origin'] = '*'
    elif origin and origin in allowed_origins.split(','):
        # Allow specific origin
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    else:
        # Default to first allowed origin or wildcard
        response.headers['Access-Control-Allow-Origin'] = allowed_origins.split(',')[0] if allowed_origins != '*' else '*'
    
    # Set other CORS headers
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
    response.headers['Access-Control-Max-Age'] = '3600'
    
    return response


def handle_preflight():
    """
    Handle OPTIONS preflight requests.
    
    Returns:
        tuple: Empty response with 200 status code
    """
    from flask import make_response
    response = make_response('', 200)
    return add_cors_headers(response)
