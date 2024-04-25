import pytest
import json
import time

from app import app

BASE_URL = "http://127.0.0.1:5000/api/v1.0/items"
BAD_ITEM_URL = "{}/5".format(BASE_URL)
GOOD_ITEM_URL = "{}/3".format(BASE_URL)


@pytest.fixture(scope="session")
def create_app():
    app
    app.config.update(
        {
            "TESTING": True,
        }
    )
    # other setup can go here
    yield app
    # clean up / reset resources here
    app.run = False


@pytest.fixture()
def client(create_app):
    return app.test_client()


def test_get_items(client):
    req = client.get(BASE_URL)
    # check BASE_URL request
    assert req.status_code == 200
    data = json.loads(req.data)
    # check BASE_URL response items
    assert len(data["items"]) == 3


@pytest.fixture(autouse=True)
def footer_function_scope():
    """Test duration"""
    start = time.time()
    yield
    stop = time.time()
    delta = stop - start
    print("\ntest duration : {:0.3} seconds".format(delta))
    print("--------------" * 3)


def test_get_item(client):
    # get one non exist item
    req = client.get(BAD_ITEM_URL)
    assert req.status_code == 404
    # get one exist item
    req = client.get(GOOD_ITEM_URL)
    data = json.loads(req.data)
    assert req.status_code == 200
    assert len(data["items"]) == 1


def test_not_found(client):
    req = client.get(BAD_ITEM_URL)
    assert req.status_code == 404


def test_bad_request(client):
    item = {"name": "laptop", "some-value": "1000"}
    # item wrong request body
    req = client.post(BASE_URL, data=json.dumps(item), content_type="application/json")
    assert req.status_code == 400


def test_create_item(client):
    # wrong request body
    item = {"name": "laptop", "some-value": "1000"}
    req = client.post(BASE_URL, data=json.dumps(item), content_type="application/json")
    assert req.status_code == 400
    # item exist
    item = {"name": "laptop", "value": int(1)}
    req = client.post(BASE_URL, data=json.dumps(item), content_type="application/json")
    assert req.status_code == 400
    # item wrong request value type
    item = {"name": "monitor", "value": str(1)}
    req = client.post(BASE_URL, data=json.dumps(item), content_type="application/json")
    assert req.status_code == 400
    # create item
    item = {"name": "printer", "value": 100}
    reponse = client.post(
        BASE_URL, data=json.dumps(item), content_type="application/json"
    )


def test_update_item(client):
    item = {"name": "laptop", "some-value": "1000"}
    # item wrong request body
    req = client.post(BASE_URL, data=json.dumps(item), content_type="application/json")
    assert req.status_code == 400


def test_update_item(client):
    # update non exist item
    req = client.put(BAD_ITEM_URL)
    assert req.status_code == 404
    # empty request body
    req = client.put(
        GOOD_ITEM_URL, data=json.dumps({}), content_type="application/json"
    )
    assert req.status_code == 400
    # request body contains str instead of int value
    req = client.put(
        GOOD_ITEM_URL,
        data=json.dumps({"name": "book", "value": str(10)}),
        content_type="application/json",
    )
    assert req.status_code == 400
    # correct request
    req = client.put(
        GOOD_ITEM_URL,
        data=json.dumps({"name": "book", "value": int(10)}),
        content_type="application/json",
    )
    assert req.status_code == 200


def test_delete_item(client):
    # delete non exist item
    req = client.delete(BAD_ITEM_URL)
    assert req.status_code == 404
    # delete exist item
    req = client.delete(GOOD_ITEM_URL)
    assert req.status_code == 204
