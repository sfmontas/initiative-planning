from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from config import API_TEST_URL, API_TEST_USER, API_TEST_PASSWORD, API_TEST_TIMEOUT


def test_setup():
    initiative_name = "Test initiative"
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=""))
    oauth.fetch_token(token_url=API_TEST_URL + 'token/',
                      username=API_TEST_USER, password=API_TEST_PASSWORD, client_id="",
                      client_secret="")
    return initiative_name, oauth


def test_create_initiative():
    # Arrange
    initiative_name, oauth = test_setup()

    # Act
    resp = oauth.post(API_TEST_URL + "initiatives/", json={"name": initiative_name}, timeout=API_TEST_TIMEOUT)

    # Assert
    assert resp.status_code == 200

    resp_body = resp.json()
    assert resp_body['name'] == initiative_name
    assert resp_body['id'] is not None


def test_update_initiative():
    # Arrange
    initiative_name, oauth = test_setup()
    create_resp = oauth.post(API_TEST_URL + "initiatives/", json={"name": initiative_name}, timeout=API_TEST_TIMEOUT)

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id is not None

    updated_name = "Test initiative with updated name"

    # Act
    update_resp = oauth.put(API_TEST_URL + f"initiatives/{initiative_id}", json={"name": updated_name}, timeout=API_TEST_TIMEOUT)

    # Assert
    resp_body = update_resp.json()
    updated_initiative_id = resp_body['id']

    assert resp_body['name'] == updated_name
    assert updated_initiative_id == initiative_id


def test_get_initiative():
    # Arrange
    initiative_name, oauth = test_setup()
    create_resp = oauth.post(API_TEST_URL + "initiatives/", json={"name": initiative_name}, timeout=API_TEST_TIMEOUT)

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id is not None

    # Act
    get_resp = oauth.get(API_TEST_URL + f"initiatives/{initiative_id}", timeout=API_TEST_TIMEOUT)

    # Assert
    resp_body = get_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id == initiative_id


def test_get_initiative_events():
    # Arrange
    initiative_name, oauth = test_setup()
    create_resp = oauth.post(API_TEST_URL + "initiatives/", json={"name": initiative_name}, timeout=API_TEST_TIMEOUT)

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id is not None

    updated_name = "Test initiative with updated name"

    update_resp = oauth.put(API_TEST_URL + f"initiatives/{initiative_id}", json={"name": updated_name},
                            timeout=API_TEST_TIMEOUT)

    resp_body = update_resp.json()
    updated_initiative_id = resp_body['id']

    assert resp_body['name'] == updated_name
    assert updated_initiative_id == initiative_id

    # Act
    get_events_resp = oauth.get(API_TEST_URL + f"initiatives/{initiative_id}/events", timeout=API_TEST_TIMEOUT)

    # Assert
    events = get_events_resp.json()

    assert len(events) == 2
    assert events[0]["name"] == "planning.initiative.initiative-defined"
    assert events[1]["name"] == "planning.initiative.initiative-modified"
