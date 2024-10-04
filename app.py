from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pickle
import numpy as np 
import pandas as pd 
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
    



from datetime import datetime

@app.route("/daily_record", methods=['GET', 'POST'])
def daily_record():
    if 'user_id' not in session:  # Ensure the user is logged in
        return redirect(url_for('signin'))  # Redirect to the sign-in page

    if request.method == 'POST':
        record_type = request.form.get('record_type')
        
        # Get the current date and time
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        # Prepare to save data based on the selected record type
        if record_type == 'bp':
            systolic = request.form.get('systolic')
            diastolic = request.form.get('diastolic')
            new_record = dailyrecord(
                title='Blood Pressure',
                systolic=systolic,
                diastolic=diastolic,
                fasting_sugar=None,
                bedtime_sugar=None,
                user_id=session['user_id'],  # Associate with the logged-in user
                record_date=current_date,  # Store the current date
                record_time=current_time   # Store the current time
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
                user_id=session['user_id'],  # Associate with the logged-in user
                record_date=current_date,  # Store the current date
                record_time=current_time   # Store the current time
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
 
 
 
 
 
sym_des = pd.read_csv("dataset/symtoms_df.csv")
precautions = pd.read_csv("dataset/precautions_df.csv")
workout = pd.read_csv("dataset/workout_df.csv")
description = pd.read_csv("dataset/description.csv")
medications = pd.read_csv('dataset/medications.csv')
diets = pd.read_csv("dataset/diets.csv")



rf = pickle.load(open('model/rf.pxl','rb'))



def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis] ['workout']


    return desc,pre,med,die,wrkout

symptoms_dict = {'itching': 0, 'skin rash': 1, 'nodal skin eruptions': 2, 'continuous sneezing': 3, 'shivering': 4, 'chills': 5, 'joint pain': 6, 'stomach pain': 7, 'acidity': 8, 'ulcers on tongue': 9, 'muscle wasting': 10, 'vomiting': 11, 'burning micturition': 12, 'spotting urination': 13, 'fatigue': 14, 'weight gain': 15, 'anxiety': 16, 'cold hands and feets': 17, 'mood swings': 18, 'weight loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches in hroat': 22, 'irregular sugar level': 23, 'cough': 24, 'high fever': 25, 'sunken eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish skin': 32, 'dark urine': 33, 'nausea': 34, 'loss of appetite': 35, 'pain behind the eyes': 36, 'back pain': 37, 'constipation': 38, 'abdominal pain': 39, 'diarrhoea': 40, 'mild fever': 41, 'yellow urine': 42, 'yellowing of eyes': 43, 'acute liver failure': 44, 'fluid overload': 45, 'swelling of stomach': 46, 'swelled lymph nodes': 47, 'malaise': 48, 'blurred and distorted vision': 49, 'phlegm': 50, 'throat irritation': 51, 'redness of eyes': 52, 'sinus pressure': 53, 'runny nose': 54, 'congestion': 55, 'chest pain': 56, 'weakness in limbs': 57, 'fast heart rate': 58, 'pain during bowel movements': 59, 'pain in anal region': 60, 'bloody stool': 61, 'irritation in anus': 62, 'neck pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen legs': 68, 'swollen blood vessels': 69, 'puffy face and eyes': 70, 'enlarged thyroid': 71, 'brittle nails': 72, 'swollen extremeties': 73, 'excessive hunger': 74, 'extra marital contacts': 75, 'drying and tingling lips': 76, 'slurred speech': 77, 'knee pain': 78, 'hip joint pain': 79, 'muscle weakness': 80, 'stiff neck': 81, 'swelling joints': 82, 'movement stiffness': 83, 'spinning movements': 84, 'loss of balance': 85, 'unsteadiness': 86, 'weakness of one body side': 87, 'loss of smell': 88, 'bladder discomfort': 89, 'foul smell of urine': 90, 'continuous feel of urine': 91, 'passage of gases': 92, 'internal itching': 93, 'toxic look (typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle pain': 97, 'altered sensorium': 98, 'red spots over body': 99, 'belly pain': 100, 'abnormal menstruation': 101, 'dischromic  patches': 102, 'watering from eyes': 103, 'increased appetite': 104, 'polyuria': 105, 'family history': 106, 'mucoid sputum': 107, 'rusty sputum': 108, 'lack of concentration': 109, 'visual disturbances': 110, 'receiving blood transfusion': 111, 'receiving unsterile injections': 112, 'coma': 113, 'stomach bleeding': 114, 'distention of abdomen': 115, 'history of alcohol consumption': 116, 'fluid overload.1': 117, 'blood in sputum': 118, 'prominent veins on calf': 119, 'palpitations': 120, 'painful walking': 121, 'pus filled pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin peeling': 125, 'silver like dusting': 126, 'small dents in nails': 127, 'inflammatory nails': 128, 'blister': 129, 'red sore around nose': 130, 'yellow crust ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}


def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[rf.predict([input_vector])[0]]
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        
        if symptoms:
            # Process the input symptoms
            user_symptoms = [s.strip().lower() for s in symptoms.split(',')]
            # Check if all user symptoms are valid
            invalid_symptoms = [s for s in user_symptoms if s not in symptoms_dict]
            
            if invalid_symptoms:
                # If there are invalid symptoms, display an error message
                message = f"Please either write symptoms or you have written misspelled symptoms: {', '.join(invalid_symptoms)}"
                return render_template('meds_rec.html', message=message,symptoms=symptoms)
            
            # Predict the disease and get additional information
            predicted_disease = get_predicted_value(user_symptoms)
            dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)
            
            # Prepare list of precautions
            my_precautions = [precaution for precaution in precautions[0]]
            
            # Render the result template with disease information
            return render_template('meds_rec.html', 
                                   predicted_disease=predicted_disease, 
                                   dis_des=dis_des,
                                   my_precautions=my_precautions, 
                                   medications=medications, 
                                   my_diet=rec_diet,
                                   workout=workout)
        else:
            message = "Please enter symptoms."
            return render_template('meds_rec.html', message=message,symptoms=symptoms)
    
    # Render the form template if the request method is not POST
    return render_template('meds_rec.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))
    




if __name__ == "__main__":
    app.run(debug=True)