import requests
from dotenv import load_dotenv
from login.script import login_to_thingsboard

load_dotenv()

def getAllDevices():
    THINGSBOARD_URL, token = login_to_thingsboard()
    headers = {"X-Authorization": f"Bearer {token}"}

    devices = []
    page = 0
    page_size = 100

    while True:
        device_url = f"{THINGSBOARD_URL}/api/tenant/devices?pageSize={page_size}&page={page}"
        response = requests.get(device_url, headers=headers)

        if response.status_code != 200:
            print("❌ Failed to fetch devices:", response.text)
            break

        data = response.json()
        page_devices = data.get("data", [])
        devices.extend(page_devices)

        if not data.get("hasNext", False):
            break
        page += 1

    print(f"\n✅ Total Devices: {len(devices)}\n")
    for idx, device in enumerate(devices, 1):
        print(f"{idx}. 📟 {device['name']}")

    return devices, THINGSBOARD_URL, token