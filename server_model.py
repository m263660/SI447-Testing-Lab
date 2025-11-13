# server_model.py
import requests

# Model for interacting with MidsQuest API
class ServerModel:
    # Constructor method
    def __init__(self, base_url="http://lnx1073302govt:8000"):
        self.base_url = base_url.rstrip("/")
        self.session_token = None

    # Method to create a new user
    def sign_up(self, username: str, password: str) -> bool:
        r = requests.post(f"{self.base_url}/user", json={"username": username, "password": password})
        return r.status_code == 200

    # Method for logging in
    def login(self, username: str, password: str) -> bool:
        r = requests.post(f"{self.base_url}/login", json={"username": username, "password": password})
        # Raises an exception if login invalid
        if r.status_code != 200:
            raise Exception(f"Login failed: {r.text}")
        # Stores session token if valid
        self.session_token = r.json()["session_token"]
        return True

    # Helper method for POST requests
    def _post(self, endpoint: str, data: dict) -> dict:
        # If no token, raises Exception
        if not self.session_token:
            raise Exception("Not logged in")
        # Sends POST request
        r = requests.post(f"{self.base_url}{endpoint}", json=data, headers={"session-token": self.session_token})
        # Raises exception if not valid
        if r.status_code != 200:
            raise Exception(f"{endpoint} failed: {r.text}")
        return r.json()

    # Handles player movement 
    def move(self, direction: str) -> str:
        return self._post("/move", {"direction": direction})["message"]

    # Gets rooms description and players
    def look(self) -> dict:
        if not self.session_token:
            raise Exception("Not logged in")
        r = requests.get(f"{self.base_url}/look", headers={"session-token": self.session_token})
        if r.status_code != 200:
            raise Exception(f"look failed: {r.text}")
        return r.json()

    # Sets player's current activity
    def doing(self, action: str) -> str:
        return self._post("/doing", {"action": action})["message"]

    # Uses an item in the current room
    def use(self, item: str) -> str:
        """200 OK with 'message' OR 'detail' — DO NOT RAISE ON 200"""
        if not self.session_token:
            raise Exception("Not logged in")
        r = requests.post(f"{self.base_url}/use", json={"item": item}, headers={"session-token": self.session_token})
        if r.status_code != 200:
            raise Exception(f"use failed: {r.text}")
        data = r.json()
        return data.get("message") or data.get("detail", "")