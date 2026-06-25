import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services import ai_service
from app.utils.config import AI_PROVIDERS, GLOBAL_CSS
from app.utils.sidebar import render_sidebar

st.set_page_config(page_title="Chat IA · CineAntologia AI", page_icon="🤖", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# CSS extra para chat
st.markdown("""
<style>
.chat-user {
    background: #1f1f2e;
    border-radius: 12px 12px 2px 12px;
    padding: 12px 16px;
    margin: 6px 0 6px auto;
    font-family: Inter, sans-serif;
    font-size: .9rem;
    max-width: 78%;
    color: #e8e4dd;
    line-height: 1.5;
}
.chat-ai {
    background: #14141e;
    border: 1px solid #2a2a3e;
    border-radius: 2px 12px 12px 12px;
    padding: 14px 18px;
    margin: 6px 0;
    font-family: Inter, sans-serif;
    font-size: .9rem;
    max-width: 88%;
    color: #e8e4dd;
    line-height: 1.65;
    white-space: pre-wrap;
}
.chat-label-user { font-size:.7rem; color:#3a3a52; font-family:'Bebas Neue',sans-serif; letter-spacing:.1em; text-align:right; margin-bottom:2px; }
.chat-label-ai { font-size:.7rem; color:#e5383b; font-family:'Bebas Neue',sans-serif; letter-spacing:.1em; margin-bottom:2px; }
.key-gate {
    background: #14141e;
    border: 1px solid #2a2a3e;
    border-radius: 8px;
    padding: 2rem;
    max-width: 520px;
    margin: 2rem auto;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

render_sidebar()

st.markdown('<p style="font-family:\'Bebas Neue\',sans-serif;font-size:2.2rem;letter-spacing:.05em;margin-bottom:.2rem">CHAT <span style="color:#e5383b">IA</span></p>', unsafe_allow_html=True)
st.markdown('<p style="color:#5a5a72;font-family:Inter,sans-serif;font-size:.88rem;margin-bottom:1.2rem">Descreva o que você quer assistir e a IA faz a curadoria por você</p>', unsafe_allow_html=True)

# ── Provedor selecionado na sidebar ───────────────────────────────────────────
provider = st.session_state.get("ai_provider", "OpenAI")
cfg = AI_PROVIDERS.get(provider, AI_PROVIDERS["OpenAI"])
model_key = f"ai_model_{provider}"
model = st.session_state.get(model_key, cfg["default_model"])

if not ai_service.has_key(provider):
    docs_url = cfg["docs_url"]
    docs_domain = docs_url.split("//")[1].split("/")[0]
    st.markdown(f"""
    <div class="key-gate">
        <p style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#e8e4dd;margin:0 0 .5rem 0">🤖 ATIVE O CHAT IA</p>
        <p style="font-size:.88rem;color:#9a9590;font-family:Inter,sans-serif;line-height:1.6;margin-bottom:1.2rem">
            Para usar o Chat IA com <strong style="color:#e8e4dd">{provider}</strong>, cole sua chave na
            <strong style="color:#e8e4dd">sidebar esquerda</strong>.<br>
            A chave fica salva apenas na sua sessão e nunca é armazenada.
        </p>
        <p style="font-size:.78rem;color:#3a3a52;font-family:Inter,sans-serif">
            Obtenha sua chave em
            <a href="{docs_url}" target="_blank" style="color:#e5383b">{docs_domain}</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Exemplos (só quando conversa vazia) ──────────────────────────────────────
if not st.session_state.chat_history:
    st.markdown('<p style="font-size:.82rem;color:#5a5a72;font-family:Inter,sans-serif;margin-bottom:.5rem">Experimente um destes prompts:</p>', unsafe_allow_html=True)
    examples = [
        "Quero algo parecido com Stranger Things, com clima anos 80 e suspense.",
        "Filmes de ficção científica filosófica estilo Blade Runner ou Her.",
        "Séries de drama criminal pesado tipo The Wire ou Breaking Bad.",
        "Algo para assistir com a família nos anos 90, leve e divertido.",
        "Filmes de terror psicológico que me façam pensar depois.",
        "Séries japonesas com boa história e personagens complexos.",
    ]
    c1, c2 = st.columns(2)
    for i, ex in enumerate(examples):
        col = c1 if i % 2 == 0 else c2
        with col:
            btn_style = "background:#14141e;border:1px solid #2a2a3e;border-radius:6px;padding:8px 12px;font-size:.8rem;color:#9a9590;width:100%;text-align:left;cursor:pointer;font-family:Inter,sans-serif;margin-bottom:6px"
            if st.button(f'"{ex}"', key=f"ex_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": ex})
                with st.spinner("Consultando a IA..."):
                    resp = ai_service.chat(st.session_state.chat_history, provider, model)
                st.session_state.chat_history.append({"role": "assistant", "content": resp})
                st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

# ── Histórico ─────────────────────────────────────────────────────────────────
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<p class="chat-label-user">VOCÊ</p><div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="chat-label-ai">🎬 CINEANTOLOGIA AI</p><div class="chat-ai">{msg["content"]}</div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_inp, col_btn = st.columns([5, 1])
with col_inp:
    user_input = st.text_input(
        "",
        placeholder="Descreva o que você quer assistir...",
        key="chat_input",
        label_visibility="collapsed"
    )
with col_btn:
    st.write("")
    send = st.button("Enviar", use_container_width=True, key="send_btn")

if send and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
    with st.spinner("Pensando..."):
        resp = ai_service.chat(st.session_state.chat_history, provider, model)
    st.session_state.chat_history.append({"role": "assistant", "content": resp})
    st.rerun()

# ── Ações ─────────────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    if st.button("🗑️  Limpar conversa", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()
