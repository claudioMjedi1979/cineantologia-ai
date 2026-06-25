import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_tmdb_key() -> str:
    """TMDb key — vem do .env local ou dos Secrets do Streamlit Cloud."""
    try:
        return st.secrets.get("TMDB_API_KEY", os.getenv("TMDB_API_KEY", ""))
    except Exception:
        return os.getenv("TMDB_API_KEY", "")

def _get_key(session_key: str, env_name: str) -> str:
    """Lê chave da sessão do usuário → Secrets do Streamlit Cloud → .env local."""
    if st.session_state.get(session_key):
        return st.session_state[session_key]
    try:
        secret = st.secrets.get(env_name, "")
        if secret:
            return secret
    except Exception:
        pass
    return os.getenv(env_name, "")


def get_openai_key() -> str:
    return _get_key("user_openai_key", "OPENAI_API_KEY")


def get_anthropic_key() -> str:
    return _get_key("user_anthropic_key", "ANTHROPIC_API_KEY")


def get_gemini_key() -> str:
    return _get_key("user_gemini_key", "GOOGLE_API_KEY")


def get_groq_key() -> str:
    return _get_key("user_groq_key", "GROQ_API_KEY")


AI_PROVIDERS = {
    "OpenAI": {
        "session_key": "user_openai_key",
        "placeholder": "sk-...",
        "docs_url": "https://platform.openai.com/api-keys",
        "models": ["gpt-4o-mini", "gpt-4o"],
        "default_model": "gpt-4o-mini",
    },
    "Claude (Anthropic)": {
        "session_key": "user_anthropic_key",
        "placeholder": "sk-ant-...",
        "docs_url": "https://console.anthropic.com/",
        "models": ["claude-haiku-4-5-20251001", "claude-sonnet-4-6"],
        "default_model": "claude-haiku-4-5-20251001",
    },
    "Gemini (Google)": {
        "session_key": "user_gemini_key",
        "placeholder": "AIza...",
        "docs_url": "https://aistudio.google.com/app/apikey",
        "models": ["gemini-1.5-flash", "gemini-2.0-flash"],
        "default_model": "gemini-1.5-flash",
    },
    "Groq (gratuito)": {
        "session_key": "user_groq_key",
        "placeholder": "gsk_...",
        "docs_url": "https://console.groq.com/keys",
        "models": ["llama-3.1-8b-instant", "llama3-70b-8192"],
        "default_model": "llama-3.1-8b-instant",
    },
}

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

DECADES = {
    "Anos 80": (1980, 1989),
    "Anos 90": (1990, 1999),
    "Anos 2000": (2000, 2009),
    "Anos 2010": (2010, 2019),
    "Anos 2020": (2020, 2029),
}

GENRES_MAP = {
    28: "Ação", 12: "Aventura", 16: "Animação", 35: "Comédia",
    80: "Crime", 99: "Documentário", 18: "Drama", 10751: "Família",
    14: "Fantasia", 36: "História", 27: "Terror", 10402: "Música",
    9648: "Mistério", 10749: "Romance", 878: "Ficção Científica",
    10770: "TV Movie", 53: "Suspense", 10752: "Guerra", 37: "Faroeste",
    # Gêneros exclusivos de TV
    10759: "Ação & Aventura", 10762: "Infantil", 10763: "Notícias",
    10764: "Reality", 10765: "Sci-Fi & Fantasia", 10766: "Novela",
    10767: "Talk Show", 10768: "Guerra & Política",
}

DORAMA_LANGUAGES = {
    "K-Drama (Coreano)": "ko",
    "J-Drama (Japonês)": "ja",
    "C-Drama (Chinês)": "zh",
    "Thai Drama (Tailandês)": "th",
}

MOVIE_LISTS = {
    "Populares": "popular",
    "Em Cartaz": "now_playing",
    "Próximas Estreias": "upcoming",
    "Mais Bem Avaliados": "top_rated",
}

TV_LISTS = {
    "Populares": "popular",
    "Em Exibição Hoje": "airing_today",
    "Na TV": "on_the_air",
    "Mais Bem Avaliadas": "top_rated",
}

# CSS global compartilhado entre todas as páginas
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0a0f !important;
    color: #e8e4dd;
}
[data-testid="stSidebar"] {
    background-color: #0f0f18 !important;
    border-right: 1px solid #1a1a28;
}
[data-testid="stSidebar"] * { color: #e8e4dd !important; }

h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 0.04em;
}
.section-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.08em;
    color: #e8e4dd;
    border-left: 3px solid #e5383b;
    padding-left: 12px;
    margin: 1.8rem 0 1rem 0;
}
.card {
    background: #14141e;
    border: 1px solid #1f1f2e;
    border-radius: 6px;
    overflow: hidden;
    height: 100%;
    transition: border-color .2s;
}
.card:hover { border-color: #e5383b; }
.card-body { padding: 10px; }
.card-title {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    color: #e8e4dd;
    margin: 0 0 4px 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.card-synopsis {
    font-size: 0.76rem;
    color: #9a9590;
    line-height: 1.45;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-top: 6px;
}
.badge {
    display: inline-block;
    background: #1f1f2e;
    color: #9a9590;
    font-size: 0.68rem;
    padding: 2px 8px;
    border-radius: 20px;
    margin: 2px 2px 0 0;
}
.rating { color: #f4c430; font-weight: 600; font-size: 0.78rem; }

/* Inputs */
.stTextInput > div > div > input {
    background: #14141e !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 6px !important;
    color: #e8e4dd !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #e5383b !important;
    box-shadow: 0 0 0 2px rgba(229,56,59,.12) !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: #14141e !important;
    border: 1px solid #2a2a3e !important;
    color: #e8e4dd !important;
}

/* Botões primários */
.stButton > button {
    background: #e5383b !important;
    color: #fff !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}
.stButton > button:hover { background: #c0282b !important; }

/* Tabs */
[data-testid="stTabs"] button {
    font-family: 'Inter', sans-serif !important;
    color: #5a5a72 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #e5383b !important;
    border-bottom-color: #e5383b !important;
}

footer { visibility: hidden; }
</style>
"""
