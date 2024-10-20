from flask import Flask, Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .models import Note, User, DeviceInformation, EgramData, PacemakerStatus
from . import db
import json

# Create the Flask app instance
app = Flask(__name__)

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    # Fetch the latest status from the database
    latest_status = PacemakerStatus.query.order_by(PacemakerStatus.id.desc()).first()
    current_status = latest_status.status if latest_status else "Out of Range"

    # Map the status to a corresponding CSS class for styling
    status_class = {
        "Connected": "connected",
        "Out of Range": "out-of-range",
        "Noise": "noise",
        "Another Device Detected": "another-device"
    }.get(current_status, "out-of-range")  # Default to 'out-of-range' if unknown

    # Render the template with user and pacemaker status
    return render_template(
        "home.html",
        user=current_user,  # Pass the current user object
        pacemaker_status=current_status,
        pacemaker_status_class=status_class
    )

@views.route('/user/<int:user_id>')
def get_user_data(user_id):
    # Function implementation here
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

@app.route('/set_clock', methods=['GET'])
def set_clock():
    # Get the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')

    # Render the HTML template with the current date and time
    return render_template('set_clock.html', current_date=current_date, current_time=current_time)

@views.route('/view_egram', methods=['GET'])
@login_required  # This ensures that the user is logged in
def view_egram():
     # Get the current date and time using the helper function
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    # Sample static data for demonstration
    egram_data = [
        {'timestamp': current_date , 'signal_value': 1.5, 'event_marker': 'AS'},
        {'timestamp': current_date, 'signal_value': 2.3, 'event_marker': 'AP'},
        {'timestamp': current_date, 'signal_value': 1.8, 'event_marker': 'VS'},
        {'timestamp': current_date, 'signal_value': 2.0, 'event_marker': 'VP'}
    ]
    # Render the HTML template with the Egram data, current user, and current date/time
    return render_template('view_egram_data.html', egram_data=egram_data, user=current_user, 
                           current_date=current_date, current_time=current_time)

@views.route('/update_status/<new_status>')
def update_status(new_status):
    # Validate the new status
    if new_status not in ["Connected", "Out of Range", "Noise", "Another Device Detected"]:
        return "Invalid status", 400

    # Create a new PacemakerStatus entry in the database
    new_entry = PacemakerStatus(status=new_status)
    db.session.add(new_entry)
    db.session.commit()

    return f"Status updated to {new_status}", 200

if __name__ == '__main__':
    app.run(debug=True)
