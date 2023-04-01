import sqlite3

from flask_login import UserMixin
from flask import url_for


class UserLogin(UserMixin):
    def from_db(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def get_name(self):
        return self.__user['name'] if self.__user else "No name"

    def get_email(self):
        return self.__user['email'] if self.__user else "No email"

    def get_avatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for("static", filename='images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Default avatar not found: " + str(e))
        else:
            img = self.__user['avatar']

        return img
