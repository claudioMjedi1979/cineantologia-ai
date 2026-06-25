from app.services import tmdb_service


def by_genre(genre_id: int, media_type: str = "movie") -> list[dict]:
    return tmdb_service.discover(media_type=media_type, genre_id=genre_id)[:12]


def by_decade(decade_range: tuple, media_type: str = "all") -> list[dict]:
    start, end = decade_range
    if media_type == "all":
        movies = tmdb_service.discover("movie", start, end)[:6]
        series = tmdb_service.discover("tv", start, end)[:6]
        return movies + series
    return tmdb_service.discover(media_type, start, end)[:12]


def by_anime(decade_range: tuple = (1980, 2029)) -> list[dict]:
    start, end = decade_range
    return tmdb_service.discover_anime(start, end)[:12]


def by_dorama(language: str = "ko", decade_range: tuple = (1980, 2029)) -> list[dict]:
    start, end = decade_range
    return tmdb_service.discover_dorama(language, start, end)[:12]


def similar_to(media_type: str, tmdb_id: int) -> list[dict]:
    return tmdb_service.get_similar(media_type, tmdb_id)
