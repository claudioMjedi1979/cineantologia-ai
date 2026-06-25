import requests
import streamlit as st
from app.utils.config import get_tmdb_key, TMDB_BASE_URL, TMDB_IMAGE_BASE, GENRES_MAP


def _get(endpoint: str, params: dict = {}) -> dict:
    key = get_tmdb_key()
    if not key:
        return {}
    p = dict(params)
    p["api_key"] = key
    p["language"] = "pt-BR"
    try:
        r = requests.get(f"{TMDB_BASE_URL}{endpoint}", params=p, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}


def search_multi(query: str, page: int = 1) -> list[dict]:
    data = _get("/search/multi", {"query": query, "page": page, "include_adult": False})
    return _normalize(data.get("results", []))


def discover(media_type: str = "movie", year_start: int = 1980, year_end: int = 2029,
             genre_id: int = None, page: int = 1) -> list[dict]:
    params = {
        "page": page,
        "sort_by": "popularity.desc",
        "vote_count.gte": 50,
    }
    if media_type == "movie":
        params["primary_release_date.gte"] = f"{year_start}-01-01"
        params["primary_release_date.lte"] = f"{year_end}-12-31"
        if genre_id:
            params["with_genres"] = genre_id
        data = _get("/discover/movie", params)
    else:
        params["first_air_date.gte"] = f"{year_start}-01-01"
        params["first_air_date.lte"] = f"{year_end}-12-31"
        if genre_id:
            params["with_genres"] = genre_id
        data = _get("/discover/tv", params)
    results = data.get("results", [])
    for r in results:
        r["media_type"] = media_type
    return _normalize(results)


def get_similar(media_type: str, tmdb_id: int) -> list[dict]:
    data = _get(f"/{media_type}/{tmdb_id}/similar")
    results = data.get("results", [])
    for r in results:
        r["media_type"] = media_type
    return _normalize(results)[:8]


def get_movie_list(list_type: str = "popular", page: int = 1) -> list[dict]:
    """list_type: popular | now_playing | upcoming | top_rated"""
    data = _get(f"/movie/{list_type}", {"page": page})
    results = data.get("results", [])
    for r in results:
        r["media_type"] = "movie"
    return _normalize(results)


def get_tv_list(list_type: str = "popular", page: int = 1) -> list[dict]:
    """list_type: popular | airing_today | on_the_air | top_rated"""
    data = _get(f"/tv/{list_type}", {"page": page})
    results = data.get("results", [])
    for r in results:
        r["media_type"] = "tv"
    return _normalize(results)


def discover_anime(year_start: int = 1980, year_end: int = 2029, page: int = 1) -> list[dict]:
    params = {
        "page": page,
        "sort_by": "popularity.desc",
        "vote_count.gte": 50,
        "with_original_language": "ja",
        "with_genres": 16,
        "first_air_date.gte": f"{year_start}-01-01",
        "first_air_date.lte": f"{year_end}-12-31",
    }
    data = _get("/discover/tv", params)
    results = data.get("results", [])
    for r in results:
        r["media_type"] = "tv"
    return _normalize(results, content_type="Anime")


def discover_dorama(language: str = "ko", year_start: int = 1980, year_end: int = 2029, page: int = 1) -> list[dict]:
    params = {
        "page": page,
        "sort_by": "popularity.desc",
        "vote_count.gte": 20,
        "with_original_language": language,
        "first_air_date.gte": f"{year_start}-01-01",
        "first_air_date.lte": f"{year_end}-12-31",
    }
    if language == "ja":
        params["without_genres"] = 16  # excluir animação dos J-dramas
    data = _get("/discover/tv", params)
    results = data.get("results", [])
    for r in results:
        r["media_type"] = "tv"
    label_map = {"ko": "Dorama", "ja": "J-Drama", "zh": "C-Drama", "th": "Thai Drama"}
    return _normalize(results, content_type=label_map.get(language, "Dorama"))


def get_trending(media_type: str = "all") -> list[dict]:
    data = _get(f"/trending/{media_type}/week")
    return _normalize(data.get("results", []))


def get_watch_providers(media_type: str, tmdb_id: int) -> list[str]:
    data = _get(f"/{media_type}/{tmdb_id}/watch/providers")
    results = data.get("results", {}).get("BR", {})
    return [p.get("provider_name", "") for p in results.get("flatrate", [])]


def poster_url(path: str | None) -> str | None:
    if not path:
        return None
    return f"{TMDB_IMAGE_BASE}{path}"


def _normalize(items: list, content_type: str = None) -> list[dict]:
    out = []
    for item in items:
        mt = item.get("media_type", "movie")
        if mt == "person":
            continue
        title = item.get("title") or item.get("name") or "Sem título"
        date = item.get("release_date") or item.get("first_air_date") or ""
        year = int(date[:4]) if date and len(date) >= 4 else None
        genre_ids = item.get("genre_ids", [])
        genres = [GENRES_MAP.get(g, "") for g in genre_ids if g in GENRES_MAP]
        out.append({
            "id": item.get("id"),
            "title": title,
            "year": year,
            "type": content_type or ("Filme" if mt == "movie" else "Série"),
            "media_type": mt if mt in ("movie", "tv") else "movie",
            "genres": [g for g in genres if g],
            "synopsis": item.get("overview", "Sinopse não disponível."),
            "poster": poster_url(item.get("poster_path")),
            "rating": round(item.get("vote_average", 0), 1),
        })
    return out
