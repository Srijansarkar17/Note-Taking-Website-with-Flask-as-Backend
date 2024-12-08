from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

#Functionalities - Login, Logout, SignUp

@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #filter the first user that have this email in the database, but there will be only one user with that email
        if user: #if user is found
            if check_password_hash(user.password, password): #we compare and check the password which the user has typed with the password of the user that has been filtered
                flash('Logged In sucessfully', category='success')
                login_user(user, remember=True) #remembers that the user is logged in until the user clears browsing history or session
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('User not found!', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required   #does not let the user logout until he is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login')) #bring the user back to the login page

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method=='POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() #if the email is already there, then the below message is shown
        if user:
            flash('User already exists', category='error')
        elif len(email) < 4:
            #We write the code to show up these messages in base.html form
            flash('Email must be greater than 3 characters.', category='error') #flashes a message on the screen when something goes wrong

        elif len(firstname) < 2:
            flash('First name must be greater than 1 character', category='error')

        elif password1!=password2:
            flash('The passwords do not match', category='error')
        
        elif len(password1) < 7:
            flash('The password must be atleast 7 characters', category='error')

        else:
            #Creating Account
            new_user = User(email=email, first_name=firstname, password = generate_password_hash(password1, method='pbkdf2:sha256')) #we hash the password with the hashing algorithm of 'sha256'
            ##adding the new_user to the database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            #After signup, redirecting them to the homepage
            return redirect(url_for('views.home'))  #inside views.py we have the home function; so blueprint name.function name
    return render_template("signup.html", user=current_user)