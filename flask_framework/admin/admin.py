from flask import Blueprint, request, render_template, url_for, redirect, flash, session, g
import sqlite3

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def is_logged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [
    {'url': '.index', 'title': 'Панель'},
    {'url': '.listuser', 'title': 'Список пользователей'},
    {'url': '.listpubs', 'title': 'Список статей'},
    {'url': '.logout', 'title': 'Выйти'}
]

db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    if not is_logged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title="Админ-панель")


@admin.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))  # admin.index == .index
        else:
            flash("Неверная пара логин/пароль", "error")

    return render_template('admin/login.html', title="Админ-панель")


@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if not is_logged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))


@admin.route('/list-pubs')
def listpubs():
    if not is_logged():
        return redirect(url_for('.login'))

    lst = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text, url FROM posts")
            lst = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('admin/listpubs.html', title="Список статей", menu=menu, list=lst)


@admin.route('/list-user')
def listuser():
    if not is_logged():
        return redirect(url_for('.login'))

    lst = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            lst = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения пользователей из БД " + str(e))

    return render_template('admin/listuser.html', title="Список пользователей", menu=menu, list=lst)