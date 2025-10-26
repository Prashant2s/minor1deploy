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

# Configure upload folder
UPLOAD_FOLDER = '../database/certificates'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load certificate database
def load_certificates():
    try:
        with open('../database/certificates.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading certificates: {e}")
        return {"certificates": [], "metadata": {}}

# Save certificate database
def save_certificates(data):
    try:
        with open('../database/certificates.json', 'w') as f:
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
        
        # Save the certificate file
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        saved_filename = f"{enrollment}_{cert_id}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, saved_filename)
        file.save(file_path)
        
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
        
        # Search for matching certificate
        matched_certificate = None
        for cert in certificates:
            cert_name = cert.get("student_name", "").lower().strip()
            cert_enrollment = cert.get("enrollment_number", "").lower().strip()
            
            # Check for exact match
            if (cert_name == student_name.lower() and 
                cert_enrollment == enrollment_number.lower()):
                matched_certificate = cert
                break
        
        if matched_certificate:
            # Calculate confidence score based on match quality
            confidence_score = 1.0  # Perfect match
            
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
    print("🎓 Starting JUET University Portal...")
    print("🌐 Server will run on http://localhost:3000")
    print("📊 Database contains 5 sample certificates")
    print("🔗 Integration with Certificate Verifier (port 5173)")
    
    app.run(host='0.0.0.0', port=3000, debug=True)