from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, healthrecords  #  healthrecords is also defined in models.py

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
    return  render_template ("index.html")
@app.route("/home")
def home():
    user_id = session.get('user_id')
    username = None
    if user_id:
        user = User.query.get(user_id)
        username = user.username if user else None
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

@app.route('/profile',methods=['GET','POST'])
def profile():
    if 'user_id' not in session:  # Ensure user is logged in
        return redirect(url_for('signin'))

    user_id = session['user_id']
    email_id = session.get('email')# Get the logged-in user's ID
    user = User.query.get(user_id)  # Retrieve the user object to get the username
    
    
    return render_template('profile.html',username=user.username,email=email_id)







@app.route('/records', methods=['GET', 'POST'])
def records():
    user_id = session['user_id']  # Get the logged-in user's ID
    user = User.query.get(user_id)
    return render_template("records.html",username=user.username)
    



@app.route("/bp", methods=['GET','POST'])
def bp():
    return render_template('bp.html')






@app.route("/dashboard")
def dashboard():
    user_id = session['user_id']  # Get the logged-in user's ID
    user = User.query.get(user_id)
    

    return render_template("dashboard.html", username=user.username, )


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))
    




if __name__ == "__main__":
    app.run(debug=True)