from functools import wraps
from flask import request, jsonify
import jwt
import logging
from datetime import datetime, timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)

# JWT Secret Key (in production, use a secure secret)
JWT_SECRET = "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"

def generate_token(user_id: int, user_type: str, username: str) -> str:
    """Generate JWT token for user authentication"""
    try:
        payload = {
            'user_id': user_id,
            'user_type': user_type,
            'username': username,
            'exp': datetime.utcnow() + timedelta(days=7)  # Token expires in 7 days
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    except Exception as e:
        logger.error(f"Token generation failed: {str(e)}")
        raise RuntimeError("Token generation failed")

def verify_token(token: str) -> dict:
    """Verify JWT token and return user info"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def require_auth(f):
    """Decorator to require authentication for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Get token from Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                response = jsonify({"error": "Authorization header missing"})
                response.status_code = 401
                return response
            
            # Extract token from "Bearer <token>" format
            if not auth_header.startswith('Bearer '):
                response = jsonify({"error": "Invalid authorization format"})
                response.status_code = 401
                return response
            
            token = auth_header.split(' ')[1]
            user_info = verify_token(token)
            
            # Add user info to kwargs
            kwargs['current_user'] = user_info
            
            return f(*args, **kwargs)
            
        except ValueError as e:
            response = jsonify({"error": str(e)})
            response.status_code = 401
            return response
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            response = jsonify({"error": "Authentication failed"})
            response.status_code = 401
            return response
    
    return decorated_function

def require_user_type(user_types: list):
    """Decorator to require specific user types"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                response = jsonify({"error": "Authentication required"})
                response.status_code = 401
                return response
            
            if current_user.get('user_type') not in user_types:
                response = jsonify({"error": "Insufficient permissions"})
                response.status_code = 403
                return response
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get current user from request (used in routes)"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        return verify_token(token)
    except:
        return None