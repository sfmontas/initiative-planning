from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from config import API_TEST_USER, API_TEST_URL, API_TEST_PASSWORD, API_TEST_TIMEOUT


def get_authenticated_client(user: str = API_TEST_USER, password: str = API_TEST_PASSWORD):
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=""))
    oauth.fetch_token(token_url=API_TEST_URL + 'token/',
                      username=user, password=password, client_id="",
                      client_secret="")
    return oauth


def create_namespace(workspace_name: str):
    authenticated_client = get_authenticated_client()
    workspace_resp = authenticated_client.post(API_TEST_URL + "workspaces/",
                                               json={"name": workspace_name},
                                               timeout=API_TEST_TIMEOUT)
    assert workspace_resp.status_code == 200
    workspace_resp_body = workspace_resp.json()
    workspace_id = workspace_resp_body["id"]

    assert workspace_id is not None

    return workspace_id
