from app.core.config import settings
import openai
import json
import logging
import re
import os
import httpx
import requests

logger = logging.getLogger(__name__)

# --- Shared Utilities ---

def _clear_proxy_env_vars():
    """Clear proxy environment variables to avoid interference."""
    for var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
        os.environ.pop(var, None)

def _determine_base_url() -> str | None:
    """Determine API base URL (auto-detect OpenRouter via key prefix, or use OPENAI_BASE_URL)."""
    if settings.OPENAI_BASE_URL:
        return settings.OPENAI_BASE_URL.strip()
    key = settings.OPENAI_API_KEY or ""
    if isinstance(key, str) and key.startswith("sk-or-"):
        return "https://openrouter.ai/api/v1"
    return None

def _using_openrouter() -> bool:
    base = _determine_base_url()
    return bool(base and "openrouter.ai" in base.lower())

def _model_id() -> str:
    """Return appropriate model identifier depending on provider."""
    # Default OpenAI model
    default_model = "gpt-4o-mini"
    # OpenRouter model identifier for OpenAI's gpt-4o-mini
    or_model = "openai/gpt-4o-mini"
    return or_model if _using_openrouter() else default_model

def _init_openai_client() -> openai.OpenAI:
    """Initialize OpenAI/OpenRouter client with consistent configuration."""
    if not settings.OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API key is required. Please configure OPENAI_API_KEY environment variable."
        )
    _clear_proxy_env_vars()
    base_url = _determine_base_url()
    return openai.OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=base_url,
        http_client=httpx.Client()
    )

def _clean_json_response(response_text: str) -> dict:
    """Clean and parse JSON response from OpenAI, handling markdown fences."""
    response_text = response_text.strip()
    if response_text.startswith('```json'):
        response_text = response_text[7:]
    if response_text.endswith('```'):
        response_text = response_text[:-3]
    return json.loads(response_text.strip())

def _validate_extracted_fields(result: dict) -> dict:
    """Validate and clean extracted fields, replacing empty/invalid values with None."""
    validated = {}
    for key, value in result.items():
        if value is None or value == "" or (isinstance(value, str) and value.strip().lower() == 'null'):
            validated[key] = None
        elif isinstance(value, str):
            validated[key] = value.strip()
        elif isinstance(value, (int, float)):
            # Handle numerical values (SGPA, CGPA, etc.)
            validated[key] = str(value)
        elif isinstance(value, list):
            # Handle subjects array
            validated[key] = value if value else None
        else:
            validated[key] = str(value) if value else None
    return validated

# --- AI Extraction ---

def extract_fields_with_ai(ocr_text: str) -> dict:
    """
    AI-powered field extraction using OpenAI API.
    Returns structured tabular data for certificate information.
    STRICTLY REQUIRES OpenAI API key - no fallback to pattern matching.
    """
    try:
        client = _init_openai_client()

        prompt = f"""
You are an AI assistant specialized in extracting structured information from university/college certificates, academic transcripts, and examination results.

Analyze the following text and return ONLY a JSON object with these fields:

{{
    "student_name": "...",
    "enrollment_number": "...",
    "degree": "...",
    "branch": "...",
    "university_name": "...",
    "graduation_date": "DD/MM/YYYY",
    "date_of_birth": "DD/MM/YYYY",
    "grade": "numerical value",
    "certificate_type": "...",
    "semester": "...",
    "academic_year": "...",
    "sgpa": "numerical value",
    "cgpa": "numerical value",
    "subjects": [{{"subject_code": "...", "subject_name": "...", "grade": "...", "credits": "..."}}],
    "total_credits": "...",
    "earned_credits": "..."
}}

CRITICAL RULES:
1. Return ONLY valid JSON — no extra text.
2. Missing fields → set to null.
3. Clean and format all text.
4. Extract embedded patterns (e.g., "Enrollment No : 231B225").
5. Prioritize numerical grades (6.1, 8.5).
6. Extract subjects as array of objects with code, name, grade, credits.
7. Format dates strictly as DD/MM/YYYY.

Text to analyze:
{ocr_text}
        """.strip()

        response = client.chat.completions.create(
            model=_model_id(),
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=1500
        )

        raw_response = response.choices[0].message.content
        parsed = _clean_json_response(raw_response)
        validated_result = _validate_extracted_fields(parsed)

        logger.info(f"AI extraction completed successfully - extracted {sum(1 for v in validated_result.values() if v)} fields")
        return validated_result

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {str(e)}\nRaw: {raw_response}")
        raise ValueError(f"AI response was not valid JSON: {str(e)}")
    except Exception as e:
        logger.error(f"OpenAI extraction failed: {str(e)}")
        raise RuntimeError(f"AI-powered extraction failed: {str(e)}")

# --- AI Summary Generation ---

def generate_ai_summary(extracted_fields: dict) -> str:
    """
    Generate AI-powered summary using OpenAI API.
    Creates a concise, professional summary of the certificate.
    STRICTLY REQUIRES OpenAI API key.
    """
    try:
        client = _init_openai_client()

        # Build summary context (excluding 'subjects' for brevity)
        fields_summary = "\n".join([
            f"{key.replace('_', ' ').title()}: {value}"
            for key, value in extracted_fields.items()
            if value and value != "null" and key != "subjects"
        ])

        prompt = f"""
You are an AI assistant that creates concise, professional summaries of academic certificates.

Based on this information, create a SINGLE LINE summary (max 200 chars) including:
- Student name
- Degree/Branch
- University
- Key dates (if available)
- Enrollment number
- Academic performance (CGPA/SGPA)

Extracted Information:
{fields_summary}

Requirements:
1. One line only.
2. Professional tone.
3. Order: Name → Degree → University → Performance.
4. Dates: DD/MM/YYYY.
5. Suitable for table display.
6. NO markdown or explanations — just the text.

Examples:
- "Prashant Singh - B.Tech CSE from Jaypee University (CGPA: 6.1)"
- "Semester 1 Result: John Doe - B.E. Electronics (SGPA: 8.2)"

Return ONLY the summary text.
        """.strip()

        response = client.chat.completions.create(
            model=_model_id(),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=200
        )

        summary = response.choices[0].message.content.strip()
        logger.info("AI summary generated successfully")
        return summary

    except Exception as e:
        logger.error(f"AI summary generation failed: {str(e)}")
        raise RuntimeError(f"AI-powered summary generation failed: {str(e)}")

# --- Fallback Extraction (Regex-based) ---

def extract_fields_fallback(ocr_text: str) -> dict:
    """
    Fallback field extraction using pattern matching when OpenAI API is not available.
    Basic regex-based extraction for common certificate fields.
    """
    try:
        result = {}

        patterns = {
            'student_name': [
                r'Student\s+Name[:\s]+([A-Za-z\s]+)',
                r'Name[:\s]+([A-Za-z\s]+)',
                r'Candidate\s+Name[:\s]+([A-Za-z\s]+)'
            ],
            'enrollment_number': [
                r'Enrollment\s+No[:\s]+([A-Za-z0-9]+)',
                r'Enroll\s+No[:\s]+([A-Za-z0-9]+)',
                r'Enrollment[:\s]+([A-Za-z0-9]+)'
            ],
            'degree': [
                r'(B\.Tech|B\.E\.|M\.Tech|B\.Sc|M\.Sc|B\.A|M\.A)',
                r'Degree[:\s]+([A-Za-z\s\.]+)'
            ],
            'university_name': [
                r'University[:\s]+([A-Za-z\s&\.]+)',
                r'Institution[:\s]+([A-Za-z\s&\.]+)'
            ],
            'cgpa': [
                r'CGPA[:\s]+([0-9\.]+)',
                r'SGPA[:\s]+([0-9\.]+)',
                r'Grade[:\s]+([0-9\.]+)'
            ]
        }

        for field, regex_list in patterns.items():
            for pattern in regex_list:
                match = re.search(pattern, ocr_text, re.IGNORECASE)
                if match:
                    result[field] = match.group(1).strip()
                    break

        # Fill missing fields with defaults
        default_fields = {
            'branch': None,
            'graduation_date': None,
            'date_of_birth': None,
            'grade': None,
            'certificate_type': 'Certificate',
            'semester': None,
            'academic_year': None,
            'sgpa': None,
            'total_credits': None,
            'earned_credits': None,
            'subjects': []
        }

        for key, default_value in default_fields.items():
            result.setdefault(key, default_value)

        extracted_count = sum(1 for v in result.values() if v)
        logger.info(f"Fallback extraction completed - extracted {extracted_count} fields")
        return result

    except Exception as e:
        logger.error(f"Fallback extraction failed: {str(e)}")
        # Minimal safe structure
        return {key: None for key in default_fields} | {
            'certificate_type': 'Certificate',
            'subjects': []
        }

# --- Fallback Summary ---

def generate_summary_fallback(extracted_fields: dict) -> str:
    """
    Fallback summary generation when OpenAI API is not available.
    Creates a basic summary from extracted fields.
    """
    try:
        parts = []

        if extracted_fields.get('student_name'):
            parts.append(extracted_fields['student_name'])
        if extracted_fields.get('degree'):
            parts.append(extracted_fields['degree'])
        if extracted_fields.get('university_name'):
            parts.append(f"from {extracted_fields['university_name']}")
        if extracted_fields.get('cgpa'):
            parts.append(f"(CGPA: {extracted_fields['cgpa']})")

        if not parts:
            return "Certificate processed successfully (AI features require API key)"

        summary = " - ".join(parts)
        return summary[:197] + "..." if len(summary) > 200 else summary

    except Exception as e:
        logger.error(f"Fallback summary generation failed: {str(e)}")
        return "Certificate processed successfully"

# --- University Database Verification ---

def verify_certificate_with_university(extracted_data: dict) -> dict:
    """
    Verify extracted certificate data against the university database.
    
    Args:
        extracted_data: Dictionary containing extracted certificate fields
        
    Returns:
        Dictionary containing verification results
    """
    try:
        # University portal URL (from environment or fallback to localhost)
        university_base_url = os.getenv('UNIVERSITY_PORTAL_URL', 'http://localhost:3000')
        university_api_url = f"{university_base_url}/api/verify"
        
        # Extract key fields for verification
        student_name = extracted_data.get('student_name', '').strip()
        enrollment_number = extracted_data.get('enrollment_number', '').strip()
        
        if not student_name or not enrollment_number:
            return {
                'student_verified': False,
                'confidence_score': 0.0,
                'message': 'Insufficient data for university verification',
                'matched_student': None,
                'verification_attempted': False
            }
        
        # Prepare verification request
        verification_data = {
            'student_name': student_name,
            'enrollment_number': enrollment_number
        }
        
        logger.info(f"Verifying certificate for: {student_name} (Enrollment: {enrollment_number})")
        
        # Send verification request to university portal
        response = requests.post(
            university_api_url,
            json=verification_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            university_response = response.json()
            
            if university_response.get('success'):
                if university_response.get('verified'):
                    logger.info(f"Certificate verified successfully for {student_name}")
                    return {
                        'student_verified': True,
                        'confidence_score': university_response.get('confidence_score', 1.0),
                        'message': 'Certificate verified against university database',
                        'matched_student': university_response.get('matched_certificate'),
                        'verification_attempted': True,
                        'verification_timestamp': university_response.get('verification_timestamp')
                    }
                else:
                    logger.info(f"Certificate not found in university database for {student_name}")
                    return {
                        'student_verified': False,
                        'confidence_score': 0.0,
                        'message': university_response.get('message', 'Certificate not found in university database'),
                        'matched_student': None,
                        'verification_attempted': True,
                        'searched_for': university_response.get('searched_for')
                    }
            else:
                logger.error(f"University API returned error: {university_response.get('error')}")
                return {
                    'student_verified': False,
                    'confidence_score': 0.0,
                    'message': f"University verification failed: {university_response.get('error')}",
                    'matched_student': None,
                    'verification_attempted': False
                }
        else:
            logger.error(f"University API request failed with status {response.status_code}")
            return {
                'student_verified': False,
                'confidence_score': 0.0,
                'message': f"Unable to connect to university database (HTTP {response.status_code})",
                'matched_student': None,
                'verification_attempted': False
            }
            
    except requests.exceptions.ConnectionError:
        logger.warning("University portal is not accessible - verification skipped")
        return {
            'student_verified': False,
            'confidence_score': 0.0,
            'message': 'University database is currently unavailable',
            'matched_student': None,
            'verification_attempted': False
        }
    except requests.exceptions.Timeout:
        logger.error("University verification request timed out")
        return {
            'student_verified': False,
            'confidence_score': 0.0,
            'message': 'University database verification timed out',
            'matched_student': None,
            'verification_attempted': False
        }
    except Exception as e:
        logger.error(f"University verification failed with error: {str(e)}")
        return {
            'student_verified': False,
            'confidence_score': 0.0,
            'message': f'University verification error: {str(e)}',
            'matched_student': None,
            'verification_attempted': False
        }
