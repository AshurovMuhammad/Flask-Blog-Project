import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from UserLogin import UserLogin
from admin.admin import admin

# конфигурация
DATABASE = '/tmp/flsk.db'
DEBUG = True
SECRET_KEY = '995e72cddc5798dcfaa7f771b63a98aafa8486bf'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsk.db')))
app.register_blueprint(admin, url_prefix="/admin")

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым стариницам"
login_manager.login_message_category = "success"


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route("/")
def index():
    return render_template("index.html", title="Главная", menu=dbase.get_menu(), posts=dbase.get_post_anonce())


@app.route("/add_post", methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.add_post(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash("Ошибка добавления статьи", category='error')
            else:
                flash("Статья добавлена успешно", category='success')
        else:
            flash("Ошибка добавления статьи", category='error')

    return render_template("add_post.html", title="Добавление статьи", menu=dbase.get_menu())


@app.route("/post/<alias>")
@login_required
def show_post(alias):
    title, post = dbase.get_post(alias)
    if not title:
        abort(404)

    return render_template("post.html", title=title, post=post, menu=dbase.get_menu())


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        user = dbase.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(request.args.get("next") or url_for('profile'))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", menu=dbase.get_menu(), title="Авторизация")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 and len(request.form['psw']) > 4 and \
                request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.add_user(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for("login"))
            else:
                flash("Ошибка при добавлении в БД", "error")

    return render_template("register.html", menu=dbase.get_menu(), title="Регистрация")


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().from_db(user_id, dbase)


@app.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    return render_template("profile.html", menu=dbase.get_menu(), title="Профиль")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/userava')
@login_required
def userava():
    img = current_user.get_avatar(app)
    if not img:
        return ""

    h = app.make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verify_ext(file.filename):
            try:
                img = file.read()
                res = dbase.update_user_avatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка обновления аватара", "error")
        else:
            flash("Ошибка обновления аватара", "error")
    return redirect(url_for('profile'))


# @app.route("/about")
# def about():
#     return render_template("about.html", title="О нас", menu=[])
#
#
# @app.route("/contact", methods=["POST", "GET"])
# def contact():
#     if request.method == 'POST':
#         if len(request.form['username']) > 2:
#             flash("Сообщение отправлено успешно!", category='success')
#         else:
#             flash("Ошибка отправки", category='error')
#     return render_template("contact.html", title="Обратная связь", menu=[])
#
#
# @app.route("/profile/<path:username>")
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f"Пользователь: {username}"
#
#
# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == 'admin' and request.form['passw'] == '123456':
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#
#     return render_template('login.html', title="Авторизация", menu=[])
#
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page404.html', title="Страница не найдена", menu=[])

if __name__ == "__main__":
    app.run(debug=True)

# # 75-dars. Flask framework // 51 // 77-videoni 2:20:00 vaqtidan boshlangan
#
# # from flask import Flask, render_template
# #
# # app = Flask(__name__)
# #
# #
# # @app.route("/")
# # def index():
# #     return render_template('index.html')
# #
# #
# # @app.route("/about")
# # def about():
# #     return render_template('about.html')
# #
# #
# # if __name__ == "__main__":
# #     app.run(debug=True)
# # ======================================================================================================================
#
# # 76-dars. Flask framework // 52 // 78
#
# from flask import Flask, render_template, url_for, request, flash, session, \
#     redirect, abort, g
# import sqlite3
# import os
# from FDataBase import FDataBase
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import LoginManager, login_user, login_required, current_user, logout_user
# from UserLogin import UserLogin
#
# # Konfiguratsiya
# DATABASE = '/tmp/flsk.db'
# DEBUG = True
# SECRET_KEY = '3e318b46796d9f7a141cf2db90f613dc8574533'
# MAX_CONTENT_LENGTH = 1024 * 1024
#
# app = Flask(__name__)
# app.config.from_object(__name__)
#
# # ma'lumotlar bazasi bizni asosiy loyihamiz ildizzida yaratish uchun
# app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsk.db')))
#
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message = 'Avtorizuytes dlya dostupa k zakritim stranitsam'
# login_manager.login_message_category = 'success'
#
#
# # Ma'lumotlar bazasini yaratib oldim
# def connect_db():
#     con = sqlite3.connect(app.config['DATABASE'])
#     con.row_factory = sqlite3.Row
#     return con
#
#
# def create_db():
#     db = connect_db()
#     with app.open_resource('sq_db.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#     db.close()
#
#
# # ma'lumotlar bazasiga ulab beradigon finksiya
# def get_db():
#     if not hasattr(g, "link_db"):
#         g.link_db = connect_db()
#     return g.link_db
#
#
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'link_db'):
#         g.link_db.close()
#
#
# dbase = None
#
#
# @app.before_request
# def before_request():
#     global dbase
#     db = get_db()
#     dbase = FDataBase(db)
#
#
# # menu = [{"name": "Bosh sahifa", "url": "index"},
# #         {"name": "Biz haqimizda", "url": "about"},
# #         {"name": "Kontaklar", "url": "contact"}]
#
# # Bosh sahifa
# @app.route("/")
# def index():
#     return render_template('index.html', title="Bosh sahifa", menu=dbase.get_menu(), posts=dbase.get_post_annonce())
#
#
# @app.route('/add_post', methods=["POST", "GET"])
# def add_post():
#     if request.method == "POST":
#         if len(request.form['name']) > 4 and len(request.form['post']) > 10:
#             res = dbase.add_post(request.form['name'], request.form['post'], request.form['url'])
#             if not res:
#                 flash("Oshibka pri dobavleniya sytatyi", category='error')
#             else:
#                 flash("Statya dobavlena uspeshno", category='success')
#         else:
#             flash("Oshibka pri dobavleniya sytatyi", category='error')
#
#     return render_template('add_post.html', title='Dobavleniya statiy', menu=dbase.get_menu())
#
#
# @app.route("/post/<alias>")
# @login_required
# def show_post(alias):
#     title, post = dbase.get_post(alias)
#     if not title:
#         abort(404)
#     return render_template('post.html', title=title, post=post, menu=dbase.get_menu())
#
#
# @app.route("/login", methods=['POST', 'GET'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('profile'))
#     if request.method == "POST":
#         user = dbase.get_user_by_email(request.form['email'])
#         if user and check_password_hash(user['psw'], request.form['psw']):
#             user_login = UserLogin().create(user)
#             login_user(user_login)
#             return redirect(request.args.get("next") or url_for('profile'))
#
#         flash("Neenaya para login/parol", 'error')
#
#     return render_template("login.html", menu=dbase.get_menu(), title='Avtorizatsiya')
#
#
# @app.route("/register", methods=["POST", "GET"])
# def register():
#     if request.method == "POST":
#         if len(request.form['name']) > 4 and len(request.form['email']) > 4 and \
#                 len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
#             hash = generate_password_hash(request.form['psw'])
#             res = dbase.add_user(request.form['name'], request.form['email'], hash)
#             if res:
#                 flash("Vi uspeshno zaregistrluvali", "success")
#                 return redirect(url_for("login"))
#             else:
#                 flash("Oshibka dobavlenii!", 'error')
#
#     return render_template("register.html", menu=dbase.get_menu(), title='Registratsiya')
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     print("load_user")
#     return UserLogin().from_db(user_id, dbase)
#
#
# @app.route('/profile')
# @login_required
# def profile():
#     return render_template("profile.html", menu=dbase.get_menu(), title='Profil')
#
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash("Vi vishli iz accaunta", 'success')
#     return redirect(url_for("login"))
#
#
# @app.route('/userava')
# @login_required
# def userava():
#     img = current_user.get_avatar(app)
#     if not img:
#         return ""
#
#     h = app.make_response(img)
#     h.headers['Content-Type'] = 'image/png'
#     return h
#
#
# # # Sayt haqida
# # @app.route("/about")
# # def about():
# #     return render_template('about.html', title="Sayt haqida", menu=[])
# #
# #
# # # Kontakt
# # @app.route("/contact", methods=["POST", "GET"])
# # def contact():
# #     if request.method == "POST":
# #         if len(request.form['username']) > 2:
# #             flash("Habar muvoffaqiyatlik yuborildi", category='success')
# #         else:
# #             flash("Xatolik roy berdi !", category='error')
# #
# #         # print(request.form)
# #         # context = {
# #         #     'username': request.form['username'],
# #         #     'email': request.form['email'],
# #         #     'message': request.form['message']
# #         # }
# #         # return render_template("contact.html", **context, title="Kontaktlar", menu=menu)
# #
# #     return render_template("contact.html", title="Konataktlar", menu=[])
# #
# #
# # # Prifil
# # @app.route("/profile/<path:username>")
# # def profile(username):
# #     if 'userLogged' not in session or session['userLogged'] != username:
# #         abort(401)
# #     return f"Foydalanuvchi: {username}"
# #
# #
# # # Login sahifasi
# # @app.route("/login", methods=['POST', 'GET'])
# # def login():
# #     if 'userLogged' in session:
# #         return redirect(url_for('profile', username=session['userLogged']))
# #     elif request.method == "POST" and request.form['username'] == 'admin' and request.form['passw'] == '123456':
# #         session['userLogged'] = request.form['username']
# #         return redirect(url_for('profile', username=session['userLogged']))
# #     return render_template('login.html', title='Avtorizatsiya', menu=[])
# #
# #
# # # with app.test_request_context():
# # #     print(url_for('index'))
# # #     print(url_for('about'))
# # #     print(url_for('profile', username='ashurov'))
# #
# #
# # # Hato sahifani kiritganda
# # @app.errorhandler(404)
# # def page_notfound(error):
# #     return render_template('page404.html', title="Sahifa topilmadi", menu=[])
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
