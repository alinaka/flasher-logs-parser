import glob
import os

path_to_logs = '/home/alina.gotovtceva/china-logs'

log_pattern = os.path.join(path_to_logs, '**', '*.log')
file_list = glob.glob(log_pattern, recursive=True)
devices_dict = {}
empty_logs_final_reflash = []
final_reflash = 0
ublox_failed = set()

for file in file_list:
    with open(file) as f:
        log = f.read()
        if "Device type: RS2_FinalReflash" in log:
            if "u-blox:0" in log:
                serial_number_index = log.find("serial-number:")
                serial_number = log[serial_number_index+14:serial_number_index+14+16]
                ublox_failed.add(serial_number)
            final_reflash += 1

for device in ublox_failed:
    print(device)
print(len(ublox_failed))

for file in file_list:
    with open(file) as f:
        log = f.read()
        if "Device type: RS2_FinalReflash" in log:
            if "u-blox:1" in log:
                serial_number_index = log.find("serial-number:")
                serial_number = log[serial_number_index+14:serial_number_index+14+16]

                if serial_number in ublox_failed:
                    ublox_failed.remove(serial_number)
for device in ublox_failed:
    print(device)
print(len(ublox_failed))
