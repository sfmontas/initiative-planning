from os import getenv
import requests

url = getenv("API_URL") or 'http://localhost:8000/'


def test_root():
    resp = requests.get(url)
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['message'] == "Hello World!"


def test_create_initiative():
    # Arrange
    initiative_name = "Test initiative"

    # Act
    resp = requests.post(url + "initiatives/", json={"name": initiative_name})

    # Assert
    assert resp.status_code == 200

    resp_body = resp.json()
    assert resp_body['name'] == initiative_name
    assert resp_body['id'] is not None


def test_update_initiative():
    # Arrange
    initiative_name = "Test initiative"
    create_resp = requests.post(url + "initiatives/", json={"name": initiative_name})

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id is not None

    updated_name = "Test initiative with updated name"

    # Act
    update_resp = requests.put(url + f"initiatives/{initiative_id}", json={"name": updated_name})

    # Assert
    resp_body = update_resp.json()
    updated_initiative_id = resp_body['id']

    assert resp_body['name'] == updated_name
    assert updated_initiative_id == initiative_id


def test_get_initiative():
    # Arrange
    initiative_name = "Test initiative"
    create_resp = requests.post(url + "initiatives/", json={"name": initiative_name})

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id is not None

    # Act
    get_resp = requests.get(url + f"initiatives/{initiative_id}")

    # Assert
    resp_body = get_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id == initiative_id


def test_get_initiative_events():
    # Arrange
    initiative_name = "Test initiative"
    create_resp = requests.post(url + "initiatives/", json={"name": initiative_name})

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id is not None

    updated_name = "Test initiative with updated name"

    update_resp = requests.put(url + f"initiatives/{initiative_id}", json={"name": updated_name})

    resp_body = update_resp.json()
    updated_initiative_id = resp_body['id']

    assert resp_body['name'] == updated_name
    assert updated_initiative_id == initiative_id

    # Act
    get_events_resp = requests.get(url + f"initiatives/{initiative_id}/events")

    # Assert
    events = get_events_resp.json()

    assert len(events) == 2
    assert events[0]["name"] == "planning.initiative.initiative-defined"
    assert events[1]["name"] == "planning.initiative.initiative-modified"
