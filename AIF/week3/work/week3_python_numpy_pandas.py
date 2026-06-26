from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)


def citizenship_check(age: int, country: str) -> str:
    normalized = country.strip().lower()
    if age >= 18 and normalized in {"uk", "britain", "united kingdom"}:
        return "Eligible adult citizen"
    if age >= 18:
        return "Adult non-UK citizen"
    return "Under 18"


def grade_label(mark: int) -> str:
    if mark >= 70:
        return "Excellent"
    if mark >= 60:
        return "Very good"
    if mark >= 50:
        return "Satisfactory"
    return "Needs improvement"


def sphere_volume(radius: float) -> float:
    return 4 / 3 * math.pi * radius**3


def cylinder_volume(radius: float, height: float) -> float:
    return math.pi * radius**2 * height


def cone_volume(radius: float, height: float) -> float:
    return math.pi * radius**2 * height / 3


def numpy_demo() -> dict:
    matrix = np.array([[2, 1, 1], [1, 3, 2], [1, 0, 0]], dtype=float)
    vector = np.array([4, 5, 6], dtype=float)
    solution = np.linalg.solve(matrix, vector)
    return {
        "matrix": matrix.tolist(),
        "determinant": round(float(np.linalg.det(matrix)), 4),
        "eigenvalues": [round(float(x), 4) for x in np.linalg.eigvals(matrix)],
        "linear_system_solution": [round(float(x), 4) for x in solution],
    }


def pandas_demo() -> dict:
    df = pd.DataFrame(
        {
            "student": ["A", "B", "C", "D", "E"],
            "python": [72, 65, 48, 81, 56],
            "math": [68, 71, 52, 77, 59],
        }
    )
    df["average"] = df[["python", "math"]].mean(axis=1)
    df["label"] = df["average"].round().astype(int).map(grade_label)
    df.to_csv(RESULTS / "week3_student_marks.csv", index=False)
    return {
        "class_average": round(float(df["average"].mean()), 2),
        "top_student": str(df.sort_values("average", ascending=False).iloc[0]["student"]),
        "output_file": "week3_student_marks.csv",
    }


def main() -> None:
    results = {
        "control_flow_examples": [
            citizenship_check(21, "UK"),
            citizenship_check(22, "Singapore"),
            citizenship_check(16, "UK"),
        ],
        "grade_examples": {str(mark): grade_label(mark) for mark in [45, 55, 65, 75]},
        "volume_functions": {
            "sphere_radius_3": round(sphere_volume(3), 3),
            "cylinder_radius_2_height_5": round(cylinder_volume(2, 5), 3),
            "cone_radius_2_height_5": round(cone_volume(2, 5), 3),
        },
        "numpy": numpy_demo(),
        "pandas": pandas_demo(),
    }
    (RESULTS / "week3_python_numpy_pandas_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
