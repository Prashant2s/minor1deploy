#!/usr/bin/env python3
"""
Initialize University Database with Sample Certificate Data
This script adds sample university certificates for verification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import db_session, init_engine, Base, get_engine
from app.db.models import Student, User
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_university_data():
    """Initialize database with sample university certificate data"""
    try:
        # Initialize database engine and create tables
        init_engine(settings.DB_URL)
        
        # Import models to ensure they are registered with Base
        from app.db import models
        
        # Create all tables
        Base.metadata.create_all(bind=get_engine())
        logger.info("Database tables created/verified")
        # Sample university certificates data for verification
        sample_students = [
            {
                "name": "Prashant Singh",
                "reg_no": "231B225",
                "enrollment_no": "231B225",
                "email": "prashant.singh@student.juet.ac.in",
                "course": "B.Tech",
                "branch": "Computer Science & Engineering",
                "university": "Jaypee University of Engineering & Technology-Guna",
                "semester": "1",
                "academic_year": "2023-24",
                "date_of_birth": "15/03/2005",
                "graduation_date": "15/06/2027",
                "cgpa": "6.07",
                "sgpa": "6.1",
                "total_credits": "20",
                "earned_credits": "20",
                "subjects": [
                    {"code": "CS101", "name": "Computer Programming", "grade": "B+", "credits": "4"},
                    {"code": "MA101", "name": "Engineering Mathematics-I", "grade": "A", "credits": "4"},
                    {"code": "PH101", "name": "Engineering Physics", "grade": "B", "credits": "3"},
                    {"code": "CH101", "name": "Engineering Chemistry", "grade": "B+", "credits": "3"},
                    {"code": "ME101", "name": "Engineering Mechanics", "grade": "B", "credits": "3"},
                    {"code": "EE101", "name": "Basic Electrical Engineering", "grade": "A-", "credits": "3"}
                ]
            },
            {
                "name": "Rahul Sharma",
                "reg_no": "231B224",
                "enrollment_no": "231B224",
                "email": "rahul.sharma@student.juet.ac.in",
                "course": "B.Tech",
                "branch": "Electronics & Communication Engineering",
                "university": "Jaypee University of Engineering & Technology-Guna",
                "semester": "1",
                "academic_year": "2023-24",
                "date_of_birth": "20/05/2005",
                "graduation_date": "15/06/2027",
                "cgpa": "7.2",
                "sgpa": "7.1",
                "total_credits": "20",
                "earned_credits": "20",
                "subjects": [
                    {"code": "EC101", "name": "Basic Electronics", "grade": "A", "credits": "4"},
                    {"code": "MA101", "name": "Engineering Mathematics-I", "grade": "A", "credits": "4"},
                    {"code": "PH101", "name": "Engineering Physics", "grade": "A-", "credits": "3"},
                    {"code": "CH101", "name": "Engineering Chemistry", "grade": "B+", "credits": "3"},
                    {"code": "ME101", "name": "Engineering Mechanics", "grade": "B+", "credits": "3"},
                    {"code": "EC102", "name": "Circuit Analysis", "grade": "A", "credits": "3"}
                ]
            },
            {
                "name": "Anjali Patel",
                "reg_no": "231B223",
                "enrollment_no": "231B223",
                "email": "anjali.patel@student.juet.ac.in",
                "course": "B.Tech",
                "branch": "Information Technology",
                "university": "Jaypee University of Engineering & Technology-Guna",
                "semester": "2",
                "academic_year": "2023-24",
                "date_of_birth": "12/08/2005",
                "graduation_date": "15/06/2027",
                "cgpa": "8.1",
                "sgpa": "8.0",
                "total_credits": "22",
                "earned_credits": "22",
                "subjects": [
                    {"code": "IT201", "name": "Data Structures", "grade": "A+", "credits": "4"},
                    {"code": "MA201", "name": "Engineering Mathematics-II", "grade": "A", "credits": "4"},
                    {"code": "CS201", "name": "Object Oriented Programming", "grade": "A", "credits": "4"},
                    {"code": "IT202", "name": "Database Management Systems", "grade": "A-", "credits": "4"},
                    {"code": "EC201", "name": "Digital Electronics", "grade": "A", "credits": "3"},
                    {"code": "HS201", "name": "Technical Communication", "grade": "A", "credits": "3"}
                ]
            }
        ]
        
        # Add sample students to database
        for student_data in sample_students:
            # Check if student already exists
            existing_student = db_session.query(Student).filter(Student.reg_no == student_data["reg_no"]).first()
            
            if not existing_student:
                student = Student(
                    name=student_data["name"],
                    reg_no=student_data["reg_no"],
                    dob=student_data["date_of_birth"]
                )
                db_session.add(student)
                logger.info(f"Added student: {student_data['name']} ({student_data['reg_no']})")
            else:
                logger.info(f"Student already exists: {student_data['name']} ({student_data['reg_no']})")
        
        # Create a default university admin user
        admin_user = db_session.query(User).filter(User.username == "university_admin").first()
        if not admin_user:
            admin_user = User(
                username="university_admin",
                email="admin@juet.ac.in",
                user_type="university",
                university_name="Jaypee University of Engineering & Technology-Guna",
                university_code="JUET"
            )
            admin_user.set_password("admin123")
            db_session.add(admin_user)
            logger.info("Created university admin user: university_admin / admin123")
        
        # Create a sample student user
        student_user = db_session.query(User).filter(User.username == "prashant_student").first()
        if not student_user:
            student_user = User(
                username="prashant_student",
                email="prashant@student.juet.ac.in",
                user_type="student",
                student_name="Prashant Singh",
                student_reg_no="231B225",
                student_dob="15/03/2005"
            )
            student_user.set_password("student123")
            db_session.add(student_user)
            logger.info("Created student user: prashant_student / student123")
        
        db_session.commit()
        logger.info("✅ University database initialization completed successfully!")
        
    except Exception as e:
        db_session.rollback()
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise

if __name__ == "__main__":
    init_university_data()