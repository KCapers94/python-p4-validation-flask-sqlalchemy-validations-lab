from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name', 'phone_number')
    def validate_author(self, key, input):
        if key == 'name':
            if input == "":
                raise ValueError("Invalid Input")
            if Author.query.filter_by(name=input).first():
                raise ValueError("Name must be unique")

        elif key == 'phone_number':
            if len(input) != 10 or not input.isdigit():
                raise ValueError("Phone number must be 10 digits")
    
        return input
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('content', 'summary', 'category', 'title')
    def post_validations(self, key, input):
        all_titles = ["Won't Believe", "Secret", "Top", "Guess"]

        if key == 'content':
            if len(input) < 250:
                raise ValueError('Content needs to be 250 characters or more')
        elif key == 'summary':
            if len(input) > 250:
                raise ValueError('Summary can be a maximum of 250 characters')
        elif key == 'category':
            if input not in ('Fiction', 'Non-Fiction'):
                raise ValueError('Category must be Fiction or Non-Fiction')
        elif key == 'title':
            if not any(title in input for title in all_titles):
                raise ValueError("Title must include 'Won't Believe', 'Secret', 'Top', or 'Guess'")

        return input

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
