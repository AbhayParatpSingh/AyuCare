Ayucare Health Prediction System
Ayucare is an AI-driven health prediction system designed to diagnose conditions based on user-input symptoms. The system is built using Flask, integrates machine learning models, and provides users with insights into their health by suggesting treatments, diets, precautions, and workouts.

Table of Contents
Features
Tech Stack
Project Structure
Installation
Usage
Datasets
Machine Learning Models
Routes
Contributors
Features
Predicts potential health conditions based on multiple symptoms.
Provides condition descriptions, precautions, recommended treatments, diets, and workout routines.
User authentication, health record management, and dashboard for personalized insights.
Supports multiple machine learning models (KNeighborsClassifier and Random Forest).
Interactive and responsive UI using Tailwind CSS.
Tech Stack
Backend: Flask, Python
Frontend: HTML, Tailwind CSS, JavaScript
Database: CSV files for health data (precautions, treatments, diets, descriptions)
Machine Learning: KNeighborsClassifier, RandomForestClassifier
Other: Pandas, NumPy, Pickle for model serialization
Project Structure
graphql
Copy code
ayucare/
│
├── .venv/                       # Virtual environment
├── .vscode/                     # VS Code configuration
├── dataset/                     # Folder for datasets
│   ├── Physio/
│   ├── Symptom-severity.csv
│   ├── Training.csv
│   ├── description.csv
│   ├── diets.csv
│   ├── medications.csv
│   ├── precautions_df.csv
│   ├── symtoms_df.csv
│   ├── workout_df.csv
├── model/                       # Machine learning models
│   ├── knn.pxl                  # KNeighborsClassifier model
│   ├── rf.pxl                   # Random Forest model
├── static/                      # Static files
│   ├── css/
│   ├── img/
│   ├── js/
│   ├── src/
├── templates/                   # HTML templates for UI
│   ├── index.html               # Main page
│   ├── dashboard.html           # Dashboard page
│   ├── register.html            # User registration page
│   ├── signin.html              # Sign-in page
│   ├── profile.html             # User profile page
│   ├── records.html             # Health records page
│   ├── meds_rec.html            # Medication recommendations
│   ├── devloper.html            # Developer information
│   ├── ...                      # Other partial templates
├── .gitignore                   # Git ignore file
├── app.py                       # Main Flask application
├── models.py                    # Contains machine learning models code
├── requirement.txt              # Project dependencies
├── tailwind.config.js           # Tailwind CSS configuration
├── disease.ipynb                # Jupyter notebook for disease-related analysis
├── physio.ipynb                 # Jupyter notebook for physiotherapy-related analysis
├── package-lock.json            # npm package lock file
├── package.json                 # npm package file
├── cbc_data.csv                 # Additional dataset for CBC
├── cbc_dataset.csv              # CBC dataset for analysis
Installation
Prerequisites
Python 3.x
Flask
Pandas, NumPy
scikit-learn
Pickle
Node.js (for Tailwind CSS)
Setup Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/ayucare.git
cd ayucare
Set up a virtual environment:

bash
Copy code
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
Install Python dependencies:

bash
Copy code
pip install -r requirement.txt
Install Tailwind CSS dependencies:

bash
Copy code
npm install
Run the application:

bash
Copy code
python app.py
Access the app: Open your browser and navigate to http://127.0.0.1:5000/.

Usage
Visit the homepage to input symptoms for diagnosis.
Create an account and log in to access personalized features.
Explore the dashboard for recommendations on treatments, diets, and workouts.
View and manage your health records.
Datasets
The application uses multiple CSV files for health-related data:

Symptom-severity.csv: Contains severity levels for various symptoms.
description.csv: Descriptions of medical conditions.
precautions_df.csv: Precautionary measures for each condition.
diets.csv: Suggested diets based on the condition.
workout_df.csv: Recommended workouts for recovery.
Training.csv: Training data for the machine learning model.
Machine Learning Models
Two machine learning models are used for predictions:

KNeighborsClassifier (knn.pxl): Predicts conditions based on proximity to similar symptoms.
RandomForestClassifier (rf.pxl): Offers an alternative, more robust prediction mechanism.
Routes
/: Home page where users can input symptoms and receive predictions.
/about: Information about the Ayucare project.
/contact: Contact form for user queries.
/dashboard: Displays personalized recommendations.
/register: Allows new users to create an account.
/signin: Existing users can sign in.
/predict: API endpoint for handling health predictions.
Contributors
Abhay Pratap Singh - Project Lead & Developer
Apoorv Verma
Aryan Singh 
Anushka Shukla 
[Other contributors]
License
This project is licensed under the MIT License. See the LICENSE file for details.
