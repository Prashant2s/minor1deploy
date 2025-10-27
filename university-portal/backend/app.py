from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload folder - use /tmp for ephemeral storage in production
UPLOAD_FOLDER = os.environ.get('UPLOAD_DIR', '/tmp/certificates')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create upload folder if it doesn't exist and we have permissions
try:
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    logger.info(f"Upload folder configured: {UPLOAD_FOLDER}")
except Exception as e:
    logger.warning(f"Could not create upload folder: {e}. File uploads will be disabled.")
    UPLOAD_FOLDER = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Certificate database path - use environment variable or fallback
DB_FILE = os.environ.get('DB_FILE', '/tmp/certificates.json')
SOURCE_DB_FILE = '../database/certificates.json'

# Initialize database file if it doesn't exist
if not os.path.exists(DB_FILE):
    try:
        # Try to load from source database first
        if os.path.exists(SOURCE_DB_FILE):
            logger.info(f"Loading initial data from {SOURCE_DB_FILE}")
            with open(SOURCE_DB_FILE, 'r') as source:
                initial_data = json.load(source)
            with open(DB_FILE, 'w') as f:
                json.dump(initial_data, f, indent=2)
            logger.info(f"Database initialized from source: {DB_FILE} with {len(initial_data.get('certificates', []))} certificates")
        else:
            # Create with empty data
            logger.info("Source database not found, creating empty database")
            initial_data = {
                "certificates": [],
                "metadata": {
                    "total_certificates": 0,
                    "last_updated": datetime.utcnow().isoformat() + 'Z',
                    "university_code": "JUET",
                    "university_name": "Jaypee University of Engineering & Technology",
                    "location": "Guna, Madhya Pradesh",
                    "website": "https://juet.ac.in"
                }
            }
            with open(DB_FILE, 'w') as f:
                json.dump(initial_data, f, indent=2)
            logger.info(f"Database initialized: {DB_FILE}")
    except Exception as e:
        logger.error(f"Could not initialize database: {e}")

# Load certificate database
def load_certificates():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading certificates: {e}")
        return {"certificates": [], "metadata": {}}

# Save certificate database
def save_certificates(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving certificates: {e}")
        return False

# Generate next certificate ID
def generate_certificate_id(certificates):
    if not certificates:
        return "JUET001"
    
    max_id = 0
    for cert in certificates:
        cert_id = cert.get('id', '')
        if cert_id.startswith('JUET'):
            try:
                num = int(cert_id[4:])  # Extract number after 'JUET'
                max_id = max(max_id, num)
            except ValueError:
                continue
    
    return f"JUET{str(max_id + 1).zfill(3)}"

@app.route('/')
def home():
    """Redirect to admin login page"""
    return """
    <html>
        <head>
            <meta http-equiv="refresh" content="0; url=/admin.html" />
        </head>
        <body>
            <p>Redirecting to admin portal...</p>
        </body>
    </html>
    """

@app.route('/info')
def info():
    """University portal information page"""
    return """
    <html>
        <head>
            <title>JUET - University Portal</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .header { background: #2E5BBA; color: white; padding: 20px; text-align: center; }
                .content { background: white; padding: 30px; margin: 20px 0; }
                .api-info { background: #e8f4fd; padding: 15px; border-left: 4px solid #2E5BBA; }
                .endpoint { margin: 10px 0; font-family: monospace; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎓 Jaypee University of Engineering & Technology</h1>
                <p>Official Certificate Database Portal</p>
            </div>
            <div class="content">
                <h2>Welcome to JUET Certificate Portal</h2>
                <p>This is the official university database for certificate verification.</p>
                
                <div class="api-info">
                    <h3>📚 Available API Endpoints:</h3>
                    <div class="endpoint"><strong>GET</strong> /api/certificates - Get all certificates</div>
                    <div class="endpoint"><strong>POST</strong> /api/certificates - Upload new certificate</div>
                    <div class="endpoint"><strong>GET</strong> /api/certificates/&lt;enrollment&gt; - Get certificate by enrollment</div>
                    <div class="endpoint"><strong>POST</strong> /api/verify - Verify certificate data</div>
                    <div class="endpoint"><strong>GET</strong> /api/stats - Get university statistics</div>
                    <div class="endpoint"><strong>GET</strong> /health - Health check</div>
                </div>
                
                <p><strong>🔗 Integration:</strong> This portal integrates with the Certificate Verifier at port 5173</p>
                <p><strong>📊 Database:</strong> Contains 5 sample certificate records for testing</p>
            </div>
        </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "JUET University Portal",
        "timestamp": datetime.utcnow().isoformat(),
        "port": 3000
    })

@app.route('/api/certificates', methods=['GET'])
def get_all_certificates():
    """Get all certificates in the database"""
    try:
        data = load_certificates()
        return jsonify({
            "success": True,
            "certificates": data.get("certificates", []),
            "total": len(data.get("certificates", [])),
            "metadata": data.get("metadata", {})
        })
    except Exception as e:
        logger.error(f"Error getting certificates: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/certificates/upload', methods=['POST'])
def upload_certificate():
    """Upload a new certificate with file to the database"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "success": False, 
                "error": "Invalid file type. Only PDF, PNG, JPG, JPEG allowed"
            }), 400
        
        # Get form data
        request_data = {
            'student_name': request.form.get('student_name'),
            'enrollment_number': request.form.get('enrollment_number'),
            'branch': request.form.get('branch'),
            'academic_year': request.form.get('academic_year'),
            'status': request.form.get('status')
        }
        
        if not request_data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Validate required fields (cgpa is now optional)
        required_fields = ['student_name', 'enrollment_number', 'branch', 'academic_year', 'status']
        for field in required_fields:
            if not request_data.get(field):
                return jsonify({
                    "success": False, 
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Load existing data
        data = load_certificates()
        certificates = data.get("certificates", [])
        
        # Get enrollment number
        enrollment = request_data['enrollment_number'].strip()
        
        # Generate certificate data
        cert_id = generate_certificate_id(certificates)
        current_time = datetime.utcnow().isoformat() + 'Z'
        
        # Extract branch abbreviation for certificate number
        branch_abbrev = {
            'Computer Science Engineering': 'CSE',
            'Information Technology': 'IT',
            'Electronics & Communication': 'ECE',
            'Mechanical Engineering': 'ME',
            'Civil Engineering': 'CE',
            'Electrical Engineering': 'EE'
        }.get(request_data['branch'], 'GEN')
        
        # Extract year from academic_year (e.g., "2019-2023" -> "2023")
        try:
            year = request_data['academic_year'].split('-')[-1]
        except:
            year = '2024'
        
        cert_number = f"JUET/{branch_abbrev}/{year}/{cert_id[4:]}"
        
        # Save the certificate file (if upload folder is available)
        saved_filename = None
        if UPLOAD_FOLDER:
            try:
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                saved_filename = f"{enrollment}_{cert_id}.{file_extension}"
                file_path = os.path.join(UPLOAD_FOLDER, saved_filename)
                file.save(file_path)
                logger.info(f"File saved: {saved_filename}")
            except Exception as e:
                logger.warning(f"Could not save file: {e}. Continuing without file storage.")
                saved_filename = None
        
        new_certificate = {
            "id": cert_id,
            "student_name": request_data['student_name'].strip(),
            "enrollment_number": enrollment,
            "registration_number": f"REG{year}{cert_id[4:]}",
            "degree": "Bachelor of Technology",
            "branch": request_data['branch'],
            "university": "Jaypee University of Engineering & Technology",
            "graduation_date": f"{year}-06-15",
            "cgpa": str(request_data.get('cgpa', 'N/A')),
            "academic_year": request_data['academic_year'],
            "certificate_type": "Degree Certificate",
            "issue_date": current_time[:10],
            "certificate_number": cert_number,
            "status": request_data['status'],
            "upload_timestamp": current_time,
            "certificate_file": saved_filename
        }
        
        # Add the new certificate
        certificates.append(new_certificate)
        
        # Update metadata
        metadata = data.get("metadata", {})
        metadata['total_certificates'] = len(certificates)
        metadata['last_updated'] = current_time
        
        data['certificates'] = certificates
        data['metadata'] = metadata
        
        # Save to file
        if save_certificates(data):
            logger.info(f"Certificate added successfully: {enrollment}")
            return jsonify({
                "success": True,
                "message": "Certificate uploaded successfully",
                "certificate": new_certificate
            }), 201
        else:
            return jsonify({
                "success": False,
                "error": "Failed to save certificate to database"
            }), 500
            
    except Exception as e:
        logger.error(f"Error uploading certificate: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/certificates', methods=['POST'])
def add_certificate():
    """Add a new certificate to the database (without file)"""
    try:
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Validate required fields (cgpa is now optional)
        required_fields = ['student_name', 'enrollment_number', 'branch', 'academic_year', 'status']
        for field in required_fields:
            if not request_data.get(field):
                return jsonify({
                    "success": False, 
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Load existing data
        data = load_certificates()
        certificates = data.get("certificates", [])
        
        # Get enrollment number
        enrollment = request_data['enrollment_number'].strip()
        
        # Generate certificate data
        cert_id = generate_certificate_id(certificates)
        current_time = datetime.utcnow().isoformat() + 'Z'
        
        # Extract branch abbreviation for certificate number
        branch_abbrev = {
            'Computer Science Engineering': 'CSE',
            'Information Technology': 'IT',
            'Electronics & Communication': 'ECE',
            'Mechanical Engineering': 'ME',
            'Civil Engineering': 'CE',
            'Electrical Engineering': 'EE'
        }.get(request_data['branch'], 'GEN')
        
        # Extract year from academic_year (e.g., "2019-2023" -> "2023")
        try:
            year = request_data['academic_year'].split('-')[-1]
        except:
            year = '2024'
        
        cert_number = f"JUET/{branch_abbrev}/{year}/{cert_id[4:]}"
        
        new_certificate = {
            "id": cert_id,
            "student_name": request_data['student_name'].strip(),
            "enrollment_number": enrollment,
            "registration_number": f"REG{year}{cert_id[4:]}",
            "degree": "Bachelor of Technology",
            "branch": request_data['branch'],
            "university": "Jaypee University of Engineering & Technology",
            "graduation_date": f"{year}-06-15",
            "cgpa": str(request_data.get('cgpa', 'N/A')),
            "academic_year": request_data['academic_year'],
            "certificate_type": "Degree Certificate",
            "issue_date": current_time[:10],
            "certificate_number": cert_number,
            "status": request_data['status'],
            "upload_timestamp": current_time
        }
        
        # Add the new certificate
        certificates.append(new_certificate)
        
        # Update metadata
        metadata = data.get("metadata", {})
        metadata['total_certificates'] = len(certificates)
        metadata['last_updated'] = current_time
        
        data['certificates'] = certificates
        data['metadata'] = metadata
        
        # Save to file
        if save_certificates(data):
            logger.info(f"Certificate added successfully: {enrollment}")
            return jsonify({
                "success": True,
                "message": "Certificate uploaded successfully",
                "certificate": new_certificate
            }), 201
        else:
            return jsonify({
                "success": False,
                "error": "Failed to save certificate to database"
            }), 500
            
    except Exception as e:
        logger.error(f"Error adding certificate: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/certificates/<enrollment_number>')
def get_certificate_by_enrollment(enrollment_number):
    """Get all certificates for a student by enrollment number"""
    try:
        data = load_certificates()
        certificates = data.get("certificates", [])
        
        # Search for all certificates by enrollment number
        matched_certificates = []
        for cert in certificates:
            if cert.get("enrollment_number", "").lower() == enrollment_number.lower():
                matched_certificates.append(cert)
        
        if matched_certificates:
            return jsonify({
                "success": True,
                "certificates": matched_certificates,
                "total": len(matched_certificates),
                "found": True
            })
        else:
            return jsonify({
                "success": False,
                "message": "No certificates found for this enrollment number",
                "found": False,
                "enrollment_number": enrollment_number
            }), 404
            
    except Exception as e:
        logger.error(f"Error getting certificate by enrollment: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/verify', methods=['POST'])
def verify_certificate():
    """Verify certificate data against university database"""
    try:
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        # Extract verification parameters
        student_name = request_data.get('student_name', '').strip()
        enrollment_number = request_data.get('enrollment_number', '').strip()
        
        if not student_name or not enrollment_number:
            return jsonify({
                "success": False, 
                "error": "student_name and enrollment_number are required"
            }), 400
        
        # Load university database
        data = load_certificates()
        certificates = data.get("certificates", [])
        
        # Helper function to normalize strings for comparison
        def normalize_string(s):
            """Normalize string by removing extra spaces, special chars, and lowercasing"""
            import re
            # Convert to lowercase and strip
            s = s.lower().strip()
            # Remove multiple spaces
            s = re.sub(r'\s+', ' ', s)
            # Remove common special characters that might cause mismatch
            s = re.sub(r'[^a-z0-9\s]', '', s)
            return s
        
        # Normalize input
        normalized_input_name = normalize_string(student_name)
        normalized_input_enrollment = normalize_string(enrollment_number)
        
        logger.info(f"Verification request - Name: '{student_name}' (normalized: '{normalized_input_name}'), Enrollment: '{enrollment_number}' (normalized: '{normalized_input_enrollment}')")
        
        # Search for matching certificate
        matched_certificate = None
        best_match_score = 0
        
        logger.info(f"Searching {len(certificates)} certificates in database")
        
        for cert in certificates:
            cert_name = normalize_string(cert.get("student_name", ""))
            cert_enrollment = normalize_string(cert.get("enrollment_number", ""))
            
            logger.debug(f"Comparing with DB cert - Name: '{cert.get('student_name', '')}' (normalized: '{cert_name}'), Enrollment: '{cert.get('enrollment_number', '')}' (normalized: '{cert_enrollment}')")
            
            # Check for exact match on enrollment (most reliable)
            if cert_enrollment == normalized_input_enrollment:
                # If enrollment matches, check name similarity
                # Calculate simple match score
                name_match = cert_name == normalized_input_name
                
                if name_match:
                    # Perfect match
                    matched_certificate = cert
                    best_match_score = 1.0
                    break
                elif best_match_score < 0.9:
                    # Enrollment matches but name doesn't - still count as match
                    # (enrollment is unique identifier)
                    matched_certificate = cert
                    best_match_score = 0.9
            
            # Also check if name matches and enrollment is similar
            # (in case of OCR errors in enrollment number)
            elif cert_name == normalized_input_name:
                # Check if enrollment numbers are similar
                if best_match_score < 0.7:
                    # Name matches - possible match
                    matched_certificate = cert
                    best_match_score = 0.7
        
        if matched_certificate:
            # Use the calculated match score as confidence
            confidence_score = best_match_score
            
            return jsonify({
                "success": True,
                "verified": True,
                "confidence_score": confidence_score,
                "matched_certificate": {
                    "student_name": matched_certificate["student_name"],
                    "enrollment_number": matched_certificate["enrollment_number"],
                    "degree": matched_certificate["degree"],
                    "branch": matched_certificate["branch"],
                    "graduation_date": matched_certificate["graduation_date"],
                    "cgpa": matched_certificate["cgpa"],
                    "certificate_number": matched_certificate["certificate_number"],
                    "status": matched_certificate["status"]
                },
                "verification_timestamp": datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                "success": True,
                "verified": False,
                "confidence_score": 0.0,
                "message": "Certificate not found in university database",
                "searched_for": {
                    "student_name": student_name,
                    "enrollment_number": enrollment_number
                },
                "verification_timestamp": datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Error verifying certificate: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/stats')
def get_university_stats():
    """Get university statistics"""
    try:
        data = load_certificates()
        certificates = data.get("certificates", [])
        metadata = data.get("metadata", {})
        
        # Calculate statistics
        branches = {}
        years = {}
        degrees = {}
        
        for cert in certificates:
            branch = cert.get("branch", "Unknown")
            year = cert.get("academic_year", "Unknown")
            degree = cert.get("degree", "Unknown")
            
            branches[branch] = branches.get(branch, 0) + 1
            years[year] = years.get(year, 0) + 1
            degrees[degree] = degrees.get(degree, 0) + 1
        
        return jsonify({
            "success": True,
            "statistics": {
                "total_certificates": len(certificates),
                "branches": branches,
                "academic_years": years,
                "degrees": degrees,
                "last_updated": metadata.get("last_updated"),
                "university_info": {
                    "name": metadata.get("university_name"),
                    "code": metadata.get("university_code"),
                    "location": metadata.get("location"),
                    "website": metadata.get("website")
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/admin.html')
def serve_admin_page():
    """Serve the admin login page"""
    try:
        return send_file('../frontend/admin.html')
    except Exception as e:
        logger.error(f"Error serving admin page: {e}")
        return "Admin page not found", 404

@app.route('/api/search')
def search_certificates():
    """Search certificates by various parameters"""
    try:
        # Get search parameters
        query = request.args.get('q', '').lower()
        branch = request.args.get('branch', '').lower()
        year = request.args.get('year', '')
        
        data = load_certificates()
        certificates = data.get("certificates", [])
        
        # Filter certificates
        results = []
        for cert in certificates:
            match = False
            
            # Text search in name, enrollment, or certificate number
            if query:
                searchable_text = f"{cert.get('student_name', '')} {cert.get('enrollment_number', '')} {cert.get('certificate_number', '')}".lower()
                if query in searchable_text:
                    match = True
            
            # Branch filter
            if branch and branch in cert.get('branch', '').lower():
                match = True
            
            # Year filter
            if year and year in cert.get('academic_year', ''):
                match = True
                
            # If no filters provided, return all
            if not query and not branch and not year:
                match = True
            
            if match:
                results.append(cert)
        
        return jsonify({
            "success": True,
            "results": results,
            "total": len(results),
            "search_params": {
                "query": query,
                "branch": branch,
                "year": year
            }
        })
        
    except Exception as e:
        logger.error(f"Error searching certificates: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print("🎓 Starting JUET University Portal...")
    print(f"🌐 Server will run on {host}:{port}")
    print("📊 Database contains certificate records")
    print("🔗 Integration with Certificate Verifier")
    
    app.run(host=host, port=port, debug=False)
