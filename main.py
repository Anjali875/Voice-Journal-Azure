import os
import tempfile
import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


VISIONAI_KEY = os.getenv("VISIONAI_KEY")
VISIONAI_REGION = os.getenv("VISIONAI_REGION")
VISIONAI_ENDPOINT = os.getenv("VISIONAI_ENDPOINT")

openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

text_client = TextAnalyticsClient(
    endpoint=VISIONAI_ENDPOINT,
    credential=AzureKeyCredential(VISIONAI_KEY)
)


def transcribe_audio(audio_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    speech_config = speechsdk.SpeechConfig(subscription=VISIONAI_KEY, region=VISIONAI_REGION)
    audio_config = speechsdk.AudioConfig(filename=tmp_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = recognizer.recognize_once()

    
    del recognizer
    del audio_config

   
    try:
        os.remove(tmp_path)
    except PermissionError:
        pass  
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return None


def analyze_mood(text):
    response = text_client.analyze_sentiment([text])[0]
    return response.sentiment, response.confidence_scores


def generate_reflection(text, mood):
    prompt = f"The user just journaled: \"{text}\"\nTheir detected mood is: {mood}.\nWrite a warm, brief, encouraging reflection (2-3 sentences) that acknowledges how they're feeling."
    response = openai_client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a gentle, supportive journaling companion. Keep responses short and warm."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content


st.set_page_config(page_title="Voice Journal", page_icon="🪞", layout="centered")

st.markdown("""
    <style>
        .stApp {
            background-color: #1a1420;
        }
        .main { background-color: transparent; }
        h1 {
            color: #e8b4bc;
        }
        .stCaption, p {
            color: #a89bb0;
        }
        .mood-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
            margin: 8px 0 16px 0;
        }
        .mood-positive { background-color: #2d3b32; color: #9fd8ac; }
        .mood-negative { background-color: #3b2530; color: #e39aab; }
        .mood-neutral { background-color: #2a2838; color: #a8a0c8; }
        .mood-mixed { background-color: #3a3325; color: #d4b876; }
        .reflection-card {
            background-color: #241d2b;
            border: 1px solid #3d3145;
            border-radius: 14px;
            padding: 20px;
            margin-top: 12px;
            line-height: 1.6;
            color: #e8dfe8;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        .transcript-box {
            background-color: #2a2130;
            border-left: 3px solid #c98ba0;
            padding: 12px 16px;
            border-radius: 8px;
            font-style: italic;
            color: #d9b8c4;
            margin: 12px 0;
        }
        div[data-testid="stAudioInput"] {
            background-color: #241d2b;
            border: 1px solid #3d3145;
            border-radius: 14px;
            padding: 4px;
        }
    </style>
""", unsafe_allow_html=True)
st.title("🪞 Voice Journal")
st.caption("Speak your mind. Reflect on your thoughts and moments.")

st.write("")
audio_value = st.audio_input("Record your journal entry")

if audio_value:
    with st.spinner("Listening..."):
        transcript = transcribe_audio(audio_value.getvalue())

    if not transcript:
        st.error("Couldn't quite catch that — try speaking a bit longer or clearer.")
    else:
        st.markdown(f'<div class="transcript-box">"{transcript}"</div>', unsafe_allow_html=True)

        with st.spinner("Sensing the mood..."):
            mood, scores = analyze_mood(transcript)

        mood_class = f"mood-{mood}"
        st.markdown(f'<span class="mood-badge {mood_class}">{mood.upper()}</span>', unsafe_allow_html=True)

        with st.spinner("Reflecting..."):
            reflection = generate_reflection(transcript, mood)

        st.markdown(f'<div class="reflection-card">{reflection}</div>', unsafe_allow_html=True)