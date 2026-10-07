import argparse
import json
import logging
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from rpa.summary import build_summary
from rpa.track_mail import query_status

LOGGER = logging.getLogger("postal-rpa")
ROOT = Path(__file__).resolve().parents[1]


def write_result(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run RPA against the local workshop only")
    parser.add_argument("--base-url", default="http://127.0.0.1:5050")
    parser.add_argument("--delay-ms", type=int, default=1200)
    parser.add_argument("--timeout-ms", type=int, default=3000)
    parser.add_argument("--mail-id", action="append", dest="mail_ids")
    parser.add_argument("--output", type=Path, default=Path("outputs") / "summary.json")
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()
    target = urlsplit(args.base_url)
    if (
        target.scheme != "http"
        or target.hostname not in {"127.0.0.1", "localhost", "::1"}
        or target.username is not None
        or target.password is not None
        or target.path not in {"", "/"}
        or target.query
        or target.fragment
    ):
        parser.error("--base-url must be a local HTTP origin")
    if not 0 <= args.delay_ms <= 10000 or args.timeout_ms <= 0:
        parser.error("delay must be 0..10000 ms and timeout must be positive")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    records = json.loads((ROOT / "fixtures" / "tracking.json").read_text(encoding="utf-8"))
    mail_ids = args.mail_ids or [record["mail_id"] for record in records]
    page = None
    current_id = "(browser startup)"
    with sync_playwright() as playwright:
        browser = None
        try:
            browser = playwright.chromium.launch(headless=not args.headed)
            page = browser.new_page()
            page.set_default_timeout(5000)
            page.goto(f"{args.base_url.rstrip('/')}/tracking?delay_ms={args.delay_ms}")
            results = []
            for current_id in mail_ids:
                LOGGER.info("Query %s delay_ms=%s timeout_ms=%s", current_id, args.delay_ms, args.timeout_ms)
                record = query_status(page, current_id, args.timeout_ms)
                LOGGER.info("Read %s status=%s", record["mail_id"], record["status"])
                results.append(record)
            write_result(args.output, build_summary(results))
            LOGGER.info("Summary written: %s", args.output)
            return 0
        except (PlaywrightError, RuntimeError, LookupError, ValueError, OSError) as error:
            LOGGER.error("Failed at %s: %s", current_id, error, exc_info=True)
            write_result(args.output, {"ok": False, "mail_id": current_id, "error": str(error)})
            if page is not None:
                try:
                    screenshot = args.output.with_suffix(".png")
                    page.screenshot(path=str(screenshot), full_page=True, timeout=3000)
                    LOGGER.info("Failure screenshot: %s", screenshot)
                except (PlaywrightError, OSError) as screenshot_error:
                    LOGGER.warning("Screenshot failed: %s", screenshot_error)
            return 1
        finally:
            if browser is not None:
                browser.close()


if __name__ == "__main__":
    raise SystemExit(main())
