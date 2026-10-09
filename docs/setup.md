# 課前環境準備（不計入 90 分鐘）

## 1. 準備帳號與工具

- Windows、Linux 或 macOS，以及 Git、VS Code、Python 3.11 以上。Linux／macOS 的 HTTP 範例另需 `curl`。本教材製作時實際使用 Windows＋Python 3.13.14；其他作業系統與版本須由講師課前確認，提供指令不代表已完成跨平台實測。
- 具有可用 Copilot 權限的帳號，且組織政策允許在 VS Code 使用 Chat 與 Agent。
- 網路可連線至組織允許的 Copilot、Python 套件來源與 Playwright 瀏覽器下載來源。
- 本教材不需 Azure、不需資料庫、不需額外 MCP，也不需 GitHub 上的 Code Review 功能授權；以 IDE Chat 做本機審查。

若網路或政策不允許安裝，請先交由 IT 協助，不要關閉憑證檢查、代理安全設定或防護軟體。

## 2. Clone repository 並安裝相依套件

直接 clone repository 至短路徑，例如 Windows 的 `C:\Workshop\post-ghcp-workshop`，或 Linux／macOS 的 `~/Workshop/post-ghcp-workshop`，不需先打包或取得 ZIP。**VS Code 只開啟此 repository 資料夾，不要開啟包含其他作業或救援副本的父資料夾。** 若同名資料夾已存在，請選新的目的地，勿覆蓋原作業。

在 VS Code 終端機依作業系統選用指令；後續範例的 `bash` 區塊同時適用 Bash 與 Zsh。

**Windows（PowerShell）**

```powershell
New-Item -ItemType Directory -Force C:\Workshop | Out-Null
Set-Location C:\Workshop
git clone https://github.com/Kenblair1226/post-ghcp-workshop.git
Set-Location .\post-ghcp-workshop
python --version
python -m venv .venv
$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $Python -m pip install -r requirements-lock.txt
& $Python -m playwright install chromium
& $Python scripts\check_environment.py
& $Python -m pytest -q
```

**Linux／macOS（Bash／Zsh）**

```bash
mkdir -p "$HOME/Workshop"
cd "$HOME/Workshop" || exit
git clone https://github.com/Kenblair1226/post-ghcp-workshop.git
cd post-ghcp-workshop || exit
python3 --version
python3 -m venv .venv
PYTHON="$(pwd)/.venv/bin/python"
"$PYTHON" -m pip install -r requirements-lock.txt
"$PYTHON" -m playwright install chromium
"$PYTHON" scripts/check_environment.py
"$PYTHON" -m pytest -q
```

環境檢查應顯示 `PASS`，未修改的 Lab 1 起始測試應為 **19 passed**；已有練習修改時數量可能不同。Chromium 下載需要時間，務必課前完成。`requirements.txt` 是直接相依套件版本；`requirements-lock.txt` 是本教材驗證時完整鎖定的安裝清單。

`instructor/` 隨 clone 保留，但包含講師解答。學員與 Copilot 不讀取、搜尋或附加此目錄，也不從其他救援副本或 `dist/` 找答案；依 `AGENTS.md` 限定每次 Lab 的工作範圍。這是操作規範，不是技術隔離。

若 `python`（Windows）或 `python3`（Linux／macOS）不存在或版本不足，使用 IT 提供的 Python 3.11 以上執行檔完整路徑。PowerShell 例如 `& "C:\Tools\Python\python.exe" -m venv .venv`；Bash／Zsh 例如 `"/opt/python/bin/python3" -m venv .venv`，路徑須改成實際位置。不要求使用 `py` launcher，也不需啟用虛擬環境，因此不需變更 PowerShell 執行原則。

Linux 若缺少 `venv` 或 Chromium 系統相依套件，請由 IT 依發行版補齊；不要自行全域安裝 Python 套件、使用 `sudo pip` 或修改系統政策。`playwright install chromium` 只下載瀏覽器，不保證系統相依套件齊全。

在 VS Code 選取 `.venv\Scripts\python.exe`（Windows）或 `.venv/bin/python`（Linux／macOS）為 Python interpreter。若沒有 Python 編輯擴充功能，仍可用以上終端機指令完成本課程。

## 3. 啟動本機網站

終端機 A（先進入 repository 根目錄）：

**Windows（PowerShell）**

```powershell
$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $Python app.py
```

**Linux／macOS（Bash／Zsh）**

```bash
PYTHON="$(pwd)/.venv/bin/python"
"$PYTHON" app.py
```

瀏覽器開啟 `http://127.0.0.1:5050`。另開終端機 B：

**Windows（PowerShell）**

```powershell
$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path
Invoke-RestMethod http://127.0.0.1:5050/health
& $Python -m pytest -q
```

**Linux／macOS（Bash／Zsh）**

```bash
PYTHON="$(pwd)/.venv/bin/python"
curl -sS http://127.0.0.1:5050/health
"$PYTHON" -m pytest -q
```

健康檢查應包含 `ok: true`、`app: postal-workshop`。終端機 A 執行伺服器時不會回到提示字元，這是正常現象；測試與 RPA 要在終端機 B 執行。Flask 的 development server 警告是預期行為，只用於本機教學，不能部署為正式服務。

如果 5050 已被其他程式使用，不要終止不明程序。PowerShell 改用 `& $Python app.py --port 5051`；Bash／Zsh 改用 `"$PYTHON" app.py --port 5051`。瀏覽器與健康檢查網址同步改為 5051，RPA 指令加 `--base-url http://127.0.0.1:5051`。

程式未啟用自動重載。**修改 Python 後，在自己啟動的伺服器終端機按 Ctrl+C，再執行 PowerShell 的 `& $Python app.py` 或 Bash／Zsh 的 `"$PYTHON" app.py`。** 前端變更則重新整理瀏覽器，必要時使用 Windows／Linux 的 Ctrl+F5 或 macOS 的 Command+Shift+R。

## 4. 確認 Copilot

在 VS Code Chat 詢問：

```text
請讀取 shipping.py，解釋 calculate_fee 的輸入與回傳值。
不要修改檔案，不要提前修復或 review。
```

確認能選取或附加專案檔案。不同版本的 VS Code／Copilot UI 名稱可能不同：分析時選可唯讀詢問的模式；需要編修時使用 Agent 或目前版本提供的編修功能。審閱終端機指令與權限提示，不要盲目允許任意命令。

## 5. 確認 Git 差異基準

clone 已包含 Git 歷史與基準，不需 `git init`、`git add .` 或先建立 commit。在 repository 根目錄：

**Windows（PowerShell）**

```powershell
git --no-pager status --short
git --no-pager diff
```

**Linux／macOS（Bash／Zsh，同樣指令）**

```bash
git --no-pager status --short
git --no-pager diff
```

剛 clone 且尚未修改時應無差異；之後用 `git --no-pager diff` 查看本次修改。**課中不要 `git add .`，也不要要求 Copilot commit、reset 或清理工作目錄。** 新增的測試檔會列在 status，內容用編輯器直接審閱。

## 選做功能的準備

clone 已包含 `AGENTS.md` 與 `.github` 內的 agents、skills、prompts 及測試指引，不必另外安裝。若使用講師提供的救援副本，請不要在複製時漏掉 `.github` 資料夾。

必做 Lab 不依賴選做功能。若要操作，先依 [選做手冊](optional-customization.md) 確認目前 Chat session 的支援範圍與設定發現情況；不為了選做題更改組織政策或開放額外工具。

## 切換救援快照

正常練習不需切換。卡關時，講師可按需建立 `lab1-review`、`lab1-tests`、`lab2-ui` 或 `lab3-rpa` 獨立資料夾。先將自己的修改存檔，停止自己啟動的伺服器，再把指定副本放到 `C:\Workshop`（Windows）或 `~/Workshop`（Linux／macOS）下的另一個資料夾；不要覆蓋原本作業，也不需 ZIP。

以 `lab2-ui` 為例，在新開的 VS Code 終端機：

**Windows（PowerShell）**

```powershell
Set-Location C:\Workshop\lab2-ui
$Python = (Resolve-Path ..\post-ghcp-workshop\.venv\Scripts\python.exe).Path
& $Python -m pytest -q
& $Python app.py
```

**Linux／macOS（Bash／Zsh）**

```bash
cd "$HOME/Workshop/lab2-ui" || exit
PYTHON="$(cd ../post-ghcp-workshop && pwd)/.venv/bin/python"
"$PYTHON" -m pytest -q
"$PYTHON" app.py
```

各副本共用原 repository 的虛擬環境，不需重新下載套件。PowerShell 的 `$Python` 與 Bash／Zsh 的 `PYTHON` 只在目前終端機設定，每個新終端機都要重新設定；Bash／Zsh 執行時使用 `"$PYTHON"`，保留引號以支援含空白的路徑。若自行採用其他位置，將上述路徑改為實際位置。救援副本不含 `.git`，不能直接使用 repository 的 diff；review 副本可讀取 `coding.diff`，其他變更用編輯器審閱。

## 常見問題

| 症狀 | 處理方式 |
|---|---|
| 套件找不到 | 確認指令使用 PowerShell 的 `& $Python` 或 Bash／Zsh 的 `"$PYTHON"`，不是系統的另一套 Python |
| Chromium executable 不存在 | PowerShell 用 `& $Python -m playwright install chromium`；Bash／Zsh 用 `"$PYTHON" -m playwright install chromium` |
| Linux 無法建立 venv 或 Chromium 缺少系統程式庫 | 請 IT 補齊發行版的 venv／瀏覽器相依套件，再重新執行環境檢查 |
| 網頁仍顯示舊的 Python 結果 | 停止並重啟自己的伺服器，確認網址與所在快照 |
| 改完 CSS 沒變化 | Windows／Linux 用 Ctrl+F5，macOS 用 Command+Shift+R，確認伺服器不是從另一個資料夾啟動 |
| API 回傳 HTTP 400 | 非法輸入可能正是預期拒絕；PowerShell 會顯示錯誤，Bash／Zsh 用 `curl -sS -i` 檢查 HTTP 狀態與回應內容 |
| RPA 失敗 | 起始版本故障是 Lab 3 的練習；課前只要求 Chromium 啟動檢查通過 |
| 無法使用瀏覽器自動化 | 兩人共用環境，或分析 `docs\evidence` 的預錄證據；後者不算執行驗收完成 |
