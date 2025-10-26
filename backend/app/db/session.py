from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()
_engine = None
_db_factory = None

db_session = scoped_session(lambda: _db_factory())

def init_engine(db_url: str):
    global _engine, _db_factory
    
    _engine = create_engine(
        db_url, 
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )
    
    _db_factory = sessionmaker(bind=_engine, autocommit=False, autoflush=False)
    logger.info("Database engine initialized")

def get_engine():
    return _engine

@contextmanager
def get_db_session():
    session = _db_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def create_tables():
    if _engine:
        Base.metadata.create_all(_engine)
        logger.info("Database tables created")