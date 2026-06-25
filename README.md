<div align="center">

# 🎬 CineAntologia AI

**Catálogo inteligente de filmes e séries com IA, busca semântica,  
recomendações personalizadas e linha do tempo cultural dos anos 80 até hoje.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![TMDb](https://img.shields.io/badge/TMDb-API-01B4E4?style=flat-square)](https://www.themoviedb.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[🚀 Demo ao Vivo](#deploy) · [📦 Instalação](#instalação-local) · [🗺️ Roadmap](#roadmap)

</div>

---

## ✨ O que é

O **CineAntologia AI** é uma aplicação pública para explorar e descobrir filmes e séries de todas as décadas, com curadoria cultural, recomendações inteligentes e chat com IA.

O **Chat IA** usa o GPT-4o-mini como curador cinematográfico: você descreve o que quer ("algo com clima anos 80 e suspense") e recebe sugestões com contexto cultural. Cada usuário usa sua própria chave OpenAI — a chave fica apenas na sessão, nunca é armazenada.

---

## 🖼️ Funcionalidades

| Página | Descrição |
|--------|-----------|
| 🏠 **Home** | Destaques da semana via TMDb Trending |
| 🎞️ **Catálogo** | Busca por título + filtros por década, gênero, tipo e onde assistir |
| 💡 **Recomendações** | Por gênero, por década e por similaridade com um título |
| 📅 **Linha do Tempo** | Contexto cultural de cada década com filmes e séries marcantes |
| 🤖 **Chat IA** | Curadoria personalizada via GPT-4o-mini com chave do próprio usuário |

---

## 🏗️ Estrutura

```
cineantologia-ai/
│
├── app/
│   ├── main.py                       # Página inicial
│   ├── pages/
│   │   ├── 1_catalogo.py             # Catálogo e busca
│   │   ├── 2_recomendacoes.py        # Recomendações
│   │   ├── 3_linha_do_tempo.py       # Timeline cultural
│   │   └── 4_chat_ia.py              # Chat com IA
│   │
│   ├── services/
│   │   ├── tmdb_service.py           # Integração TMDb API
│   │   ├── recommendation_service.py # Lógica de recomendações
│   │   └── ai_service.py             # Integração OpenAI
│   │
│   └── utils/
│       ├── config.py                 # Configurações, CSS global e constantes
│       └── sidebar.py                # Sidebar compartilhada
│
├── .streamlit/
│   └── config.toml                   # Tema dark customizado
│
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## 📦 Instalação Local

### Pré-requisitos
- Python 3.11+
- Chave TMDb gratuita: [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

```bash
# 1. Clone
git clone https://github.com/seu-usuario/cineantologia-ai.git
cd cineantologia-ai

# 2. Ambiente virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Dependências
pip install -r requirements.txt

# 4. Variáveis de ambiente
cp .env.example .env
# Edite o .env e coloque sua TMDB_API_KEY

# 5. Rode
streamlit run app/main.py
```

---

## ☁️ Deploy

### Streamlit Community Cloud (gratuito — recomendado)

1. Faça fork deste repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte o repo
3. **Main file path:** `app/main.py`
4. Em **Secrets**, adicione:

```toml
TMDB_API_KEY = "sua_chave_aqui"

# Opcional: se quiser bancar o Chat IA para todos os usuários
# OPENAI_API_KEY = "sua_chave_aqui"
```

### Docker

```bash
docker build -t cineantologia-ai .
docker run -p 8501:8501 -e TMDB_API_KEY=sua_chave cineantologia-ai
```

---

## 🤖 Sobre o Chat IA

O Chat IA usa **GPT-4o-mini** com um system prompt especializado em curadoria cinematográfica.

**Para o usuário público:** ele cola a própria chave OpenAI na sidebar (fica só na sessão, nunca armazenada no servidor). Quem não tem chave usa normalmente as outras 4 páginas.

**Para o dono do app:** se quiser que todos usem sem chave, coloque `OPENAI_API_KEY` nos Secrets do Streamlit Cloud — a chave do servidor tem prioridade.

---

## 🗺️ Roadmap

### ✅ v1 — MVP Público (atual)
- [x] TMDb API — busca, catálogo, trending, similares, watch providers
- [x] Catálogo com filtros por título, década, gênero e tipo
- [x] Recomendações por gênero, década e similaridade
- [x] Linha do tempo cultural por década
- [x] Chat IA com GPT-4o-mini (chave do usuário)
- [x] Deploy Streamlit Cloud

### 🔜 v2 — Busca Semântica
- [ ] Embeddings com `text-embedding-3-small`
- [ ] Busca por "clima" e vibe do filme
- [ ] SQLite local com vetores

### 🔮 v3 — Arquitetura Avançada
- [ ] PostgreSQL + pgvector
- [ ] Pipeline Bronze/Silver/Gold
- [ ] Agentes especialistas por gênero/década
- [ ] RAG com sinopses e críticas

---

## 🛠️ Tech Stack

- **App:** [Streamlit](https://streamlit.io)
- **Dados:** [TMDb API](https://www.themoviedb.org/documentation/api) (gratuita)
- **IA:** [OpenAI GPT-4o-mini](https://openai.com)
- **Linguagem:** Python 3.11+

---

<div align="center">
  <sub>Dados fornecidos por <a href="https://www.themoviedb.org">The Movie Database (TMDb)</a> · Feito com ❤️ e Streamlit</sub>
</div>
