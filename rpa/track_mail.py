from playwright.sync_api import Page


def query_status(page: Page, mail_id: str, timeout_ms: int) -> dict[str, str]:
    page.get_by_label("虛構郵件編號").fill(mail_id)
    page.get_by_role("button", name="查詢", exact=True).click()
    page.wait_for_timeout(300)
    result = page.get_by_test_id("query-result")
    state = result.get_attribute("data-state")
    if state == "not-found":
        raise LookupError(f"{mail_id}：查無資料。")
    if state != "found":
        raise RuntimeError(f"{mail_id}：查詢結果尚未可用，data-state={state}。")
    cells = result.locator("tbody tr").locator("td")
    return {
        "mail_id": cells.nth(0).inner_text(),
        "status": cells.nth(1).inner_text(),
    }
