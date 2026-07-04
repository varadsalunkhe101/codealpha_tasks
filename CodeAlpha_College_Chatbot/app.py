# Import required modules
from flask import Flask, render_template, request, jsonify
import json
import os

# Create Flask application
app = Flask(
    __name__,
    template_folder="templates",   # HTML files folder
    static_folder="static"         # CSS, JS, Images folder
)

# --------------------------------------------------
# Debug Information
# Checks whether required folders and files exist
# --------------------------------------------------
print("Current Directory:", os.getcwd())
print("Templates Folder Exists:", os.path.exists("templates"))
print("Index File Exists:", os.path.exists("templates/index.html"))

# --------------------------------------------------
# Load chatbot knowledge base from JSON file
# --------------------------------------------------
with open("chatbot_data.json", "r", encoding="utf-8") as file:
    chatbot_data = json.load(file)


# --------------------------------------------------
# Function to find chatbot response
# --------------------------------------------------
def get_response(user_message):

    # Convert user message to lowercase and remove spaces
    user_message = user_message.lower().strip()

    # Loop through all intents
    for intent in chatbot_data["intents"]:

        # Check all patterns inside an intent
        for pattern in intent["patterns"]:

            # Exact match
            # Example:
            # User: "admission"
            # Pattern: "admission"
            if user_message == pattern.lower():
                return intent["response"]

            # Partial match
            # Example:
            # User: "tell me about admission process"
            # Pattern: "admission"
            if pattern.lower() in user_message:
                return intent["response"]

    # Default response if no match is found
    return (
        "Sorry, I couldn't understand your question. "
        "Please ask about admissions, courses, fees, placements, "
        "scholarships, hostel, library, or contact information."
    )


# --------------------------------------------------
# Home Route
# Opens chatbot webpage
# URL: http://127.0.0.1:5000/
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Chat Route
# Receives user message from JavaScript
# Sends chatbot response back as JSON
# --------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():

    # Get JSON data sent from frontend
    data = request.get_json()

    # Extract user's message
    user_message = data.get("message", "")

    # Generate chatbot response
    response = get_response(user_message)

    # Send response back to frontend
    return jsonify({
        "response": response
    })


# --------------------------------------------------
# Run Flask Development Server
# Debug=True automatically reloads changes
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)