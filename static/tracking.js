const form = document.querySelector("#tracking-form");
const input = document.querySelector("#mail-id");
const button = form.querySelector("button");
const result = document.querySelector('[data-testid="query-result"]');
const table = result.querySelector("table");
const message = document.querySelector("#query-message");
const rawDelay = new URLSearchParams(location.search).get("delay_ms") ?? "1200";
const delay = Number(rawDelay);

if (!/^\d+$/.test(rawDelay) || !Number.isSafeInteger(delay) || delay > 10000) {
  message.textContent = "delay_ms 必須是 0 到 10000 的整數。";
  result.dataset.state = "error";
  button.disabled = true;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const mailId = input.value.trim();
  button.disabled = true;
  table.hidden = true;
  result.dataset.state = "loading";
  message.textContent = `正在查詢 ${mailId}…`;
  try {
    const response = await fetch(`/api/tracking/${encodeURIComponent(mailId)}`);
    const data = await response.json();
    await new Promise((resolve) => setTimeout(resolve, delay));
    if (response.status === 404) {
      message.textContent = `${mailId}：查無資料`;
      result.dataset.state = "not-found";
      return;
    }
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    result.querySelector('[data-testid="mail-id"]').textContent = data.mail_id;
    result.querySelector('[data-testid="mail-service"]').textContent = data.service;
    result.querySelector('[data-testid="mail-status"]').textContent = data.status;
    table.hidden = false;
    message.textContent = `${mailId}：查詢完成`;
    result.dataset.state = "found";
  } catch (error) {
    console.error("Tracking request failed", error);
    message.textContent = `${mailId}：查詢失敗，請檢查本機伺服器。`;
    result.dataset.state = "error";
  } finally {
    button.disabled = false;
  }
});
