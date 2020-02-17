import argparse
import glob
import json
import operator
import os
import psutil
from collections import defaultdict
from datetime import datetime


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--devtype", default="RS2_LoopTesting")
    argparser.add_argument("--home", default=os.getenv("HOME"))
    args = argparser.parse_args()

    path_to_logs = os.path.join(args.home, ".local", "share", "Emlid", "Emlid Manufacturing Flash Tool", "logs")
    logfile = max(glob.glob(os.path.join(path_to_logs, '*/{}.json'.format(args.devtype))), key=os.path.getmtime)

    print("Looking into {}".format(logfile))
    last_logfile = max(glob.glob(os.path.join(path_to_logs, '*', 'devices', '*.log')), key=os.path.getmtime)
    print("Last modified logfile is {}\n".format(last_logfile))

    for proc in psutil.process_iter():
        if "Emlid" in proc.name():
            start_time = datetime.fromtimestamp(proc.create_time())
            print("Flasher session is running {}".format(datetime.now() - start_time))
            break
    else:
        print("Flasher is no longer running")
    print()

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
                            failed_tests[test["name"]+ ' ' + result["port_path"]] += 1
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


if __name__ == "__main__":
    main()
