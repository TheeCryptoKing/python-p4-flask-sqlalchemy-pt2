from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
#  MetaData is a class provided by SQLAlchemy to manage database metadata and naming conventions.

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
# This line creates an instance of MetaData and sets a naming convention for foreign keys in the database. The naming convention specified in the dictionary will be used to generate names for foreign key constraints.

db = SQLAlchemy(metadata=metadata)

class Owner(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    pets = db.relationship('Pet', backref='owner')

    def __repr__(self):
        return f'<Pet Owner {self.name}>'

class Pet(db.Model):
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)

    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))

    def __repr__(self):
        return f'<Pet {self.name}, {self.species}>'

