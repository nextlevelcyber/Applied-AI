from pathlib import Path


try:
    import requests
except ModuleNotFoundError as exc:
    raise SystemExit(
        "requests is not installed. Install it before running Week 10 API practice."
    ) from exc


RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)

url = "https://api.github.com/zen"
response = requests.get(url, timeout=15)

output = RESULTS / "week10_public_api_response.txt"
output.write_text(
    f"URL: {url}\n"
    f"Status code: {response.status_code}\n"
    f"Response text: {response.text.strip()}\n",
    encoding="utf-8",
)

print(output.read_text(encoding="utf-8"))
