import sqlite3
import os
from FDataBase import FDataBase
from flask import Flask, render_template, url_for, request, \
    flash, session, redirect, abort, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from UserLogin import UserLogin

# Configurations
DATABASE = '/tmp/flsk.db'
DEBUG = True
SECRET_KEY = '76a8f48df9e554102d0dbe84ca01574661cd3d3b'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsk.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Log in to access restricted pages"
login_manager.login_message_category = 'success'


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


# menu = [{'name': "Home", 'url': 'index'},
#         {'name': "Python projects", 'url': "project"},
#         {'name': 'About', 'url': "about"},
#         {'name': 'Contact', 'url': 'contact'}]


@app.route('/')
def index():
    return render_template('index.html', menu=dbase.get_menu(), title="Home Page", posts=dbase.get_post_annonce())


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.add_post(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash("Error adding post!", category='error')
            else:
                flash("Post added successfully", category='success')
        else:
            flash("Error adding post!", category='error')

    return render_template('add_post.html', menu=dbase.get_menu(), title="Add Post")


@app.route("/post/<alias>")
@login_required
def show_post(alias):
    title, post = dbase.get_post(alias)
    if not title:
        return render_template('page404.html', menu=dbase.get_menu(), title='Page not found')

    return render_template('post.html', menu=dbase.get_menu(), title=title, post=post)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        user = dbase.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(request.args.get("next") or url_for('profile'))
        flash("Invalid username/password pair!", 'error')
    return render_template('login.html', menu=dbase.get_menu(), title='Log In')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 and \
                len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.add_user(request.form['name'], request.form['email'], hash)
            if res:
                flash("You have successfully registered", 'success')
                return redirect(url_for('login'))
            else:
                flash("Error while adding to db", 'error')

    return render_template('signup.html', menu=dbase.get_menu(), title='Sign Up')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out", "success")
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().from_db(user_id, dbase)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', menu=dbase.get_menu(), title='Profile')


@app.route('/userava')
@login_required
def userava():
    img = current_user.get_avatar(app)
    if not img:
        return ""
    h = app.make_response(img)
    h.headers["Content-Type"] = 'image/png'
    return h


# @app.route('/about')
# def about():
#     return render_template('about.html', menu=[], title='About')
#
#
# @app.route('/profile/<path:username>')
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f"User {username}"
#
#
# @app.route('/contact', methods=["POST", "GET"])
# def contact():
#     if request.method == "POST":
#         # print(request.form)  # ImmutableMultiDict([('username', 'Muhammad'), ('email', 'muhammaddiyorashuro5@gmail.com'), ('message', 'sss')])
#         # print(request.form['username'])  # Muhammad
#         if len(request.form['username']) > 2:
#             flash("Successfully", category='success')
#         else:
#             flash("Error, something is wrong!", category='error')
#         context = {
#             'username': request.form['username'],
#             'email': request.form['email'],
#             'message': request.form['message']
#         }
#         return render_template('contact.html', menu=[], title='Contact', **context)
#     return render_template('contact.html', menu=[], title='Contact')
#
#
# @app.route('/project')
# def projects():
#     return render_template('project.html', menu=[], title='Project')
#
#
# @app.route('/login', methods=["POST", 'GET'])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == "POST" and request.form['username'] == 'Muhammad' and request.form['passw'] == '123456':
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#     return render_template('login.html', menu=[], title='Log In')
#
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page404.html', menu=[], title='Page not found')
#
#
# # with app.test_request_context():
# #     print(url_for('index'))
# #     print(url_for('about'))
# #     print(url_for('contact'))


if __name__ == '__main__':
    app.run(debug=True)
