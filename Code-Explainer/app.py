from flask import Flask, request, jsonify, render_template
from google.cloud import translate_v3 as translate
import openai
from guesslang import Guess

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for easier development

# Initialize Google Translate API client
client = translate.TranslationServiceClient()

# Initialize OpenAI API (replace with your actual OpenAI API key)
openai.api_key = 'your_openai_api_key' # either you can enter your key directly or if not create .env file, store your key and recall using dotenv. 

# Initialize Guesslang
guess = Guess()

# Function to detect programming language
def detect_language(code):
    language = guess.language_name(code)
    return language

# Function to explain code using OpenAI
def explain_code(code):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Explain the following {detect_language(code)} code in simple English:\n\n{code}", # You can write a better prompt according to your requirement
        max_tokens=150
    )
    explanation = response.choices[0].text.strip()
    return explanation

# Function to add comments to code using OpenAI
def add_comments(code):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Add comments to the following {detect_language(code)} code:\n\n{code}\n\nComments:",
        max_tokens=100
    )
    comments = response.choices[0].text.strip()
    return comments

# Function to translate English text to multiple languages using Google Translate API
def translate_to_target_languages(english_text, target_languages):
    translations = {}
    parent = f"projects/your-project-id/locations/global"  # Replace with your actual Google Cloud project ID

    for lang_code in target_languages:
        response = client.translate_text(
            parent=parent,
            contents=[english_text],
            target_language_code=lang_code,
        )
        translations[lang_code] = response.translations[0].translated_text

    return translations

# Endpoint to render the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to handle code explanation request
@app.route('/explain', methods=['POST'])
def explain_code_endpoint():
    data = request.get_json()
    code = data.get('code', '')

    # Detect programming language
    language = detect_language(code)

    # Explain code in English
    explanation = explain_code(code)

    # Prepare response
    response_data = {
        "original_code": code,
        "language": language,
        "english_explanation": explanation,
    }

    return jsonify(response_data)

# Endpoint to handle adding comments request
@app.route('/add_comments', methods=['POST'])
def add_comments_endpoint():
    data = request.get_json()
    code = data.get('code', '')

    # Add comments to code
    comments = add_comments(code)

    # Prepare response
    response_data = {
        "original_code": code,
        "comments": comments,
    }

    return jsonify(response_data)

# Endpoint to handle code translation request
@app.route('/translate', methods=['POST'])
def translate_code():
    data = request.get_json()
    explanation = data.get('explanation', '')
    target_language = data.get('target_language', 'fr')  # Default to French if not specified

    # Translate explanation to target language
    translations = translate_to_target_languages(explanation, [target_language])

    # Prepare response
    response_data = {
        "original_text": explanation,
        "translated_text": translations[target_language],
    }

    return jsonify(response_data)

# Endpoint to handle user comments submission
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    data = request.get_json()
    comment = data.get('comment', '')

    # Store comment in a database or file
    with open('comments.txt', 'a') as f:
        f.write(comment + '\n')

    return jsonify({"message": "Comment added!"})

# Endpoint to handle user feedback submission
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    feedback = data.get('feedback', '')
    rating = data.get('rating', '')

    # Store feedback in a database or file
    with open('feedback.txt', 'a') as f:
        f.write(f"Rating: {rating}, Feedback: {feedback}\n")

    return jsonify({"message": "Feedback submitted!"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
