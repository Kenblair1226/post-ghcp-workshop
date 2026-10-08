"""Create an optional local checkpoint for instructor-led rescue or validation."""

import argparse
import difflib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = ("lab1-start", "lab1-review", "lab1-tests", "lab2-ui", "lab3-rpa", "instructor-solution")
STUDENT_DIRS = (
    "templates", "static", "rpa", "fixtures", "tests", "docs/evidence",
    ".github/agents", ".github/skills", ".github/prompts", ".github/instructions",
)
STUDENT_FILES = (
    ".gitignore", "app.py", "shipping.py", "requirements.txt", "requirements-lock.txt", "pytest.ini",
    "AGENTS.md", ".github/copilot-instructions.md",
    "docs/setup.md", "docs/rules.md", "docs/labs.md", "docs/worksheet.md", "docs/optional-customization.md",
    "scripts/check_environment.py", "scripts/verify_summary.py",
)
SOLUTION = ROOT / "instructor" / "solution"


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def add_express(path: Path, before: str, after: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(after) == 1:
        return
    if text.count(before) != 1:
        raise ValueError(f"Expected one checkpoint marker in {path}")
    path.write_text(text.replace(before, after), encoding="utf-8")


def create_checkpoint(stage: str, destination: Path) -> None:
    if stage not in STAGES:
        raise ValueError(f"Unknown checkpoint: {stage}")
    destination.mkdir(parents=True, exist_ok=False)
    for name in STUDENT_FILES:
        copy_file(ROOT / name, destination / name)
    for name in STUDENT_DIRS:
        for source in (ROOT / name).rglob("*"):
            if source.is_file() and "__pycache__" not in source.parts and source.suffix != ".pyc":
                copy_file(source, destination / source.relative_to(ROOT))
    copy_file(ROOT / "README.md", destination / "README.md")
    if stage != "lab1-start":
        add_express(
            destination / "shipping.py",
            'SERVICE_FEES = {"standard": 0, "registered": 20}',
            'SERVICE_FEES = {"standard": 0, "registered": 20, "express": 30}',
        )
        add_express(
            destination / "templates" / "index.html",
            "<!-- service-options -->",
            '<option value="express">快捷</option>',
        )
    if stage in {"lab1-review", "lab1-tests"}:
        diff = []
        for relative in ("shipping.py", "templates/index.html"):
            diff.extend(difflib.unified_diff(
                (ROOT / relative).read_text(encoding="utf-8").splitlines(keepends=True),
                (destination / relative).read_text(encoding="utf-8").splitlines(keepends=True),
                fromfile=f"before/{relative}", tofile=f"after/{relative}",
            ))
        (destination / "coding.diff").write_text("".join(diff), encoding="utf-8")
    if stage == "lab1-tests":
        copy_file(ROOT / "instructor" / "review-findings.md", destination / "review-findings.md")
    if stage in {"lab2-ui", "lab3-rpa", "instructor-solution"}:
        for relative in ("shipping.py", "tests/test_shipping_regression.py"):
            copy_file(SOLUTION / relative, destination / relative)
    if stage in {"lab3-rpa", "instructor-solution"}:
        for relative in ("templates/index.html", "static/styles.css", "static/app.js"):
            copy_file(SOLUTION / relative, destination / relative)
    if stage == "instructor-solution":
        copy_file(SOLUTION / "rpa" / "track_mail.py", destination / "rpa" / "track_mail.py")
    (destination / "CHECKPOINT.txt").write_text(
        f"{stage}\nOpen only this folder in VS Code. See README.md and docs/labs.md.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=STAGES, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error(f"{output} already exists; choose a new directory to protect your work")
    create_checkpoint(args.stage, output)
    print(f"Created local checkpoint: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
