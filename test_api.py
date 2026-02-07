
import requests
import json
import sys

def test_endpoint(port):
    url = f"http://127.0.0.1:{port}/students/batches/25"
    print(f"Testing {url}...")
    try:
        response = requests.get(url, timeout=2)
        print(f"Status Code: {response.status_code}")
        try:
            data = response.json()
            print("Response JSON (First 2 items):")
            print(json.dumps(data['data'][:2] if 'data' in data else data[:2], indent=2))
            print(f"Total items: {len(data['data']) if 'data' in data else len(data)}")
        except:
            print("Response Text:", response.text[:200])
    except Exception as e:
        print(f"Error accessing port {port}: {e}")
    print("-" * 20)

if __name__ == "__main__":
    test_endpoint(8000)
    test_endpoint(9000)
