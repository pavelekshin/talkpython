import requests
import json
import time
import logbook
import sys
from collections import namedtuple

URL = "http://www.omdbapi.com/"
APIKEY = "4ef2f6df"


def search_movies_api(url, payload, searchtype):
    api_log = logbook.Logger("API")

    t0 = time.time()

    keyword = payload.get("s")
    imdbid = payload.get("i")
    year = payload.get("year")

    if searchtype == "s" and not keyword:
        api_log.warn("No keyword supplied")
        raise ValueError("Must specify a search term (keyword).")

    if searchtype == "i" and not imdbid:
        api_log.warn("No imdbID is provided")
        raise ValueError("Must specify a search term (imdbID).")

    if searchtype == "s":
        api_log.trace("Starting search for {}".format(keyword))
    if searchtype == "i":
        api_log.trace("Starting search for {}".format(imdbid))

    resp = requests.get(URL, params=payload)

    api_log.trace(
        "Request to {}. with params {} and headers {}.".format(
            resp.request.url, payload, resp.request.headers
        )
    )

    api_log.trace(
        "Request finished, status code {}. Reponse headers {}.".format(
            resp.status_code, resp.headers
        )
    )

    resp.raise_for_status()

    if not resp.json():
        data = json.dumps(resp.text)
    else:
        data = resp.json()

    t1 = time.time()

    if searchtype == "s":
        api_log.trace(
            "Finished search for {}, {} results in {} ms.".format(
                keyword, data.get("totalResults"), int(1000 * (t1 - t0))
            )
        )
    if searchtype == "i":
        api_log.trace(
            "Finished search for {} results in {} ms.".format(
                imdbid, int(1000 * (t1 - t0))
            )
        )

    return data


def abstract_connection(URL, payload, app_log, st):
    try:
        data = search_movies_api(URL, payload, searchtype=st)
    except requests.exceptions.ConnectionError:
        msg = "Could not find server. Check your network connection."
        print("ERROR: " + msg)
        app_log.warn(msg)
    except ValueError:
        msg = "You must specify a search term."
        print("ERROR: " + msg)
        app_log.warn(msg)
    except Exception as x:
        msg = "Oh that didn't work!: {}".format(x)
        print(msg)
        app_log.exception(x)

    if not data.get("Error"):
        return data
    else:
        raise ValueError("Movies search find nothing by entered keyword")


def main():
    app_log = logbook.Logger("App")

    Record = namedtuple("Record", ("Title", "Year", "imdbID", "Type", "Poster"))
    movies = []

    keyword = input("Keyword of title search: ")
    year = input("Optional enter movie year: ")

    payload_search = {"s": keyword, "y": year, "apikey": APIKEY}

    app_log.info("Make movies search by keyword")
    data = abstract_connection(URL, payload_search, app_log, st="s")

    for row in data["Search"]:
        movies.append(Record(**row))

    payload_imdbid = {"i": movies[0].imdbID, "apikey": APIKEY}

    data.clear()
    app_log.info("Make movie search by imdbId")
    data = abstract_connection(URL, payload_imdbid, app_log, st="i")

    print(f"""For {data["Title"]} {data["Year"]} ratings is:""")

    for item in data["Ratings"]:
        print(
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
