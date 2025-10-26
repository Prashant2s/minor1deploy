from app.db.session import init_engine, db_session
from app.core.config import settings
from app.db.models import Certificate, ExtractedField

init_engine(settings.DB_URL)

# Delete child rows first to avoid FK violations
fe = db_session.query(ExtractedField).delete(synchronize_session=False)
fc = db_session.query(Certificate).delete(synchronize_session=False)
db_session.commit()
print(f"deleted certificates={fc}, deleted fields={fe}")
