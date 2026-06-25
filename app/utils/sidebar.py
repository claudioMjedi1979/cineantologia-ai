import streamlit as st
from app.utils.config import get_tmdb_key, AI_PROVIDERS


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <p style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
           letter-spacing:.06em;margin-bottom:0;color:#e8e4dd">
           🎬 CINEANTOLOGIA
        </p>
        <p style="font-family:'Bebas Neue',sans-serif;font-size:.85rem;
           letter-spacing:.15em;color:#e5383b;margin-top:0">AI</p>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<p style="font-size:.72rem;color:#5a5a72;font-family:Inter,sans-serif;letter-spacing:.08em">NAVEGAÇÃO</p>', unsafe_allow_html=True)

        pages = [
            ("🏠", "Home", "main"),
            ("🎞️", "Catálogo", "pages/1_catalogo"),
            ("💡", "Recomendações", "pages/2_recomendacoes"),
            ("📅", "Linha do Tempo", "pages/3_linha_do_tempo"),
            ("🤖", "Chat IA", "pages/4_chat_ia"),
        ]
        for icon, label, _ in pages:
            st.markdown(f'<p style="font-size:.85rem;font-family:Inter,sans-serif;color:#9a9590;margin:4px 0">{icon} {label}</p>', unsafe_allow_html=True)

        st.markdown("---")

        # ── Chat IA — seletor de provedor ──────────────────────────────────
        st.markdown('<p style="font-size:.72rem;color:#5a5a72;font-family:Inter,sans-serif;letter-spacing:.08em">CHAT IA · PROVEDOR</p>', unsafe_allow_html=True)

        provider_names = list(AI_PROVIDERS.keys())
        selected_provider = st.selectbox(
            "Provedor de IA",
            provider_names,
            index=provider_names.index(st.session_state.get("ai_provider", "OpenAI")),
            label_visibility="collapsed",
            key="provider_selector",
        )
        st.session_state["ai_provider"] = selected_provider

        cfg = AI_PROVIDERS[selected_provider]
        session_key = cfg["session_key"]
        has_key = bool(st.session_state.get(session_key))

        # Seletor de modelo
        model_list = cfg["models"]
        current_model_key = f"ai_model_{selected_provider}"
        default_model_idx = 0
        if st.session_state.get(current_model_key) in model_list:
            default_model_idx = model_list.index(st.session_state[current_model_key])

        selected_model = st.selectbox(
            "Modelo",
            model_list,
            index=default_model_idx,
            label_visibility="collapsed",
            key=f"model_sel_{selected_provider}",
        )
        st.session_state[current_model_key] = selected_model

        st.markdown("---")

        # ── Chave do provedor selecionado ──────────────────────────────────
        if has_key:
            st.success(f"✓ Chave {selected_provider} configurada", icon=None)
            if st.button("Remover chave", key=f"remove_{session_key}"):
                st.session_state[session_key] = ""
                st.rerun()
        else:
            st.markdown(f'<p style="font-size:.72rem;color:#5a5a72;font-family:Inter,sans-serif;letter-spacing:.08em">ATIVAR {selected_provider.upper()}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:.78rem;color:#9a9590;font-family:Inter,sans-serif">Cole sua chave {selected_provider}. Fica apenas na sessão.</p>', unsafe_allow_html=True)
            key_input = st.text_input(
                "Chave",
                type="password",
                placeholder=cfg["placeholder"],
                label_visibility="collapsed",
                key=f"key_input_{session_key}",
            )
            if st.button("Salvar chave", key=f"save_{session_key}"):
                if len(key_input) > 10:
                    st.session_state[session_key] = key_input.strip()
                    st.success("Chave salva!")
                    st.rerun()
                else:
                    st.error("Chave muito curta. Verifique e tente novamente.")

            st.markdown(
                f'<p style="font-size:.7rem;color:#3a3a52;font-family:Inter,sans-serif;margin-top:6px">'
                f'Obtenha em <a href="{cfg["docs_url"]}" target="_blank" style="color:#e5383b">{cfg["docs_url"].split("//")[1].split("/")[0]}</a></p>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        if not get_tmdb_key():
            st.warning("TMDB_API_KEY não configurada.", icon="⚠️")

        st.markdown('<p style="font-size:.68rem;color:#2a2a3e;font-family:Inter,sans-serif;text-align:center;margin-top:1rem">Dados: TMDb · Deploy: Streamlit Cloud</p>', unsafe_allow_html=True)
