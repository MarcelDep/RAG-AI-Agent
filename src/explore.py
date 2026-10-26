import requests

url = "https://api2.openreview.net/notes/search"
params = {
    "invitation": "ICLR.cc/2024/Conference/-/Submission",
    "term": "transformer",
    "limit": 5,
    "offset": 0,
}

for offset in (0, 5):
    params["offset"] = offset
    response = requests.get(url, params=params, timeout=30)
    print(f"\nOffset {offset}: HTTP {response.status_code}")

    response.raise_for_status()
    data = response.json()

    print("Liczba wyników:", len(data.get("notes", [])))
    print("Łączna liczba:", data.get("count"))

    for note in data.get("notes", []):
        print("-", note.get("content", {}).get("title", {}).get("value", "(brak tytułu)"))