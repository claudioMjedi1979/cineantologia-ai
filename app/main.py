import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.services import tmdb_service
from app.utils.config import get_tmdb_key, GLOBAL_CSS
from app.utils.sidebar import render_sidebar

st.set_page_config(
    page_title="CineAntologia AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:2rem 0 1.5rem 0">
    <p style="font-family:'Bebas Neue',sans-serif;font-size:clamp(2.8rem,7vw,5.5rem);
       line-height:.95;color:#e8e4dd;margin:0">
        CINE<span style="color:#e5383b">ANTOLOGIA</span><br>AI
    </p>
    <p style="font-family:'Inter',sans-serif;font-size:1rem;font-weight:300;
       color:#5a5a72;margin-top:.8rem;max-width:520px">
        Catálogo inteligente de filmes, séries, animes e doramas com IA — dos anos 80 até hoje.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Busca rápida ──────────────────────────────────────────────────────────────
col_s, col_btn = st.columns([5, 1])
with col_s:
    query = st.text_input("", placeholder="🔍  Buscar filme ou série...", label_visibility="collapsed", key="home_search")
with col_btn:
    st.write("")
    if st.button("Buscar", use_container_width=True):
        if query:
            st.session_state["search_query"] = query
            st.switch_page("pages/1_catalogo.py")

# ── Navegação rápida ──────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("🎞️  Catálogo", use_container_width=True):
        st.switch_page("pages/1_catalogo.py")
with c2:
    if st.button("💡  Recomendações", use_container_width=True):
        st.switch_page("pages/2_recomendacoes.py")
with c3:
    if st.button("📅  Linha do Tempo", use_container_width=True):
        st.switch_page("pages/3_linha_do_tempo.py")
with c4:
    if st.button("🤖  Chat IA", use_container_width=True):
        st.switch_page("pages/4_chat_ia.py")

# ── API Key warning ───────────────────────────────────────────────────────────
if not get_tmdb_key():
    st.error("**TMDB_API_KEY** não configurada. Adicione no `.env` local ou nos Secrets do Streamlit Cloud.", icon="🔑")
    st.code("TMDB_API_KEY=sua_chave_aqui", language="bash")
    st.stop()

# ── Trending ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">EM ALTA ESTA SEMANA</div>', unsafe_allow_html=True)

with st.spinner("Carregando destaques..."):
    trending = tmdb_service.get_trending("all")

if not trending:
    st.warning("Não foi possível carregar os destaques. Verifique a TMDB_API_KEY.")
    st.stop()

def render_card(item: dict, show_synopsis: bool = True):
    poster = item.get("poster")
    img_html = (
        f'<img src="{poster}" style="width:100%;aspect-ratio:2/3;object-fit:cover;display:block">'
        if poster else
        '<div style="width:100%;aspect-ratio:2/3;background:#1f1f2e;display:flex;align-items:center;justify-content:center;color:#2a2a3e;font-size:2rem">🎬</div>'
    )
    synopsis_html = f'<p class="card-synopsis">{item.get("synopsis","")[:140]}</p>' if show_synopsis else ""
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
            {''.join(f'<span class="badge">{g}</span>' for g in item.get('genres',[])[:2])}
            {synopsis_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

cols = st.columns(6)
for i, item in enumerate(trending[:12]):
    with cols[i % 6]:
        render_card(item, show_synopsis=(i < 6))

# ── Em Cartaz nos Cinemas ─────────────────────────────────────────────────────
st.markdown('<div class="section-label">EM CARTAZ NOS CINEMAS</div>', unsafe_allow_html=True)
with st.spinner("Carregando..."):
    now_playing = tmdb_service.get_movie_list("now_playing")
if now_playing:
    cols2 = st.columns(6)
    for i, item in enumerate(now_playing[:6]):
        with cols2[i]:
            render_card(item, show_synopsis=False)

# ── Séries em Exibição Hoje ───────────────────────────────────────────────────
st.markdown('<div class="section-label">SÉRIES EM EXIBIÇÃO HOJE</div>', unsafe_allow_html=True)
with st.spinner("Carregando..."):
    airing_today = tmdb_service.get_tv_list("airing_today")
if airing_today:
    cols3 = st.columns(6)
    for i, item in enumerate(airing_today[:6]):
        with cols3[i]:
            render_card(item, show_synopsis=False)

# ── Mais Bem Avaliados ────────────────────────────────────────────────────────
st.markdown('<div class="section-label">MAIS BEM AVALIADOS</div>', unsafe_allow_html=True)
with st.spinner("Carregando..."):
    top_rated = tmdb_service.get_movie_list("top_rated")
if top_rated:
    cols4 = st.columns(6)
    for i, item in enumerate(top_rated[:6]):
        with cols4[i]:
            render_card(item, show_synopsis=False)

st.markdown("""
<hr style="border-color:#1a1a26;margin-top:2.5rem">
<p style="text-align:center;color:#2a2a3e;font-size:.72rem;font-family:Inter,sans-serif">
CineAntologia AI · Dados via TMDb · Feito com Streamlit · Open Source
</p>""", unsafe_allow_html=True)
