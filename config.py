import os

os.environ["USE_TF"] = "0"
os.environ["TRANSFORMERS_NO_TF"] = "1"

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Embedding
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

# Retrieval
TOP_K = 3

# Ollama models
OLLAMA_RAG_MODEL = "mistral"
OLLAMA_VISION_MODEL = "llava"

# Database
DB_PATH = BASE_DIR / "db" / "embeddings.db"

# Knowledge base
KNOWLEDGE_DIR = BASE_DIR / "knowledge"

# User history
MAX_HISTORY = 3
