
"""Central settings. Edit values here only; every other file imports them."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"

# Names come from check_setup.py output (Part 6). Chat name has NO "models/" prefix.
CHAT_MODEL = "gemini-3.6-flash"
EMBED_MODEL = "models/gemini-embedding-001"

CHUNK_SIZE = 800        # characters per chunk
CHUNK_OVERLAP = 150     # characters shared between neighbouring chunks
TOP_K = 4               # chunks retrieved per question
MAX_DISTANCE = 1.0      # relevance cutoff: lower = stricter (tune in Part 9)
MAX_QUESTION_CHARS = 500

REFUSAL = ("I can only answer HR and recruitment questions "
           "based on the company documents.")
