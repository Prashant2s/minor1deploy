from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Index, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base
import hashlib
import secrets

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    user_type = Column(String(20), nullable=False)  # 'student' or 'university'
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Student-specific fields
    student_name = Column(String(200), nullable=True)
    student_reg_no = Column(String(100), unique=True, nullable=True)
    student_dob = Column(String(10), nullable=True)
    
    # University-specific fields
    university_name = Column(String(200), nullable=True)
    university_code = Column(String(50), unique=True, nullable=True)
    
    certificates = relationship('Certificate', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password: str):
        """Hash and set password"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        self.password_hash = f"{salt}:{password_hash.hex()}"
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches the hash"""
        if ':' not in self.password_hash:
            return False
        salt, stored_hash = self.password_hash.split(':', 1)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return password_hash.hex() == stored_hash
    
    __table_args__ = (
        Index('idx_users_username', 'username'),
        Index('idx_users_email', 'email'),
        Index('idx_users_type', 'user_type'),
        Index('idx_users_student_reg_no', 'student_reg_no'),
        Index('idx_users_university_code', 'university_code'),
    )

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    dob = Column(String(10), nullable=True)
    reg_no = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    certificates = relationship('Certificate', back_populates='student', cascade='all, delete-orphan')
    
    __table_args__ = (
        Index('idx_students_reg_no', 'reg_no'),
        Index('idx_students_name', 'name'),
    )

class Certificate(Base):
    __tablename__ = 'certificates'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=True)
    image_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=True)
    status = Column(String(50), default='processed', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user = relationship('User', back_populates='certificates')
    student = relationship('Student', back_populates='certificates')
    fields = relationship('ExtractedField', back_populates='certificate', cascade='all, delete-orphan')
    
    __table_args__ = (
        Index('idx_certificates_user_id', 'user_id'),
        Index('idx_certificates_student_id', 'student_id'),
        Index('idx_certificates_created_at', 'created_at'),
        Index('idx_certificates_status', 'status'),
    )

class ExtractedField(Base):
    __tablename__ = 'extracted_fields'
    
    id = Column(Integer, primary_key=True)
    certificate_id = Column(Integer, ForeignKey('certificates.id'), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    field_type = Column(String(50), default='extracted', nullable=False)  # 'extracted', 'ai_summary', 'verification'
    
    certificate = relationship('Certificate', back_populates='fields')
    
    __table_args__ = (
        Index('idx_extracted_fields_certificate_id', 'certificate_id'),
        Index('idx_extracted_fields_key', 'key'),
        Index('idx_extracted_fields_type', 'field_type'),
        Index('idx_extracted_fields_cert_key', 'certificate_id', 'key'),  # Composite index for faster lookups
    )