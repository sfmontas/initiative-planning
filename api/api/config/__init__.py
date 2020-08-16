from os import getenv
# Test configuration
API_TEST_URL = getenv("API_TEST_URL") or 'http://localhost:8000/'
API_TEST_USER = getenv("API_TEST_USER") or "elvinv"
API_TEST_USER_NO_PERMISSIONS = getenv("API_TEST_USER") or "vivim"
API_TEST_PASSWORD = getenv("API_TEST_PASSWORD") or "password"
API_TEST_TIMEOUT = getenv("API_TEST_TIMEOUT") or .5

OAUTH_SECRET_KEY = getenv("OAUTH_SECRET_KEY") or "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
OAUTH_JWT_ALGORITHM = getenv("OAUTH_JWT_ALGORITHM") or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("OAUTH_JWT_ALGORITHM") or 30

SQL_DB_URL = "mysql://root:pass123@mysql:3306/initiative_planning"


