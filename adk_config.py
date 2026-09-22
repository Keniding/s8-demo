import os

PROYECTO = "agentpay-latam-lab"
REGION = "us-central1"
MODELO = "gemini-2.5-flash-lite"

os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", PROYECTO)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", REGION)
