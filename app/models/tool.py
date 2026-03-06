from app.extensions import db

class Tool(db.Model):
    __tablename__ = 'tools'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    imgUrl = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'url': self.url,
            'imgUrl': self.imgUrl,
            'content': self.content
        }