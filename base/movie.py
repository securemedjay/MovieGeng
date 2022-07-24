import requests


TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie"
TMDB_API_KEY = "60a893cf2f4ee27e8b6e3e813c727c6d"


class MovieDisplay:

    def __init__(self):
        self.title = ""
        self.title_id = ""

    def search_TMDB(self, title):
        self.title = title

        request_body = {
            "api_key": TMDB_API_KEY,
            "query": self.title,
        }
        response = requests.get(url=TMDB_SEARCH_URL, params=request_body)
        results = response.json()["results"]
        return results

    def details(self, title_id):
        self.title_id = title_id
        url = f"{TMDB_MOVIE_URL}/{self.title_id}"
        request_body = {
            "api_key": TMDB_API_KEY,
        }
        response = requests.get(url=url, params=request_body)
        result = response.json()
        return result
        # print(result)
        # title = result["title"]
        # year = result["release_date"].split("-")[0]
        # description = result["overview"]
        # img_url = f"https://image.tmdb.org/t/p/w500{result['poster_path']}"

        # return [title, year, description, img_url]
