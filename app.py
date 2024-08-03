from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

# Initialize Flask app
app = Flask(__name__)

# Initialize MongoDB client
try:
    client = MongoClient(CONNECTION_STRING)
    db = client['quiz_database']
    collection = db['combined_data']  # Collection for combined data
    # Test the connection
    client.server_info()
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_demographics', methods=['POST'])
def submit_demographics():
    if request.method == 'POST':
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
        question1_data = request.form.to_dict()
        collection.update_one({}, {'$set': {'question1_data': question1_data}}, upsert=True)
        return redirect(url_for('result1'))

@app.route('/submit_question2', methods=['POST'])
def submit_question2():
    if request.method == 'POST':
        # Collect all question data
        question2_data = request.form.to_dict()

        # Assuming 'answers' field is passed in JSON format
        question2_answers = json.loads(question2_data.get('answers', '[]'))

        # Store the data in MongoDB
        collection.update_one({}, {'$set': {'question2_data': question2_answers}}, upsert=True)
        return redirect(url_for('result2'))

@app.route('/result1')
def result1():
    # Retrieve combined data from MongoDB
    combined_data = collection.find_one()
    return render_template('result1.html', combined_data=combined_data)

@app.route('/result2')
def result2():
    # Retrieve combined data from MongoDB
    combined_data = collection.find_one()
    return render_template('result2.html', combined_data=combined_data)

if __name__ == '__main__':
    app.run(debug=True)
