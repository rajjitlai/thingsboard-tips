import requests
from dotenv import load_dotenv
import time

load_dotenv()


def getSpecificDeviceData(device_name, devices, THINGSBOARD_URL, token):
    headers = {"X-Authorization": f"Bearer {token}"}
    device_id = None

    for device in devices:
        if device.get("name") == device_name:
            device_id = device["id"]["id"]
            break

    if not device_id:
        print(f"\n❌ Device '{device_name}' not found.")
        return

    print(f"\n✅ Found device: {device_name}")

    # Set time range (last 7 days)
    end_ts = int(time.time() * 1000)
    start_ts = end_ts - 7 * 24 * 60 * 60 * 1000

    telemetry_url = (
        f"{THINGSBOARD_URL}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
        f"?keys=temperature,humidity&startTs={start_ts}&endTs={end_ts}&limit=10000"
    )

    telemetry_resp = requests.get(telemetry_url, headers=headers)

    if telemetry_resp.status_code == 200:
        print("\n📡 Telemetry Data:")
        telemetry = telemetry_resp.json()
        for key, records in telemetry.items():
            print(f"\n📈 {key}:")
            for entry in records:
                ts = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(entry["ts"] / 1000)
                )
                print(f"  - {ts} → {entry['value']}")
    else:
        print("\n❌ Failed to fetch telemetry:", telemetry_resp.text)
