from flask import Flask, render_template, session, redirect, request, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, connect_db, User, Link
from os import environ, path
from dotenv import load_dotenv
from forms import SignUpForm, LoginForm, EditProfileForm, AddLink
import json
import requests
import pdb

app = Flask(__name__, template_folder = "templates")

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['SQLALCHEMY_ECHO'] = environ.get("SQLALCHEMY_ECHO")
app.config['SESSION_TYPE'] = environ.get("SESSION_TYPE")

TOKEN = environ.get("TOKEN")
#connect to db
connect_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.app_context().push()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def homepage():
    """show home page"""
    return render_template('base.html')

@app.route('/', methods = ['POST'])
def shorten_link():
    """show home page"""
    link = request.form["link"]

    print(link)

    data = { "url": link}
    """
    headers = {
        'Authorization': 'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    }

    data = '{ "long_url": "https://dev.bitly.com", "domain": "bit.ly", "group_guid": "Ba1bc23dE4F" }'

    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    print(response)
    pdb.set_trace()
    """
    response = requests.post('https://cleanuri.com/api/v1/shorten', data).json()

    if response.get('result_url'):
        return render_template('save_shortened.html', link=response['result_url'])
    elif response.get('error'):
        flash(f"{response['error']}", 'error')
    else:
        flash('Error in shortening link, try again or contact support', 'error')


    return redirect('/')

@app.route('/link/short/add', methods=["POST"])
@login_required
def handle_add_shortink():
    """Handle new shortlink"""

    new_link = Link(
            link = request.form["link"],
            platform = request.form["platform"],
            user_id = current_user.get_id()
        )

    db.session.add(new_link)
    db.session.commit()

    return redirect('/links')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Show form for organizations to sign up and if already sign"""
    form = SignUpForm()
    if form.validate_on_submit():
        """Get form data and add organization to database"""
        try:
            user = User.signup(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                email = form.email.data,
                password=form.password.data
            )

            if user:
                db.session.commit()

        except Exception as e:
            if 'user_email_key' in str(e):
                flash("Email already registered", 'error')
            else:
                flash("Error in creating account, please try again", 'error')

            return render_template('signup.html', form=form)

        return redirect(url_for('login'))
    else:
        """show form"""
        return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show form for user to login """
    form = LoginForm()
    if form.validate_on_submit():
        """Get form data and add to database"""
        user = User.authenticate(
            email = form.email.data,
            password=form.password.data
        )

        if user:
            login_user(user)
        else:
            flash('Invalid email or password', 'error')
            return redirect('/')

        return redirect('/links')
    else:
        """show form"""
        return render_template('/login.html', form=form)

@app.route('/links')
@login_required
def show_links():
    """show all links"""
    links = Link.query.filter_by(user_id = current_user.get_id()).all()
    return render_template('/show_links.html', links=links)

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def show_profile():
    """show profile page for organization and edit"""
    user = User.query.get(current_user.get_id())

    return render_template('profile.html', user = user)

@app.route('/profile/edit', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    """show profile page for organization and edit"""
    user = User.query.get(current_user.get_id())
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        #get form data and save to database and redirect to profile overview
        user.first_name = form.first_name.data,
        user.last_name = form.last_name.data,
        user.email = form.email.data

        db.session.commit()
        flash('Profile successfully edited', 'success')
        return redirect('/profile')
    else:
        return render_template('edit_profile.html', form=form)


@app.route('/links/add', methods=['GET', 'POST'])
@login_required
def add_link():
    """Show form for user to add link """
    form = AddLink()
    if form.validate_on_submit():
        """Get form data and add to database"""
        new_link = Link(
            platform = form.platform.data,
            link=form.link.data,
            user_id = current_user.get_id()
        )

        db.session.add(new_link)
        db.session.commit()

        return redirect('/links')
    else:
        """show form"""
        return render_template('/add_links.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')