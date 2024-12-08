#Any page except login page which the user can navigate to is put in this file. The login page will be put in the auth.py file

from flask import Blueprint, render_template, request, redirect, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

#In Flask, a Blueprint is a way to organize your application into smaller, modular components. It allows you to create reusable pieces of an application that can be registered later in the main app
#This file just has a bunch of urls defined in it

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) #Home page, this is a Blueprint and we need to register these blueprints in our __init__.py file
@login_required #we cannot get to the home page unless we are logged in
def home():
    if request.method == "POST":
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/deleteNote', methods=['POST'])
def delete_note():
    note = json.loads(request.data) #takes in data from the post request, loads as a python dictionary
    note_id = note['noteId'] #access the noteid attribute
    note = Note.query.get(note_id) #look for the note with the noteid
    if note: #then check if that note exists
        if note.user_id == current_user.id: #if the note exists, then we check if the user signed in does own this note
            db.session.delete(note)
            db.session.commit()
    return jsonify({})