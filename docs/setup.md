# 課前環境準備（不計入 90 分鐘）

## 1. 準備帳號與工具

- Windows、Git、VS Code、Python 3.11 以上。本教材製作時實際使用 Windows＋Python 3.13.14；其他版本須由講師課前確認。
- 具有可用 Copilot 權限的帳號，且組織政策允許在 VS Code 使用 Chat 與 Agent。
- 網路可連線至組織允許的 Copilot、Python 套件來源與 Playwright 瀏覽器下載來源。
- 本教材不需 Azure、不需資料庫、不需額外 MCP，也不需 GitHub 上的 Code Review 功能授權；以 IDE Chat 做本機審查。

若網路或政策不允許安裝，請先交由 IT 協助，不要關閉憑證檢查、代理安全設定或防護軟體。

## 2. 解壓學員教材

解壓 `lab1-start.zip` 至短路徑，例如 `C:\Workshop`，得到 `C:\Workshop\lab1-start`。**只開啟此資料夾，不要開啟所有教材的父資料夾。**

在 VS Code 的 PowerShell 終端機：

```powershell
Set-Location C:\Workshop\lab1-start
python --version
python -m venv .venv
$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $Python -m pip install -r requirements-lock.txt
& $Python -m playwright install chromium
& $Python scripts\check_environment.py
& $Python -m pytest -q
```

環境檢查應顯示 `PASS`，起始測試應為 **19 passed**。Chromium 下載需要時間，務必課前完成。`requirements.txt` 是直接相依套件版本；`requirements-lock.txt` 是本教材驗證時完整鎖定的安裝清單。

若 `python` 不存在，使用 IT 提供的 Python 執行檔完整路徑，例如 `& "C:\Tools\Python\python.exe" -m venv .venv`。不要求使用 `py` launcher，也不執行 `Activate.ps1`，因此不需變更 PowerShell 執行原則。

在 VS Code 選取 `.venv\Scripts\python.exe` 為 Python interpreter。若沒有 Python 編輯擴充功能，仍可用以上終端機指令完成本課程。

## 3. 啟動本機網站

終端機 A：

```powershell
$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $Python app.py
```

瀏覽器開啟 `http://127.0.0.1:5050`。另開終端機 B：

```powershell
$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path
Invoke-RestMethod http://127.0.0.1:5050/health
& $Python -m pytest -q
```

健康檢查應包含 `ok: true`、`app: postal-workshop`。終端機 A 執行伺服器時不會回到提示字元，這是正常現象；測試與 RPA 要在終端機 B 執行。Flask 的 development server 警告是預期行為，只用於本機教學，不能部署為正式服務。

如果 5050 已被其他程式使用，不要終止不明程序。改用 `& $Python app.py --port 5051`，瀏覽器網址同步改為 5051，RPA 指令加 `--base-url http://127.0.0.1:5051`。

程式未啟用自動重載。**修改 Python 後，在自己啟動的伺服器終端機按 Ctrl+C，再執行 `& $Python app.py`。** 前端變更則重新整理瀏覽器，必要時使用 Ctrl+F5。

## 4. 確認 Copilot

在 VS Code Chat 詢問：

```text
請讀取 shipping.py，解釋 calculate_fee 的輸入與回傳值。
不要修改檔案，不要提前修復或 review。
```

確認能選取或附加專案檔案。不同版本的 VS Code／Copilot UI 名稱可能不同：分析時選可唯讀詢問的模式；需要編修時使用 Agent 或目前版本提供的編修功能。審閱終端機指令與權限提示，不要盲目允許任意命令。

## 5. 建立本機差異基準

僅在剛解壓、尚未修改的學員資料夾執行一次：

```powershell
git init
git add .
```

這會將起始內容放入暫存區作為比較基準，不需要 commit、Git 身分設定或遠端 repository。之後用 `git --no-pager diff` 查看本次修改。**課中不要再次 `git add .`，也不要要求 Copilot commit、reset 或清理工作目錄。** 新增的測試檔用編輯器直接審閱。

## 切換救援快照

講師會提供 `lab1-review`、`lab1-tests`、`lab2-ui` 或 `lab3-rpa`。先將自己的修改存檔，停止自己啟動的伺服器，再把快照解壓到 `C:\Workshop` 下的另一個資料夾；不要覆蓋原本作業。

以 `lab2-ui` 為例，在新開的 VS Code 終端機：

```powershell
Set-Location C:\Workshop\lab2-ui
$Python = (Resolve-Path ..\lab1-start\.venv\Scripts\python.exe).Path
& $Python -m pytest -q
& $Python app.py
```

各快照共用同一個原始虛擬環境，不需重新下載套件。`$Python` 只在目前終端機有效，每個新終端機都要重新設定。若自行採用其他解壓位置，將上述路徑改為實際位置。

## 常見問題

| 症狀 | 處理方式 |
|---|---|
| 套件找不到 | 確認指令使用 `$Python`，不是系統的另一套 Python |
| Chromium executable 不存在 | 用相同 `$Python` 執行 `-m playwright install chromium` |
| 網頁仍顯示舊的 Python 結果 | 停止並重啟自己的伺服器，確認網址與所在快照 |
| 改完 CSS 沒變化 | Ctrl+F5，確認伺服器不是從另一個資料夾啟動 |
| PowerShell 顯示 API 呼叫錯誤 | 若送出非法輸入而回傳 400，這可能正是預期拒絕，請閱讀回應內容 |
| RPA 失敗 | 起始版本故障是 Lab 3 的練習；課前只要求 Chromium 啟動檢查通過 |
| 無法使用瀏覽器自動化 | 兩人共用環境，或分析 `docs\evidence` 的預錄證據；後者不算執行驗收完成 |
