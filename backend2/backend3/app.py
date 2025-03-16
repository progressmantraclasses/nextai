from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔹 Load the Mentor Data
df = pd.read_csv("career_mentors_data.csv")  # ✅ Ensure this file exists

# 🔹 API Endpoint for Mentor Recommendation
@app.route("/recommend_mentors", methods=["POST"])
def recommend_mentors():
    try:
        data = request.json
        branch = data.get("branch")
        skills = data.get("skills")
        interest = data.get("interest")

        if not all([branch, skills, interest]):
            return jsonify({"error": "Missing required fields"}), 400

        # 🔹 Filter mentors based on interest & skills
        filtered_mentors = df[df["Field of Mastery"].str.contains(interest, case=False, na=False)]

        # 🔹 Select Top 10 Mentors Sorted by Rating
        top_mentors = filtered_mentors.sort_values(by="Mentor Rating", ascending=False).head(10)

        # 🔹 Convert to JSON
        mentor_list = top_mentors.to_dict(orient="records")

        return jsonify({"mentors": mentor_list})

    except Exception as e:
        return jsonify({"error": str(e)})

# 🔹 Run Flask App
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
