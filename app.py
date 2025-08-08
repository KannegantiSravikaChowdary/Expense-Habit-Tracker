from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import json
import os

app = Flask(__name__)
CORS(app)
app.secret_key = '18b77bc6bb50e13fe8993a089fd0c9f4'

# Load model and encoder
model = joblib.load("model.pkl")
goal_encoder = joblib.load("goal_encoder.pkl")

USER_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get_started")
def get_started():
    return render_template("get_started.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        users = load_users()
        if email in users:
            return render_template("register.html", error="User already exists. Please login.")

        users[email] = {
            "name": name,
            "password": password
        }
        save_users(users)
        return render_template("register.html", success="Registration successful! Please login.")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        users = load_users()
        if email in users and users[email]["password"] == password:
            session["user"] = email
            session["name"] = users[email]["name"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["name"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        income = int(data["Monthly Income"])
        food = int(data["Food"])
        rent = int(data["Rent"])
        shopping = int(data["Shopping"])
        savings = int(data["Savings"])
        loans = int(data["Loans"])
        education = int(data["Education"])
        entertainment = int(data["Entertainment"])
        health = int(data["Health"])
        goal = data["Financial Goal"]

        goal_encoded = goal_encoder.transform([goal])[0]
        features = np.array([[income, food, rent, shopping, savings, loans,
                              education, entertainment, health, goal_encoded]])

        label = model.predict(features)[0]
        label_map = {0: "Saver", 1: "Balanced", 2: "Overspender"}
        label_name = label_map[label]

        savings_percent = savings / income
        score = round(min(100, savings_percent * 100), 2)

        if label_name == "Saver":
            tip = "Great job! Keep saving consistently."
        elif label_name == "Balanced":
            tip = "You're doing okay. Try to save a bit more if possible."
        else:
            tip = "You're overspending. Set a stricter budget and track your spending."

        return jsonify({
            "label": label_name,
            "budget_score": score,
            "smart_tip": tip
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
