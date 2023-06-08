from requests import post
from os import getenv
from dotenv import load_dotenv
from django.utils import timezone
from datetime import datetime

# import hashlib
# import base64
# import random
# import string

load_dotenv()


def refresh_token(request):
    if timezone.now() < datetime.fromisoformat(request.session["expiry"]):
        return
    token_url = "https://accounts.spotify.com/api/token"
    refresh_token = request.session["refresh_token"]

    response = post(
        token_url,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": getenv("client_id"),
            "client_secret": getenv("client_secret"),
        },
    )

    if response.status_code == 200:
        response_data = response.json()
        request.session["access_token"] = response_data.get("access_token")
        print("token refreshed successfully")


# def generate_code_verifier(length=64):
#     characters = string.ascii_letters + string.digits + "-._~"
#     return "".join(random.choice(characters) for i in range(length))


# def generate_code_challenge(code_verifier):
#     code_challenge = hashlib.sha256(code_verifier.encode()).digest()
#     code_challenge = base64.urlsafe_b64encode(code_challenge).rstrip(b"=").decode()
#     return code_challenge
