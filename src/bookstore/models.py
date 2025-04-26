from .extensions import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"<Book {self.title} by {self.author}"

    def to_dict(self):
        """
        Convert to dictionary
        :return: dictionary of book object
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'price': self.price,
            'description': self.description
        }
