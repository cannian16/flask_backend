from app.extensions import db

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    website_url = db.Column(db.String(200))
    content = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'website_url': self.website_url,
            'content': self.content,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }