import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self,_id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def findByUsername(cls, username):
        connection = sqlite3.connect("usersDatabase.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user


    @classmethod
    def findByUserid(cls, _id):
        connection = sqlite3.connect("usersDatabase.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user



    class UserRegister(Resource):
        parser = reqparse.RequestParser()
        parser.add_argument("username",
            type = str,
            required = True,
            help = "username is required"
        )
        parser.add_argument("password",
        type = str,
        required = True,
        help = "password is required"
        )
        def post(self):
            data = UserRegister.parser.parse_args()
            connection = sqlite3.connect("usersDatabase.db")
            cursor = connection.cursor()

            query = "INSERT INTO users VALUES (NULL , ?, ?)"
            cursor.execute(query,(data["username"],data["password"]))

            connection.commit()
            connection.close()

            return {"message": "successfully added"},201
