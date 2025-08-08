import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
df = pd.read_csv("expenses.csv")

# Encode 'Financial Goal'
le = LabelEncoder()
df['Financial Goal'] = le.fit_transform(df['Financial Goal'])

# Map label (if necessary)
if df["Label"].dtype == object:
    df["Label"] = df["Label"].map({"Saver": 0, "Balanced": 1, "Overspender": 2})

# Features and target
X = df.drop(columns=["Label"])  # now it drops correct column
y = df["Label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoder
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("goal_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("✅ Model and encoder saved.")
