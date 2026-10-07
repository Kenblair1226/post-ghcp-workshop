from playwright.sync_api import Page


def query_status(page: Page, mail_id: str, timeout_ms: int) -> dict[str, str]:
    page.get_by_label("虛構郵件編號").fill(mail_id)
    page.get_by_role("button", name="查詢", exact=True).click()
    page.locator(
        '[data-testid="query-result"]:is([data-state="found"],'
        '[data-state="not-found"],[data-state="error"])'
    ).wait_for(state="attached", timeout=timeout_ms)
    result = page.get_by_test_id("query-result")
    state = result.get_attribute("data-state")
    if state == "not-found":
        raise LookupError(f"{mail_id}：查無資料。")
    if state == "error":
        raise RuntimeError(f"{mail_id}：查詢頁回報錯誤。")
    actual_id = result.get_by_test_id("mail-id").inner_text()
    if actual_id != mail_id:
        raise ValueError(f"{mail_id}：頁面回傳了不同的郵件編號 {actual_id}。")
    return {"mail_id": actual_id, "status": result.get_by_test_id("mail-status").inner_text()}
