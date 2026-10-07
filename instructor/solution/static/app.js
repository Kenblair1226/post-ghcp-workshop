const form = document.querySelector("#quote-form");
const fields = document.querySelector("#quote-fields");
const weight = document.querySelector("#weight");
const service = document.querySelector("#service");
const errorBox = document.querySelector("#error");
const weightError = document.querySelector("#weight-error");
const serviceError = document.querySelector("#service-error");
const progress = document.querySelector("#progress");
const result = document.querySelector("#result");
const button = document.querySelector("#submit-button");
let submitting = false;

function clearErrors() {
  errorBox.textContent = "";
  weightError.textContent = "";
  serviceError.textContent = "";
  weight.removeAttribute("aria-invalid");
  service.removeAttribute("aria-invalid");
}

form.addEventListener("input", () => {
  clearErrors();
  result.textContent = "資料已變更，請重新試算。";
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (submitting) return;
  clearErrors();
  result.textContent = "尚未試算";
  const rawWeight = weight.value.trim();
  const grams = Number(rawWeight);
  if (!/^\d+$/.test(rawWeight) || !Number.isSafeInteger(grams) || grams < 1 || grams > 20000) {
    weightError.textContent = "重量錯誤：請輸入 1–20,000 的整數公克。";
    weight.setAttribute("aria-invalid", "true");
    weight.focus();
    return;
  }
  if (!["standard", "registered", "express"].includes(service.value)) {
    serviceError.textContent = "服務錯誤：請選擇一般、掛號或快捷。";
    service.setAttribute("aria-invalid", "true");
    service.focus();
    return;
  }
  submitting = true;
  fields.disabled = true;
  form.setAttribute("aria-busy", "true");
  button.textContent = "試算中…";
  progress.textContent = "正在取得試算結果。";
  try {
    const response = await fetch("/api/quote", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ weight_grams: grams, service: service.value }),
    });
    const data = await response.json();
    if (!response.ok) {
      errorBox.textContent = data.error || `試算失敗（HTTP ${response.status}）。`;
      return;
    }
    if (!Number.isInteger(data.fee) || data.fee < 0 || data.currency !== "TWD") {
      throw new Error("Unexpected quote response");
    }
    result.textContent = `試算費用：${data.fee} 元`;
  } catch (error) {
    console.error("Quote request failed", error);
    errorBox.textContent = "無法取得報價，請確認本機伺服器後再試一次。";
  } finally {
    submitting = false;
    fields.disabled = false;
    form.removeAttribute("aria-busy");
    button.textContent = "試算費用";
    progress.textContent = "";
  }
});
