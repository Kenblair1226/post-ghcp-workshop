import sys
from importlib.metadata import PackageNotFoundError, version


def main() -> int:
    if sys.version_info < (3, 11):
        print("FAIL: Python 3.11+ is required.", file=sys.stderr)
        return 1
    print(f"Python: {sys.version.split()[0]}")
    for name in ("Flask", "pytest", "playwright"):
        try:
            print(f"{name}: {version(name)}")
        except PackageNotFoundError:
            print(f"FAIL: {name} is missing. Install requirements.txt.", file=sys.stderr)
            return 1
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.set_content("<title>Workshop ready</title>")
            assert page.title() == "Workshop ready"
            browser.close()
    except PlaywrightError as error:
        print(f"FAIL: Chromium cannot launch: {error}", file=sys.stderr)
        return 1
    print("PASS: Python packages and Chromium are ready. Check Copilot login and localhost separately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
