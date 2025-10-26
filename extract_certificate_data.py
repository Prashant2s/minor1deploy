#!/usr/bin/env python3
"""
AI-Extracted Certificate Information (Tabular Format)
======================================================
This script extracts certificate information using AI and presents it in various tabular formats.
Supports CSV, Excel, JSON, and HTML output formats for easy viewing and analysis.
"""

import os
import sys
import json
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from tabulate import tabulate
import argparse

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

# Import backend modules
from backend.app.services.extract import extract_fields_with_ai, generate_ai_summary
from backend.app.services.ocr import run_ocr
from backend.app.core.config import settings

class CertificateDataExtractor:
    """Enhanced certificate data extractor with tabular export capabilities."""
    
    def __init__(self, output_dir: str = "extracted_data"):
        """Initialize the extractor with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.extracted_data = []
        
    def extract_from_file(self, file_path: Path) -> Dict[str, Any]:
        """Extract certificate data from a single file."""
        try:
            print(f"Processing: {file_path.name}")
            
            # Run OCR to extract text
            ocr_text = run_ocr(file_path)
            
            # Extract fields using AI
            extracted_fields = extract_fields_with_ai(ocr_text)
            
            # Generate summary
            summary = generate_ai_summary(extracted_fields)
            
            # Format subjects for better display
            subjects_formatted = []
            if extracted_fields.get('subjects'):
                for subject in extracted_fields['subjects']:
                    if isinstance(subject, dict):
                        subjects_formatted.append(
                            f"{subject.get('subject_code', '')}: {subject.get('subject_name', '')} "
                            f"(Grade: {subject.get('grade', '')}, Credits: {subject.get('credits', '')})"
                        )
            
            # Create comprehensive data record
            record = {
                "File": file_path.name,
                "Processing Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Student Name": extracted_fields.get('student_name', ''),
                "Enrollment No": extracted_fields.get('enrollment_number', ''),
                "Degree": extracted_fields.get('degree', ''),
                "Branch": extracted_fields.get('branch', ''),
                "University": extracted_fields.get('university_name', ''),
                "Graduation Date": extracted_fields.get('graduation_date', ''),
                "Date of Birth": extracted_fields.get('date_of_birth', ''),
                "Certificate Type": extracted_fields.get('certificate_type', ''),
                "Semester": extracted_fields.get('semester', ''),
                "Academic Year": extracted_fields.get('academic_year', ''),
                "SGPA": extracted_fields.get('sgpa', ''),
                "CGPA": extracted_fields.get('cgpa', ''),
                "Grade": extracted_fields.get('grade', ''),
                "Total Credits": extracted_fields.get('total_credits', ''),
                "Earned Credits": extracted_fields.get('earned_credits', ''),
                "Subjects Count": len(subjects_formatted),
                "Subjects": '; '.join(subjects_formatted) if subjects_formatted else '',
                "AI Summary": summary,
                "Raw Data": json.dumps(extracted_fields)
            }
            
            return record
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return {
                "File": file_path.name,
                "Error": str(e),
                "Processing Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def extract_from_directory(self, directory: Path, file_patterns: List[str] = None) -> List[Dict]:
        """Extract data from all certificates in a directory."""
        if file_patterns is None:
            file_patterns = ['*.jpg', '*.jpeg', '*.png', '*.pdf', '*.tiff', '*.bmp']
        
        all_files = []
        for pattern in file_patterns:
            all_files.extend(directory.glob(pattern))
        
        print(f"Found {len(all_files)} certificate files to process")
        
        for file_path in all_files:
            record = self.extract_from_file(file_path)
            self.extracted_data.append(record)
        
        return self.extracted_data
    
    def export_to_csv(self, filename: str = None) -> Path:
        """Export extracted data to CSV format."""
        if not filename:
            filename = f"certificates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        output_path = self.output_dir / filename
        
        if self.extracted_data:
            keys = self.extracted_data[0].keys()
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.extracted_data)
            
            print(f"CSV exported to: {output_path}")
        
        return output_path
    
    def export_to_excel(self, filename: str = None) -> Path:
        """Export extracted data to Excel format with formatting."""
        if not filename:
            filename = f"certificates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        output_path = self.output_dir / filename
        
        if self.extracted_data:
            df = pd.DataFrame(self.extracted_data)
            
            # Create Excel writer with xlsxwriter engine
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Main data sheet
                df.to_excel(writer, sheet_name='Certificate Data', index=False)
                
                # Summary statistics sheet
                summary_df = self._create_summary_statistics()
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            print(f"Excel exported to: {output_path}")
        
        return output_path
    
    def export_to_json(self, filename: str = None) -> Path:
        """Export extracted data to JSON format."""
        if not filename:
            filename = f"certificates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "extraction_date": datetime.now().isoformat(),
                "total_certificates": len(self.extracted_data),
                "certificates": self.extracted_data
            }, f, indent=2, ensure_ascii=False)
        
        print(f"JSON exported to: {output_path}")
        return output_path
    
    def export_to_html(self, filename: str = None) -> Path:
        """Export extracted data to HTML table format."""
        if not filename:
            filename = f"certificates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        output_path = self.output_dir / filename
        
        if self.extracted_data:
            df = pd.DataFrame(self.extracted_data)
            
            # Create styled HTML
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extracted Certificate Data</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #fff;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: #fff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .grade-high {{ color: #2e7d32; font-weight: bold; }}
        .grade-medium {{ color: #f57c00; }}
        .grade-low {{ color: #c62828; }}
    </style>
</head>
<body>
    <h1>AI-Extracted Certificate Information</h1>
    
    <div class="summary">
        <h2>Summary Statistics</h2>
        <p><strong>Total Certificates:</strong> {len(self.extracted_data)}</p>
        <p><strong>Extraction Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Universities:</strong> {len(set(d.get('University', '') for d in self.extracted_data if d.get('University')))}</p>
        <p><strong>Average CGPA:</strong> {self._calculate_average_cgpa():.2f}</p>
    </div>
    
    {df.to_html(classes='certificate-table', index=False)}
    
    <script>
        // Add CGPA coloring
        document.querySelectorAll('td').forEach(cell => {{
            if (cell.innerHTML.match(/^\\d+\\.\\d+$/)) {{
                const value = parseFloat(cell.innerHTML);
                if (value >= 8.0) cell.className = 'grade-high';
                else if (value >= 6.0) cell.className = 'grade-medium';
                else if (value > 0) cell.className = 'grade-low';
            }}
        }});
    </script>
</body>
</html>
"""
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTML exported to: {output_path}")
        
        return output_path
    
    def print_table(self, max_rows: int = 10):
        """Print extracted data as a formatted table in console."""
        if not self.extracted_data:
            print("No data to display")
            return
        
        # Select key columns for console display
        display_columns = [
            'Student Name', 'Enrollment No', 'Degree', 'Branch', 
            'University', 'SGPA', 'CGPA', 'Certificate Type'
        ]
        
        # Create display data
        display_data = []
        for record in self.extracted_data[:max_rows]:
            display_row = [record.get(col, '') for col in display_columns]
            display_data.append(display_row)
        
        # Print table
        print("\n" + "="*100)
        print("EXTRACTED CERTIFICATE DATA (TABULAR FORMAT)")
        print("="*100)
        print(tabulate(display_data, headers=display_columns, tablefmt='grid'))
        
        if len(self.extracted_data) > max_rows:
            print(f"\n... and {len(self.extracted_data) - max_rows} more records")
        
        # Print summary
        print("\n" + "-"*50)
        print("SUMMARY STATISTICS")
        print("-"*50)
        self._print_summary()
    
    def _create_summary_statistics(self) -> pd.DataFrame:
        """Create summary statistics DataFrame."""
        summary = {
            'Metric': [],
            'Value': []
        }
        
        summary['Metric'].append('Total Certificates')
        summary['Value'].append(len(self.extracted_data))
        
        summary['Metric'].append('Unique Universities')
        universities = set(d.get('University', '') for d in self.extracted_data if d.get('University'))
        summary['Value'].append(len(universities))
        
        summary['Metric'].append('Average CGPA')
        summary['Value'].append(f"{self._calculate_average_cgpa():.2f}")
        
        summary['Metric'].append('Certificate Types')
        cert_types = set(d.get('Certificate Type', '') for d in self.extracted_data if d.get('Certificate Type'))
        summary['Value'].append(', '.join(cert_types))
        
        return pd.DataFrame(summary)
    
    def _calculate_average_cgpa(self) -> float:
        """Calculate average CGPA from extracted data."""
        cgpas = []
        for record in self.extracted_data:
            try:
                cgpa = float(record.get('CGPA', 0))
                if cgpa > 0:
                    cgpas.append(cgpa)
            except (ValueError, TypeError):
                continue
        
        return sum(cgpas) / len(cgpas) if cgpas else 0.0
    
    def _print_summary(self):
        """Print summary statistics to console."""
        print(f"Total Certificates: {len(self.extracted_data)}")
        
        universities = set(d.get('University', '') for d in self.extracted_data if d.get('University'))
        print(f"Unique Universities: {len(universities)}")
        
        print(f"Average CGPA: {self._calculate_average_cgpa():.2f}")
        
        cert_types = set(d.get('Certificate Type', '') for d in self.extracted_data if d.get('Certificate Type'))
        print(f"Certificate Types: {', '.join(cert_types)}")


def test_single_extraction():
    """Test extraction with a single certificate."""
    extractor = CertificateDataExtractor()
    
    # Create a test image path
    test_file = Path("test_certificate.jpg")
    
    if test_file.exists():
        # Extract data
        record = extractor.extract_from_file(test_file)
        extractor.extracted_data = [record]
        
        # Display and export
        extractor.print_table()
        extractor.export_to_csv()
        extractor.export_to_excel()
        extractor.export_to_json()
        extractor.export_to_html()
    else:
        print(f"Test file {test_file} not found. Creating sample data...")
        
        # Create sample data for demonstration
        sample_data = {
            "File": "sample_certificate.jpg",
            "Processing Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Student Name": "Prashant Singh",
            "Enrollment No": "231B225",
            "Degree": "B.Tech",
            "Branch": "Computer Science & Engineering",
            "University": "Jaypee University of Engineering & Technology",
            "Graduation Date": "15/06/2027",
            "Date of Birth": "15/03/2005",
            "Certificate Type": "Semester Result",
            "Semester": "1",
            "Academic Year": "2023-24",
            "SGPA": "6.1",
            "CGPA": "6.07",
            "Grade": "",
            "Total Credits": "20",
            "Earned Credits": "20",
            "Subjects Count": 6,
            "Subjects": "CS101: Computer Programming (Grade: B+, Credits: 4); MA101: Engineering Mathematics-I (Grade: A, Credits: 4)",
            "AI Summary": "Prashant Singh - B.Tech CSE from Jaypee University (CGPA: 6.07, Semester 1)",
            "Raw Data": "{}"
        }
        
        extractor.extracted_data = [sample_data]
        
        # Display and export
        extractor.print_table()
        extractor.export_to_csv("sample_certificates.csv")
        extractor.export_to_excel("sample_certificates.xlsx")
        extractor.export_to_json("sample_certificates.json")
        extractor.export_to_html("sample_certificates.html")


def main():
    """Main function with CLI interface."""
    parser = argparse.ArgumentParser(
        description="AI-Extracted Certificate Information (Tabular Format)"
    )
    parser.add_argument(
        'input',
        nargs='?',
        help='Input file or directory path'
    )
    parser.add_argument(
        '-o', '--output',
        default='extracted_data',
        help='Output directory for exported files'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['csv', 'excel', 'json', 'html', 'all'],
        default='all',
        help='Export format (default: all)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run test extraction with sample data'
    )
    
    args = parser.parse_args()
    
    if args.test:
        test_single_extraction()
        return
    
    # Initialize extractor
    extractor = CertificateDataExtractor(output_dir=args.output)
    
    if args.input:
        input_path = Path(args.input)
        
        if input_path.is_file():
            # Process single file
            record = extractor.extract_from_file(input_path)
            extractor.extracted_data = [record]
        elif input_path.is_dir():
            # Process directory
            extractor.extract_from_directory(input_path)
        else:
            print(f"Error: {input_path} not found")
            return
    else:
        # Run test mode
        test_single_extraction()
        return
    
    # Display results
    extractor.print_table()
    
    # Export to specified formats
    if args.format in ['csv', 'all']:
        extractor.export_to_csv()
    if args.format in ['excel', 'all']:
        extractor.export_to_excel()
    if args.format in ['json', 'all']:
        extractor.export_to_json()
    if args.format in ['html', 'all']:
        extractor.export_to_html()
    
    print(f"\nAll exports saved to: {extractor.output_dir}")


if __name__ == "__main__":
    main()