import sqlite3
import time
import math
import re
from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = 'SELECT * FROM mainmenu'
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except IOError:
            print("Ошибка чтения из БД")
        return []

    def add_post(self, title, text, url):
        try:
            self.__cur.execute("SELECT COUNT() as 'count' FROM posts WHERE url LIKE ?", (url,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Статья с таким url уже существует")
                return False
            base = url_for('static', filename='images')
            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>", r"\g<tag>" + base +
                          r"/\g<url>>", text)
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    def get_post(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))

        return False, False

    def get_post_anonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))

        return []

    def add_user(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def update_user_avatar(self, avatar, user_id):
        if not avatar:
            return False
        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True












# import sqlite3
# import time
# import math
# import re
# from flask import url_for
#
#
# class FDataBase:
#     def __init__(self, db):
#         self.__db = db
#         self.__cur = db.cursor()
#
#     def get_menu(self):
#         sql = 'SELECT * FROM mainmenu'
#         try:
#             self.__cur.execute(sql)
#             res = self.__cur.fetchall()
#             if res:
#                 return res
#         except IOError:
#             print("Oshibka chteniya baza dannix")
#         return []
#
#     def add_post(self, title, text, url):
#         try:
#             self.__cur.execute("SELECT COUNT() as 'count' FROM posts WHERE url LIKE ?", (url,))
#             res = self.__cur.fetchone()
#             if res['count'] > 0:
#                 print("Statya s takim url uje sushestvuet!")
#                 return False
#             base = url_for('static', filename='images')
#             text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
#                           r"\g<tag>" + base + r"/\g<url>>", text)
#             tm = math.floor(time.time())
#             self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
#             self.__db.commit()
#
#         except sqlite3.Error as e:
#             print("Oshibka dabvleniya syayty v bazu dannix" + str(e))
#             return False
#         return True
#
#     def get_post(self, alias):
#         try:
#             self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
#             res = self.__cur.fetchone()
#             if res:
#                 return res
#         except sqlite3.Error as e:
#             print("Oshibka dabvleniya syayty v bazu dannix" + str(e))
#
#         return False, False
#
#     def get_post_annonce(self):
#         try:
#             self.__cur.execute(f'SELECT id, title, text, url FROM posts ORDER BY time DESC')
#             res = self.__cur.fetchall()
#             if res:
#                 return res
#         except sqlite3.Error as e:
#             print("Oshibka dabvleniya syayty v bazu dannix" + str(e))
#
#         return []
#
#     def add_user(self, name, email, hpsw):
#         try:
#             self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
#             res = self.__cur.fetchone()
#             if res['count'] > 0:
#                 print("Polzovatel s takim email uje sushestvuet!")
#                 return False
#
#             tm = math.floor(time.time())
#             self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (name, email, hpsw, tm))
#             self.__db.commit()
#
#         except sqlite3.Error as e:
#             print("Oshibka dabvleniya syayty v bazu dannix" + str(e))
#             return False
#
#         return True
#
#     def get_user(self, user_id):
#         try:
#             self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
#             res = self.__cur.fetchone()
#             if not res:
#                 print("Polzovatel ne nayden")
#                 return False
#             return res
#         except sqlite3.Error as e:
#             print("Oshibqa pri polucheniya dannix iz baza dannix" + str(e))
#
#         return False
#
#     def get_user_by_email(self, email):
#         try:
#             self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
#             res = self.__cur.fetchone()
#             if not res:
#                 print("Polzovatel ne nayden")
#                 return False
#             return res
#         except sqlite3.Error as e:
#             print("Oshibqa polucheniya dannix iz baza dannix" + str(e))
#
#         return False