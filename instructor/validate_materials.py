"""Validate repository materials in local copies without altering learner source files."""

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from playwright.sync_api import expect, sync_playwright
from checkpoints import STAGES, create_checkpoint

ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "PYTHONUTF8": "1"}


def run(stage: Path, *args: str, expected_code: int = 0) -> subprocess.CompletedProcess:
    result = subprocess.run(
        [sys.executable, *args], cwd=stage, env=ENV,
        capture_output=True, text=True, encoding="utf-8", timeout=90,
    )
    if result.returncode != expected_code:
        raise AssertionError(f"{stage.name}: {args}\n{result.stdout}\n{result.stderr}")
    return result


@contextmanager
def server(stage: Path):
    code = (
        "from app import create_app; from werkzeug.serving import make_server; "
        "server=make_server('127.0.0.1',0,create_app()); "
        "print(server.server_port,flush=True); server.serve_forever()"
    )
    logs = stage / "outputs"
    logs.mkdir(exist_ok=True)
    with (logs / "server.log").open("w", encoding="utf-8") as error_log:
        process = subprocess.Popen(
            [sys.executable, "-u", "-c", code], cwd=stage, env=ENV,
            stdout=subprocess.PIPE, stderr=error_log, text=True, encoding="utf-8",
        )
        try:
            port = process.stdout.readline().strip()
            if not port.isdigit():
                raise RuntimeError(f"Server did not start; see {logs / 'server.log'}")
            origin = f"http://127.0.0.1:{port}"
            with urlopen(f"{origin}/health", timeout=5) as response:
                assert json.load(response) == {"ok": True, "app": "postal-workshop"}
            yield origin
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            process.stdout.close()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_ui(stage: Path, origin: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1100, "height": 850})
            page.goto(origin)
            weight = page.get_by_label("包裹重量（公克）")
            weight.focus()
            weight.fill("1000")
            page.keyboard.press("Tab")
            expect(page.locator("#service")).to_be_focused()
            page.locator("#service").select_option("express")
            page.keyboard.press("Tab")
            expect(page.locator("#submit-button")).to_be_focused()
            page.keyboard.press("Enter")
            expect(page.locator("#result")).to_have_text("試算費用：90 元")
            weight.fill("1001")
            expect(page.locator("#result")).to_contain_text("重新試算")
            weight.fill("0")
            page.locator("#submit-button").click()
            expect(weight).to_have_attribute("aria-invalid", "true")
            expect(page.locator("#weight-error")).to_contain_text("1–20,000")
            weight.fill("1000")
            page.locator("#submit-button").click()
            expect(page.locator("#result")).to_have_text("試算費用：90 元")
            page.screenshot(path=str(stage / "outputs" / "solution-desktop.png"), full_page=True)
            page.set_viewport_size({"width": 375, "height": 812})
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            page.screenshot(path=str(stage / "outputs" / "solution-mobile.png"), full_page=True)
            page.goto(f"{origin}/?scoutTheme=dark")
            expect(page.locator("html")).to_have_attribute("data-theme", "dark")
            page.screenshot(path=str(stage / "outputs" / "solution-dark.png"), full_page=True)
            weight.fill("1000")
            requests = []

            def delayed_quote(route):
                requests.append(route.request)
                time.sleep(0.15)
                route.fulfill(status=200, json={"fee": 60, "currency": "TWD"})

            page.route("**/api/quote", delayed_quote)
            busy = page.evaluate("""() => {
                const form = document.querySelector('#quote-form');
                form.requestSubmit(); form.requestSubmit();
                return document.querySelector('#quote-fields').disabled;
            }""")
            assert busy
            expect(page.locator("#result")).to_have_text("試算費用：60 元")
            expect(page.locator("#submit-button")).to_be_enabled()
            assert len(requests) == 1
            page.unroute("**/api/quote", delayed_quote)
            page.route("**/api/quote", lambda route: route.fulfill(status=500, json={"error": "模擬伺服器錯誤"}))
            page.locator("#submit-button").click()
            expect(page.locator("#error")).to_have_text("模擬伺服器錯誤")
            expect(page.locator("#submit-button")).to_be_enabled()
            page.unroute("**/api/quote")
            page.route("**/api/quote", lambda route: route.abort())
            page.locator("#submit-button").click()
            expect(page.locator("#error")).to_contain_text("無法取得報價")
            expect(page.locator("#submit-button")).to_be_enabled()
            page.unroute("**/api/quote")
            page.locator("#submit-button").click()
            expect(page.locator("#result")).to_have_text("試算費用：60 元")
        finally:
            browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--capture-evidence", action="store_true")
    args = parser.parse_args()
    output_dir = args.output.resolve()
    if output_dir.exists():
        parser.error(f"{output_dir} already exists; choose a new directory to protect your work")
    output_dir.mkdir(parents=True)
    report = {}
    for stage_name in STAGES:
        stage = output_dir / stage_name
        create_checkpoint(stage_name, stage)
        (stage / "outputs").mkdir(exist_ok=True)
        result = run(stage, "-m", "pytest", "-q")
        report[stage_name] = result.stdout.strip()
        assert not (stage / "instructor").exists()
        assert not (stage / ".venv").exists()
        print(f"PASS unit tests in local checkpoint: {stage_name}")

    review = output_dir / "lab1-review"
    xml_path = review / "outputs" / "regression.xml"
    run(
        review, "-m", "pytest", "-q", "-c", str(review / "pytest.ini"),
        str(ROOT / "instructor" / "solution" / "tests" / "test_shipping_regression.py"),
        f"--junitxml={xml_path}", expected_code=1,
    )
    tree = ET.parse(xml_path)
    assert len(tree.findall(".//failure")) == 6
    assert not tree.findall(".//error")
    report["regression_proof"] = "Six assertion failures on the known-defective review checkpoint."
    print("PASS regression tests detect the six expected failures")

    starter = output_dir / "lab1-start"
    with server(starter) as origin:
        failure = run(
            starter, "-m", "rpa.cli", "--base-url", origin,
            "--output", "outputs/delay.json", expected_code=1,
        )
        delay = read_json(starter / "outputs" / "delay.json")
        assert delay["ok"] is False and "loading" in delay["error"]
        fast = run(
            starter, "-m", "rpa.cli", "--base-url", origin, "--delay-ms", "0",
            "--output", "outputs/fast.json",
        )
        actual = read_json(starter / "outputs" / "fast.json")
        expected = read_json(starter / "fixtures" / "expected_summary.json")
        assert actual["ok"] is True and actual != expected
        assert actual["records"][0]["status"] == "掛號"
        comparison = run(starter, "scripts/verify_summary.py", "outputs/fast.json", expected_code=1)
        if args.capture_evidence:
            evidence = ROOT / "docs" / "evidence"
            evidence.mkdir(exist_ok=True)
            (evidence / "rpa-delay.log").write_text(
                failure.stderr.replace(str(starter), "<workshop>"), encoding="utf-8",
            )
            (evidence / "rpa-fast.log").write_text(
                fast.stderr.replace(str(starter), "<workshop>") + "\n" + comparison.stdout,
                encoding="utf-8",
            )
            for source, name in (("delay.png", "rpa-delay.png"), ("fast.json", "rpa-fast.json")):
                shutil.copy2(starter / "outputs" / source, evidence / name)
    report["starter_rpa"] = "Loading failure and incorrect-column summary reproduced."
    print("PASS both intentionally broken RPA scenarios reproduced")

    solution = output_dir / "instructor-solution"
    expected = read_json(solution / "fixtures" / "expected_summary.json")
    with server(solution) as origin:
        for delay_ms in (1200, 1800):
            output = f"outputs/success-{delay_ms}.json"
            run(solution, "-m", "rpa.cli", "--base-url", origin, "--delay-ms", str(delay_ms), "--output", output)
            assert read_json(solution / output) == expected
            run(solution, "scripts/verify_summary.py", output)
        run(
            solution, "-m", "rpa.cli", "--base-url", origin, "--delay-ms", "1800",
            "--timeout-ms", "200", "--output", "outputs/timeout.json", expected_code=1,
        )
        timeout = read_json(solution / "outputs" / "timeout.json")
        assert timeout["ok"] is False and "Timeout" in timeout["error"]
        run(
            solution, "-m", "rpa.cli", "--base-url", origin, "--delay-ms", "0",
            "--mail-id", "MISSING", "--output", "outputs/missing.json", expected_code=1,
        )
        missing = read_json(solution / "outputs" / "missing.json")
        assert missing["ok"] is False and "查無資料" in missing["error"]
        check_ui(solution, origin)
    report["solution_rpa"] = "Both delays match fixtures; timeout and missing ID fail explicitly."
    report["solution_ui"] = "Keyboard, mobile, themes, stale results, validation, duplicate submits and recovery passed."
    (output_dir / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PASS solution RPA and UI; validation.json written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
