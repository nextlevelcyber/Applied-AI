from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

source = RESULTS_DIR / "cars_exercise.txt"
filtered = RESULTS_DIR / "cars_without_ford.txt"
word_counts = RESULTS_DIR / "word_counts.txt"

source.write_text(
    "\n".join(
        [
            "Hyundai Tucson 2006",
            "Mitsubishi Outlander 2015",
            "Ford Focus 1998",
            "Ford Fiesta 2012",
            "Toyota Corolla 2019",
        ]
    )
    + "\n",
    encoding="utf-8",
)

lines = source.read_text(encoding="utf-8").splitlines()
kept_lines = [line for line in lines if "ford" not in line.lower()]
filtered.write_text("\n".join(kept_lines) + "\n", encoding="utf-8")

words = []
for line in lines:
    words.extend(word.lower() for word in line.split())

counts = Counter(words)
word_counts.write_text(
    "\n".join(f"{word}: {count}" for word, count in sorted(counts.items()))
    + "\n",
    encoding="utf-8",
)

print(f"Created {source}")
print(f"Created {filtered}")
print(f"Created {word_counts}")
