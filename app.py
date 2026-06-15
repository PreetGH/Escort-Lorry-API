from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# in-memory storage (simple version)
weather_data = {}

API_KEY = "supersecret123"



# -----------------------
# AUTH MIDDLEWARE
# -----------------------
@app.before_request
def check_key():
    if request.method == "POST":
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401


# -----------------------
# RECEIVE WEATHER FROM ROBLOX
# -----------------------
@app.route("/weather", methods=["POST"])
def receive_weather():
    data = request.json

    server_id = data.get("serverId")
    if not server_id:
        return jsonify({"error": "Missing serverId"}), 400

    weather_data[server_id] = {
        "data": data,
        "lastUpdate": time.time()
    }

    return jsonify({
        "success": True,
        "message": "Weather stored",
        "serverId": server_id
    })

def get_active_servers():
    now = time.time()
    active = {}

    for server_id, info in weather_data.items():
        if now - info["lastUpdate"] < 120:  # 2 minutes timeout
            active[server_id] = info["data"]

    return active

@app.route("/status", methods=["GET"])
def status():
    active = get_active_servers()

    if len(active) == 0:
        return jsonify({
            "status": "critical",
            "message": "No Roblox servers are reporting data",
            "warning": True
        })

    return jsonify({
        "status": "healthy",
        "servers": len(active)
    })

# -----------------------
# GET ALL WEATHER
# -----------------------
@app.route("/weather", methods=["GET"])
def get_weather():
    active = get_active_servers()

    if not active:
        return jsonify({
            "status": "warning",
            "message": "No active servers detected",
            "active_servers": 0
        })

    return jsonify({
        "status": "ok",
        "active_servers": len(active),
        "data": active
    })


# -----------------------
# GET SINGLE SERVER WEATHER
# -----------------------
@app.route("/weather/<server_id>", methods=["GET"])
def get_server_weather(server_id):
    info = weather_data.get(server_id)

    if not info:
        return jsonify({"error": "Server not found"}), 404

    # stale check
    if time.time() - info["lastUpdate"] > 120:
        return jsonify({
            "status": "stale",
            "message": "Server data expired"
        })

    return jsonify({
        "status": "ok",
        "data": info["data"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
