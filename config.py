import os

from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_BASE = "https://api.together.xyz/v1"
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
