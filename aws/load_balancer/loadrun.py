import requests
import time


def send_requests(url, num_requests, interval):
    for _ in range(num_requests):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Request sent successfully to {url}")
            else:
                print(f"Failed to send request to {url}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending request to {url}: {e}")
        time.sleep(interval)


# Example usage
url = "http://alexey-alb-393258063.eu-central-1.elb.amazonaws.com/"
num_requests = 5000
interval = 10 / num_requests  # Interval in seconds
send_requests(url, num_requests, interval)
