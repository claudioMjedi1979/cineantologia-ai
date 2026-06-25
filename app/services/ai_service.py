from app.utils.config import (
    get_openai_key, get_anthropic_key, get_gemini_key, get_groq_key, AI_PROVIDERS,
)

SYSTEM_PROMPT = """Você é o CineAntologia AI, curador especialista em filmes, séries, animes e doramas de todas as décadas.

Quando o usuário pedir recomendações, identifique: gênero, clima, época, referências e tom emocional.
Responda de forma envolvente, com contexto cultural, mencionando apenas títulos reais que existem.

Regras:
- Responda sempre em português brasileiro
- Máximo 3 parágrafos de contexto
- Finalize sempre com uma lista de sugestões neste formato exato:

🎬 Título (Ano) — motivo em uma linha

- Mínimo 4 e máximo 6 sugestões por resposta
- Varie entre filmes e séries quando fizer sentido
- Se o usuário pedir algo muito específico, seja preciso; se for vago, explore a atmosfera pedida"""


def _no_key_msg(provider_name: str, docs_url: str) -> str:
    return (
        f"⚠️ **Chave {provider_name} não configurada.**\n\n"
        f"Cole sua chave na **sidebar esquerda** — campo *Ativar Chat IA*.\n\n"
        f"Obtenha em: {docs_url}"
    )


def _handle_error(e: Exception, provider_name: str) -> str:
    err = str(e).lower()
    if "invalid_api_key" in err or "invalid api key" in err or "authentication" in err or "401" in err:
        return f"❌ **Chave {provider_name} inválida.** Verifique a chave na sidebar e tente novamente."
    if "quota" in err or "rate_limit" in err or "429" in err:
        return f"❌ **Limite de uso {provider_name} atingido.** Aguarde ou verifique seu plano."
    return f"❌ Erro ao conectar com {provider_name}: {str(e)}"


def _chat_openai(messages: list[dict], model: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        return "❌ Pacote `openai` não instalado. Rode: `pip install openai`"
    key = get_openai_key()
    if not key:
        return _no_key_msg("OpenAI", "platform.openai.com/api-keys")
    try:
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            max_tokens=800,
            temperature=0.85,
        )
        return response.choices[0].message.content
    except Exception as e:
        return _handle_error(e, "OpenAI")


def _chat_claude(messages: list[dict], model: str) -> str:
    try:
        import anthropic
    except ImportError:
        return "❌ Pacote `anthropic` não instalado. Rode: `pip install anthropic`"
    key = get_anthropic_key()
    if not key:
        return _no_key_msg("Anthropic (Claude)", "console.anthropic.com")
    try:
        client = anthropic.Anthropic(api_key=key)
        response = client.messages.create(
            model=model,
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        return _handle_error(e, "Claude")


def _chat_gemini(messages: list[dict], model: str) -> str:
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        return "❌ Pacote `google-genai` não instalado. Rode: `pip install google-genai`"
    key = get_gemini_key()
    if not key:
        return _no_key_msg("Google (Gemini)", "aistudio.google.com/app/apikey")
    try:
        client = genai.Client(api_key=key)
        # Converte formato OpenAI → formato Gemini
        history = [
            genai_types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[genai_types.Part(text=m["content"])],
            )
            for m in messages[:-1]
        ]
        response = client.models.generate_content(
            model=model,
            contents=history + [genai_types.Content(
                role="user",
                parts=[genai_types.Part(text=messages[-1]["content"])],
            )],
            config=genai_types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=800,
                temperature=0.85,
            ),
        )
        return response.text
    except Exception as e:
        return _handle_error(e, "Gemini")


def _chat_groq(messages: list[dict], model: str) -> str:
    try:
        from groq import Groq
    except ImportError:
        return "❌ Pacote `groq` não instalado. Rode: `pip install groq`"
    key = get_groq_key()
    if not key:
        return _no_key_msg("Groq", "console.groq.com/keys")
    try:
        client = Groq(api_key=key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            max_tokens=800,
            temperature=0.85,
        )
        return response.choices[0].message.content
    except Exception as e:
        return _handle_error(e, "Groq")


def chat(messages: list[dict], provider: str = "OpenAI", model: str = None) -> str:
    m = model or AI_PROVIDERS.get(provider, {}).get("default_model", "")
    if provider == "OpenAI":
        return _chat_openai(messages, m or "gpt-4o-mini")
    if provider == "Claude (Anthropic)":
        return _chat_claude(messages, m or "claude-haiku-4-5-20251001")
    if provider == "Gemini (Google)":
        return _chat_gemini(messages, m or "gemini-1.5-flash")
    if provider == "Groq (gratuito)":
        return _chat_groq(messages, m or "llama-3.1-8b-instant")
    return "❌ Provedor de IA não reconhecido."


def has_key(provider: str) -> bool:
    """Retorna True se há chave configurada para o provedor."""
    getters = {
        "OpenAI": get_openai_key,
        "Claude (Anthropic)": get_anthropic_key,
        "Gemini (Google)": get_gemini_key,
        "Groq (gratuito)": get_groq_key,
    }
    getter = getters.get(provider)
    return bool(getter()) if getter else False
