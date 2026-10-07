import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare RPA output with an independent fixture")
    parser.add_argument("actual", type=Path)
    args = parser.parse_args()
    expected_path = Path(__file__).resolve().parents[1] / "fixtures" / "expected_summary.json"
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    actual = json.loads(args.actual.read_text(encoding="utf-8"))
    if actual != expected:
        print("FAIL: Output differs from the expected fixture.")
        print("Expected:", json.dumps(expected, ensure_ascii=False))
        print("Actual:  ", json.dumps(actual, ensure_ascii=False))
        return 1
    print("PASS: All three mail IDs and statuses match the independent fixture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
