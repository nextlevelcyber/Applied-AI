import json
from pathlib import Path


RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)


def mean(values):
    return sum(values) / len(values)


def words_longer_than(words, min_length):
    return [word for word in words if len(word) > min_length]


def count_first_letters(words):
    counts = {}
    for word in words:
        first = word[0].lower()
        counts[first] = counts.get(first, 0) + 1
    return counts


city_temperatures = {
    "London": [11.2, 12.4, 10.9],
    "Middlesbrough": [9.8, 10.1, 11.0],
    "Paris": [14.4, 15.2, 13.9],
}

city_averages = {
    city: round(mean(values), 2) for city, values in city_temperatures.items()
}

terms = ("python", "function", "sequence", "tuple", "list", "string", "range")

result = {
    "city_averages": city_averages,
    "long_terms": words_longer_than(list(terms), 5),
    "first_letter_counts": count_first_letters(list(terms)),
}

(RESULTS / "week3_functions_sequences_results.json").write_text(
    json.dumps(result, indent=2),
    encoding="utf-8",
)

print(json.dumps(result, indent=2))
