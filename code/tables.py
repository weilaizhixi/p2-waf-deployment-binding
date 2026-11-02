"""Render only the six whitelisted CSV summaries as Markdown tables."""
from utils import md_table
from verify import SCHEMAS


def render(datasets):
    return {"TABLE_" + name.removesuffix(".csv") + ".md": md_table(SCHEMAS[name], rows) for name, rows in datasets.items()}
