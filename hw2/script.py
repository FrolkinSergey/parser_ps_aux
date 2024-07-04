import tarfile
import os
import json
from collections import Counter

archive_file_row = "access.tar.gz"
logs_folder = "logs_folder"

def extract_logs(tar_file, target_dir):
    with tarfile.open(tar_file, "r:gz") as tar:
        tar.extractall(path=target_dir)

def analyze_log(log_file):
    total_requests = 0
    http_methods_counter = Counter()
    ip_counter = Counter()
    longest_requests = []

    with open(log_file, "r") as file:
        for line in file:
            total_requests += 1
            items = line.split()
            ip = items[0]
            date = "[" + items[3][1:] + " " + items[4][:-1] + "]"
            url_row = items[10]
            url = url_row.replace('"', '')
            http_method = items[5][1:]
            http_methods_counter[http_method] += 1
            ip_counter[ip] += 1
            duration = int(items[-1])

            if len(longest_requests) < 3:
                longest_requests.append({
                    "ip": ip,
                    "date": date,
                    "method": http_method,
                    "url": url,
                    "duration": duration
                })
            else:
                longest_requests.sort(key=lambda x: x['duration'], reverse=True)
                if duration > longest_requests[2]['duration']:
                    longest_requests.pop()
                    longest_requests.append({
                        "ip": ip,
                        "date": date,
                        "method": http_method,
                        "url": url,
                        "duration": duration
                    })

    top_ips = dict(ip_counter.most_common(3))
    total_stat = dict(http_methods_counter)

    return {
        "top_ips": top_ips,
        "top_longest": longest_requests,
        "total_stat": total_stat,
        "total_requests": total_requests,
    }

def main(archive_file, target_dir):
    extract_logs(archive_file, target_dir)
    logs = [f"{target_dir}/{f}" for f in os.listdir(target_dir) if f.endswith(".log")]

    for log_file in logs:
        log_stats = analyze_log(log_file)
        output_file = log_file.replace(".log", ".json")

        with open(output_file, "w") as json_file:
            json.dump(log_stats, json_file, indent=4)
            print(f"Statistics for {log_file}:")
            print(json.dumps(log_stats, indent=4))

if __name__ == "__main__":
    main(archive_file=archive_file_row, target_dir=logs_folder)
