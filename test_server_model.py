# test_server_model.py
import pytest, random
from unittest.mock import patch
from server_model import ServerModel

# Fixture, creates a ServerModel instance
@pytest.fixture
def api():
    return ServerModel(base_url="http://test")

# Unit Tests
# Tests for successful sign-up
@pytest.mark.unit
def test_sign_up_success(api):
    with patch("requests.post") as m:
        m.return_value.status_code = 200
        assert api.sign_up("u", "p") is True

# Tests failure for sign-up
@pytest.mark.unit
def test_sign_up_fail(api):
    with patch("requests.post") as m:
        m.return_value.status_code = 400
        assert api.sign_up("u", "p") is False

# Tests for successful login and token storage
@pytest.mark.unit
def test_login_success(api):
    with patch("requests.post") as m:
        m.return_value.status_code = 200
        m.return_value.json.return_value = {"session_token": "abc"}
        api.login("u", "p")
        assert api.session_token == "abc"

# Integration Test
@pytest.mark.integration

# Test function with real API
def test_full_flow():

    # Instance with API URL
    server = ServerModel(base_url="http://lnx1073302govt:8000")

    # Generates unique user
    user = f"test_{random.randint(0,999999)}"
    pwd = "pwd"

    # Tests sign up, login and token
    assert server.sign_up(user, pwd) is True
    server.login(user, pwd)
    assert server.session_token is not None

    # Tests move and message
    msg = server.move("north")
    assert "moved" in msg.lower() or "cannot" in msg.lower()

    # Tests look and key
    data = server.look()
    assert "description" in data

    # Tests doing and message
    msg = server.doing("wave")
    assert "wave" in msg.lower()

    # Catches expected error for no item
    try:
        msg = server.use("potion")
    except Exception as e:
        msg = str(e)

    # Asserts on message
    assert "potion" in msg.lower() or "usable" in msg.lower() or "nearby" in msg.lower()