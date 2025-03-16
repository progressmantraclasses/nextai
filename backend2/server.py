from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# 🔹 Adzuna API Configuration (Replace with your API Key)
ADZUNA_API_ID = "83230ad8"  # 🔥 Replace with your API ID
ADZUNA_API_KEY = "bf37a2d589a340997bae225d742647a5"  # 🔥 Replace with your API Key
API_URL = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={ADZUNA_API_ID}&app_key={ADZUNA_API_KEY}&results_per_page=20&what="

# 🔹 Career Categories
CAREER_FIELDS = [
    "Data Scientist", "Software Engineer", "Cybersecurity Analyst", "AI Researcher", "Web Developer",
    "Digital Marketer", "Blockchain Developer", "Product Manager", "Network Engineer", "UX/UI Designer",
    "Machine Learning Engineer", "DevOps Engineer", "Cloud Architect", "Business Analyst", "Game Developer",
    "Financial Analyst", "Healthcare Data Analyst", "Civil Engineer", "Marketing Specialist", "HR Manager"
]

# 🔹 Fetch Job Market Data for 20+ Careers
def fetch_jobs():
    career_data = []
    
    for career in CAREER_FIELDS:
        response = requests.get(API_URL + career)
        if response.status_code == 200:
            jobs = response.json().get('results', [])
            career_data.append({
                "career": career,
                "job_count": len(jobs),
                "top_companies": list(set([job["company"]["display_name"] for job in jobs[:5]]))  # Get top 5 companies
            })
    
    return career_data

# 🔹 AI Model to predict future trends (Mock Data)
def predict_future_trends():
    return {
    "Data Science": "+42% (Google Trends)",
    "Cybersecurity": "+65% (Google Trends)",
    "AI Research": "+38% (Adzuna Job Market)",
    "Cloud Computing": "+38% (Adzuna Job Market)",
    "Blockchain Development": "+28% (Google Trends)",
    "Machine Learning": "+60% (Google Trends)",
    "Software Engineering": "+23% (Google Trends)",
    "DevOps": "+18% (Adzuna Job Market)",
    "Game Development": "+35% (Google Trends)",
    "Web Development": "+14% (Google Trends)",
    "Product Management": "+19% (Google Trends)",
    "UI/UX Design": "+26% (Google Trends)",
    "HR Technology": "+8% (Adzuna Job Market)",
    "Marketing": "+22% (Google Trends)",
    "Financial Analysis": "+30% (Google Trends)",
    "Healthcare Analytics": "+57% (Google Trends)",
    "Civil Engineering": "+12% (Adzuna Job Market)",
    "Digital Marketing": "+45% (Google Trends)",
    "Network Engineering": "+11% (Google Trends)",
    "Accounting": "-10% (Google Trends)"
}


@app.route('/get_jobs', methods=['GET'])
def get_jobs():
    jobs = fetch_jobs()
    return jsonify({"careers": jobs})

@app.route('/predict_career_growth', methods=['GET'])
def predict_career_growth():
    trends = predict_future_trends()
    return jsonify({"career_growth": trends})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


