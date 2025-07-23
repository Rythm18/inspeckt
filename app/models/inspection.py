from app import db

class Inspection(db.Model):
    __tablename__ = 'inspections'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_number = db.Column(db.String(20), nullable=False)
    inspected_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    damage_report = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'reviewed', 'completed', name='inspection_status'), default='pending', nullable=False)
    image_url = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Inspection {self.vehicle_number}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_number': self.vehicle_number,
            'inspected_by': self.inspected_by,
            'damage_report': self.damage_report,
            'status': self.status,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def validate_image_url(image_url):
        """Validate that image URL ends with .jpg, .jpeg, or .png"""
        if not image_url:
            return True
        
        valid_extensions = ['.jpg', '.jpeg', '.png']
        return any(image_url.lower().endswith(ext) for ext in valid_extensions)