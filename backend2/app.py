from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import os
from pydub import AudioSegment
import tempfile
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini API (Replace with your valid API key)
genai.configure(api_key="AIzaSyC42XOUXsiO2pB1TR2Lw1nqZfo8Z97uC6M") #<---Insert API Key here

try:
    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_audio(audio_file_path):
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"
        except Exception as e:
            return f"An error occurred during audio processing: {e}"

    def get_career_advice(transcript):
        if transcript:
            try:
                # Call Gemini API for career advice
                response = model.generate_content(
                    f"Based on the following conversation, provide career advice:\n\n{transcript}\n\nCareer advice:"
                )
                return response.text.strip()
            except Exception as e:
                return f"Error getting career advice from Gemini: {e}"
        else:
            return "No audio transcript available."

    @app.route('/analyze', methods=['POST'])
    def analyze_video():
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400

        video_file = request.files['video']

        if video_file.filename == '':
            return jsonify({'error': 'No selected video file'}), 400

        if video_file:
            try:
                video_path = tempfile.mktemp(suffix=".webm")
                video_file.save(video_path)

                audio_path = tempfile.mktemp(suffix=".wav")
                video = AudioSegment.from_file(video_path, "webm")
                video.export(audio_path, format="wav")

                transcript = analyze_audio(audio_path)

                career_advice = get_career_advice(transcript)

                os.remove(video_path)
                os.remove(audio_path)

                return jsonify({'analysis': career_advice})

            except Exception as e:
                return jsonify({'error': f"An error occurred: {e}"}), 500
        else:
            return jsonify({'error': 'Invalid video file'}), 400

    if __name__ == '__main__':
        app.run(debug=True)

except Exception as e:
    print(f"Error initializing Gemini: {e}")
    print("Please check your API key and ensure 'gemini-pro' is accessible.")