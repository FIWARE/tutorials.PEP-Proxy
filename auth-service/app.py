from flask import Flask, request
import jwt as pyjwt

app = Flask(__name__)

ROLE_PERMISSIONS = {
    "farm-manager":         {"GET", "POST", "PATCH", "DELETE", "PUT"},
    "livestock-supervisor": {"GET", "POST", "PATCH", "DELETE"},
    "read-only-consultant": {"GET"},
    "crop-supervisor":      {"GET", "POST", "PATCH"},
    "equipment-supervisor": {"GET", "POST", "PATCH"},
    "field-worker":         {"GET"},
}


@app.route("/health")
def health():
    return "", 200


@app.route("/auth", methods=["GET", "POST"])
def auth():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return "", 401

    token = auth_header[7:]
    try:
        payload = pyjwt.decode(token, options={"verify_signature": False, "verify_exp": True})
    except pyjwt.ExpiredSignatureError:
        return "", 401
    except pyjwt.DecodeError:
        return "", 401

    roles = payload.get("realm_access", {}).get("roles", [])
    method = request.headers.get("X-Forwarded-Method", "GET").upper()

    for role in roles:
        if role in ROLE_PERMISSIONS and method in ROLE_PERMISSIONS[role]:
            return "", 200

    return "", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
