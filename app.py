from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from pymongo import MongoClient
import uuid  # For generating unique IDs

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_PERMANENT'] = False

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
app.config['SESSION_MONGODB'] = client

# Initialize Flask-Session
Session(app)

db = client['quiz_database']
collection = db['combined_data']  # Collection for combined data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_demographics', methods=['POST'])
def submit_demographics():
    if request.method == 'POST':
        # Generate a unique identifier for the user
        user_id = str(uuid.uuid4())
        
        session['user_id'] = user_id

        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        education = request.form.get('education')
        occupation = request.form.get('occupation')
        income = request.form.get('income')
        marital_status = request.form.get('marital-status')
        city_town = request.form.get('city-town')
        urs = request.form.get('urs')
        state = request.form.get('state')
        ethnicity = request.form.get('ethnicity')
        family_history = request.form.get('family-history')
        personal_history = request.form.get('personal-history')
        alcohol = request.form.get('alcohol') == 'on'
        tobacco = request.form.get('tobacco') == 'on'
        drugs = request.form.get('drugs') == 'on'
        history_trauma_abuse = request.form.get('history-trauma-abuse')
        resilience_score = request.form.get('resilience-score')
        positivity_score = request.form.get('positivity-score')
        supportive_family = request.form.get('supportive-family') == 'on'
        community_groups = request.form.get('community-groups') == 'on'
        attendance_punctuality = request.form.get('attendance-punctuality')
        academic_performance = request.form.get('academic-performance')
        extracurricular_activities = request.form.get('extracurricular-activities')
        relationships_peers_family = request.form.get('relationships-peers-family')
        social_skills = request.form.get('social-skills')
        sense = request.form.get('sense')

        # Insert demographics data into MongoDB
        demographics_data = {
            'user_id': user_id,
            'name': name,
            'email': email,
            'age': age,
            'dob': dob,
            'gender': gender,
            'education': education,
            'occupation': occupation,
            'income': income,
            'marital_status': marital_status,
            'city_town': city_town,
            'urs': urs,
            'state': state,
            'ethnicity': ethnicity,
            'family_history': family_history,
            'personal_history': personal_history,
            'alcohol': alcohol,
            'tobacco': tobacco,
            'drugs': drugs,
            'history_trauma_abuse': history_trauma_abuse,
            'resilience_score': resilience_score,
            'positivity_score': positivity_score,
            'supportive_family': supportive_family,
            'community_groups': community_groups,
            'attendance_punctuality': attendance_punctuality,
            'academic_performance': academic_performance,
            'extracurricular_activities': extracurricular_activities,
            'relationships_peers_family': relationships_peers_family,
            'social_skills': social_skills,
            'sense': sense
        }

        # Insert demographics data into MongoDB
        collection.insert_one(demographics_data)

        # Redirect to quiz page
        return redirect(url_for('questions'))

@app.route('/questions')
def questions():
    return render_template('question.html')

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    if request.method == 'POST':
        # Retrieve user_id from session
        user_id = session.get('user_id')

        # If user_id is not found in session, handle error or redirect to demographics page
        if not user_id:
            return redirect(url_for('index'))

        # Extract quiz data from form
        quiz_data = request.form.to_dict()

        # Update existing document in MongoDB with quiz data
        collection.update_one(
            {'user_id': user_id},
            {'$set': {'quiz_data': quiz_data}}
        )

        # Redirect to result page
        return redirect(url_for('result'))

@app.route('/result')
def result():
    # Retrieve user_id from session
    user_id = session.get('user_id')

    # If user_id is not found in session, handle error or redirect to demographics page
    if not user_id:
        return redirect(url_for('index'))

    # Retrieve combined data from MongoDB
    combined_data = collection.find_one({'user_id': user_id})

    return render_template('result.html', combined_data=combined_data)

if __name__ == '__main__':
    app.run(debug=True)
