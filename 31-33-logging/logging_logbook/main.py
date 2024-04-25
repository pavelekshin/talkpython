import functools
import time
import logbook
from collections import namedtuple
import api


URL = "http://www.omdbapi.com/"
APIKEY = "4ef2f6df"


def main():
    app_log = logbook.Logger(__name__)
    Record = namedtuple("Record", ("Title", "Year", "imdbID", "Type", "Poster"))
    movies = []

    keyword = input("Keyword of title search: ")
    year = input("Optional enter movie year: ")

    app_log.info("Make movies search by {}".format(keyword))

    ms = api.MovieSearch(URL, APIKEY)

    if not keyword:
        app_log.warn("No keyword supplied")
        raise ValueError("Must specify a search term (keyword).")

    app_log.trace("Starting search for {}".format(keyword))

    t0 = time.time()

    resp = ms.search_movie(s=keyword, y=year)

    t1 = time.time()

    app_log.trace(
        "Finished search for {}, {} results in {} ms.".format(
            keyword, resp.get("totalResults"), int(1000 * (t1 - t0))
        )
    )

    for row in resp["Search"]:
        movies.append(Record(**row))

    print("\nSearch result: ")
    print(f"{'id':<4} {'movie':50} {'type':6} {'year:'}")
    print(f"_" * 70)
    for cnt, movie in enumerate(movies, start=1):
        print(f"{cnt:<4} {movie.Title:50} {movie.Type:<6} {movie.Year:8}")
        app_log.info(f"{cnt:<4} {movie.Title:50} {movie.Type:<6} {movie.Year:8}")

    movieid = input("\nSelect one of movie: ")

    if not movieid:
        app_log.warn("No imdbID is provided")
        raise ValueError("Must specify a search term (imdbID).")

    imdbid = movies[int(movieid) - 1].imdbID

    app_log.info("Make movie search by imdbId".format(imdbid))
    app_log.trace("Starting search for {}".format(imdbid))

    t0 = time.time()

    resp = ms.search_movie_id(imdbid)

    t1 = time.time()

    app_log.trace(
        "Finished search for {}, {} results in {} ms.".format(
            imdbid, len(resp.get("Ratings")), int(1000 * (t1 - t0))
        )
    )
    print(f"""For {resp["Title"]} {resp["Year"]} ratings is:""")

    for item in resp["Ratings"]:
        print(
            """For source "{}", movie ratings is "{}" """.format(
                item["Source"], item["Value"]
            )
        )
        app_log.info(
            """For source "{}", movie ratings is "{}" """.format(
                item["Source"], item["Value"]
            )
        )


def init_logging(filename: str = None):
    level = logbook.TRACE

    if filename:
        logbook.TimedRotatingFileHandler(filename, level=level).push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=level).push_application()

    msg = "Logging initialized, level: {}, mode: {}".format(
        level, "stdout mode" if not filename else "file mode: " + filename
    )
    logger = logbook.Logger("Startup")
    logger.notice(msg)


if __name__ == "__main__":
    init_logging("movie_log.log")
    main()
