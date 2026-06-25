import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services import recommendation_service, tmdb_service
from app.utils.config import DECADES, GENRES_MAP, DORAMA_LANGUAGES, GLOBAL_CSS
from app.utils.sidebar import render_sidebar

st.set_page_config(page_title="Recomendações · CineAntologia AI", page_icon="💡", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown('<p style="font-family:\'Bebas Neue\',sans-serif;font-size:2.2rem;letter-spacing:.05em;margin-bottom:.3rem">RECOMENDAÇÕES</p>', unsafe_allow_html=True)
st.markdown('<p style="color:#5a5a72;font-family:Inter,sans-serif;font-size:.88rem;margin-bottom:1.2rem">Descubra por gênero, década ou similaridade com um título</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎭  Por Gênero", "📅  Por Década", "🎌  Anime", "🌸  Dorama", "🔗  Similares a...",
])

def render_grid(items, ncols=6):
    if not items:
        st.info("Sem resultados para esta seleção.")
        return
    cols = st.columns(ncols)
    for i, item in enumerate(items[:ncols*2]):
        with cols[i % ncols]:
            poster = item.get("poster")
            img_html = (
                f'<img src="{poster}" style="width:100%;aspect-ratio:2/3;object-fit:cover;display:block">'
                if poster else
                '<div style="width:100%;aspect-ratio:2/3;background:#1f1f2e;display:flex;align-items:center;justify-content:center;color:#2a2a3e;font-size:1.8rem">🎬</div>'
            )
            st.markdown(f"""
            <div class="card">{img_html}
            <div class="card-body">
                <p class="card-title" title="{item['title']}">{item['title']}</p>
                <span class="badge">{item.get('year','—')}</span>
                <span class="badge">{item['type']}</span>
                <span class="rating"> ★{item.get('rating',0)}</span>
            </div></div>""", unsafe_allow_html=True)

# ── Tab 1: Por Gênero ─────────────────────────────────────────────────────────
with tab1:
    g1, g2 = st.columns([2, 1])
    with g1:
        selected_genre = st.selectbox("Gênero", sorted(GENRES_MAP.values()), key="genre_sel")
    with g2:
        media_g = st.selectbox("Tipo", ["Filme", "Série"], key="genre_type")
    genre_id = next(k for k, v in GENRES_MAP.items() if v == selected_genre)
    mt = "movie" if media_g == "Filme" else "tv"
    with st.spinner("Buscando..."):
        items1 = recommendation_service.by_genre(genre_id, mt)
    st.markdown(f'<div class="section-label">{selected_genre.upper()} · {media_g.upper()}S</div>', unsafe_allow_html=True)
    render_grid(items1)

# ── Tab 2: Por Década ─────────────────────────────────────────────────────────
with tab2:
    d1, d2 = st.columns([2, 1])
    with d1:
        selected_decade = st.selectbox("Década", list(DECADES.keys()), key="dec_sel")
    with d2:
        media_d = st.selectbox("Tipo", ["Tudo", "Filme", "Série"], key="dec_type")
    mt2 = {"Tudo": "all", "Filme": "movie", "Série": "tv"}[media_d]
    with st.spinner("Buscando..."):
        items2 = recommendation_service.by_decade(DECADES[selected_decade], mt2)
    st.markdown(f'<div class="section-label">{selected_decade.upper()}</div>', unsafe_allow_html=True)
    render_grid(items2)

# ── Tab 3: Anime ─────────────────────────────────────────────────────────────
with tab3:
    a1, a2 = st.columns([2, 1])
    with a1:
        selected_decade_a = st.selectbox("Década", ["Todas"] + list(DECADES.keys()), key="anime_dec")
    with a2:
        st.write("")
    decade_range_a = DECADES.get(selected_decade_a, (1980, 2029)) if selected_decade_a != "Todas" else (1980, 2029)
    with st.spinner("Buscando animes..."):
        items_anime = recommendation_service.by_anime(decade_range_a)
    st.markdown('<div class="section-label">ANIME · MAIS POPULARES</div>', unsafe_allow_html=True)
    render_grid(items_anime)

# ── Tab 4: Dorama ─────────────────────────────────────────────────────────────
with tab4:
    dr1, dr2, dr3 = st.columns([2, 1.5, 1])
    with dr1:
        selected_decade_d = st.selectbox("Década", ["Todas"] + list(DECADES.keys()), key="dorama_dec")
    with dr2:
        dorama_origin = st.selectbox("Origem", list(DORAMA_LANGUAGES.keys()), key="dorama_lang")
    with dr3:
        st.write("")
    decade_range_d = DECADES.get(selected_decade_d, (1980, 2029)) if selected_decade_d != "Todas" else (1980, 2029)
    lang_code = DORAMA_LANGUAGES[dorama_origin]
    with st.spinner("Buscando doramas..."):
        items_dorama = recommendation_service.by_dorama(lang_code, decade_range_d)
    st.markdown(f'<div class="section-label">{dorama_origin.upper()} · MAIS POPULARES</div>', unsafe_allow_html=True)
    render_grid(items_dorama)

# ── Tab 5: Similares ──────────────────────────────────────────────────────────
with tab5:
    st.markdown('<p style="font-size:.85rem;color:#9a9590;font-family:Inter,sans-serif">Digite um filme ou série como referência e encontre títulos parecidos</p>', unsafe_allow_html=True)
    sq = st.text_input("", placeholder="Ex: Stranger Things, Blade Runner, Dark...", key="sim_query", label_visibility="collapsed")

    if sq:
        with st.spinner("Buscando referência..."):
            ref = tmdb_service.search_multi(sq)
        if ref:
            chosen = ref[0]
            st.markdown(f"""
            <div style="background:#14141e;border:1px solid #e5383b;border-radius:6px;padding:10px 14px;margin-bottom:1rem;display:inline-block">
                <span style="font-size:.72rem;color:#e5383b;font-family:'Bebas Neue',sans-serif;letter-spacing:.08em">REFERÊNCIA SELECIONADA</span><br>
                <span style="font-family:Inter,sans-serif;font-weight:600;color:#e8e4dd">{chosen['title']}</span>
                <span style="font-size:.78rem;color:#5a5a72"> · {chosen.get('year','—')} · {chosen['type']}</span>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("Buscando similares..."):
                similar = recommendation_service.similar_to(chosen["media_type"], chosen["id"])

            if similar:
                st.markdown('<div class="section-label">VOCÊ TAMBÉM VAI GOSTAR</div>', unsafe_allow_html=True)
                render_grid(similar)
            else:
                st.info("Sem similares encontrados para este título no TMDb.")
        else:
            st.warning("Título não encontrado. Tente outro nome.")
