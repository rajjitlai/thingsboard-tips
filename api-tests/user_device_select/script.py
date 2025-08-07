def returnDeviceName(devices):
    print("\n🔍 Choose device by number or type exact name:\n")
    choice = input("➡️ Enter device number or name: ").strip()

    # Try to interpret as index number
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(devices):
            return devices[index]["name"]
        else:
            print("❌ Invalid index selected.")
            return None
    else:
        # Check if name exists
        for device in devices:
            if device["name"].lower() == choice.lower():
                return device["name"]
        print("❌ No device with that name found.")
        return None
