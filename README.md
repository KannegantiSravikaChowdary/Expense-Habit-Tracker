# 📊 Expense Habit Tracker

The **Expense Habit Tracker** is a Flask-based web application that uses **machine learning** to classify users as **Saver**, **Balanced**, or **Overspender** based on their income, expenses, and financial goals.  
It also calculates a **budget score**, gives **smart saving tips**, and visualizes spending with a **pie chart**.

---

## 🚀 Features
- **ML Prediction** – Predicts your spending habit using a **Random Forest Classifier**.  
- **Budget Score** – 0–100 score to reflect financial health.  
- **Smart Saving Tips** – Personalized advice based on your prediction.  
- **Pie Chart** – Visualizes your expense distribution.  
- **Multiple Goals** – Choose from goals like *Home*, *Car*, *Trip*, *House Construction*, etc.  
- **Authentication** – Login/Register with JSON-based storage.  
- **Interactive Dashboard** – Clean, attractive UI with real-time updates.

---

## 🧠 Machine Learning Model
We use `RandomForestClassifier` from **scikit-learn** because:
- It handles both categorical and numerical data well.
- It is robust to overfitting for small/medium datasets.
- It provides high accuracy for classification problems.

The trained model and encoder are saved as:
  
    model.pkl
    goal_encoder.pkl


---

## 🔑 Secret Key in Flask
Flask requires a `SECRET_KEY` for:
- Securing **sessions** (so cookies can’t be tampered with)  
- Protecting against **CSRF attacks**  
- Encrypting sensitive session data  

We generate it in Python like this:
```python
import secrets
secrets.token_hex(16)
```

In app.py, you set it like:
  app.secret_key = 'YOUR_SECRET_KEY'

⚠ Never share your secret key publicly.
If it leaks, regenerate it using the above command.

**📂Project Structure**
```
Expense-Habit-Tracker/
│
├── app.py                  # Flask backend
├── model.pkl               # Trained Random Forest model
├── goal_encoder.pkl        # Encoder for 'Financial Goal'
├── expenses.csv            # Dataset
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/
│   ├── style.css
│   ├── login-image.jpg
│   └── register-image.jpg
└── README.md
```
**🛠 Installation & Setup**

Clone the repository:
```
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

Create a virtual environment:
```
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

Install dependencies:
```
pip install -r requirements.txt
```

Run the Flask app:
```
python app.py
```

Open in browser:
```
http://127.0.0.1:5000
```

**📊 Dataset**

The dataset (expenses.csv) contains:
Monthly Income
Expense categories (Rent, Food, Education, etc.)
Financial Goal (encoded with LabelEncoder)
Spending habit label (Saver, Balanced, Overspender)

