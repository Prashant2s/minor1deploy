from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import logging

from app.db.session import db_session
from app.db.models import Certificate, ExtractedField, Student, User
from app.services.images import save_and_process_file, is_allowed_file
from app.services.ocr import run_ocr
from app.services.extract import extract_fields_with_ai, generate_ai_summary, verify_certificate_with_university
from app.services.auth import generate_token, require_auth, require_user_type, get_current_user
from app.core.config import settings

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__)

# Authentication endpoints
@api_bp.route("/auth/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'user_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        user_type = data['user_type']
        if user_type not in ['student', 'university']:
            return jsonify({"error": "user_type must be 'student' or 'university'"}), 400
        
        # Check if user already exists
        existing_user = db_session.query(User).filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({"error": "Username or email already exists"}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            user_type=user_type
        )
        user.set_password(data['password'])
        
        # Set user-specific fields
        if user_type == 'student':
            user.student_name = data.get('student_name')
            user.student_reg_no = data.get('student_reg_no')
            user.student_dob = data.get('student_dob')
        elif user_type == 'university':
            user.university_name = data.get('university_name')
            user.university_code = data.get('university_code')
        
        db_session.add(user)
        db_session.commit()
        
        # Generate token
        token = generate_token(user.id, user.user_type, user.username)
        
        return jsonify({
            "message": "User registered successfully",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type
            }
        })
        
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        db_session.rollback()
        return jsonify({"error": "Registration failed"}), 500

@api_bp.route("/auth/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
        
        # Find user by username or email
        user = db_session.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401
        
        if not user.is_active:
            return jsonify({"error": "Account is deactivated"}), 401
        
        # Generate token
        token = generate_token(user.id, user.user_type, user.username)
        
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type
            }
        })
        
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return jsonify({"error": "Login failed"}), 500

@api_bp.route("/auth/me", methods=['GET'])
@require_auth
def get_current_user_info(current_user):
    try:
        user = db_session.query(User).filter(User.id == current_user['user_id']).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type,
                "student_name": user.student_name,
                "student_reg_no": user.student_reg_no,
                "university_name": user.university_name,
                "university_code": user.university_code
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get user info: {str(e)}")
        return jsonify({"error": "Failed to get user info"}), 500

def simple_university_verification(extracted_fields: dict) -> dict:
    """Simple verification logic directly in routes."""
    verification_result = {
        "student_verified": False,
        "enrollment_verified": False,
        "confidence_score": 0.0,
        "matched_student": None
    }
    
    try:
        student_name = extracted_fields.get('student_name')
        enrollment_number = extracted_fields.get('enrollment_number')
        
        if enrollment_number:
            # Try to match by enrollment number
            student = db_session.query(Student).filter(Student.reg_no == enrollment_number).first()
            if student:
                verification_result["student_verified"] = True
                verification_result["enrollment_verified"] = True
                verification_result["confidence_score"] = 0.8
                verification_result["matched_student"] = {
                    "name": student.name
                }
        
        return verification_result
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        return verification_result

@api_bp.route("/certificates/upload", methods=['POST'])
def upload_certificate():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
            
        if not is_allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Allowed: PDF, JPG, JPEG, PNG, TIFF, BMP, WEBP"}), 400

        filename = secure_filename(file.filename)
        upload_path = Path(settings.UPLOAD_DIR)
        file_path = upload_path / filename
        
        processed_path, file_type = save_and_process_file(file.stream, file_path)
        ocr_text = run_ocr(processed_path)
        
        if not ocr_text.strip():
            return jsonify({"error": "No text could be extracted from the certificate. Please ensure the image is clear and readable."}), 400
        
        extracted_fields = extract_fields_with_ai(ocr_text)
        summary = generate_ai_summary(extracted_fields)
        
        # Verify certificate against university database
        verification = verify_certificate_with_university(extracted_fields)
        
        cert = Certificate(
            image_path=str(processed_path), 
            status='processed',
            user_id=None,  # No authentication required
            original_filename=filename
        )
        db_session.add(cert)
        db_session.flush()
        
        # Store extracted fields with proper typing
        for key, value in extracted_fields.items():
            if value and value != "null":
                field = ExtractedField(
                    certificate_id=cert.id, 
                    key=key, 
                    value=str(value), 
                    confidence=0.9,  # High confidence for AI extraction
                    field_type='extracted'
                )
                db_session.add(field)
        
        # Store AI summary
        summary_field = ExtractedField(
            certificate_id=cert.id, 
            key='ai_summary', 
            value=summary, 
            confidence=1.0,
            field_type='ai_summary'
        )
        db_session.add(summary_field)
        
        # Store verification results
        verification_field = ExtractedField(
            certificate_id=cert.id,
            key='verification_result',
            value=str(verification),
            confidence=verification.get('confidence_score', 0.0),
            field_type='verification'
        )
        db_session.add(verification_field)
        db_session.commit()
        
        # Create structured tabular response with enhanced fields
        tabular_data = {
            "student_name": extracted_fields.get("student_name", "-"),
            "enrollment_number": extracted_fields.get("enrollment_number", "-"),
            "degree": extracted_fields.get("degree", "-"),
            "branch": extracted_fields.get("branch", "-"),
            "university_name": extracted_fields.get("university_name", "-"),
            "graduation_date": extracted_fields.get("graduation_date", "-"),
            "date_of_birth": extracted_fields.get("date_of_birth", "-"),
            "grade": extracted_fields.get("grade", "-"),
            "certificate_type": extracted_fields.get("certificate_type", "-"),
            "semester": extracted_fields.get("semester", "-"),
            "academic_year": extracted_fields.get("academic_year", "-"),
            "sgpa": extracted_fields.get("sgpa", "-"),
            "cgpa": extracted_fields.get("cgpa", "-"),
            "total_credits": extracted_fields.get("total_credits", "-"),
            "earned_credits": extracted_fields.get("earned_credits", "-"),
            "subjects": extracted_fields.get("subjects", [])
        }
        
        return jsonify({
            "id": cert.id,
            "file_type": file_type,
            "summary": summary,
            "tabular_data": tabular_data,
            "verification": verification,
            "confidence_score": verification.get('confidence_score', 0.0)
        }), 201
        
    except Exception as e:
        db_session.rollback()
        logger.error(f"Certificate upload failed: {str(e)}")
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

@api_bp.route("/certificates", methods=['GET'])
def list_certificates():
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        
        certs = db_session.query(Certificate).order_by(Certificate.created_at.desc()).limit(limit).offset(offset).all()
        
        result = []
        for cert in certs:
            # Build map of extracted fields for quick lookup
            fields_map = {}
            for f in cert.fields:
                if f.field_type == 'extracted':
                    fields_map[f.key] = f.value
            
            tabular_data = {
                "student_name": fields_map.get("student_name", "-"),
                "degree": fields_map.get("degree", "-"),
                "branch": fields_map.get("branch", "-"),
                "university_name": fields_map.get("university_name", "-"),
                "enrollment_number": fields_map.get("enrollment_number", "-"),
                "sgpa": fields_map.get("sgpa", "-"),
                "cgpa": fields_map.get("cgpa", "-"),
                "semester": fields_map.get("semester", "-"),
                "academic_year": fields_map.get("academic_year", "-")
            }
            
            result.append({
                "id": cert.id,
                "status": cert.status,
                "created_at": cert.created_at.isoformat(),
                "tabular_data": tabular_data
            })
        
        return jsonify({"certificates": result, "count": len(result), "limit": limit, "offset": offset})
        
    except Exception as e:
        logger.error(f"Failed to list certificates: {str(e)}")
        return jsonify({"error": "Failed to fetch certificates"}), 500

@api_bp.route("/certificates/<int:cert_id>", methods=['GET'])
def get_certificate(cert_id: int):
    try:
        cert = db_session.get(Certificate, cert_id)
        if not cert:
            return jsonify({"error": "Certificate not found"}), 404
        
        # Extract structured data from fields
        extracted_fields = {}
        summary = ""
        verification = {}
        
        for field in cert.fields:
            if field.field_type == 'ai_summary':
                summary = field.value
            elif field.field_type == 'verification':
                try:
                    import ast
                    verification = ast.literal_eval(field.value)
                except:
                    verification = {"student_verified": False, "enrollment_verified": False, "confidence_score": 0.0}
            elif field.field_type == 'extracted':
                extracted_fields[field.key] = {"value": field.value, "confidence": field.confidence}
        
        # Create structured tabular data with enhanced fields
        tabular_data = {
            "student_name": extracted_fields.get("student_name", {}).get("value", "-"),
            "enrollment_number": extracted_fields.get("enrollment_number", {}).get("value", "-"),
            "degree": extracted_fields.get("degree", {}).get("value", "-"),
            "branch": extracted_fields.get("branch", {}).get("value", "-"),
            "university_name": extracted_fields.get("university_name", {}).get("value", "-"),
            "graduation_date": extracted_fields.get("graduation_date", {}).get("value", "-"),
            "date_of_birth": extracted_fields.get("date_of_birth", {}).get("value", "-"),
            "grade": extracted_fields.get("grade", {}).get("value", "-"),
            "certificate_type": extracted_fields.get("certificate_type", {}).get("value", "-"),
            "semester": extracted_fields.get("semester", {}).get("value", "-"),
            "academic_year": extracted_fields.get("academic_year", {}).get("value", "-"),
            "sgpa": extracted_fields.get("sgpa", {}).get("value", "-"),
            "cgpa": extracted_fields.get("cgpa", {}).get("value", "-"),
            "total_credits": extracted_fields.get("total_credits", {}).get("value", "-"),
            "earned_credits": extracted_fields.get("earned_credits", {}).get("value", "-"),
            "subjects": extracted_fields.get("subjects", {}).get("value", [])
        }
        
        return jsonify({
            "id": cert.id,
            "status": cert.status,
            "created_at": cert.created_at.isoformat(),
            "summary": summary,
            "tabular_data": tabular_data,
            "verification": verification,
            "field_count": len(extracted_fields)
        })
        
    except Exception as e:
        logger.error(f"Failed to get certificate {cert_id}: {str(e)}")
        return jsonify({"error": "Failed to fetch certificate"}), 500

@api_bp.route("/certificates/<int:cert_id>/image", methods=['GET'])
def get_certificate_image(cert_id: int):
    try:
        cert = db_session.get(Certificate, cert_id)
        if not cert:
            return jsonify({"error": "Certificate not found"}), 404
            
        image_path = Path(cert.image_path)
        if not image_path.exists():
            return jsonify({"error": "Image file not found"}), 404
            
        return send_file(image_path, as_attachment=False)
        
    except Exception as e:
        logger.error(f"Failed to serve image: {str(e)}")
        return jsonify({"error": "Failed to serve image"}), 500

# Download endpoints
@api_bp.route("/certificates/<int:cert_id>/download", methods=['GET'])
def download_certificate_file(cert_id: int):
    """Download the original certificate file (no auth required for demo)."""
    try:
        cert = db_session.query(Certificate).filter(Certificate.id == cert_id).first()
        if not cert:
            return jsonify({"error": "Certificate not found"}), 404
        
        file_path = Path(cert.image_path)
        if not file_path.exists():
            return jsonify({"error": "File not found"}), 404
        
        filename = cert.original_filename or f"certificate_{cert_id}.png"
        return send_file(
            str(file_path),
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        return jsonify({"error": "Download failed"}), 500

@api_bp.route("/certificates/<int:cert_id>/export", methods=['GET'])
def export_certificate_data(cert_id: int):
    """Export certificate data as JSON (no auth required for demo)."""
    try:
        cert = db_session.query(Certificate).filter(Certificate.id == cert_id).first()
        if not cert:
            return jsonify({"error": "Certificate not found"}), 404
        
        # Get all extracted fields
        fields = {}
        for field in cert.fields:
            if field.field_type == 'extracted':
                fields[field.key] = field.value
        
        # Get summary
        summary_field = next((f for f in cert.fields if f.key == 'ai_summary'), None)
        summary = summary_field.value if summary_field else None
        
        # Get verification data
        verification_field = next((f for f in cert.fields if f.key == 'verification'), None)
        verification = verification_field.value if verification_field else None
        
        export_data = {
            "certificate_id": cert.id,
            "created_at": cert.created_at.isoformat(),
            "status": cert.status,
            "summary": summary,
            "extracted_fields": fields,
            "verification": verification
        }
        
        response = jsonify(export_data)
        response.headers['Content-Disposition'] = f'attachment; filename=certificate_{cert_id}_data.json'
        return response
        
    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        return jsonify({"error": "Export failed"}), 500

@api_bp.route("/certificates/<int:cert_id>/reverify", methods=['POST'])
def reverify_certificate(cert_id: int):
    """Re-verify a certificate against the university database."""
    try:
        cert = db_session.query(Certificate).filter(Certificate.id == cert_id).first()
        if not cert:
            return jsonify({"error": "Certificate not found"}), 404
        
        # Get extracted fields from certificate
        extracted_fields = {}
        for field in cert.fields:
            if field.field_type == 'extracted':
                extracted_fields[field.key] = field.value
        
        # Re-verify with university
        verification = verify_certificate_with_university(extracted_fields)
        
        # Update verification field in database
        verification_field = db_session.query(ExtractedField).filter(
            ExtractedField.certificate_id == cert_id,
            ExtractedField.key == 'verification_result'
        ).first()
        
        if verification_field:
            verification_field.value = str(verification)
            verification_field.confidence = verification.get('confidence_score', 0.0)
        else:
            verification_field = ExtractedField(
                certificate_id=cert.id,
                key='verification_result',
                value=str(verification),
                confidence=verification.get('confidence_score', 0.0),
                field_type='verification'
            )
            db_session.add(verification_field)
        
        db_session.commit()
        
        return jsonify({
            "success": True,
            "message": "Certificate re-verified successfully",
            "verification": verification
        })
        
    except Exception as e:
        db_session.rollback()
        logger.error(f"Re-verification failed: {str(e)}")
        return jsonify({"error": f"Re-verification failed: {str(e)}"}), 500

@api_bp.route("/certificates/my-certificates", methods=['GET'])
def get_my_certificates():
    """Get certificates for the current user"""
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        
        query = db_session.query(Certificate)  # Return all certificates since no auth
        certs = query.order_by(Certificate.created_at.desc()).limit(limit).offset(offset).all()
        
        result = []
        for cert in certs:
            summary_field = next((f for f in cert.fields if f.key == 'ai_summary'), None)
            summary = summary_field.value if summary_field else "No summary available"
            
            result.append({
                "id": cert.id,
                "status": cert.status,
                "created_at": cert.created_at.isoformat(),
                "original_filename": cert.original_filename,
                "summary": summary[:200] + "..." if len(summary) > 200 else summary
            })
        
        return jsonify({"certificates": result, "count": len(result), "limit": limit, "offset": offset})
        
    except Exception as e:
        logger.error(f"Failed to get user certificates: {str(e)}")
        return jsonify({"error": "Failed to fetch certificates"}), 500

@api_bp.route("/health", methods=['GET'])
def health_check():
    """Health check endpoint for deployment monitoring."""
    try:
        # Check if OpenAI API key is configured
        api_key_status = "configured" if settings.OPENAI_API_KEY else "missing"
        
        return jsonify({
            "status": "healthy",
            "service": "University Certificate Verifier API",
            "ai_status": api_key_status,
            "version": "1.0.0",
            "features": [
                "AI-powered certificate extraction",
                "OCR text recognition", 
                "Tabular data formatting",
                "University verification",
                "User authentication",
                "File downloads"
            ]
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
