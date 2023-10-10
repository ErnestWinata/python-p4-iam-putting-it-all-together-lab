from flask import request, session, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
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

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            return user.to_dict(), 200
        else:
            return {'error': 'Unauthorized'}, 401

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {'error': 'Unauthorized'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {'message': 'Logged out successfully'}, 200

class RecipeIndex(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            recipes = Recipe.query.filter_by(user_id=user_id).all()
            return [recipe.to_dict() for recipe in recipes], 200
        else:
            return {'error': 'Unauthorized'}, 401

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')

if __name__ == '__main__':
    app.run()

