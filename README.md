# 郵務寄件作業小幫手｜GitHub Copilot Workshop

90 分鐘本機開發實作：Coding → Code Review → 補測試、UI/UX 改善，以及 RPA 問題查找。所有郵件編號與費率均為虛構，不連接正式系統。

**直接 clone 本 repository 即可開始，不需下載學員 ZIP 或執行打包工具。** 專案刻意保留教學缺陷；既有測試通過，不代表所有需求已正確實作。

## 快速開始

先安裝 Git、VS Code、Python 3.11 以上，並確認 Copilot 權限。在 PowerShell 執行：

```powershell
New-Item -ItemType Directory -Force C:\Workshop | Out-Null
Set-Location C:\Workshop
git clone https://github.com/Kenblair1226/post-ghcp-workshop.git
Set-Location .\post-ghcp-workshop
python -m venv .venv
$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $Python -m pip install -r requirements-lock.txt
& $Python -m playwright install chromium
& $Python scripts\check_environment.py
& $Python -m pytest -q
& $Python app.py
```

在 VS Code 開啟 `C:\Workshop\post-ghcp-workshop`，瀏覽器開啟 `http://127.0.0.1:5050`。伺服器保持在終端機 A 執行；在終端機 B 重新設定 `$Python` 後執行測試與 RPA。完整安裝、interpreter 選擇與疑難排解見 [環境手冊](docs/setup.md)。

若資料夾已存在，請改用新的 clone 目的地，不覆蓋原作業。clone 已包含 Git 歷史，不需要 `git init` 或 `git add .` 建立基準；以 `git --no-pager diff` 審閱自己的修改。

## 學員入口

| 順序 | 入口 |
|---|---|
| 課前 | [環境準備](docs/setup.md) |
| 課中 | [三個 Lab 的步驟與提示詞](docs/labs.md) |
| 需求判定 | [業務規格與驗收資料](docs/rules.md) |
| 成果紀錄 | [學員作業單](docs/worksheet.md) |
| 選做 | [AGENTS.md、custom agents、skills 與 prompts](docs/optional-customization.md) |

依序延續自己的程式，不要求 Copilot 一次完成整場課程。`AGENTS.md` 與 `.github` 的客製化設定已隨 clone 取得，不需另外安裝。

**練習範圍：** `instructor/` 內含講師手冊、課程設計與解答。學員與 Copilot 不讀取、搜尋或附加此目錄，也不從其他救援副本或 `dist/` 找答案。講師資源仍存在 repository 中；此限制是操作規範，不是權限或安全隔離。卡關時由講師提供提示或指定的獨立救援副本，不自行覆蓋作業。

## 常用指令

每個新的 PowerShell 終端機先設定 interpreter：

```powershell
$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $Python -m pytest -q
git --no-pager diff
& $Python -m rpa.cli --headed
```

起始 RPA 的故障是 Lab 3 的練習，不是安裝失敗。修改 Python 後，停止並重啟自己啟動的伺服器；不要終止他人的程序。

不要提交或提供真實客戶資料、內部憑證或正式系統截圖給 Copilot。本機執行程式不代表 Copilot 離線運作。
