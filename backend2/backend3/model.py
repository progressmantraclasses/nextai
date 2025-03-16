import pandas as pd  # ✅ Import pandas
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# 🔹 Load dataset
df = pd.read_csv("career_mentors_data.csv")  # ✅ Make sure file exists

# 🔹 Encode categorical variables
label_encoders = {}
for column in ["Mentor Name", "Field of Mastery", "Best Course", "Platform", "Certifications Needed", "Internship Opportunities"]:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# 🔹 Selecting features and target variables
X = df[["Field of Mastery", "Best Course", "Platform", "Certifications Needed"]]
y_mentor = df["Mentor Name"]
y_internship = df["Internship Opportunities"]

# 🔹 Splitting the dataset
X_train, X_test, y_mentor_train, y_mentor_test = train_test_split(X, y_mentor, test_size=0.2, random_state=42)
X_train, X_test, y_internship_train, y_internship_test = train_test_split(X, y_internship, test_size=0.2, random_state=42)

# 🔹 Training models
mentor_model = RandomForestClassifier(n_estimators=100, random_state=42)
mentor_model.fit(X_train, y_mentor_train)

internship_model = RandomForestClassifier(n_estimators=100, random_state=42)
internship_model.fit(X_train, y_internship_train)

# 🔹 Save models and encoders
joblib.dump(mentor_model, "mentor_model.pkl")
joblib.dump(internship_model, "internship_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

print("✅ AI Mentor & Internship Prediction Model Trained Successfully!")
