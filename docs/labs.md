# 學員實作手冊

總長 90 分鐘。每次交給 Copilot 的任務都包含「目標、檔案、限制、驗收方式」。以下提示詞可貼入 Chat；必要時使用檔案附加功能，不假定 Copilot 自動取得終端機或瀏覽器內容。

所有命令均在目前教材資料夾執行，`$Python` 與兩個終端機的設定見 `setup.md`。**不將自己的程式、日誌或截圖上傳到未經組織核可的外部服務。**

## 00:00–00:05｜開場

1. 終端機 A 啟動 `& $Python app.py`，開啟 `http://127.0.0.1:5050`。
2. 終端機 B 執行 `& $Python -m pytest -q`，起始版本應為 19 passed。
3. 確認 VS Code 只開啟目前學員資料夾，讀取 `rules.md`。

## Lab 1｜Coding → Code Review → 補 Test Case（45 分鐘）

起點：`lab1-start`。全程延續自己剛修改的功能，不需切換三個專案。

### A. Coding（18 分鐘）

**目標：** 新增快捷服務，讓 1,000 公克快捷報價為 90 元。

先閱讀 `shipping.py`、`app.py`、`templates\index.html` 與 `static\app.js`，找出計算、API 與畫面的關係，再貼：

```text
請閱讀 docs/rules.md、shipping.py、app.py、templates/index.html 與 static/app.js。
任務：新增 express 快捷服務，加價 30 元，和一般、掛號三選一。
請先列出需要修改的檔案，再完成核心計算與網頁選單串接。
保留既有 API 格式和一般、掛號功能，不新增套件或重寫專案。
不要修改 docs/rules.md，也不要 git add、commit、reset。
如果發現其他缺陷請記錄；必要的連帶修正請解釋原因。
執行既有測試，並核對 1000 公克的一般 60 元、掛號 80 元、快捷 90 元。
```

審閱差異：

```powershell
git --no-pager diff -- shipping.py app.py templates static
& $Python -m pytest -q
```

重啟自己的 Flask 伺服器，重新整理網頁，測試三種服務。另直接呼叫 API：

```powershell
Invoke-RestMethod http://127.0.0.1:5050/api/quote -Method Post -ContentType "application/json" -Body '{"weight_grams":1000,"service":"express"}'
```

**檢查點：** 回傳 `fee: 90`；一般與掛號仍正常；說明哪個檔案負責顯示、哪個檔案負責計算。此時不要求完整邊界覆蓋。

卡關：先附加指定檔案，請 Copilot 縮小修改範圍。超過 2 分鐘仍無進展，由講師提供 `lab1-review` 接續；其中 `coding.diff` 可當作待 review 的差異。

### B. Code Review（12 分鐘）

**目標：** 檢查剛完成的功能與相關既有路徑，取得可驗證的結論。

開新 Chat 或切換至唯讀分析，附上 `rules.md`、程式差異與相關檔案：

```text
請 review 本次快捷服務變更，以及直接相關的既有費率與輸入驗證邏輯。
只分析，先不要修改檔案。不要只看 diff 而忽略被呼叫的既有程式。
依 docs/rules.md 檢查功能完整性、上下限、非法輸入與前後端一致性。
不需要風格或命名建議，也不要為了湊數編造問題。
每項發現提供：檔案與行號、觸發輸入、預期／實際結果、影響、修正方向。
區分本次引入與既有缺陷，區分已重現與推測。
能執行時使用最小範例重現，最後列出應補的回歸測試。
不要 git add、commit、reset 或修改業務規格。
```

不要直接複製結論到作業單。挑一項用終端機重現：

```powershell
& $Python -c "from shipping import calculate_fee; print(calculate_fee(20000, 'standard'))"
```

將結果對照需求表，記錄「預期、實際、原因」。若這個輸入已正確，再檢查另一個需求邊界；沒有缺陷時記錄已通過與缺少的測試，不要求硬湊問題。

**檢查點：** 至少有一項經人工核對的 review 結論；尚未修復的問題有可重現輸入。需要提示時使用：

```text
請逐一核對重量最小值、最大值，以及前後一個單位；不要只驗證正常輸入。
```

若 Coding 已經修好所有問題，講師可提供獨立的 review 練習副本，保留自己的成果不動。

### C. 補 Test Case 與修正（15 分鐘）

**目標：** 將 review 發現變成測試，不只追求全綠。

```text
請閱讀 docs/rules.md、tests/test_shipping.py 與剛才的 review 結論。
先建立需求／問題／測試對照表，再新增 tests/test_shipping_regression.py。
第一輪只修改測試，不修改實作。
優先覆蓋已重現缺陷、重量 1/1000/1001/2000/20000、
0/負數/20001/非整數/布林值、三種服務及未知服務。
預期值由需求表推導，不可以被測函式計算自己的預期結果。
同類案例使用 pytest 參數化。不要修改規格或放寬斷言來通過。
執行測試，區分實作缺陷與測試寫錯造成的失敗。
```

```powershell
& $Python -m pytest tests\test_shipping_regression.py -q
```

查看失敗的輸入與斷言，確認符合 review 發現，再貼：

```text
根據已確認的失敗案例，最小幅度修正實作。
不修改需求、不放寬測試斷言，保留快捷與既有服務。
執行全部測試，說明每個修正對應哪項 review 發現。
```

```powershell
& $Python -m pytest -q
```

重啟伺服器後，直接送出非法重量，應收到 HTTP 400，而非報價：

```powershell
Invoke-RestMethod http://127.0.0.1:5050/api/quote -Method Post -ContentType "application/json" -Body '{"weight_grams":0,"service":"standard"}'
```

PowerShell 對 HTTP 400 顯示錯誤是預期現象；檢查訊息有明確拒絕重量。學員新增測試數量可不同，不要求與講師相同；要求需求覆蓋與正確斷言。

**完成標準：** 功能可用；有 review 證據；至少一個新測試曾抓到錯誤並在修正後通過。若所有缺陷早已修正，由講師協助在獨立錯誤副本執行新測試證明效力，不要刻意破壞自己的正確版本。

## Lab 2｜UI/UX 改善（15 分鐘）

起點：自己的 Lab 1 成果，或 `lab2-ui`。本單元不改費率規則。

先用瀏覽器操作一次，指出目前最容易誤解或誤用的地方。切換到 375px 窄螢幕，觀察是否需要左右捲動。

```text
請改善 templates/index.html、static/styles.css 與 static/app.js。
使用者是反覆處理寄件試算的內部作業人員，目標是清楚、防呆，不是只換顏色。
保留現有 API、DOM id 與主題變數，不新增 UI 框架，也不改 RPA 查詢頁。
必做：
1. 重量有 label、單位、範圍；錯誤顯示在欄位旁並與欄位建立無障礙關聯。
2. Tab、Enter 可完成試算，焦點清楚。
3. 375px 寬度沒有水平捲動。
4. 請求中防止重複送出，HTTP 或網路失敗後仍可再操作。
5. 修改輸入後清除或標示舊報價失效，避免誤用。
不得改變費率需求；完成後列出需要我在瀏覽器人工確認的項目。
```

**五分鐘人工驗收：**

| 操作 | 預期 |
|---|---|
| 不用滑鼠，以 Tab 移動並 Enter 送出 | 焦點清楚，可完成合法試算 |
| 空白或輸入 0 | 欄位旁有可理解的錯誤，不只變色 |
| 1000 公克、快捷 | 顯示 90 元 |
| 將重量改為 1001 | 舊報價清除或失效，重新試算為 100 元 |
| DevTools 設為 375px 寬度 | 主要頁面不產生水平捲動 |
| DevTools Network 設 Offline 後送出 | 清楚提示失敗，按鈕恢復；恢復網路後可再試 |

要觀察「送出中」，可在瀏覽器 DevTools 使用慢速網路模擬，再連按兩次；Network 面板不應出現重複的報價請求。完成後關閉離線／限速設定。

```powershell
& $Python -m pytest -q
```

**檢查點：** 說明一項降低操作錯誤的設計；費率測試仍通過。沒有 Copilot 瀏覽器工具也能完成，提供畫面時只用這個教學系統的截圖。

## Lab 3｜RPA 問題查找（18 分鐘）

起點：自己的專案，或 `lab3-rpa`。只改 `rpa\track_mail.py`，不修改查詢頁、fixtures 或預期結果。

### 1. 重現與保留證據（4 分鐘）

確認本機伺服器仍在執行。終端機 B：

```powershell
New-Item -ItemType Directory -Force outputs | Out-Null
& $Python -m rpa.cli --headed --output outputs\delay.json 2> outputs\delay.log
$LASTEXITCODE
Get-Content outputs\delay.log
Get-Content -Encoding utf8 outputs\delay.json
```

起始版本預期失敗，結束碼 1，輸出 `ok: false`，並儲存 `outputs\delay.png`。讀日誌，確認是在哪個編號與畫面狀態失敗。

再執行零延遲診斷：

```powershell
& $Python -m rpa.cli --delay-ms 0 --output outputs\fast.json
& $Python scripts\verify_summary.py outputs\fast.json
```

通常腳本能結束，但比對會失敗。若機器忙碌使零延遲仍未在固定等待內完成，保留此證據並先修等待問題，再查資料定位；不要把零延遲當成保證或修復。

### 2. 定位與修正（8 分鐘）

附加 `rpa\track_mail.py`、日誌、`templates\tracking.html`、`static\tracking.js` 與相關 fixture：

```text
請診斷本機 RPA，先不要修改。
根據 rpa/track_mail.py、失敗日誌、查詢頁 DOM 與 fixtures，
分別解釋「查詢尚未完成」和「腳本跑完但摘要不符」的可能原因。
列出事實、假設與最小驗證步驟，不把結束碼 0 當成資料正確。
```

核對分析後：

```text
請只以最小變更修正 rpa/track_mail.py 的等待條件與欄位定位。
不要增加固定 sleep、無限重試、吞掉例外或以空白結果冒充成功。
保留 query_status 的介面與既有 CLI 輸出格式，等待上限使用 timeout_ms。
區分查無資料、逾時與頁面錯誤，並核對回傳郵件編號。
不要修改查詢頁、fixtures、預期結果或 requirements。
```

### 3. 成功與失敗驗收（6 分鐘）

不同延遲都要輸出相同的正確三筆摘要：

```powershell
& $Python -m rpa.cli --delay-ms 1200 --output outputs\normal.json
& $Python scripts\verify_summary.py outputs\normal.json
& $Python -m rpa.cli --delay-ms 1800 --output outputs\slow.json
& $Python scripts\verify_summary.py outputs\slow.json
```

接著故意觸發失敗：

```powershell
& $Python -m rpa.cli --delay-ms 1800 --timeout-ms 200 --output outputs\timeout.json
$LASTEXITCODE
Get-Content -Encoding utf8 outputs\timeout.json
& $Python -m rpa.cli --mail-id MISSING --delay-ms 0 --output outputs\missing.json
$LASTEXITCODE
Get-Content -Encoding utf8 outputs\missing.json
& $Python -m pytest tests\test_summary.py -q
```

前兩個 RPA 失敗情境均應結束碼 1、`ok: false`，原因分別是逾時與查無資料。摘要單元測試通過只能證明資料整理，不等於瀏覽器等待與定位正確。

**檢查點：** 能說明根因與修正，而不是只說「Copilot 幫我改好了」。無法使用瀏覽器者分析 `docs\evidence`，並在作業單標記尚未執行驗收。

## 01:23–01:30｜收尾

保留四分鐘緩衝、三分鐘展示。完成 `worksheet.md`，分享一項 review 證據、一個抓到錯誤的測試，以及一個 RPA 根因。不需提交真實資料、不需推送 GitHub。
