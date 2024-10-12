from flask import Flask, Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User, DeviceInformation
from . import db
import json

# Create the Flask app instance
app = Flask(__name__)

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # providing the schema for the note
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)  # adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # this function expects a JSON from the INDEX.js file
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()


@app.route('/user/<int:user_id>')
def get_user_data(user_id):
    # Fetch the user by their ID
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return "User not found", 404

    # Fetch the associated device information (if any)
    device = DeviceInformation.query.filter_by(user_id=user.id).first()

    # Pass both user and device data to the template
    return render_template('about.html', user=user, device=device)

    # Register your views Blueprint with the Flask app
    app.register_blueprint(views)


if __name__ == '__main__':
    app.run(debug=True)
