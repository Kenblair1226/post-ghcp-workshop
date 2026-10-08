# 郵務寄件作業小幫手｜學員教材

這是 90 分鐘 GitHub Copilot 本機開發實作。所有郵件編號與費率均為虛構，不連接正式系統。

## 從這裡開始

1. 課前依 `docs\setup.md` 完成環境準備。
2. 課中依 `docs\labs.md` 操作三個 Lab；提示詞可直接複製。
3. 以 `docs\rules.md` 判斷正確行為，以 `docs\worksheet.md` 記錄發現與成果。
4. 完成必做後，依 `docs\optional-customization.md` 選做 Copilot 客製化，不需全部完成。

| 順序 | 活動 |
|---|---|
| 開場 | 環境確認 |
| Lab 1 | Coding → Code Review → 補 Test Case 與修正 |
| Lab 2 | UI/UX 改善 |
| Lab 3 | RPA 問題查找 |
| 選做 | AGENTS.md、custom agents、skills 與 prompts |
| 收尾 | 成果展示 |

請只在 VS Code 開啟目前練習的資料夾，不開啟包含所有快照的父資料夾。`CHECKPOINT.txt` 表示目前版本；不同快照是救援起點，不需要每次都切換。

這個專案刻意留有待改善的程式與介面。**既有測試全部通過，不代表功能沒有缺陷。** 不要要求 Copilot 一次完成整場課程；依單元範圍逐步修改，並自己核對結果。

`AGENTS.md` 與 `.github` 中已預先放好可重用設定；必做 Lab 不需手動使用 custom agent 或 skill。不同 VS Code session 類型的支援範圍不同，prompt files 僅供支援的 Local Chat 使用，替代操作見選做手冊。

## 常用指令

在已設定 `$Python` 的 PowerShell 終端機中：

```powershell
& $Python app.py
& $Python -m pytest -q
& $Python -m rpa.cli --headed
```

伺服器需使用獨立終端機保持執行，網址是 `http://127.0.0.1:5050`。`$Python` 設定方式與換快照方法見環境手冊。

不要提交或提供真實客戶資料、內部憑證或正式系統截圖給 Copilot。本機執行程式不代表 Copilot 離線運作。
