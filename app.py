from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, User,dailyrecord,UserProfile  #  healthrecords is also defined in models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/AyuCare_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Required for session management

db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/home")
def home():
    user_id = session.get('user_id')  # Retrieve the logged-in user's ID from the session
    

    if user_id:
        user = User.query.get(user_id)  # Query the User model to get the user
        if user:
            username = user.username  # Get the username from the user object

    return render_template("index.html", username=username)

@app.route('/test-db')
def test_db():
    try:
        db.session.execute('SELECT 1')  # Simple test query
        return "Database is working!"
    except Exception as e:
        return f"Database connection failed: {e}"



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        identifier = request.form['identifier']  # Could be email or username
        password = request.form['password']

        # Check if the user exists in the database by email or username
        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()

        if user and user.check_password(password):
            # If user exists and password matches, sign in
            session['user_id'] = user.id
            session['email'] = user.email
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            # If user does not exist or password doesn't match, show error
            flash('Invalid email or username or password. Please try again or register if you are a new user.')
            return redirect(url_for('signin'))

    return render_template('signin.html')





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Debug info
        print(f"Received POST request: Username: {username}, Email: {email}, Password: {password}")

        # Check if all fields are filled
        if not username or not email or not password:
            print("Error: Missing required fields")
            return "All fields are required."

        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            print("Error: Username or email already exists.")
            return "Username or email already exists."

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            print("User successfully registered and added to the database.")
            # Redirect to the signin page after successful registration
            return redirect(url_for('signin'))
        
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            print(f"Database Error: {e}")  # More detailed error output
            return "Registration failed. Please try again."

    return render_template('register.html')


@app.route('/profile')
def profile():
    user_id = session.get('user_id')  # Get the logged-in user ID from the session
    
    if not user_id:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('signin'))
    
    # Fetch the user from the User model
    user = User.query.get(user_id)
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('signin'))
    
    # Fetch the user profile
    user_profile = UserProfile.query.filter_by(user_id=user_id).first()

    return render_template('profile.html', user=user, user_profile=user_profile)





@app.route('/profile_edit', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')  # Ensure user is logged in and get user_id from session

    # Fetch the user's profile
    user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    
    if not user_profile:
        flash('Profile not found.', 'danger')
        return redirect(url_for('profile'))  # Redirect to profile if no profile exists

    if request.method == 'POST':
        # Get data from form
        user_profile.phone_number = request.form['phone_number']
        user_profile.age = request.form['age']
        user_profile.weight = request.form['weight']
        user_profile.address = request.form['address']
        user_profile.bio = request.form['bio']
        
        # Update the 'updated_at' field
        user_profile.updated_at = datetime.now()

        # Commit changes to the database
        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    # Render the edit profile template with the current user profile data
    return render_template('profile_form.html', user_profile=user_profile)

@app.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    user_id = session.get('user_id')  # Get the logged-in user's ID

    if not user_id:
        flash('You need to be logged in to create a profile.', 'danger')
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Check if the user already has a profile
    user_profile = UserProfile.query.filter_by(user_id=user_id).first()
    if user_profile:
        flash('Profile already exists. You can edit it instead.', 'warning')
        return redirect(url_for('edit_profile'))

    if request.method == 'POST':
        # Collect data from the form
        phone_number = request.form['phone_number']
        age = request.form['age']
        weight = request.form['weight']
        address = request.form['address']
        bio = request.form['bio']

        # Create a new profile record
        new_profile = UserProfile(
            user_id=user_id,
            phone_number=phone_number,
            age=age,
            weight=weight,
            address=address,
            bio=bio
        )

        # Save to the database
        db.session.add(new_profile)
        db.session.commit()

        flash('Profile created successfully!', 'success')
        return redirect(url_for('profile'))  # Redirect to the profile view

    # Render the form for adding a new profile
    return render_template('profile_form.html', user_profile=None)






@app.route('/records', methods=['GET', 'POST'])
def records():
    if 'user_id' not in session:  # Ensure user is logged in
        return render_template('records.html')
    else:
     user_id = session['user_id']  # Get the logged-in user's ID
     user = User.query.get(user_id)
     return render_template("records.html",username=user.username)
    



@app.route("/daily_record", methods=['GET', 'POST'])
def daily_record():
    if 'user_id' not in session:  # Ensure the user is logged in
        return redirect(url_for('signin'))  # Redirect to the sign-in page

    if request.method == 'POST':
        record_type = request.form.get('record_type')

        # Prepare to save data based on selected record type
        if record_type == 'bp':
            systolic = request.form.get('systolic')
            diastolic = request.form.get('diastolic')
            new_record = dailyrecord(
                title='Blood Pressure',
                systolic=systolic,
                diastolic=diastolic,
                fasting_sugar=None,
                bedtime_sugar=None,
                user_id=session['user_id']  # Associate with the logged-in user
            )
        elif record_type == 'sugar':
            fasting_sugar = request.form.get('fasting_sugar')
            bedtime_sugar = request.form.get('bedtime_sugar')
            new_record = dailyrecord(
                title='Sugar',
                systolic=None,  # Set to None as these fields are not used for sugar
                diastolic=None,
                fasting_sugar=fasting_sugar,
                bedtime_sugar=bedtime_sugar,
                user_id=session['user_id']  # Associate with the logged-in user
            )
        else:
            flash('Please select a valid reading type.', 'error')
            return redirect(url_for('daily_record'))

        # Add the new record to the database
        db.session.add(new_record)
        db.session.commit()
        flash('Record added successfully!', 'success')
        return redirect(url_for('daily_record'))  # Redirect to another route after adding

    return render_template('bp.html', title='Add Daily Record')
   






@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:  # Ensure user is logged in
        return render_template('dashboard.html')
    else:
     user_id = session['user_id']  # Get the logged-in user's ID
     user = User.query.get(user_id)
     return render_template("dashboard.html",username=user.username)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))
    




if __name__ == "__main__":
    app.run(debug=True)