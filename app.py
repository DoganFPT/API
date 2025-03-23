from flask import Flask, render_template, request, redirect, url_for,jsonify
from dotenv import load_dotenv
import jwt
import os
import bcrypt
import datetime

app = Flask(__name__)

#keep this hidden
SECRET_KEY = your_private_key

#dummy data for testing eventually will use a db for this
users = {
    "user1" : {"password": "password1", "role" : "admin"},
    "user2" : {"password": "password2", "role" : "user"}
}



@app.route("/login", methods = ["POST"])

def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)

    if user and user["password"] == password:
        payload = {
            "role": user["role"],    
            "sub" : username,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify({"token":token})
    return jsonify({"message":"invalid credentials"})


def token_req(f):
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "missing Token"})

        try:
            if token.startswith("Bearer "):
                token= token[7:]

            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_role = decoded["role"]
            current_user = decoded["sub"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"})
        except jwt.InvalidTokenError:
            return jsonify({"message" : "invalid token"})

        return f(current_user,user_role, *args, **kwargs)
    return decorator

@app.route("/protected",methods=["GET"])
#makes sure you have a token
@token_req

def protected(current_user):
    return jsonify({"message": f"Welcome, {current_user} You have access to this resource."})

@app.route("/admin", methods=["GET"])
@token_req
def admins(current_user, user_role):
    if user_role != "admin":
        return jsonify({"not an admin"})
    return jsonify({f"Welcome {curren_user} You have access to admin resources."})


if __name__ == "__main__":
    app.run(debug=True)

