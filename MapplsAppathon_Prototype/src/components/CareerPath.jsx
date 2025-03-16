import React, { useState } from "react";
import axios from "axios";

const CareerPath = () => {
  const [formData, setFormData] = useState({
    current_role: "",
    gender: "",
    skills: "",
    experience: "",
    current_salary: ""
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");

  // 🔹 Handle Input Changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 🔹 Fetch AI Predictions
  const fetchCareerPrediction = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict_career", formData);
      setPrediction(response.data);
      setError("");
    } catch (err) {
      setError("Career path not found. Try a different role.");
      setPrediction(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-10">
      <h1 className="text-4xl font-bold mb-6 text-center">🚀 AI Career Path Predictor</h1>

      <div className="max-w-2xl mx-auto bg-gray-800 p-6 rounded-lg shadow-lg">
        {/* Input Fields */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            name="current_role"
            placeholder="Enter your current job role..."
            className="p-3 bg-gray-700 text-white rounded border border-gray-600 w-full"
            value={formData.current_role}
            onChange={handleChange}
          />
          <select
            name="gender"
            className="p-3 bg-gray-700 text-white rounded border border-gray-600 w-full"
            value={formData.gender}
            onChange={handleChange}
          >
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Non-Binary">Non-Binary</option>
          </select>
          <input
            type="text"
            name="skills"
            placeholder="Top Skills (comma-separated)..."
            className="p-3 bg-gray-700 text-white rounded border border-gray-600 w-full"
            value={formData.skills}
            onChange={handleChange}
          />
          <select
            name="experience"
            className="p-3 bg-gray-700 text-white rounded border border-gray-600 w-full"
            value={formData.experience}
            onChange={handleChange}
          >
            <option value="">Select Experience</option>
            <option value="0-2 years">0-2 years</option>
            <option value="3-5 years">3-5 years</option>
            <option value="6-8 years">6-8 years</option>
            <option value="9-12 years">9-12 years</option>
            <option value="12+ years">12+ years</option>
          </select>
          <input
            type="number"
            name="current_salary"
            placeholder="Current Salary (in LPA)..."
            className="p-3 bg-gray-700 text-white rounded border border-gray-600 w-full"
            value={formData.current_salary}
            onChange={handleChange}
          />
        </div>

        {/* Predict Button */}
        <div className="text-center mt-6">
          <button
            className="px-5 py-3 bg-blue-600 rounded hover:bg-blue-800 text-lg"
            onClick={fetchCareerPrediction}
          >
            Predict Career Path
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && <p className="text-red-500 text-center mt-4">{error}</p>}

      {/* Prediction Results */}
      {prediction && (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg mt-6 max-w-2xl mx-auto">
          <h2 className="text-2xl mb-4 text-center">🎯 Your Future Career Prediction 🚀</h2>
          <p className="text-green-300 text-lg">
            <strong>Next Role:</strong> {prediction.next_role}
          </p>
          <p className="text-yellow-300 text-lg">
            <strong>Expected Salary:</strong> {prediction.expected_salary}
          </p>
        </div>
      )}
    </div>
  );
};

export default CareerPath;
