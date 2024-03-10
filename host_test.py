import requests
import threading
from tqdm import tqdm

def is_web_ui(port):
    url = f"http://62.217.120.40:{port}"
    try:
        response = requests.get(url, timeout=1)
        return response.status_code == 200 and 'text/html' in response.headers.get('content-type', '').lower()
    except (requests.ConnectionError, requests.Timeout):
        return False

def check_port(port, progress_bar, result_file):
    if is_web_ui(port):
        result = f"Port {port}: Web UI found"
        print("\n"+port)
    else:
        result = f"Port {port}: No Web UI"


    progress_bar.update(1)

    # Write the result to the file
    with open(result_file, 'a') as file:
        file.write(result + '\n')

def check_ports_for_web_ui():
    # Define the range of ports you want to check (e.g., 1 to 65535)
    start_port = 1
    end_port = 65535

    # Set the number of threads (adjust as needed)
    num_threads = 300

    result_file = "port_scan_results.txt"

    # Create threads and distribute the workload
    threads = []
    step = (end_port - start_port + 1) // num_threads

    with tqdm(total=end_port - start_port + 1, desc="Scanning ports") as pbar:
        for i in range(num_threads):
            start = start_port + i * step
            end = start + step - 1 if i < num_threads - 1 else end_port
            thread = threading.Thread(target=lambda: [check_port(port, pbar, result_file) for port in range(start, end + 1)])
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    check_ports_for_web_ui()
