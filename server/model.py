import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# ✅ **Load Dataset**
df = pd.read_csv("student_career_data_5000.csv")  # Ensure file is in the same directory

# ✅ **Define Features & Target**
features = [
    "Gender", "Age", "GPA", "Major", "Interested Domain", "Projects", "Internships",
    "Certifications", "Python", "SQL", "Java", "C++", "JavaScript", "Cloud",
    "AI", "Cybersecurity", "Soft Skills", "Work Experience (Years)"
]
target = "Future Career"

X = df[features]
y = df[target]

# ✅ **Encode Categorical Variables**
label_encoders = {}
categorical_features = ["Gender", "Major", "Interested Domain", "Certifications", "Soft Skills"]

for col in categorical_features:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])  # Convert categories to numbers
    label_encoders[col] = le

# ✅ **Encode Target Variable**
le_target = LabelEncoder()
y = le_target.fit_transform(y)
label_encoders["Future Career"] = le_target  # Save for later decoding

# ✅ **Scale Numerical Features**
numerical_features = [
    "GPA", "Age", "Projects", "Internships", "Python", "SQL", "Java",
    "C++", "JavaScript", "Cloud", "AI", "Cybersecurity", "Work Experience (Years)"
]
scaler = StandardScaler()
X[numerical_features] = scaler.fit_transform(X[numerical_features])

# ✅ **Split Data for Training & Testing**
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ **Train the Model (Random Forest)**
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# ✅ **Save the Model & Encoders**
pickle.dump(model, open("career_model.pkl", "wb"))
pickle.dump(label_encoders, open("label_encoders.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("✅ Model training complete! 🎯")
