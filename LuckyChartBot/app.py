from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

API_KEY = "AIzaSyDJPbfw2UmiElw9xfZ8y8lIUcx96ghu5dw"  # Replace with your Gemini API key
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def call_gemini_api(prompt):
    # Check for identity-related questions
    identity_keywords = [
        "who made you", "who created you", "who developed you",
        "what are you", "who are you", "what model are you",
        "what's your name", "what is your name" ,"when was you created"
    ]
    
    if any(keyword in prompt.lower() for keyword in identity_keywords):
        return "I'm Lucky's AI assistant. I was created by Lucky to help you!"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    response = requests.post(
        API_URL,
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        result = response.json()
        response_text = result['candidates'][0]['content']['parts'][0]['text']
        # Filter out "gemini" references
        filtered_response = response_text.replace("Gemini", "Lucky").replace("gemini", "Lucky").replace("Google", "Lucky").replace("google", "Lucky")
        return filtered_response
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
        
    try:
        response = call_gemini_api(message)
        return jsonify({
            'response': response,
            'timestamp': datetime.now().strftime("%H:%M")
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)