from flask import Flask, request
from flask_cors import CORS
from app.db.session import init_engine, db_session, Base, get_engine
from app.api.routes import api_bp
from app.core.config import settings

def create_app() -> Flask:
    app = Flask(__name__)

    # CORS configuration
    CORS(
        app,
        origins=settings.CORS_ORIGIN.split(',') if ',' in settings.CORS_ORIGIN else [settings.CORS_ORIGIN],
        allow_headers=['Content-Type', 'Authorization'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        supports_credentials=True
    )

    # DB
    init_engine(settings.DB_URL)

    # Import models and create tables
    from app.db import models
    try:
        Base.metadata.create_all(bind=get_engine())
    except Exception as e:
        # Tables might already exist, which is fine
        print(f"Note: Database tables may already exist: {e}")
        pass
    
    # Run migration for field_type column
    try:
        from sqlalchemy import text
        with get_engine().connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='extracted_fields' AND column_name='field_type'
            """))
            if not result.fetchone():
                print("Adding field_type column...")
                conn.execute(text("""
                    ALTER TABLE extracted_fields 
                    ADD COLUMN field_type VARCHAR(50) DEFAULT 'extracted' NOT NULL
                """))
                conn.commit()
                print("✅ Added field_type column")
    except Exception as e:
        print(f"Migration note: {e}")
        pass

    @app.teardown_appcontext
    def remove_session(exception=None):
        db_session.remove()
    
    # Root endpoint
    @app.route("/")
    def root():
        return {
            "message": "University Certificate Verifier API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "health": "/api/v1/health",
                "auth": "/api/v1/auth/*",
                "certificates": "/api/v1/certificates/*"
            }
        }

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app

# Create the WSGI application instance for gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)