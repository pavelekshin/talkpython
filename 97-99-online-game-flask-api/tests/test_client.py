import json
import os
import random
import re
import pytest
import time

from app import create_app
from config.config import TestingConfig, DevelopmentConfig
from db.db_folder import get_db_path

BASE_URL = "http://127.0.0.1:5000"
BAD_URL = "{}/api/v2/game/status".format(BASE_URL)
USERNAME = "Test1"
UUID4 = "^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[4][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
GAME_ID = None
ROLLS = ['Rock', 'Gun', 'Lightning', 'Devil', 'Dragon', 'Water', 'Air', 'Paper', 'Sponge', 'Wolf', 'Tree', 'Human',
         'Snake', 'Scissors', 'Fire']


@pytest.fixture(scope="session")
def app():
    cfg = TestingConfig()
    app = create_app(config=cfg)
    # other setup can go here
    yield app
    # clean up / reset resources here
    app.run = False
    if getattr(cfg, "db_name", None) is not None:
        try:
            os.remove(getattr(cfg, "db_name"))
        except OSError as ex:
            print(f"Oops: {ex}")
            pass


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def footer():
    start = time.time()
    yield
    stop = time.time()
    delta = stop - start
    print("\ntest duration : {:0.3} seconds".format(delta))
    print("--------------" * 3)


@pytest.mark.parametrize(
    "url", [f"{BASE_URL}/"]
)
def test_home_page(client, url):
    req = client.get(url)
    # check BASE_URL request
    assert req.status_code == 200
    data = req.data.decode("utf-8")
    # check BASE_URL response
    assert "Hello world!" == data


@pytest.mark.parametrize(
    "url",
    [
        f"{BASE_URL}/api/game/users/Bob"
    ]
)
def test_find_nonexistent_user(client, url):
    req = client.get(url)
    # check request status code
    assert req.status_code == 404
    data = req.json
    # check response
    assert data["message"] == "User was not found!"


@pytest.mark.parametrize(
    "url, body, content_type",
    [
        (
                f"{BASE_URL}/api/game/users",
                {"user": USERNAME},
                "application/json",
        )
    ]
)
def test_create_user(client, url, body, content_type):
    req = client.put(url,
                     data=json.dumps(body),
                     content_type=content_type
                     )
    # check request status code
    assert req.status_code == 200
    # check response
    assert len(req.json) == 3


@pytest.mark.parametrize(
    "url",
    [
        f"{BASE_URL}/api/game/users/{USERNAME}"
    ]
)
def test_find_user(client, url):
    req = client.get(url)
    # check request status code
    assert req.status_code == 200
    # check response
    assert len(req.json) == 3


@pytest.mark.parametrize(
    "url",
    [
        f"{BASE_URL}/api/game/games"
    ]
)
def test_get_game_id(client, url, monkeypatch):
    global GAME_ID
    req = client.get(url)
    # check request status code
    assert req.status_code == 200
    data = req.json
    # check response
    game_id = data["game_id"]
    assert bool(re.match(UUID4, game_id)) is True
    GAME_ID = game_id


@pytest.mark.parametrize(
    "url, rolls",
    [
        (
                f"{BASE_URL}/api/game/rolls",
                ROLLS
        )
    ]
)
def test_get_all_rolls(client, url, rolls):
    req = client.get(url)
    # check request status code
    assert req.status_code == 200
    # check response
    assert len(req.json) == 15
    # check rolls
    assert rolls == req.json


@pytest.mark.parametrize(
    "url",
    [
        f"{BASE_URL}/api/game/top_scores"
    ]
)
def test_top_scores(client, url):
    req = client.get(url)
    # check request status code
    assert req.status_code == 200


@pytest.fixture(scope="function")
def body(request):
    return {
        "game_id": GAME_ID,
        "user": USERNAME,
        "roll": random.choice(ROLLS)
    }


@pytest.mark.parametrize(
    "url, body, content_type",
    [
        (
                f"{BASE_URL}/api/game/play_round",
                {
                    "game_id": GAME_ID,
                    "user": USERNAME,
                    "roll": random.choice(ROLLS)
                },
                "application/json",
        )
    ],
    indirect=["body"]
)
def test_play_round(client, url, body, content_type):
    req = client.post(url,
                      data=json.dumps(body), content_type=content_type)
    # check request status code
    assert req.status_code == 200
    is_over = False
    while not is_over:
        req = client.post(url,
                          data=json.dumps(body), content_type=content_type)
        is_over = req.json.get("is_final_round")
    assert req.status_code == 200
    assert is_over is True


@pytest.fixture(scope="function")
def url(request):
    return f"{BASE_URL}/api/game/{GAME_ID}/status"


@pytest.mark.parametrize(
    "url",
    [
        f"{BASE_URL}/api/game/{GAME_ID}/status"
    ],
    indirect=True
)
def test_get_game_status(client, url):
    req = client.get(url)
    # check request status code
    assert req.status_code == 200


@pytest.mark.parametrize(
    "url",
    [
        f"{BAD_URL}"
    ]
)
def test_not_found(client, url):
    req = client.get(BAD_URL)
    assert req.status_code == 404
