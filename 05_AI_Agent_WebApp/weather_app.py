from flask import Flask, render_template, request, redirect, url_for, session
from utils.agent_utils import invoke_agent, agent
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key for session management

@app.route('/')
def home():
    if 'thread_id' not in session:
        session['thread_id'] = str(uuid.uuid4())  # Generate a unique thread ID for each session
    if 'messages' not in session:
        session['messages'] = []
    return render_template('chat.html', messages = session.get('messages', []))

@app.route('/another')
def another():
    return "Hello, Another!"

@app.route('/send', methods=['POST'])
def send_message():
    user_message = request.form['user_message']
    user_lat = request.form.get('latitude')
    user_lon = request.form.get('longitude')

    # Store the user's location in the session if available, 
    # One time per session, so that the agent can use it for location-based queries
    if user_lat and user_lon:
        session['user_session'] = {'lat': user_lat, 'lon': user_lon}
    
    response = invoke_agent(agent, user_message, session['thread_id'])
    
    session['messages'].append({'type': 'human', 'content': user_message})
    session['messages'].append({'type': 'ai', 'content': response['messages'][-1].content})

    session.modified = True
        
    return redirect(url_for('home'))

app.run(debug=True)
