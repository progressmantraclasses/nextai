import React, { useRef, useState } from "react";
import axios from "axios";

function AIVideoConsultation() {
    const videoRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const [recording, setRecording] = useState(false);
    const [careerAdvice, setCareerAdvice] = useState("");
    const [videoBlob, setVideoBlob] = useState(null);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            videoRef.current.srcObject = stream;
            mediaRecorderRef.current = new MediaRecorder(stream);

            let chunks = [];
            mediaRecorderRef.current.ondataavailable = (event) => chunks.push(event.data);

            mediaRecorderRef.current.onstop = () => {
                const blob = new Blob(chunks, { type: "video/webm" });
                setVideoBlob(blob);
            };

            mediaRecorderRef.current.start();
            setRecording(true);

            setTimeout(() => stopRecording(), 60000);
        } catch (error) {
            console.error("Error accessing camera", error);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current) {
            mediaRecorderRef.current.stop();
            setRecording(false);
            videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
        }
    };

    const uploadVideo = async () => {
        if (!videoBlob) {
            alert("No video recorded");
            return;
        }

        const formData = new FormData();
        formData.append("video", videoBlob, "recorded-video.webm");

        try {
            const response = await axios.post("http://127.0.0.1:5000/analyze", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            setCareerAdvice(response.data.analysis);
        } catch (error) {
            console.error("Error analyzing video:", error);
            alert("Failed to analyze the video");
        }
    };

    return (
        <div className="bg-gray-900 text-white min-h-screen flex flex-col items-center justify-center p-6">
            <h1 className="text-4xl font-bold text-blue-400 mb-6">AI Career Guidance</h1>
            <div className="border-2 border-blue-500 p-4 rounded-lg shadow-lg">
                <video ref={videoRef} autoPlay muted className="w-96 rounded-lg border border-gray-700"></video>
                <div className="flex justify-center space-x-4 mt-4">
                    {!recording ? (
                        <button
                            onClick={startRecording}
                            className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-6 rounded-lg transition duration-200"
                        >
                            Start Recording
                        </button>
                    ) : (
                        <button
                            onClick={stopRecording}
                            className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-6 rounded-lg transition duration-200"
                        >
                            Stop Recording
                        </button>
                    )}
                </div>
                <button
                    onClick={uploadVideo}
                    className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-lg mt-4 transition duration-200 w-full"
                >
                    Analyze Career
                </button>
            </div>
            {careerAdvice && (
                <div className="mt-6 p-6 bg-gray-800 rounded-lg shadow-lg w-full max-w-2xl">
                    <h2 className="text-2xl font-bold text-blue-300">Career Suggestions:</h2>
                    <p className="mt-2 text-gray-300 whitespace-pre-line">{careerAdvice}</p>
                </div>
            )}
        </div>
    );
}

export default AIVideoConsultation;
