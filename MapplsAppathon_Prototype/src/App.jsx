import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import AIVideoConsultation from "./components/AIVideoConsultation";
import CareerForm from "./components/CareerForm";
import GetJobs from "./components/GetJobs";
import CareerPath from "./components/CareerPath";
import CareerMentor from "./components/CareerMentor";
import LearningRoadmap from "./components/LearningRoadmap";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/ai" element={<AIVideoConsultation />} />
        <Route path="/career" element={<CareerForm />} />
        <Route path="/jobs" element={<GetJobs />} />
        <Route path="/careerpath" element={<CareerPath />} />
        <Route path="/careermentor" element={<CareerMentor />} />
        <Route path="/learning" element={<LearningRoadmap />} />
      </Routes>
    </Router>
  );
}

export default App;