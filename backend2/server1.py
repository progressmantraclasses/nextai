
from flask import Flask, jsonify
import requests
from flask_cors import CORS
from pytrends.request import TrendReq
import time

app = Flask(__name__)
CORS(app)  # Enable CORS

# 🔹 Adzuna API Configuration (Replace with your API Key)
ADZUNA_API_ID = "83230ad8"  # 🔥 Replace with your API ID
ADZUNA_API_KEY = "bf37a2d589a340997bae225d742647a5"  # 🔥 Replace with your API Key
API_URL = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={ADZUNA_API_ID}&app_key={ADZUNA_API_KEY}&results_per_page=20&what="

# 🔹 Career Fields for Prediction
CAREER_FIELDS = [
    "Data Science", "Software Engineering", "Cybersecurity", "AI Research", "Web Development",
    "Blockchain", "Machine Learning", "DevOps", "Cloud Computing", "Game Development",
    "Digital Marketing", "Product Management", "Networking", "UI/UX Design", "Finance Analysis",
    "Healthcare Analytics", "Civil Engineering", "Marketing", "HR Management", "Business Analysis"
]

# 🔹 Google Trends Setup
pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))

# 🔹 Fetch Job Market Data for 20+ Careers (From Adzuna API)
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
        else:
            career_data.append({
                "career": career,
                "job_count": 0,
                "top_companies": [],
                "error": "Failed to fetch data"
            })
    
    return career_data

# 🔹 Get Career Growth Trends from Google Trends
def fetch_google_trends():
    trends_data = {}

    for career in CAREER_FIELDS:
        try:
            print(f"Fetching Google Trends data for: {career}")  # Debugging log
            pytrends.build_payload([career], timeframe='today 5-y', geo='IN')
            trend = pytrends.interest_over_time()

            if not trend.empty:
                last_value = trend.iloc[-1][career]  # Get latest trend data
                trends_data[career] = f"+{last_value}% (Based on Google Trends)" if last_value >= 0 else f"{last_value}% (Declining)"
            else:
                trends_data[career] = "No Data Available"

            time.sleep(10)  # 🔥 Google Trends API Rate Limit Handling
        except Exception as e:
            print(f"Error fetching {career}: {e}")  # Debugging log
            trends_data[career] = "API Error"

    return trends_data

# 🔹 API Endpoint: Fetch Job Market Data
@app.route('/get_jobs', methods=['GET'])
def get_jobs():
    jobs = fetch_jobs()
    return jsonify({"careers": jobs})

# 🔹 API Endpoint: Fetch Career Growth Trends
@app.route('/predict_career_growth', methods=['GET'])
def predict_career_growth():
    trends = fetch_google_trends()
    return jsonify({"career_growth": trends})

# 🔹 Handle Invalid API Calls (404 Error)
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Invalid endpoint. Use /get_jobs or /predict_career_growth"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
