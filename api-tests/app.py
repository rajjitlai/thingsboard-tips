from get_all_devices.script import getAllDevices
from get_specific_device_data.script import getSpecificDeviceData
from user_device_select.script import returnDeviceName

if __name__ == "__main__":
    devices, tb_url, token = getAllDevices()
    device_name = returnDeviceName(devices)

    if device_name:
        getSpecificDeviceData(device_name, devices, tb_url, token)
    else:
        print("⚠️ No valid device selected.")
