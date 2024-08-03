from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from pymongo import MongoClient
import uuid 
import json 
from dotenv import load_dotenv
import os

load_dotenv()
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_MONGODB'] = MongoClient(CONNECTION_STRING)
app.config['SESSION_MONGODB_DB'] = 'quiz_database'  # Name of your database for sessions
app.config['SESSION_MONGODB_COLLECT'] = 'sessions' 

Session(app)

client = MongoClient(CONNECTION_STRING)
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

        demographics_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'age': request.form.get('age'),
            'dob': request.form.get('dob'),
            'gender': request.form.get('gender'),
            'education': request.form.get('education'),
            'occupation': request.form.get('occupation'),
            'income': request.form.get('income'),
            'marital_status': request.form.get('marital-status'),
            'city_town': request.form.get('city-town'),
            'urs': request.form.get('urs'),
            'state': request.form.get('state'),
            'ethnicity': request.form.get('ethnicity'),
            'family_history': request.form.get('family-history'),
            'personal_history': request.form.get('personal-history'),
            'alcohol': request.form.get('alcohol') == 'on',
            'tobacco': request.form.get('tobacco') == 'on',
            'drugs': request.form.get('drugs') == 'on',
            'history_trauma_abuse': request.form.get('history-trauma-abuse'),
            'resilience_score': request.form.get('resilience-score'),
            'positivity_score': request.form.get('positivity-score'),
            'supportive_family': request.form.get('supportive-family') == 'on',
            'community_groups': request.form.get('community-groups') == 'on',
            'attendance_punctuality': request.form.get('attendance-punctuality'),
            'academic_performance': request.form.get('academic-performance'),
            'extracurricular_activities': request.form.get('extracurricular-activities'),
            'relationships_peers_family': request.form.get('relationships-peers-family'),
            'social_skills': request.form.get('social-skills'),
            'sense': request.form.get('sense')
        }

        demographics_document = {
            'user_id': user_id,
            'demographics': demographics_data,
            'question1_data': {},
            'question2_data': {}
        }

        collection.insert_one(demographics_document)

        return redirect(url_for('options'))

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/select_question', methods=['POST'])
def select_question():
    selected_option = request.form.get('question_option')
    if selected_option == 'question1':
        return redirect(url_for('question1'))
    elif selected_option == 'question2':
        return redirect(url_for('question2'))

@app.route('/question1')
def question1():
    return render_template('question1.html')

@app.route('/question2')
def question2():
    return render_template('question2.html')

@app.route('/submit_question1', methods=['POST'])
def submit_question1():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('index'))

        question1_data = request.form.to_dict()
        collection.update_one({'user_id': user_id}, {'$set': {'question1_data': question1_data}})

        return redirect(url_for('result1', question='question1'))

@app.route('/submit_question2', methods=['POST'])
def submit_question2():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('index'))

        # Collect all question data
        question2_data = request.form.to_dict()

        # Assuming 'answers' field is passed in JSON format
        question2_answers = json.loads(question2_data.get('answers', '[]'))

        # Store the data in MongoDB
        collection.update_one({'user_id': user_id}, {'$set': {'question2_data': question2_answers}})

        return redirect(url_for('result2', question='question2'))




@app.route('/result1')
def result1():
    # Retrieve user_id from session
    user_id = session.get('user_id')

    # If user_id is not found in session, handle error or redirect to demographics page
    if not user_id:
        return redirect(url_for('index'))

    # Retrieve combined data from MongoDB
    combined_data = collection.find_one({'user_id': user_id})

    return render_template('result1.html', combined_data=combined_data)

@app.route('/result2')
def result2():
    # Retrieve user_id from session
    user_id = session.get('user_id')

    # If user_id is not found in session, handle error or redirect to demographics page
    if not user_id:
        return redirect(url_for('index'))

    # Retrieve combined data from MongoDB
    combined_data = collection.find_one({'user_id': user_id})

    return render_template('result2.html', combined_data=combined_data)

if __name__ == '__main__':
    app.run(debug=True)
