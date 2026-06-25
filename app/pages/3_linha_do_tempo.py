import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services import tmdb_service
from app.utils.config import DECADES, GLOBAL_CSS
from app.utils.sidebar import render_sidebar

st.set_page_config(page_title="Linha do Tempo · CineAntologia AI", page_icon="📅", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

DECADE_CONTEXT = {
    "Anos 80": {
        "tema": "A Era do Blockbuster",
        "texto": "Os anos 80 consolidaram o blockbuster como formato dominante. Spielberg e Lucas reinventaram o entretenimento popular. O VHS transformou o consumo doméstico. Surgiu o horror teen, a ficção científica pop e os filmes de ação de alta adrenalina.",
        "marcos": [
            "Star Wars e o nascimento do universo expandido",
            "MTV e a revolução do videoclipe",
            "VHS e o mercado de locadoras",
            "O slasher e o cinema de terror teen",
        ],
    },
    "Anos 90": {
        "tema": "O Cinema Independente Explode",
        "texto": "Tarantino, os Irmãos Coen e o movimento indie transformaram Hollywood. O thriller psicológico e o drama realista dominaram as premiações. As séries começaram a ganhar atenção crítica séria com Twin Peaks e NYPD Blue.",
        "marcos": [
            "Sundance e o renascimento do cinema indie",
            "A ascensão do DVD e a morte do VHS",
            "CGI e os primeiros grandes efeitos digitais (Jurassic Park)",
            "Seinfeld e o sitcom como forma de arte",
        ],
    },
    "Anos 2000": {
        "tema": "Franquias e a Era Digital",
        "texto": "O cinema de franquia tomou conta das bilheterias. O Senhor dos Anéis, X-Men e Matrix definiram uma geração. Ao mesmo tempo, HBO criou o conceito de TV premium com Sopranos e The Wire.",
        "marcos": [
            "DVD no auge — o mercado mais lucrativo da história",
            "The Sopranos e a TV como literatura",
            "Rotten Tomatoes e a crítica colaborativa",
            "YouTube e o fim do monopólio televisivo",
        ],
    },
    "Anos 2010": {
        "tema": "O Streaming Muda Tudo",
        "texto": "Netflix, HBO Max e Amazon Prime reinventaram a distribuição de conteúdo. O MCU se tornou o maior fenômeno da história do cinema. A TV tornou-se o medium mais ambicioso narrativamente com Game of Thrones e Breaking Bad.",
        "marcos": [
            "Breaking Bad e o peak TV definitivo",
            "MCU e o cinema compartilhado como negócio",
            "Streaming substituindo o broadcast",
            "Binge-watching como comportamento cultural",
        ],
    },
    "Anos 2020": {
        "tema": "Pandemia, IA e Conteúdo Global",
        "texto": "A pandemia acelerou o streaming e desafiou os cinemas. Conteúdos internacionais como Squid Game globalizaram audiências. A IA começa a entrar na produção audiovisual como ferramenta criativa.",
        "marcos": [
            "Squid Game e a virada do conteúdo asiático",
            "Oscar para filmes internacionais (Parasita, CODA)",
            "Guerras do streaming: Disney+, HBO Max, Apple TV+",
            "IA generativa na criação audiovisual",
        ],
    },
}

st.markdown('<p style="font-family:\'Bebas Neue\',sans-serif;font-size:2.2rem;letter-spacing:.05em;margin-bottom:.3rem">LINHA DO TEMPO CULTURAL</p>', unsafe_allow_html=True)
st.markdown('<p style="color:#5a5a72;font-family:Inter,sans-serif;font-size:.88rem;margin-bottom:2rem">Décadas de cinema e TV com contexto cultural e os títulos mais marcantes</p>', unsafe_allow_html=True)

for decade_name, (year_start, year_end) in DECADES.items():
    ctx = DECADE_CONTEXT.get(decade_name, {})

    # Cabeçalho da década
    st.markdown(f"""
    <div style="display:flex;align-items:baseline;gap:1rem;margin-bottom:.8rem">
        <span style="font-family:'Bebas Neue',sans-serif;font-size:4.5rem;line-height:1;color:#1f1f2e">{year_start}<span style="color:#e5383b">s</span></span>
        <span style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;color:#5a5a72;letter-spacing:.1em">{ctx.get('tema','').upper()}</span>
    </div>
    """, unsafe_allow_html=True)

    info_col, films_col = st.columns([1, 2.8])

    with info_col:
        st.markdown(f"""
        <div style="background:#14141e;border:1px solid #1f1f2e;border-radius:6px;padding:1rem 1.2rem;margin-bottom:.8rem">
            <p style="font-size:.82rem;color:#9a9590;font-family:Inter,sans-serif;line-height:1.55;margin:0">{ctx.get('texto','')}</p>
        </div>
        <div style="background:#14141e;border:1px solid #1f1f2e;border-radius:6px;padding:1rem 1.2rem">
            <p style="font-family:'Bebas Neue',sans-serif;font-size:1rem;color:#e5383b;margin:0 0 .5rem 0;letter-spacing:.06em">MARCOS</p>
            {''.join(f'<p style="font-size:.78rem;color:#9a9590;font-family:Inter,sans-serif;margin:4px 0">· {m}</p>' for m in ctx.get('marcos', []))}
        </div>
        """, unsafe_allow_html=True)

    with films_col:
        with st.spinner(f"Carregando {decade_name}..."):
            movies = tmdb_service.discover("movie", year_start, year_end)[:3]
            series = tmdb_service.discover("tv", year_start, year_end)[:3]
            items = movies + series

        cols = st.columns(6)
        for i, item in enumerate(items[:6]):
            with cols[i]:
                poster = item.get("poster")
                img_html = (
                    f'<img src="{poster}" style="width:100%;aspect-ratio:2/3;object-fit:cover;display:block">'
                    if poster else
                    '<div style="width:100%;aspect-ratio:2/3;background:#1f1f2e;display:flex;align-items:center;justify-content:center;color:#2a2a3e;font-size:1.5rem">🎬</div>'
                )
                label = "FILME" if item["type"] == "Filme" else "SÉRIE"
                label_color = "#4a9eff" if item["type"] == "Série" else "#9a9590"
                st.markdown(f"""
                <div class="card">{img_html}
                <div class="card-body">
                    <p style="font-size:.68rem;color:{label_color};font-family:'Bebas Neue',sans-serif;letter-spacing:.08em;margin:0 0 2px 0">{label}</p>
                    <p class="card-title" style="font-size:.8rem">{item['title']}</p>
                    <span class="badge">{item.get('year','—')}</span>
                    <span class="rating"> ★{item.get('rating',0)}</span>
                </div></div>""", unsafe_allow_html=True)

    st.markdown('<hr style="border-color:#1a1a26;margin:2rem 0">', unsafe_allow_html=True)
