"""Offline entry point for P2 S1; never starts experiments or uses APIs."""
import argparse
import json
import sys
from pathlib import Path
import integrity
import tables
import verify


ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="check integrity and aggregate arithmetic without writing outputs")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs", help="output directory; inside the release only outputs/ is allowed")
    args = parser.parse_args()
    sealed = integrity.verify(ROOT)
    datasets, summary, checks = verify.run(ROOT)
    if not args.verify_only:
        output = args.output.resolve()
        try:
            inside = output.relative_to(ROOT)
        except ValueError:
            inside = None
        if inside is not None and (not inside.parts or inside.parts[0] != "outputs"):
            raise ValueError("Choose outputs/ or a directory outside the release; release inputs are read-only")
        if ROOT.is_relative_to(output):
            raise ValueError("Output must not be an ancestor of the release")
        output.mkdir(parents=True, exist_ok=True)
        artifacts = {"summary.json": json.dumps(summary, indent=2, ensure_ascii=False) + "\n", "verification.json": json.dumps({"integrity": sealed, "checks": checks}, indent=2, ensure_ascii=False) + "\n", **tables.render(datasets)}
        for name in artifacts:
            if (output / name).is_symlink():
                raise ValueError("Refusing symlink output: " + name)
        for name, value in artifacts.items():
            (output / name).write_text(value, encoding="utf-8", newline="\n")
        print("Wrote " + str(len(artifacts)) + " files to " + str(output))
    print("PASS: " + str(sealed["inventory_files"]) + " release files; " + str(len(checks)) + " aggregate checks")
    print("Scope: summary checks and table rendering; no raw-data or full-experiment replication.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
