from source.app.settings.definitions_settings import db
from datetime import datetime, timezone
import uuid

class ReviewsEntity(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    by = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=False)
    note = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)
    to = db.Column(db.String, nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
