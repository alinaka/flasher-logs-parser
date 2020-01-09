import glob
import os
import re
from collections import defaultdict

import matplotlib.pyplot as plt

path_to_logs = os.path.join(os.getenv("HOME"), ".local", "share", "Emlid", "Emlid Manufacturing Flash Tool", "logs")
log_pattern = os.path.join(path_to_logs, '**', '*.log')
file_list = glob.glob(log_pattern, recursive=True)
results = defaultdict(int)

for file in file_list:
    with open(file) as f:
        log = f.read()
        result_prefix = "3G_antenna result: result: "
        result_indexes = [m.start() for m in re.finditer(result_prefix, log)]

        for result_index in result_indexes:
            result = log[result_index + len(result_prefix):result_index + len(result_prefix) + 6]
            result = result.strip('"\\n')
            try:
                result = int(result)
            except ValueError:
                continue
            results[result] += 1

values = sorted(results.keys())
frequency = [results[k] for k in values]

plt.bar(values, frequency)
plt.xticks(values)
plt.ylabel('Frequency')
plt.title('3G antenna test results')
plt.savefig("out.png")
print("Saved bar chart to `out.png`")
