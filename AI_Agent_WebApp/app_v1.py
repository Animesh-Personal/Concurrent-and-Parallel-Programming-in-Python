from flask import Flask, render_template, request
from prompts import SYSTEM_PROMPT

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/another')
def another():
    return "Hello, Another!"

@app.route('/send', methods=['POST'])
def send_message():
    user_input = request.form['user_input']
    print(f"User input: {user_input}")
    return "Message sent!"

app.run(debug=True)

