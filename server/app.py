from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import traceback

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)  # Allow frontend requests



# ✅ Load trained model & encoders
model = pickle.load(open("career_model.pkl", "rb"))
label_encoders = pickle.load(open("label_encoders.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route("/")
def home():
    return "Career Prediction API is Running! 🚀"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        print("\n========================= REQUEST RECEIVED =========================")
        print("🔍 Headers:", request.headers)

        # ✅ Ensure JSON data is received
        if request.headers.get("Content-Type") != "application/json":
            return jsonify({"error": "Invalid content type. Use application/json"}), 415

        data = request.get_json()
        print("✅ Received Raw Data:", data)

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        # ✅ Define Expected Feature Order
        expected_features = [
            "Gender", "Age", "GPA", "Major", "Interested Domain", "Projects",
            "Internships", "Certifications", "Python", "SQL", "Java", "C++",
            "JavaScript", "Cloud", "AI", "Cybersecurity", "Soft Skills", "Work Experience (Years)"
        ]

        # ✅ Convert received JSON data into DataFrame
        input_df = pd.DataFrame([data])

        # ✅ Rename columns to match training data
        rename_map = {"Interested_Domain": "Interested Domain"}
        input_df.rename(columns=rename_map, inplace=True)

        # ✅ Fill missing columns with default values
        for col in expected_features:
            if col not in input_df.columns:
                print(f"⚠️ Missing feature: {col} - Filling with default value")
                input_df[col] = "None" if col in label_encoders else 0

        # ✅ Ensure correct column order
        input_df = input_df[expected_features]

        # ✅ Encode categorical variables safely
        categorical_features = ["Gender", "Major", "Interested Domain", "Certifications", "Soft Skills"]
        for col in categorical_features:
            if col in label_encoders:
                if input_df[col].values[0] not in label_encoders[col].classes_:
                    print(f"⚠️ Unseen category in '{col}': {input_df[col].values[0]}. Adding it dynamically.")
                    label_encoders[col].classes_ = np.append(label_encoders[col].classes_, input_df[col].values[0])
                input_df[col] = label_encoders[col].transform([input_df[col].values[0]])

        # ✅ Scale numerical values
        numerical_features = ["GPA", "Age", "Projects", "Internships", "Python", "SQL", "Java", "C++",
                              "JavaScript", "Cloud", "AI", "Cybersecurity", "Work Experience (Years)"]
        input_df[numerical_features] = scaler.transform(input_df[numerical_features])

        print("\n📊 Final Processed Data for Prediction:\n", input_df)

        # ✅ Predict career
        prediction = model.predict(input_df)
        predicted_career = label_encoders["Future Career"].inverse_transform(prediction)[0]

        print("✅ Predicted Career:", predicted_career)
        return jsonify({"career_prediction": predicted_career})

    except Exception as e:
        print("❌ Error Occurred:", str(e))
        print(traceback.format_exc())  # Print full error details for debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # ✅ Allow external access





