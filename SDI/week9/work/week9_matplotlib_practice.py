import os
from pathlib import Path


RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(RESULTS / ".matplotlib_cache"))

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ModuleNotFoundError as exc:
    raise SystemExit(
        "matplotlib is not installed. Install it before running Week 9 practice."
    ) from exc

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
ticket_counts = [18, 21, 17, 24, 22, 19]

plt.figure(figsize=(8, 4.5))
plt.plot(months, ticket_counts, marker="o")
plt.title("Support Tickets By Month")
plt.xlabel("Month")
plt.ylabel("Ticket count")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RESULTS / "week9_line_chart.png", dpi=160)
plt.close()

categories = ["Setup", "Python", "Database", "API"]
hours = [8.5, 14.0, 11.5, 9.0]

plt.figure(figsize=(8, 4.5))
plt.bar(categories, hours)
plt.title("Practice Hours By Topic")
plt.xlabel("Topic")
plt.ylabel("Hours")
plt.tight_layout()
plt.savefig(RESULTS / "week9_bar_chart.png", dpi=160)
plt.close()

print("Created Week 9 Matplotlib chart outputs.")
