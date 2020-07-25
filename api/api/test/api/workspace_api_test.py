import requests

from config import API_TEST_URL, API_TEST_USER_NO_PERMISSIONS, API_TEST_TIMEOUT
from test.api.api_test_helpers import get_authenticated_client

workspace_name = "Test Workspace"
authenticated_client = get_authenticated_client()


def test_create_workspace():
    # Act
    resp = authenticated_client.post(API_TEST_URL + "workspaces/",
                                     json={"name": workspace_name},
                                     timeout=API_TEST_TIMEOUT)

    # Assert
    assert resp.status_code == 200

    resp_body = resp.json()
    assert resp_body['name'] == workspace_name
    assert resp_body['id'] is not None


def test_unauthenticated_create_workspace():
    # Act
    resp = requests.post(API_TEST_URL + "workspaces/", json={"name": workspace_name}, timeout=API_TEST_TIMEOUT)

    # Assert
    assert resp.status_code == 401


def test_unauthorized_create_workspace():
    # Arrange
    authenticated_client_user_without_permissions = get_authenticated_client(user=API_TEST_USER_NO_PERMISSIONS)

    # Act
    resp = authenticated_client_user_without_permissions.post(API_TEST_URL + "workspaces/",
                                                              json={"name": workspace_name},
                                                              timeout=API_TEST_TIMEOUT)

    # Assert
    assert resp.status_code == 403


def test_update_workspace():
    # Arrange
    create_resp = authenticated_client.post(API_TEST_URL + "workspaces/",
                                            json={"name": workspace_name},
                                            timeout=API_TEST_TIMEOUT)

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    workspace_id = resp_body['id']

    assert resp_body['name'] == workspace_name
    assert workspace_id is not None

    updated_name = "Test workspace with updated name"

    # Act
    update_resp = authenticated_client.put(API_TEST_URL + f"workspaces/{workspace_id}", json={"name": updated_name},
                                           timeout=API_TEST_TIMEOUT)

    # Assert
    resp_body = update_resp.json()
    updated_workspace_id = resp_body['id']

    assert resp_body['name'] == updated_name
    assert updated_workspace_id == workspace_id


def test_get_workspace():
    # Arrange
    create_resp = authenticated_client.post(API_TEST_URL + "workspaces/",
                                            json={"name": workspace_name},
                                            timeout=API_TEST_TIMEOUT)

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    workspace_id = resp_body['id']

    assert resp_body['name'] == workspace_name
    assert workspace_id is not None

    # Act
    get_resp = authenticated_client.get(API_TEST_URL + f"workspaces/{workspace_id}", timeout=API_TEST_TIMEOUT)

    # Assert
    resp_body = get_resp.json()
    workspace_id = resp_body['id']

    assert resp_body['name'] == workspace_name
    assert workspace_id == workspace_id


def test_get_workspace_events():
    # Arrange
    create_resp = authenticated_client.post(API_TEST_URL + "workspaces/",
                                            json={"name": workspace_name},
                                            timeout=API_TEST_TIMEOUT)

    assert create_resp.status_code == 200

    resp_body = create_resp.json()
    workspace_id = resp_body['id']

    assert resp_body['name'] == workspace_name
    assert workspace_id is not None

    updated_name = "Test workspace with updated name"

    update_resp = authenticated_client.put(API_TEST_URL + f"workspaces/{workspace_id}", json={"name": updated_name},
                                           timeout=API_TEST_TIMEOUT)

    resp_body = update_resp.json()
    updated_workspace_id = resp_body['id']

    assert resp_body['name'] == updated_name
    assert updated_workspace_id == workspace_id

    # Act
    get_events_resp = authenticated_client.get(API_TEST_URL + f"workspaces/{workspace_id}/events",
                                               timeout=API_TEST_TIMEOUT)

    # Assert
    events = get_events_resp.json()

    assert len(events) == 2
    assert events[0]["name"] == "planning.workspace.workspace-defined"
    assert events[1]["name"] == "planning.workspace.workspace-modified"
