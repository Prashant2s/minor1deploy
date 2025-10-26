#!/usr/bin/env python3
"""
Web-based Certificate Data Viewer
==================================
Interactive web application for viewing AI-extracted certificate data.
"""

from flask import Flask, render_template_string, request, jsonify, send_file
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import os
import sys

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from extract_certificate_data import CertificateDataExtractor

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Certificate Data Extraction Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container-main {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-top: 30px;
            padding: 30px;
        }
        .header-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .stats-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        .stats-card h3 {
            color: #667eea;
            font-size: 2rem;
            margin-bottom: 5px;
        }
        .stats-card p {
            color: #666;
            margin: 0;
        }
        .table-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            overflow-x: auto;
        }
        .table thead {
            background: #f8f9fa;
        }
        .table th {
            border-top: none;
            font-weight: 600;
            color: #495057;
            text-transform: uppercase;
            font-size: 0.85rem;
            padding: 12px;
        }
        .table td {
            vertical-align: middle;
            padding: 12px;
        }
        .badge-cgpa {
            font-size: 0.9rem;
            padding: 5px 10px;
        }
        .cgpa-high { background-color: #28a745; }
        .cgpa-medium { background-color: #ffc107; color: black; }
        .cgpa-low { background-color: #dc3545; }
        .upload-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 30px;
            border: 2px dashed #dee2e6;
            text-align: center;
            margin-bottom: 30px;
        }
        .upload-section:hover {
            border-color: #667eea;
            background: #f1f3ff;
        }
        .filter-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .export-buttons {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            margin-bottom: 20px;
        }
        .detail-modal {
            max-width: 800px;
        }
        .subject-list {
            background: #f8f9fa;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        }
        .subject-item {
            background: white;
            border-radius: 5px;
            padding: 8px;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="container container-main">
        <div class="header-section">
            <h1 class="mb-0"><i class="bi bi-file-earmark-text"></i> AI Certificate Data Extraction Dashboard</h1>
            <p class="mb-0 mt-2">Advanced Document Analysis & Information Extraction System</p>
        </div>

        <!-- Statistics Section -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="stats-card">
                    <h3 id="total-certs">{{ stats.total }}</h3>
                    <p>Total Certificates</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <h3 id="universities">{{ stats.universities }}</h3>
                    <p>Universities</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <h3 id="avg-cgpa">{{ stats.avg_cgpa }}</h3>
                    <p>Average CGPA</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <h3 id="success-rate">{{ stats.success_rate }}%</h3>
                    <p>Extraction Success</p>
                </div>
            </div>
        </div>

        <!-- Upload Section -->
        <div class="upload-section">
            <h4><i class="bi bi-cloud-upload"></i> Upload Certificate</h4>
            <p>Drag and drop or click to upload certificate images</p>
            <input type="file" id="file-upload" accept="image/*,.pdf" style="display:none">
            <button class="btn btn-primary" onclick="document.getElementById('file-upload').click()">
                Choose File
            </button>
        </div>

        <!-- Filter Section -->
        <div class="filter-section">
            <div class="row">
                <div class="col-md-3">
                    <input type="text" class="form-control" id="search-name" placeholder="Search by name...">
                </div>
                <div class="col-md-3">
                    <select class="form-select" id="filter-university">
                        <option value="">All Universities</option>
                        {% for uni in universities %}
                        <option value="{{ uni }}">{{ uni }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <select class="form-select" id="filter-degree">
                        <option value="">All Degrees</option>
                        <option value="B.Tech">B.Tech</option>
                        <option value="B.E.">B.E.</option>
                        <option value="M.Tech">M.Tech</option>
                        <option value="B.Sc">B.Sc</option>
                        <option value="M.Sc">M.Sc</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <button class="btn btn-secondary w-100" onclick="clearFilters()">
                        <i class="bi bi-x-circle"></i> Clear Filters
                    </button>
                </div>
            </div>
        </div>

        <!-- Export Buttons -->
        <div class="export-buttons">
            <button class="btn btn-success" onclick="exportData('csv')">
                <i class="bi bi-file-earmark-spreadsheet"></i> Export CSV
            </button>
            <button class="btn btn-success" onclick="exportData('excel')">
                <i class="bi bi-file-earmark-excel"></i> Export Excel
            </button>
            <button class="btn btn-info" onclick="exportData('json')">
                <i class="bi bi-file-code"></i> Export JSON
            </button>
            <button class="btn btn-warning" onclick="exportData('html')">
                <i class="bi bi-file-earmark-code"></i> Export HTML
            </button>
        </div>

        <!-- Data Table -->
        <div class="table-container">
            <table class="table table-hover" id="data-table">
                <thead>
                    <tr>
                        <th>Student Name</th>
                        <th>Enrollment No</th>
                        <th>Degree</th>
                        <th>Branch</th>
                        <th>University</th>
                        <th>Semester</th>
                        <th>SGPA</th>
                        <th>CGPA</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="table-body">
                    {% for cert in certificates %}
                    <tr>
                        <td><strong>{{ cert['Student Name'] }}</strong></td>
                        <td>{{ cert['Enrollment No'] }}</td>
                        <td>{{ cert['Degree'] }}</td>
                        <td>{{ cert['Branch'] }}</td>
                        <td>{{ cert['University'] }}</td>
                        <td>{{ cert['Semester'] }}</td>
                        <td>
                            {% if cert['SGPA'] %}
                            <span class="badge badge-cgpa {% if cert['SGPA']|float >= 8.0 %}cgpa-high{% elif cert['SGPA']|float >= 6.0 %}cgpa-medium{% else %}cgpa-low{% endif %}">
                                {{ cert['SGPA'] }}
                            </span>
                            {% endif %}
                        </td>
                        <td>
                            {% if cert['CGPA'] %}
                            <span class="badge badge-cgpa {% if cert['CGPA']|float >= 8.0 %}cgpa-high{% elif cert['CGPA']|float >= 6.0 %}cgpa-medium{% else %}cgpa-low{% endif %}">
                                {{ cert['CGPA'] }}
                            </span>
                            {% endif %}
                        </td>
                        <td>
                            <button class="btn btn-sm btn-outline-primary" onclick='showDetails({{ cert|tojson }})'>
                                <i class="bi bi-eye"></i> View
                            </button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <!-- Detail Modal -->
    <div class="modal fade" id="detailModal" tabindex="-1">
        <div class="modal-dialog modal-lg detail-modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Certificate Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="modal-body">
                    <!-- Content will be populated by JavaScript -->
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function showDetails(cert) {
            let content = `
                <div class="row">
                    <div class="col-md-6">
                        <h6>Personal Information</h6>
                        <table class="table table-sm">
                            <tr><td><strong>Name:</strong></td><td>${cert['Student Name'] || '-'}</td></tr>
                            <tr><td><strong>Enrollment No:</strong></td><td>${cert['Enrollment No'] || '-'}</td></tr>
                            <tr><td><strong>Date of Birth:</strong></td><td>${cert['Date of Birth'] || '-'}</td></tr>
                        </table>
                    </div>
                    <div class="col-md-6">
                        <h6>Academic Information</h6>
                        <table class="table table-sm">
                            <tr><td><strong>Degree:</strong></td><td>${cert['Degree'] || '-'}</td></tr>
                            <tr><td><strong>Branch:</strong></td><td>${cert['Branch'] || '-'}</td></tr>
                            <tr><td><strong>University:</strong></td><td>${cert['University'] || '-'}</td></tr>
                            <tr><td><strong>Graduation Date:</strong></td><td>${cert['Graduation Date'] || '-'}</td></tr>
                        </table>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-6">
                        <h6>Performance Metrics</h6>
                        <table class="table table-sm">
                            <tr><td><strong>Semester:</strong></td><td>${cert['Semester'] || '-'}</td></tr>
                            <tr><td><strong>Academic Year:</strong></td><td>${cert['Academic Year'] || '-'}</td></tr>
                            <tr><td><strong>SGPA:</strong></td><td>${cert['SGPA'] || '-'}</td></tr>
                            <tr><td><strong>CGPA:</strong></td><td>${cert['CGPA'] || '-'}</td></tr>
                        </table>
                    </div>
                    <div class="col-md-6">
                        <h6>Credits Information</h6>
                        <table class="table table-sm">
                            <tr><td><strong>Total Credits:</strong></td><td>${cert['Total Credits'] || '-'}</td></tr>
                            <tr><td><strong>Earned Credits:</strong></td><td>${cert['Earned Credits'] || '-'}</td></tr>
                            <tr><td><strong>Certificate Type:</strong></td><td>${cert['Certificate Type'] || '-'}</td></tr>
                            <tr><td><strong>Grade:</strong></td><td>${cert['Grade'] || '-'}</td></tr>
                        </table>
                    </div>
                </div>
            `;
            
            if (cert['Subjects']) {
                content += `
                    <div class="mt-3">
                        <h6>Subjects</h6>
                        <div class="subject-list">
                            ${cert['Subjects']}
                        </div>
                    </div>
                `;
            }
            
            if (cert['AI Summary']) {
                content += `
                    <div class="mt-3">
                        <h6>AI Summary</h6>
                        <div class="alert alert-info">
                            ${cert['AI Summary']}
                        </div>
                    </div>
                `;
            }
            
            document.getElementById('modal-body').innerHTML = content;
            new bootstrap.Modal(document.getElementById('detailModal')).show();
        }

        function exportData(format) {
            window.location.href = `/export?format=${format}`;
        }

        function clearFilters() {
            document.getElementById('search-name').value = '';
            document.getElementById('filter-university').value = '';
            document.getElementById('filter-degree').value = '';
            filterTable();
        }

        function filterTable() {
            const nameFilter = document.getElementById('search-name').value.toLowerCase();
            const uniFilter = document.getElementById('filter-university').value;
            const degreeFilter = document.getElementById('filter-degree').value;
            
            const rows = document.querySelectorAll('#table-body tr');
            rows.forEach(row => {
                const name = row.cells[0].textContent.toLowerCase();
                const uni = row.cells[4].textContent;
                const degree = row.cells[2].textContent;
                
                const nameMatch = !nameFilter || name.includes(nameFilter);
                const uniMatch = !uniFilter || uni === uniFilter;
                const degreeMatch = !degreeFilter || degree === degreeFilter;
                
                row.style.display = nameMatch && uniMatch && degreeMatch ? '' : 'none';
            });
        }

        // Add event listeners
        document.getElementById('search-name').addEventListener('input', filterTable);
        document.getElementById('filter-university').addEventListener('change', filterTable);
        document.getElementById('filter-degree').addEventListener('change', filterTable);
        
        // File upload handler
        document.getElementById('file-upload').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const formData = new FormData();
                formData.append('file', file);
                
                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Certificate processed successfully!');
                        location.reload();
                    } else {
                        alert('Error processing certificate: ' + data.error);
                    }
                });
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main dashboard page."""
    extractor = CertificateDataExtractor()
    
    # Load sample data or existing data
    data_file = Path('extracted_data/sample_certificates.json')
    if data_file.exists():
        with open(data_file, 'r') as f:
            data = json.load(f)
            certificates = data.get('certificates', [])
    else:
        # Create sample data
        certificates = [{
            "Student Name": "Prashant Singh",
            "Enrollment No": "231B225",
            "Degree": "B.Tech",
            "Branch": "Computer Science & Engineering",
            "University": "Jaypee University of Engineering & Technology",
            "Semester": "1",
            "Academic Year": "2023-24",
            "SGPA": "6.1",
            "CGPA": "6.07",
            "Total Credits": "20",
            "Earned Credits": "20",
            "Subjects": "CS101: Computer Programming (B+); MA101: Mathematics (A)",
            "AI Summary": "Prashant Singh - B.Tech CSE from Jaypee University",
            "Certificate Type": "Semester Result",
            "Graduation Date": "15/06/2027",
            "Date of Birth": "15/03/2005",
            "Grade": ""
        }]
    
    # Calculate statistics
    stats = {
        'total': len(certificates),
        'universities': len(set(c.get('University', '') for c in certificates if c.get('University'))),
        'avg_cgpa': calculate_avg_cgpa(certificates),
        'success_rate': 100
    }
    
    universities = list(set(c.get('University', '') for c in certificates if c.get('University')))
    
    return render_template_string(HTML_TEMPLATE, 
                                 certificates=certificates, 
                                 stats=stats,
                                 universities=universities)

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload and processing."""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Save and process file
        temp_path = Path('temp') / file.filename
        temp_path.parent.mkdir(exist_ok=True)
        file.save(str(temp_path))
        
        # Process with extractor
        extractor = CertificateDataExtractor()
        record = extractor.extract_from_file(temp_path)
        
        # Add to existing data
        data_file = Path('extracted_data/sample_certificates.json')
        if data_file.exists():
            with open(data_file, 'r') as f:
                data = json.load(f)
        else:
            data = {'certificates': []}
        
        data['certificates'].append(record)
        
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Clean up
        temp_path.unlink()
        
        return jsonify({'success': True, 'data': record})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/export')
def export():
    """Export data in various formats."""
    format_type = request.args.get('format', 'csv')
    
    extractor = CertificateDataExtractor()
    
    # Load existing data
    data_file = Path('extracted_data/sample_certificates.json')
    if data_file.exists():
        with open(data_file, 'r') as f:
            data = json.load(f)
            extractor.extracted_data = data.get('certificates', [])
    
    # Export based on format
    if format_type == 'csv':
        file_path = extractor.export_to_csv('export.csv')
    elif format_type == 'excel':
        file_path = extractor.export_to_excel('export.xlsx')
    elif format_type == 'json':
        file_path = extractor.export_to_json('export.json')
    elif format_type == 'html':
        file_path = extractor.export_to_html('export.html')
    else:
        return "Invalid format", 400
    
    return send_file(str(file_path), as_attachment=True)

def calculate_avg_cgpa(certificates):
    """Calculate average CGPA."""
    cgpas = []
    for cert in certificates:
        try:
            cgpa = float(cert.get('CGPA', 0))
            if cgpa > 0:
                cgpas.append(cgpa)
        except:
            continue
    return f"{sum(cgpas)/len(cgpas):.2f}" if cgpas else "0.00"

if __name__ == '__main__':
    print("Starting Certificate Data Viewer...")
    print("Access the dashboard at: http://localhost:5001")
    app.run(debug=True, port=5001)