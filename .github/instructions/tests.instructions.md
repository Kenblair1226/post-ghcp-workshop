---
description: 編寫郵務 Lab 的 pytest 測試時使用。
applyTo: "tests/**/*.py"
---

# Test authoring

- 預期結果由業務規格或獨立 fixture 推導，不呼叫被測函式計算 expected。
- 同類邊界使用 pytest 參數化；驗證具體例外型別或 API 狀態與內容，不以任意 Exception 代表正確拒絕。
- 補測試階段先保留實作，以失敗案例確認缺陷；未獲修正指示前不修改產品程式。
- 不為了全綠而移除案例、放寬斷言或改寫業務規格。
