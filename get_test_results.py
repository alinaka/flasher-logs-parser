import glob
import json
import operator
import os
from collections import defaultdict

path_to_logs = os.path.join(os.getenv("HOME"), ".local", "share", "Emlid", "Emlid Manufacturing Flash Tool", "logs")
logfile = max(glob.glob(os.path.join(path_to_logs, '*/RS2_LoopTesting.json')), key=os.path.getmtime)

print("Looking into {}\n".format(logfile))

failed_tests, errors, counts = [defaultdict(int) for _ in range(3)]

with open(logfile) as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        print("JSON is empty")
        exit(1)
    for result in data:
        if result["result_type"] == "ErrorOccurred":
            errors[result["error_msg"]] += 1
        elif result["result_type"] == "TestsFailed":
            for test in result["tests"]:
                for k, v in test.items():
                    if v is False:
                        failed_tests[k] += 1
        counts[result["result_type"]] += 1

for res_type, count in counts.items():
    print(res_type, count)

print()

if errors:
    print("Errors: ")
    for error, count in sorted(errors.items(), key=operator.itemgetter(1), reverse=True):
        print("> {}:".format(error), count)
if failed_tests:
    print("Tests failed: ")
    for failed, count in sorted(failed_tests.items(), key=operator.itemgetter(1), reverse=True):
        print("> {}:".format(failed), count)
