import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
import numpy as np

# Load dataset
file_path = "career_data_5000_updated.csv"
df = pd.read_csv(file_path)

# 🔹 Add "Other" Category in Training Data
for column in ["Current Role", "Gender", "Top Skills", "Experience", "Next Role"]:
    df[column] = df[column].astype(str)  # Ensure all values are strings
    df[column] = df[column].fillna("Other")  # Replace NaN with "Other"

# 🔹 Encode Categorical Variables with "Other"
label_encoders = {}
for column in ["Current Role", "Gender", "Top Skills", "Experience", "Next Role"]:
    le = LabelEncoder()
    df[column] = df[column].astype(str)  # Ensure string format
    unique_values = list(df[column].unique())  # Get unique values
    if "Other" not in unique_values:
        unique_values.append("Other")  # Ensure "Other" is included
    le.fit(unique_values)  # Fit encoder with "Other"
    df[column] = le.transform(df[column])
    label_encoders[column] = le  # Store the encoder

# Convert Salary to Numeric Values
df["Current Salary"] = df["Current Salary"].str.replace("₹", "").str.replace(" LPA", "").astype(float)
df["Next Role Salary"] = df["Next Role Salary"].str.replace("₹", "").str.replace(" LPA", "").astype(float)

# Train-Test Split
X = df[["Current Role", "Gender", "Top Skills", "Experience", "Current Salary"]]
y_next_role = df["Next Role"]
y_next_salary = df["Next Role Salary"]

X_train, X_test, y_next_role_train, y_next_role_test = train_test_split(X, y_next_role, test_size=0.2, random_state=42)
X_train, X_test, y_next_salary_train, y_next_salary_test = train_test_split(X, y_next_salary, test_size=0.2, random_state=42)

# Train Model for Next Role Prediction (Classification)
next_role_model = LogisticRegression(max_iter=1000)
next_role_model.fit(X_train, y_next_role_train)

# Train Model for Next Salary Prediction (Regression)
next_salary_model = RandomForestRegressor(n_estimators=100, random_state=42)
next_salary_model.fit(X_train, y_next_salary_train)

# Save Models & Encoders
joblib.dump(next_role_model, "next_role_model.pkl")
joblib.dump(next_salary_model, "next_salary_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

print("✅ AI Model Trained Successfully with 'Other' Category!")
