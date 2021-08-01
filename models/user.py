import sqlite3
from flask_restful import Resource, reqparse
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def find_by_username(cls, username):
        # connection = sqlite3.connect('C:/Users/hb21315/PycharmProjects/test/rest-apis-flask-python-master\section_6_test/assign/data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username,))
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        #
        # return user
        return cls.query.filter_by(username=username).first()

    def save_to_db(self):
        # connection = sqlite3.connect(
    #         #     'C:/Users/hb21315/PycharmProjects/test/rest-apis-flask-python-master/section_6_test/assign/data.db')
    #         # cursor = connection.cursor()
    #         #
    #         # query = "INSERT INTO items VALUES(?, ?)"
    #         # cursor.execute(query, (self.name, self.price))
    #         #
    #         # connection.commit()
    #         # connection.close()
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        # connection = sqlite3.connect('C:/Users/hb21315/PycharmProjects/test/rest-apis-flask-python-master/section_6_test/assign/data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE email=?"
        # result = cursor.execute(query,
        #                         (email,))  # create tuple with brackets (,) and comma after item - tuple needed in query
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)  # expands row, same as row[0], row[1], row[2]
        # else:
        #     user = None
        #
        # connection.close()
        # return user
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        # connection = sqlite3.connect('C:/Users/hb21315/PycharmProjects/test/rest-apis-flask-python-master/section_6_test/assign/data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id,))
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        #
        # return user
        return cls.query.filter_by(id=_id).first()