from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

user_name = None

rules = {
    "greeting": {
        "inputs": ["hi", "hello", "hey", "good morning", "good evening", "sup", "yo"],
        "responses": [
            "Hello!",
            "Hey there!",
            "Hi, how can I help you today?",
            "Nice to see you."
        ]
    },

    "how_are_you": {
        "inputs": ["how are you", "how are u", "what's up", "how r u"],
        "responses": [
            "I'm doing great.",
            "All good here. How about you?",
            "Running smoothly."
        ]
    },

    "goodbye": {
        "inputs": ["bye", "goodbye", "exit", "see you", "see ya"],
        "responses": [
            "Goodbye!",
            "See you later!",
            "Take care!"
        ]
    },

    "help": {
        "inputs": ["help", "what can you do", "commands"],
        "responses": [
            "I can chat, remember your name, tell time, and respond to basic questions.",
            "Try saying hi, tell me your name, or ask for time."
        ]
    },

    "mood_sad": {
        "inputs": ["i am sad", "feeling low", "not good", "i feel bad"],
        "responses": [
            "I'm here for you.",
            "That sounds tough. Want to talk about it?",
            "You’re not alone."
        ]
    },

    "mood_happy": {
        "inputs": ["i am happy", "feeling good", "great day"],
        "responses": [
            "That’s great to hear!",
            "Love that energy!",
            "Keep it going 😊"
        ]
    },

   "joke": {
    "inputs": ["tell me a joke", "joke", "make me laugh", "funny"],
    "responses": [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "I asked my code why it crashed… it said 'I don’t know, I just felt like it.'",
        "There are only 10 types of people in the world: those who understand binary and those who don’t.",
        "My code doesn’t have bugs. It just develops random features.",
        "I would tell you a UDP joke… but you might not get it."
    ]
},

    "motivation": {
    "inputs": ["motivate me", "i feel lazy", "give me motivation", "inspire me"],
    "responses": [
        "You don’t need to feel ready. You just need to start.",
        "Small progress is still progress. Don’t underestimate it.",
        "Discipline beats motivation on the days you don’t feel like it.",
        "You’re not behind. You’re building at your own pace.",
        "Even slow steps move you forward."
    ]
},

    "time": {
        "inputs": ["time", "what time is it", "current time"],
        "responses": ["__DYNAMIC_TIME__"]
    }
}


def match_rule(user_input):
    user_input = user_input.lower().strip()

    best_match = None
    best_score = 0

    for rule in rules.values():
        for pattern in rule["inputs"]:
            pattern = pattern.lower()

            if pattern == user_input:
                return rule

            if pattern in user_input:
                score = len(pattern.split()) * 3
            else:
                pattern_words = pattern.split()
                score = 0

                for word in pattern_words:
                    if word in user_input:
                        score += 1
            if score > best_score and score >= 2:
                best_score = score
                best_match = rule

    return best_match

def get_response(user_input):
    global user_name

    user_input = user_input.lower().strip()

    if "my name is" in user_input:
        user_name = user_input.replace("my name is", "").strip().title()
        return f"Nice to meet you, {user_name}!"

    if "i am" in user_input or "i'm" in user_input:
        if len(user_input.split()) <= 5:
            user_name = user_input.replace("i am", "").replace("i'm", "").strip().title()
            return f"Got it, {user_name}."

    if "what is my name" in user_input:
        return f"Your name is {user_name}" if user_name else "I don't know your name yet."

    if "time" in user_input:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"

    if "bye" in user_input or "exit" in user_input:
        return f"Goodbye {user_name if user_name else ''}".strip()
    
    rule = match_rule(user_input)

    if rule:
        response = random.choice(rule["responses"])

        if response == "__DYNAMIC_TIME__":
            return datetime.now().strftime("%H:%M:%S")

        return response

    return "I don't understand that."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]
    response = get_response(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)