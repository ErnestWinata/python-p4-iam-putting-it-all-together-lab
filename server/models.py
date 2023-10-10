from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    _password_hash = Column('password', String, nullable=False)
    image_url = Column(String)
    bio = Column(String)
    
    @hybrid_property
    def password(self):
        return self._password_hash
    
    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')
    
    def authenticate(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)

    recipes = relationship('Recipe', backref='user', lazy=True)

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    instructions = Column(String, nullable=False)
    minutes_to_complete = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

