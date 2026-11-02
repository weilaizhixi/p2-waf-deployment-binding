"""Small arithmetic/table helpers adapted from the P2 analysis utilities."""
import csv
import math


def load_csv(path, fields):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != fields:
            raise ValueError("Unexpected CSV schema: " + path.name)
        rows = list(reader)
    if not rows or any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError("Empty or malformed CSV: " + path.name)
    return rows


def wilson(k, n, z=1.959963984540054):
    """Wilson 95% bounds in percent, rounded to one decimal, as in P2."""
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(100 * max(0.0, c - h), 1), round(100 * min(1.0, c + h), 1)


def md_table(fields, rows):
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(fields) + " |", "|" + "|".join(["---"] * len(fields)) + "|"]
    lines.extend("| " + " | ".join(cell(row[key]) for key in fields) + " |" for row in rows)
    return "\n".join(lines) + "\n"
