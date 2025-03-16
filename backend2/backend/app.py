from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Models & Encoders
next_role_model = joblib.load("next_role_model.pkl")
next_salary_model = joblib.load("next_salary_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# 🔹 Function to Handle Unseen Labels
def safe_encode(encoder, value):
    """Returns encoded value if it exists, else assigns 'Other' category"""
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        print(f"⚠️ Unseen value detected: {value}. Assigning to 'Other'.")
        return encoder.transform(["Other"])[0]  # Assign "Other" category for unseen labels

# 🔹 Prediction Function
def predict_career_path(current_role, gender, skills, experience, current_salary):
    try:
        # Encode Inputs Safely
        encoded_role = safe_encode(label_encoders["Current Role"], current_role)
        encoded_gender = safe_encode(label_encoders["Gender"], gender)
        encoded_skills = safe_encode(label_encoders["Top Skills"], skills)
        encoded_experience = safe_encode(label_encoders["Experience"], experience)

        # Prepare Input for Prediction
        X_input = np.array([[encoded_role, encoded_gender, encoded_skills, encoded_experience, float(current_salary)]])
        
        # Predict Next Role & Salary
        predicted_role_encoded = next_role_model.predict(X_input)[0]
        predicted_salary = next_salary_model.predict(X_input)[0]

        # Decode Predicted Role
        predicted_role = label_encoders["Next Role"].inverse_transform([predicted_role_encoded])[0]

        return {"next_role": predicted_role, "expected_salary": f"₹{round(predicted_salary, 2)} LPA"}
    
    except Exception as e:
        return {"error": str(e)}

# 🔹 API Endpoint
@app.route("/predict_career", methods=["POST"])
def predict_career():
    data = request.json
    current_role = data.get("current_role")
    gender = data.get("gender")
    skills = data.get("skills")
    experience = data.get("experience")
    current_salary = data.get("current_salary")

    if not all([current_role, gender, skills, experience, current_salary]):
        return jsonify({"error": "Missing required fields"}), 400

    prediction = predict_career_path(current_role, gender, skills, experience, current_salary)
    return jsonify(prediction)

# 🔹 Run Flask App
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
