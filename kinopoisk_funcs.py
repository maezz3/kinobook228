# pip install kinopoisk-api-unofficial-client
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.film_top_request import FilmTopRequest
from kinopoisk_unofficial.model.dictonary.top_type import TopType
from secret import kinopoisk_auth


def search(keywords: str):
    api = KinopoiskApiClient(kinopoisk_auth)
    request = SearchByKeywordRequest(keywords)
    for i in api.films.send_search_by_keyword_request(request).films:
        yield get_film(i.film_id)


def get_film(film_id: int):
    api = KinopoiskApiClient(kinopoisk_auth)
    request = FilmRequest(film_id)
    return api.films.send_film_request(request).film


def get_top_100_popular():
    api = KinopoiskApiClient(kinopoisk_auth)
    request = FilmTopRequest(TopType.TOP_100_POPULAR_FILMS)
    for i in api.films.send_film_top_request(request).films:
        yield get_film(i.film_id)


def get_top_250_best():
    api = KinopoiskApiClient(kinopoisk_auth)
    request = FilmTopRequest(TopType.TOP_250_BEST_FILMS)
    for i in api.films.send_film_top_request(request).films:
        yield get_film(i.film_id)


def get_top_await():
    api = KinopoiskApiClient(kinopoisk_auth)
    request = FilmTopRequest(TopType.TOP_AWAIT_FILMS)
    for i in api.films.send_film_top_request(request).films:
        yield get_film(i.film_id)
