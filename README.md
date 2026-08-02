# 🪞 Voice Journal — To reflect back on your moments

This is a voice-first journaling app. Speak your thoughts, and the app transcribes them, senses the emotional tone, and responds with a short, warm reflection — no typing required.

What it does:
Record — Speak a journal entry into your mic.
Transcribe — Your voice is converted to text using Azure AI Speech.
Sense the mood — Azure AI Language analyzes the sentiment of your entry (positive / negative / neutral / mixed).
Reflect — Azure OpenAI generates a short, encouraging reflection based on what you said and how you're feeling.

All of this happens in a single, minimal interface — record, and the reflection appears.

Azure AI Services Used:
Service	Purpose
Azure AI Speech	Converts recorded voice journal entries into text
Azure AI Language (Sentiment Analysis)	Detects the emotional tone of the journal entry
Azure OpenAI	Generates a personalized, mood-aware reflection
🛠️ Tech Stack
Frontend/App: Streamlit
Speech-to-Text: azure-cognitiveservices-speech
Sentiment Analysis: azure-ai-textanalytics
Text Generation: openai (Azure OpenAI SDK)
Deployment: Azure App Service

Setup & Installation:
Clone the repo
bash
   git clone https://github.com/Anjali875/Voice-Journal-Azure-.git
   cd Voice Journal
Create and activate a virtual environment
bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
Install dependencies
bash
   pip install -r requirements.txt

Set up environment variables Create a .env file in the project root:
   VISIONAI_KEY=your_azure_ai_services_key
   VISIONAI_REGION=your_region
   VISIONAI_ENDPOINT=your_azure_ai_services_endpoint

   AZURE_OPENAI_KEY=your_openai_key
   AZURE_OPENAI_ENDPOINT=your_openai_endpoint
   AZURE_OPENAI_DEPLOYMENT=your_deployment_name
   AZURE_OPENAI_API_VERSION=2024-12-01-preview
Run the app:
   streamlit run main.py
Deployment:
Deployed through Vercel

Why This Project:
Most AI demos are text-in, text-out. Voice Journal is built around a fully voice-driven, emotionally-aware interaction — speaking your day out loud and getting a moment of reflection back, without needing to read or type anything.
