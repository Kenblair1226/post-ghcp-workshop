# Workshop guidance

- 使用繁體中文解釋；保留程式識別名稱。只處理使用者指定的 Lab 或教材維護範圍。
- 課堂練習以 [業務規格](docs/rules.md) 為準。只用虛構資料與本機服務，不改需求或預期 fixture 來配合錯誤輸出。
- 起始程式刻意保留教學缺陷；不要自行修完整個專案。分析／review 任務先不修改檔案，區分已驗證結果與推測。
- 學員直接 clone repository，在根目錄開始練習，不需先打包或產生快照。
- 做學員練習時，不讀取或搜尋 `instructor/`、其他救援副本或 `dist/` 找答案，也不將它們附加給 Copilot。維護教材時才可處理講師資源；這是操作規範，不是存取隔離。
- 使用 [環境手冊](docs/setup.md) 中已確認的 Python interpreter。PowerShell 的 `$Python` 與 Bash／Zsh 的 `PYTHON` 須在各終端機設定，不假設新終端機已設定；教材指令同時提供 Windows PowerShell 與 Linux／macOS Bash／Zsh 版本，不執行全域安裝或修改系統政策。
- 在 Windows PowerShell 執行 Python 指令前，先於 repository 根目錄執行 `$Python = (Resolve-Path .\.venv\Scripts\python.exe).Path`，再使用 `& $Python` 執行 Python；每個新終端機都須先完成此設定。
- 修改程式後執行相關測試；區分刻意重現的失敗與非預期失敗。未實際執行的命令、瀏覽器操作或 Copilot 行為不得宣稱已驗證。
- 未經要求不 stage、commit、push、reset 或覆寫學員作業；切換快照使用不同資料夾。
- 本機分析也可能將上下文送給 Copilot；不提供真實客戶資料、憑證或正式系統畫面。
