import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services import tmdb_service
from app.utils.config import (
    DECADES, GENRES_MAP, DORAMA_LANGUAGES,
    MOVIE_LISTS, TV_LISTS, GLOBAL_CSS,
)
from app.utils.sidebar import render_sidebar

st.set_page_config(page_title="Catálogo · CineAntologia AI", page_icon="🎞️", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown('<p style="font-family:\'Bebas Neue\',sans-serif;font-size:2.2rem;letter-spacing:.05em;margin-bottom:.3rem">CATÁLOGO</p>', unsafe_allow_html=True)

# ── Linha 1: Busca ────────────────────────────────────────────────────────────
default_q = st.session_state.pop("search_query", "")
query = st.text_input("", placeholder="🔍  Buscar título...", value=default_q, label_visibility="collapsed")

# ── Linha 2: Tipo + Categoria/Origem ─────────────────────────────────────────
fc1, fc2 = st.columns([1.5, 2])
with fc1:
    tipo = st.selectbox("Tipo", ["Todos", "Filme", "Série", "Anime", "Dorama"])

# Categorias dependem do tipo (estilo TMDb)
categoria = None
dorama_lang = "ko"
with fc2:
    if tipo == "Filme":
        categoria = st.selectbox("Categoria", list(MOVIE_LISTS.keys()) + ["Descobrir (por gênero/década)"])
    elif tipo == "Série":
        categoria = st.selectbox("Categoria", list(TV_LISTS.keys()) + ["Descobrir (por gênero/década)"])
    elif tipo == "Dorama":
        dorama_lang = DORAMA_LANGUAGES.get(
            st.selectbox("Origem", list(DORAMA_LANGUAGES.keys())), "ko"
        )
    else:
        st.write("")  # espaço vazio para Todos e Anime

# ── Linha 3: Década + Gênero (só no modo Descobrir) ──────────────────────────
use_discover = tipo in ("Todos", "Anime", "Dorama") or categoria == "Descobrir (por gênero/década)"
decada, genero = "Todas", "Todos os Gêneros"
if use_discover and tipo not in ("Anime", "Dorama"):
    fd1, fd2 = st.columns(2)
    with fd1:
        decada = st.selectbox("Década", ["Todas"] + list(DECADES.keys()))
    with fd2:
        genre_names = ["Todos os Gêneros"] + sorted(GENRES_MAP.values())
        genero = st.selectbox("Gênero", genre_names)
elif tipo in ("Anime", "Dorama"):
    fd1, _ = st.columns(2)
    with fd1:
        decada = st.selectbox("Década", ["Todas"] + list(DECADES.keys()))

# ── Busca / Listas / Discover ─────────────────────────────────────────────────
results = []
year_start, year_end = DECADES.get(decada, (1980, 2029)) if decada != "Todas" else (1980, 2029)
genre_id = next((k for k, v in GENRES_MAP.items() if v == genero), None)

with st.spinner("Buscando..."):
    if query:
        results = tmdb_service.search_multi(query)
        if tipo not in ("Todos",):
            results = [r for r in results if r["type"] == tipo]
    elif tipo == "Filme" and categoria and categoria != "Descobrir (por gênero/década)":
        results = tmdb_service.get_movie_list(MOVIE_LISTS[categoria])
    elif tipo == "Série" and categoria and categoria != "Descobrir (por gênero/década)":
        results = tmdb_service.get_tv_list(TV_LISTS[categoria])
    elif tipo == "Anime":
        results = tmdb_service.discover_anime(year_start, year_end)
    elif tipo == "Dorama":
        results = tmdb_service.discover_dorama(dorama_lang, year_start, year_end)
    elif tipo == "Todos":
        m = tmdb_service.discover("movie", year_start, year_end, genre_id)[:10]
        s = tmdb_service.discover("tv", year_start, year_end, genre_id)[:10]
        results = m + s
    else:
        mt = {"Filme": "movie", "Série": "tv"}.get(tipo, "movie")
        results = tmdb_service.discover(mt, year_start, year_end, genre_id)

# ── Label dos resultados ──────────────────────────────────────────────────────
if query:
    label = f"{len(results)} TÍTULOS ENCONTRADOS"
elif tipo == "Filme" and categoria and categoria != "Descobrir (por gênero/década)":
    label = f"FILMES · {categoria.upper()}"
elif tipo == "Série" and categoria and categoria != "Descobrir (por gênero/década)":
    label = f"SÉRIES · {categoria.upper()}"
elif tipo in ("Anime", "Dorama"):
    label = f"{tipo.upper()} · {decada.upper() if decada != 'Todas' else 'TODAS AS DÉCADAS'}"
else:
    label = f"CATÁLOGO · {decada.upper() if decada != 'Todas' else 'TODAS AS DÉCADAS'}"
st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)

if not results:
    st.info("Nenhum resultado. Tente outros filtros ou termos.")
else:
    cols = st.columns(5)
    for i, item in enumerate(results):
        with cols[i % 5]:
            poster = item.get("poster")
            img_html = (
                f'<img src="{poster}" style="width:100%;aspect-ratio:2/3;object-fit:cover;display:block">'
                if poster else
                '<div style="width:100%;aspect-ratio:2/3;background:#1f1f2e;display:flex;align-items:center;justify-content:center;color:#2a2a3e;font-size:2rem">🎬</div>'
            )
            providers = tmdb_service.get_watch_providers(item["media_type"], item["id"])
            provider_html = ""
            if providers:
                provider_html = f'<p style="font-size:.68rem;color:#5a5a72;margin-top:4px">📺 {", ".join(providers[:2])}</p>'

            st.markdown(f"""
            <div class="card">
                {img_html}
                <div class="card-body">
                    <p class="card-title" title="{item['title']}">{item['title']}</p>
                    <div style="margin-bottom:4px">
                        <span class="badge">{item['type']}</span>
                        <span class="badge">{item.get('year','—')}</span>
                        <span class="rating">★ {item.get('rating',0)}</span>
                    </div>
                    {''.join(f'<span class="badge">{g}</span>' for g in item.get('genres',[])[:3])}
                    <p class="card-synopsis">{item.get('synopsis','')[:150]}</p>
                    {provider_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
