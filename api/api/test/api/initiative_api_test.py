import requests

from config import API_TEST_URL, API_TEST_USER_NO_PERMISSIONS, API_TEST_TIMEOUT
from test.api.api_test_helpers import get_authenticated_client, create_namespace

workspace_name = "Test Workspace"
initiative_name = "Test Initiative"
authenticated_client = get_authenticated_client()


def test_create_initiative():
    # Arrange
    workspace_id = create_namespace(workspace_name)

    # Act
    resp = authenticated_client.post(API_TEST_URL + f"workspace/{workspace_id}/initiatives/",
                                     json={"name": initiative_name},
                                     timeout=API_TEST_TIMEOUT)

    # Assert
    assert resp.status_code == 200

    resp_body = resp.json()
    assert resp_body['name'] == initiative_name
    assert resp_body['id'] is not None


def test_unauthenticated_create_initiative():
    # Arrange
    workspace_id = create_namespace(workspace_name)

    # Act
    resp = requests.post(API_TEST_URL + f"workspace/{workspace_id}/initiatives/",
                         json={"name": initiative_name},
                         timeout=API_TEST_TIMEOUT)

    # Assert
    assert resp.status_code == 401


def test_unauthorized_create_initiative():
    # Arrange
    workspace_id = create_namespace(workspace_name)
    authenticated_client_user_without_permissions = get_authenticated_client(user=API_TEST_USER_NO_PERMISSIONS)

    # Act
    resp = authenticated_client_user_without_permissions.post(API_TEST_URL + f"workspace/{workspace_id}/initiatives/",
                                                              json={"name": initiative_name},
                                                              timeout=API_TEST_TIMEOUT)

    # Assert
    assert resp.status_code == 403


def test_update_initiative():
    # Arrange
    workspace_id = create_namespace(workspace_name)
    create_resp = authenticated_client.post(API_TEST_URL + f"workspace/{workspace_id}/initiatives/",
                                            json={"name": initiative_name},
                                            timeout=API_TEST_TIMEOUT)

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id is not None

    updated_name = "Test initiative with updated name"

    # Act
    update_resp = authenticated_client.put(API_TEST_URL + f"workspace/{workspace_id}/initiatives/{initiative_id}",
                                           json={"name": updated_name},
                                           timeout=API_TEST_TIMEOUT)

    # Assert
    assert update_resp.status_code == 200

    resp_body = update_resp.json()
    updated_initiative_id = resp_body['id']

    assert resp_body['name'] == updated_name
    assert updated_initiative_id == initiative_id


def test_get_initiative():
    # Arrange
    workspace_id = create_namespace(workspace_name)
    create_resp = authenticated_client.post(API_TEST_URL + f"workspace/{workspace_id}/initiatives/",
                                            json={"name": initiative_name},
                                            timeout=API_TEST_TIMEOUT)

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id is not None

    # Act
    get_resp = authenticated_client.get(API_TEST_URL + f"workspace/{workspace_id}/initiatives/{initiative_id}",
                                        timeout=API_TEST_TIMEOUT)

    # Assert
    resp_body = get_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id == initiative_id


def test_get_initiative_events():
    # Arrange
    workspace_id = create_namespace(workspace_name)
    create_resp = authenticated_client.post(API_TEST_URL + f"workspace/{workspace_id}/initiatives/",
                                            json={"name": initiative_name},
                                            timeout=API_TEST_TIMEOUT)

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    initiative_id = resp_body['id']

    assert resp_body['name'] == initiative_name
    assert initiative_id is not None

    updated_name = "Test initiative with updated name"

    update_resp = authenticated_client.put(API_TEST_URL + f"workspace/{workspace_id}/initiatives/{initiative_id}",
                                           json={"name": updated_name},
                                           timeout=API_TEST_TIMEOUT)

    resp_body = update_resp.json()
    updated_initiative_id = resp_body['id']

    assert resp_body['name'] == updated_name
    assert updated_initiative_id == initiative_id

    # Act
    get_events_resp = \
        authenticated_client.get(API_TEST_URL + f"workspace/{workspace_id}/initiatives/{initiative_id}/events",
                                 timeout=API_TEST_TIMEOUT)

    # Assert
    events = get_events_resp.json()

    assert len(events) == 2
    assert events[0]["name"] == "planning.initiative.initiative-defined"
    assert events[1]["name"] == "planning.initiative.initiative-modified"
