import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("students_data.csv")

# Drop unnecessary columns
df.drop(columns=["Student ID", "Name", "Projects"], inplace=True)

# Mapping Skill Levels to Numeric Values
skill_mapping = {"Weak": 1, "Average": 5, "Strong": 10}
df["Python"] = df["Python"].map(skill_mapping)
df["SQL"] = df["SQL"].map(skill_mapping)
df["Java"] = df["Java"].map(skill_mapping)

# Convert numerical columns properly
df["GPA"] = pd.to_numeric(df["GPA"], errors="coerce")
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

# Remove rows with missing values
df.dropna(inplace=True)

# Encode categorical variables
label_encoders = {}
categorical_columns = ["Gender", "Major", "Interested Domain", "Future Career"]

for col in categorical_columns:
    label_encoders[col] = LabelEncoder()
    df[col] = label_encoders[col].fit_transform(df[col])  # Convert text to numbers

# Normalize numerical values
scaler = StandardScaler()
df[["GPA", "Age", "Python", "SQL", "Java"]] = scaler.fit_transform(df[["GPA", "Age", "Python", "SQL", "Java"]])

# Splitting data into features & target
X = df.drop(columns=["Future Career"])  # Features
y = df["Future Career"]  # Target variable (now encoded)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model, encoders, and scaler
pickle.dump(model, open("career_model.pkl", "wb"))
pickle.dump(label_encoders, open("label_encoders.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("✅ Model training complete & saved successfully!")
