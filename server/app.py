from flask import request, session, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import db
from models import User

class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        image_url = data.get('image_url', '')
        bio = data.get('bio', '')

        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'error': 'Username already taken'}, 422

        new_user = User(username=username, image_url=image_url, bio=bio)
        new_user.password = password

        try:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return new_user.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Could not create user'}, 422




