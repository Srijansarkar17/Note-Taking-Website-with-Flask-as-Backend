from . import db #we are importing from the current package(website folder), because models is located inside the website folder itself
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model): #to store the Notes
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #each user has different notes, so for that we need a foreign key, this references the table 'User' and 'id is the primary key of the User table
    #this foreign key is a one-to-many relationship means one user having many notes


#we are inheritting the user class from db.model and UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.Relationship('Note')

