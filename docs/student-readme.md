# 郵務寄件作業小幫手｜學員教材

這是 90 分鐘 GitHub Copilot 本機開發實作。所有郵件編號與費率均為虛構，不連接正式系統。

## 從這裡開始

1. 課前依 `docs\setup.md` 完成環境準備。
2. 課中依 `docs\labs.md` 操作三個 Lab；提示詞可直接複製。
3. 以 `docs\rules.md` 判斷正確行為，以 `docs\worksheet.md` 記錄發現與成果。

| 時間 | 活動 |
|---|---|
| 00:00–00:05 | 環境確認 |
| 00:05–00:50 | Lab 1：Coding → Code Review → 補 Test Case 與修正 |
| 00:50–01:05 | Lab 2：UI/UX 改善 |
| 01:05–01:23 | Lab 3：RPA 問題查找 |
| 01:23–01:30 | 成果展示與緩衝 |

請只在 VS Code 開啟目前練習的資料夾，不開啟包含所有快照的父資料夾。`CHECKPOINT.txt` 表示目前版本；不同快照是救援起點，不需要每次都切換。

這個專案刻意留有待改善的程式與介面。**既有測試全部通過，不代表功能沒有缺陷。** 不要要求 Copilot 一次完成整場課程；依單元範圍逐步修改，並自己核對結果。

## 常用指令

在已設定 `$Python` 的 PowerShell 終端機中：

```powershell
& $Python app.py
& $Python -m pytest -q
& $Python -m rpa.cli --headed
```

伺服器需使用獨立終端機保持執行，網址是 `http://127.0.0.1:5050`。`$Python` 設定方式與換快照方法見環境手冊。

不要提交或提供真實客戶資料、內部憑證或正式系統截圖給 Copilot。本機執行程式不代表 Copilot 離線運作。
