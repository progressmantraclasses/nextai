import React from "react";
import { Link } from "react-router-dom";

const features = [
  { name: "Mentors", link: "/careermentor", description: "AI suggests mentors based on career interests." },
  { name: "Career Path Predictor", link: "/careerpath", description: "Earn points, badges & certificates for completing career goals." },
  { name: "Career Quiz", link: "/career", description: "Personalized PDF reports with AI-suggested actions." },
  { name: "AI Consultation", link: "/ai", description: "AI mentor analyzes skills & preferences via WebRTC + GPT-4 Vision." },
  { name: "JOb's", link: "/jobs", description: "Answers career-related queries using ChatGPT API." },
  { name: "Learning Roadmap", link: "/learning", description: "Recommends skills, projects & certifications based on AI analysis." },
];

const LandingPage = () => {
  return (
    <div className="bg-[#0a0f1f] text-white min-h-screen">
      {/* Navbar */}
      <nav className="bg-[#12172c] p-4 shadow-lg fixed w-full top-0 z-10 border-b border-gray-600">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-cyan-400">AI Career Mapping Tool</h1>
          <ul className="flex space-x-6">
            <li><Link to="/" className="hover:text-cyan-300">Home</Link></li>
            {features.map((feature, index) => (
              <li key={index}><Link to={feature.link} className="hover:text-cyan-300">{feature.name}</Link></li>
            ))}
          </ul>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="relative h-screen flex flex-col justify-center items-center text-center px-6 mt-16 overflow-hidden">
        <video className="absolute top-0 left-0 w-full h-full object-cover opacity-30">
          <source src="https://aaftonline.com/blog/wp-content/uploads/2024/08/Career-Growth-vs-Career-Development-The-Key-Differences.jpg" />
        </video>
        <h2 className="text-6xl font-bold text-cyan-300 z-10 drop-shadow-lg">Your AI-Powered Career Guide</h2>
        <p className="mt-4 text-lg max-w-3xl text-gray-300 z-10">Navigate your tech career with AI-driven guidance, mentorship, skill-building, and job market insights – all in one place.</p>
        <Link to="/mentor-matching" className="mt-6 px-6 py-3 bg-cyan-500 rounded-lg hover:bg-cyan-600 text-white text-lg shadow-lg z-10">
          Get Started
        </Link>
      </header>

      {/* Features Section */}
      <section className="py-16 px-6 max-w-7xl mx-auto">
        <h3 className="text-3xl font-semibold text-center mb-10 text-cyan-400">Features</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="p-6 bg-white/10 backdrop-blur-lg rounded-xl shadow-xl border border-cyan-400/50 hover:shadow-cyan-500 transition-all duration-300 transform hover:-translate-y-2 hover:scale-105"
            >
              <h4 className="text-xl font-bold text-cyan-300">{feature.name}</h4>
              <p className="mt-2 text-gray-300">{feature.description}</p>
              <Link to={feature.link} className="mt-4 inline-block text-cyan-400 hover:underline">
                Learn More →
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#12172c] py-6 mt-12 text-center border-t border-gray-600">
        <p>&copy; 2025 AI Career Mapping Tool. All rights reserved.</p>
        <p className="mt-2 text-gray-400">Contact: support@careerai.com | Privacy Policy | Terms of Service</p>
      </footer>
    </div>
  );
};

export default LandingPage;
