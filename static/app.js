const form = document.querySelector("#quote-form");
const weight = document.querySelector("#weight");
const service = document.querySelector("#service");
const errorBox = document.querySelector("#error");
const result = document.querySelector("#result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.textContent = "";
  try {
    const response = await fetch("/api/quote", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ weight_grams: Number(weight.value), service: service.value }),
    });
    const data = await response.json();
    if (!response.ok) {
      errorBox.textContent = data.error;
      result.textContent = "";
      return;
    }
    result.textContent = `試算費用：${data.fee} 元`;
  } catch (error) {
    console.error("Quote request failed", error);
    errorBox.textContent = "無法取得報價，請確認本機伺服器是否啟動。";
    result.textContent = "";
  }
});
