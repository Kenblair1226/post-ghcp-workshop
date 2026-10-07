import json
from pathlib import Path

import pytest

from rpa.summary import build_summary

ROOT = Path(__file__).resolve().parents[1]


def test_summary_matches_fixture():
    records = json.loads((ROOT / "fixtures" / "tracking.json").read_text(encoding="utf-8"))
    expected = json.loads((ROOT / "fixtures" / "expected_summary.json").read_text(encoding="utf-8"))
    assert build_summary(records) == expected


@pytest.mark.parametrize(
    "records",
    [
        [{"mail_id": "", "status": "已投遞"}],
        [{"mail_id": "DEMO0001", "status": ""}],
        [{"mail_id": "DEMO0001"}],
        [{"mail_id": "DEMO0001", "status": "已投遞"}] * 2,
    ],
)
def test_reject_incomplete_or_duplicate_records(records):
    with pytest.raises(ValueError):
        build_summary(records)
