import React, { useState } from "react";
import axios from "axios";
import { FaUserCircle } from "react-icons/fa"; // 👤 Profile Icon

const MentorRecommendation = () => {
  const [formData, setFormData] = useState({
    branch: "",
    skills: "",
    interest: "",
  });

  const [mentors, setMentors] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Handle Input Change
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Fetch Mentor Recommendations
  const fetchMentors = async () => {
    setLoading(true);
    setError("");
    setMentors([]);

    try {
      const response = await axios.post("http://127.0.0.1:5000/recommend_mentors", formData);
      setMentors(response.data.mentors);
    } catch (err) {
      setError("Failed to fetch mentors. Try again.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-10">
      <h1 className="text-4xl font-bold mb-6 text-center text-cyan-300">🚀 AI Mentor Recommendation</h1>

      <div className="max-w-2xl mx-auto bg-gray-800 p-6 rounded-lg shadow-lg">
        <div className="grid grid-cols-1 gap-4">
          <input
            type="text"
            name="branch"
            placeholder="Your Branch (e.g., CSE, Mechanical)"
            className="p-3 bg-gray-700 text-white rounded border border-gray-600 w-full"
            value={formData.branch}
            onChange={handleChange}
          />
          <input
            type="text"
            name="skills"
            placeholder="Top Skills (comma-separated)"
            className="p-3 bg-gray-700 text-white rounded border border-gray-600 w-full"
            value={formData.skills}
            onChange={handleChange}
          />
          <input
            type="text"
            name="interest"
            placeholder="Interest Field (e.g., AI, Blockchain, Cybersecurity)"
            className="p-3 bg-gray-700 text-white rounded border border-gray-600 w-full"
            value={formData.interest}
            onChange={handleChange}
          />
        </div>

        <div className="text-center mt-6">
          <button
            className="px-5 py-3 bg-cyan-500 rounded hover:bg-cyan-600 text-lg"
            onClick={fetchMentors}
            disabled={loading}
          >
            {loading ? "Fetching..." : "Get Mentor Recommendations"}
          </button>
        </div>
      </div>

      {/* Mentor Recommendations */}
      {mentors.length > 0 && (
        <div className="mt-10 max-w-5xl mx-auto">
          <h2 className="text-2xl mb-4 text-cyan-300 text-center">👨‍🏫 Top 10 Recommended Mentors</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mentors.map((mentor, index) => (
              <div
                key={index}
                className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-2xl transition-all hover:scale-105"
              >
                {/* 👤 Profile Icon */}
                <div className="flex items-center gap-3 mb-3">
                  <FaUserCircle className="text-gray-400 text-3xl" />
                  <h3 className="text-xl font-bold text-yellow-300">{mentor["Mentor Name"]}</h3>
                </div>

                <p className="text-gray-300">⭐ Rating: {mentor["Mentor Rating"]}/5</p>
                <p className="text-green-300">🏆 Field: {mentor["Field of Mastery"]}</p>
                <p className="text-blue-300">📈 Growth: {mentor["Career Growth"]}</p>
                <p className="text-gray-400">ℹ️ {mentor["About Career"]}</p>
                <p className="text-orange-400">🎓 Course: {mentor["Best Course"]}</p>

                {/* View Details Button */}
                <a
                  href={`/mentor/${mentor["Mentor Name"].replace(/\s+/g, "-").toLowerCase()}`}
                  className="mt-4 inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-all"
                >
                  View Details →
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {error && <p className="text-red-500 text-center mt-6">{error}</p>}
    </div>
  );
};

export default MentorRecommendation;
