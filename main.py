import csv
import glob
import json
import os

path_to_logs = '/home/alina.gotovtceva/Downloads/logs'

json_pattern = os.path.join(path_to_logs, '**', '*FinalReflash.json')
file_list = glob.glob(json_pattern, recursive=True)
devices_dict = {}

for file in file_list:
    with open(file) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            continue
        for device in data["testing_results"]:
            if device["serial_number"]:
                devices_dict[device["serial_number"][:-4]] = {
                    "preovernight": None
                }

print(len(devices_dict.keys()))
json_pattern = os.path.join(path_to_logs, '**', '*PreOvernight.json')
file_list = glob.glob(json_pattern, recursive=True)

for file in file_list:
    with open(file) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            continue
        for device in data["testing_results"]:
            serial_number = device["serial_number"][:-4]
            if serial_number in devices_dict and devices_dict[serial_number]["preovernight"] != "AllTestsPassed":
                devices_dict[serial_number] = {
                    "preovernight": device["result_type"]
                }

with open('serial_numbers_rs2.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["#", "serial number", "preovernight"])
    for i, number in enumerate(devices_dict, 1):
        writer.writerow([i, number, devices_dict[number].get("preovernight")])
