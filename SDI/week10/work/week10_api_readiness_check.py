from pathlib import Path


try:
    import requests
except ModuleNotFoundError as exc:
    raise SystemExit(
        "requests is not installed. Install it before running Week 10 API practice."
    ) from exc


RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)

output = RESULTS / "week10_api_readiness.txt"
output.write_text(
    "requests is installed. Use this week to practise reading API documentation, "
    "checking response status codes, and saving safe evidence separate from ICA code.\n",
    encoding="utf-8",
)

print(output.read_text(encoding="utf-8"))
