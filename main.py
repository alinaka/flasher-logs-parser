import csv
import glob
import json
import os
import re

path_to_logs = '/home/alina.gotovtceva/Downloads/logs'

json_pattern = os.path.join(path_to_logs, '**', '*FinalReflash.json')
file_list = glob.glob(json_pattern, recursive=True)
devices_dict = {}
empty_logs_final_reflash = []

for file in file_list:
    with open(file) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            empty_logs_final_reflash.append(file)
            continue
        for device in data["testing_results"]:
            if device["serial_number"]:
                devices_dict[device["serial_number"][:-4]] = {
                    "preovernight": None
                }

print(len(devices_dict.keys()))
json_pattern = os.path.join(path_to_logs, '**', '*PreOvernight.json')
file_list = glob.glob(json_pattern, recursive=True)

preovernight_passed = set()
s = []
empty_logs_preovernight = []
for file in file_list:
    with open(file) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            empty_logs_preovernight.append(file[38:-22])
            continue
        for device in data["testing_results"]:
            additional_test_info = ""
            if len(device["serial_number"]) >= 20:
                if len(device["serial_number"]) == 20:
                    serial_number = device["serial_number"][:-4]
                else:
                    split = device["serial_number"].split(",")
                    serial_number = split[0][:-4]
                    test_info = split[1:]
                    for test in test_info:
                        k, v = test.split(":")
                        if v == "0":
                            additional_test_info = test_info
                            break
                if serial_number and device["result_type"] == "AllTestsPassed":
                    preovernight_passed.add(serial_number)
                if serial_number in devices_dict:
                    devices_dict[serial_number].update({
                        "additional_test_info": additional_test_info
                    })
                    if devices_dict[serial_number]["preovernight"] != "AllTestsPassed":
                        devices_dict[serial_number].update({
                            "preovernight": device["result_type"]
                        })
                if serial_number not in devices_dict and device["result_type"] == "AllTestsPassed":
                    devices_dict[serial_number] = {
                        "preovernight": device["result_type"],
                        "not_in_reflash": 1,
                        "additional_test_info": additional_test_info
                    }
            else:
                if device["result_type"] == "AllTestsPassed":
                    s.append(device["serial_number"])
print(*set(s), sep="\n")
print(len(s))
print(len(preovernight_passed))
with open('serial_numbers_rs2.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["#", "serial number", "preovernight", "device failed test, but flasher assummed everything is ok", "devices that passed pre-overnight, but didn't appear at FinalReflash"])
    for i, number in enumerate(devices_dict, 1):
        writer.writerow([i, number, devices_dict[number].get("preovernight"),
                         devices_dict[number].get("additional_test_info"),
                         devices_dict[number].get("not_in_reflash")])

with open('empty_logs_final_reflash.txt', 'w') as f:
    f.write("\n".join(empty_logs_final_reflash))

with open('empty_logs_preovernight.txt', 'w') as f:
    f.write("\n".join(empty_logs_preovernight))
d = []
for file in empty_logs_preovernight:

    if os.listdir(os.path.join(os.path.dirname(file), "devices")):
        import subprocess
        from subprocess import check_output
        try:
            output = check_output(["grep", "-r", "result:", os.path.join(os.path.dirname(file), "devices")])
        except subprocess.CalledProcessError as e:
            continue
        print(output)
        d.append(file[38:-22])
    else:
        pass
#
# print(d)
# with open('empty_logs_preovernight.txt', 'w') as f:
#     f.write("\n".join(d))
