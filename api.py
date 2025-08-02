import requests
import json
import random
import time
import math

# Device tokens
cart_keys = {
    "Tracker A": "dHZBftocoQTOMqZB2Djp",
    "Tracker B": "HdzyyAnWut7xXU0vBkGb",
}

# Base URL and headers
base_url = "http://dev.nibiaa.com:8080/api/v1"
headers = {"Content-Type": "application/json"}

# Initial state (unique per device)
data = {
    cart: {
        "lat": 27.5 + random.uniform(0, 0.5),
        "lon": 93.9 + random.uniform(0, 0.5),
        "alt": random.uniform(0, 100),
        "speed": random.uniform(0, 5),
        "bearing": random.uniform(0, 360),
        "battery": random.randint(60, 100),
        "fuel": random.randint(30, 100),
        "signal": random.randint(50, 100),
    }
    for cart in cart_keys
}


def knots_to_mps(knots):
    return knots * 0.514


def update_position(lat, lon, speed_knots, bearing):
    speed_mps = knots_to_mps(speed_knots)
    distance = speed_mps * 4  # 4 seconds

    bearing_rad = math.radians(bearing)
    dx = distance * math.cos(bearing_rad)
    dy = distance * math.sin(bearing_rad)

    new_lat = lat + (dy / 111111)
    new_lon = lon + (dx / (111111 * math.cos(math.radians(lat))))
    return new_lat, new_lon


def update_device_state(state):
    target_speed = random.choices(
        [0, random.uniform(1, 4), random.uniform(5, 12), random.uniform(13, 18)],
        weights=[1, 2, 5, 2],
        k=1,
    )[0]

    delta = (target_speed - state["speed"]) * 0.1
    state["speed"] += delta

    state["bearing"] += random.uniform(-5, 5)
    state["bearing"] %= 360

    state["lat"], state["lon"] = update_position(
        state["lat"], state["lon"], state["speed"], state["bearing"]
    )

    battery_drain = 0.02 * state["speed"]
    if state["speed"] < 1:
        battery_drain -= 0.2
    state["battery"] = max(0, min(100, state["battery"] - battery_drain))

    fuel_burn = 0.05 * state["speed"]
    state["fuel"] = max(0, state["fuel"] - fuel_burn)

    state["signal"] = max(30, min(100, state["signal"] + random.uniform(-2, 2)))


# Send telemetry data
def send_telemetry(cart_id):
    state = data[cart_id]
    update_device_state(state)

    telemetry = {
        "ts": int(time.time() * 1000),
        "values": {
            # Position and Movement
            "latitude": round(state["lat"], 6),
            "longitude": round(state["lon"], 6),
            "altitude": round(state["alt"], 2),
            "speed": round(state["speed"], 2),
            "bearing": round(state["bearing"], 2),
            # Device Health
            "batteryLevel": round(state["battery"], 2),
            "fuelLevel": round(state["fuel"], 2),
            "signalStrength": round(state["signal"], 2),
            "engineStatus": "ON" if state["speed"] > 1 else "OFF",
            "status": "Active" if state["speed"] > 1 else "Idle",
            # Environmental Data
            "temperature": random.randint(22, 40),  # °C
            "humidity": random.randint(30, 90),  # %
            "windSpeed": round(random.uniform(0.5, 10), 2),  # m/s
            "windDirection": random.randint(0, 360),  # degrees
            "pressure": round(random.uniform(980, 1025), 2),  # hPa
        },
    }

    url = f"{base_url}/{cart_keys[cart_id]}/telemetry"

    try:
        response = requests.post(url, data=json.dumps(telemetry), headers=headers)
        if response.status_code == 200:
            print(f"{cart_id} - ✅ Sent: {telemetry['values']}")
        else:
            print(f"{cart_id} - ❌ HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"{cart_id} - ❌ Error: {e}")


# Main loop
if __name__ == "__main__":
    while True:
        for cart in cart_keys:
            send_telemetry(cart)
        time.sleep(1)
