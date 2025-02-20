import os
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)


DATABASE_USER = os.getenv('POSTGRES_USER', 'username')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
DATABASE_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DATABASE_NAME = os.getenv('POSTGRES_NAME', 'name')

DATABASE_URI = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URI)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


Session = sessionmaker(bind=engine)
session = Session()


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Pong!"}), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()
    return jsonify([user.to_dict() for user in users]), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = session.query(User).get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or not all(key in data for key in ("name", "email")):
        return jsonify({"error": "Invalid input"}), 400

    new_user = User(name=data["name"], email=data["email"])
    try:
        session.add(new_user)
        session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 409


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]

    try:
        session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 409


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    session.delete(user)
    session.commit()
    return jsonify({"message": "User deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT', 8080), host=os.getenv('HOST', '0.0.0.0'))