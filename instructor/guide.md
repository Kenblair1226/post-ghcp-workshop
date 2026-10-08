# 講師手冊（不發給學員）

## 帶課策略

課程總長 90 分鐘，Lab 大標題標示各自配時，小節依學員進度彈性操作。不要在課堂重新講完整產品介紹，也不要現場安裝套件。學員遇到環境問題時即配對或提供救援快照。

不是比賽讓 AI 產生最多程式，而是讓學員展示「提供需求 → 審閱產物 → 用獨立證據驗證」。Copilot 的輸出不固定，評分依需求與結果，不要求與講師解答逐字一致。

## 發放教材

在 repository 根目錄執行：

```powershell
$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $Python scripts\export_materials.py --output dist\workshop
```

每個 ZIP 包含單一完整資料夾、學員 README、規格、操作手冊、作業單、程式與測試，另含 `AGENTS.md`、預定義客製化設定及選做手冊。`SHA256.json` 提供封裝檔校驗值。程式以白名單匯出，不包含 repository 根目錄的講師設計說明、`instructor`、虛擬環境或 `.git`，也不會把整個 `.github` 無差別發給學員。

| ZIP | 用途 | 預設測試 |
|---|---|---|
| `lab1-start.zip` | 正常開場；一般／掛號，尚無快捷 | 19 通過 |
| `lab1-review.zip` | Coding 卡關救援；快捷已完成，附 coding.diff | 19 通過 |
| `lab1-tests.zip` | Review 卡關救援；附已確認問題，尚未補測試 | 19 通過 |
| `lab2-ui.zip` | Lab 1 已完成，保留待改善 UI | 48 通過 |
| `lab3-rpa.zip` | 已改善 UI，但 RPA 保留故障 | 48 通過 |
| `instructor-solution.zip` | 完成版，僅供講師 | 48 通過 |

以上測試數是教材內建案例數；學員自己的完成版不必相同。將學員版與解答版放在不同的發放位置，不要要求學員開啟上層資料夾。不能只依賴 Copilot ignore 設定來隔離解答。

只在需要時發放下一個救援包，否則完整費率測試可能提前出現在學員可搜尋的其他資料夾。封裝輸出是快照；修改原始檔後需輸出到新的目錄並重新驗證，不覆寫學員作業。

## 課前走查

```powershell
& $Python scripts\check_environment.py
& $Python -m pytest instructor\tests\test_customizations.py -q
& $Python instructor\validate_materials.py --packages dist\workshop
```

自動驗證包括起始與完成版測試、已知錯誤被回歸測試攔截、RPA 的兩種故障與修復後行為，以及 UI 的鍵盤操作、窄螢幕、錯誤與重複送出。輸出 `validation.json`；畫面位於完成版 `outputs`，僅為教學資料。

`instructor\tests` 另驗證預定義設定的基本欄位、相對連結與各快照的包含範圍；不匯入學員測試，也不改變課堂的基準測試數。

預錄證據可由同一指令加 `--capture-evidence` 產生至 `docs\evidence`，之後重新封裝到新目錄才會進入學員 ZIP。證據檔不是答案，包含等待失敗的日誌／截圖及零延遲錯誤摘要。

請仍用實際教室網路、VS Code、Copilot 帳號和學員電腦進行至少一次人工試教。自動驗證不保證模型回覆速度、權限政策或 90 分鐘的人工操作配時。

## 帶課節點與講師提問

| 節點 | 講師動作 |
|---|---|
| 開場 | 確認網站、Copilot、19 個基準測試；不排除全部環境問題才開課 |
| Coding | 宣布新需求，請學員先說明修改範圍，再展示正常情境 |
| Review | 要求先不修改，附需求與差異 |
| 補測試 | 問「預期結果從哪裡來？」；確認有意義的失敗後才修正 |
| UI/UX | 落後組別換 lab2-ui，避免阻塞後續操作 |
| RPA | UI 改動不得影響 tracking 頁，保留成功與失敗情境驗收 |
| 選做 | 已完成必做者可擇一操作，不全班等待、不延長課程 |
| 收尾 | 展示一個 review 證據、一個測試、一個 RPA 根因 |

## Lab 1 解答與教學重點（45 分鐘）

### Coding

最小功能變更為在 `shipping.py` 的 `SERVICE_FEES` 增加 `"express": 30`，在試算頁增加對應 `<option>`。API 已將服務交給核心函式，不需多一份服務清單或重寫 endpoint。

要求學員解釋這條路徑：表單 → JSON → `/api/quote` → `calculate_fee` → 結果畫面。

### Review

兩個預埋缺陷：

| 缺陷 | 起始行為 | 正確行為 |
|---|---|---|
| `weight_grams >= 20000` | 拒絕最大合法值 | 20,000 合法 |
| 未檢查下限 | 0／負值被算成基本費 | 明確拒絕 |

都屬於既有缺陷，不要說是 Copilot 新增快捷時造成的。正確修正見 `solution\shipping.py`。已使用 `type(value) is int` 排除 Python 中屬於 int 子類別的 bool，這裡是刻意的精確型別檢查。

若 Copilot 在 Coding 就修好：肯定修正，要求 review 驗證並補回歸測試；不要要求它重新製造 bug。可用獨立 `lab1-review` 副本示範重現。

### Test Case

參考：`solution\tests\test_shipping_regression.py`。核心案例 21 個、API 回歸 8 個，共新增 29 個。

對 `lab1-review` 的錯誤程式執行這份測試時，應有六個失敗：最大值、零、負數、API 零、API 負數、API 最大值快捷。**收集失敗或 ImportError 不算有效的紅燈示範。**

在獨立副本放入學員的測試，先失敗再使用正確 `shipping.py` 執行通過。不要把正確函式的回傳值作為測試的 expected，也不要以 `pytest.raises(Exception)` 接受任何錯誤。

## Lab 2 解答與教學重點（15 分鐘）

參考 `solution\templates\index.html`、`solution\static\app.js` 與 `solution\static\styles.css`。

完成版使用 label／aria-describedby、欄位錯誤、可見焦點、響應式寬度、請求中停用 fieldset、finally 恢復操作與修改輸入後清除舊結果。鎖定送出中的欄位也避免使用者改值後看到舊請求結果。

UI 評量以任務完成與錯誤預防為主，不評「好不好看」的主觀喜好。顏色沿用 `--cp-*` 主題變數；無需仿製官方品牌。

若學員只改配色，追問：「重量改了，這個報價還有效嗎？斷網之後按鈕能不能再用？」

## Lab 3 解答與教學重點（18 分鐘）

參考 `solution\rpa\track_mail.py`。

| 情境 | 起始版 | 完成版 |
|---|---|---|
| 預設 1200ms 延遲 | 固定等待 300ms 後仍 loading，結束碼 1 | 等待查詢終態，再讀資料 |
| 0ms 延遲 | 常能結束，但第二欄是服務，不是狀態 | 以 `data-testid="mail-status"` 定位 |
| 延遲 1800ms、上限 200ms | 不正確的固定等待行為 | 明確逾時，ok=false |
| MISSING | 查無資料 | 與逾時區分的查無資料錯誤 |

零延遲也不能保證固定 300ms 內完成，尤其教室電腦負載高時；這正是不能以 sleep 保證 readiness 的原因。

`query-result` 的 `data-state` 是頁面狀態契約。完成版等待 found／not-found／error 的 attached 狀態；not-found 時容器沒有表格，不保證具有可見面積，因此不可一律等待 visible。資料定位以語意屬性而非欄位位置為準。

不要接受：

- 把 sleep 改成 3 秒，或停用 timeout。
- 改 fixture 讓錯誤狀態變成預期值。
- 直接讀 JSON 取代 UI 自動化，繞過本 Lab 的目標。
- 逾時後回傳空清單並宣稱成功。

## 選做客製化的帶法

學員操作見 [選做手冊](../docs/optional-customization.md)。先完成必做，剩餘時間只選一項，也可留作課後延伸；不用為選做題增加共同授課配時。

講師課前在實際 VS Code 版本與 Chat harness 中確認：

- `AGENTS.md`／共用指引有被發現，並可觀察 References 或診斷資訊；不能只憑模型自述載入成功。
- `postal-reviewer`、`postal-rpa-diagnostician` 可手動選取，工具只有讀取與搜尋。兩者不代跑命令、不編修；需要修正時由學員切回一般 Agent。
- `postal-test-design`、`postal-rpa-diagnosis` 是手動啟用的 skills，範例不包含已知缺陷解答或完整測試答案。
- `.prompt.md` 僅用於支援的 Local Chat。Agent Host 不載入 prompt files，改用 custom agent 或 skill，不要求變更組織政策。

請區分「檔案存在」「設定被發現」「實際載入」「回覆遵守」四件事。教材自動驗證只能涵蓋檔案與封裝；不能取代 VS Code / Copilot 的互動確認。文字指令與工具清單也不是安全沙箱。

參考成果：一條精簡 AGENTS.md 規則、一個保留唯讀工具範圍的新 agent、一個新增欄位的 skill 模板，或一個適用目前 session 的 prompt。未操作或使用手動附加替代者照實記錄，不影響三個 Lab 的完成判定。

## 救援與完成判定

任一階段卡住，先給提示，再指出檔案，最後才提供快照。切換時存檔、停止自己的伺服器、另開新資料夾；不要求 git reset 或覆蓋作業。

完成判定：能展示需求對照、review 證據、有效回歸測試、可操作介面，以及正確的三筆 RPA 摘要。只能分析預錄日誌者標記「完成分析，未完成執行驗收」，不列為實際修復成功。

## 參考文件

- Flask 測試：https://flask.palletsprojects.com/en/stable/testing/
- Playwright Python 定位器：https://playwright.dev/python/docs/locators
- Playwright 等待 API：https://playwright.dev/python/docs/api/class-locator#locator-wait-for
- pytest 參數化：https://docs.pytest.org/en/stable/how-to/parametrize.html
