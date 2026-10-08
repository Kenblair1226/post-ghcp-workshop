# 選做｜把好用的指令變成團隊可重用的設定

先完成三個必做 Lab，再依剩餘時間選一項操作；也可課後完成。**不延長原本 90 分鐘、不要求全部選做、不影響必做成果判定。**

這些檔案已放入 repository 與所有學員教材包，不需安裝外部 skills、額外 MCP 或付費服務。`AGENTS.md` 是專案指引，不是 custom agent；兩者用途不同。

## 先認識四種用途

| 類型 | 回答的問題 | 本教材範例 | 啟用方式 |
|---|---|---|---|
| 專案指引 | 在這個專案要遵守什麼？ | `AGENTS.md` | 支援的 Chat 依設定自動載入 |
| Custom agent | 以什麼角色、哪些工具工作？ | `.github\agents\postal-reviewer.agent.md` | 在 agent 選單手動選取 |
| Skill | 這類任務有哪些可重用步驟與資源？ | `.github\skills\postal-test-design\SKILL.md` | 本教材設為手動啟用 |
| Prompt file | 如何快速送出一次標準任務？ | `.github\prompts\postal-review.prompt.md` | 支援的 Local Chat 輸入 `/postal-review` |

另提供 `.github\instructions\tests.instructions.md`，以 `applyTo` 限定測試檔案的指引；`.github\copilot-instructions.md` 只連結共用 `AGENTS.md`，避免維護兩份重複規則。

## 確認目前 VS Code 支援哪些功能

先選擇這次使用的 Chat session target／agent harness，再開啟 **Chat: Open Customizations** 或 Chat 的 **Configure Chat**，查看指引、agents 與 skills。舊版介面可能以 **Chat: Configure Custom Agents** 等命令顯示。

依官方文件，prompt files 目前仍適用於 **Local agent**；**Agent Host sessions 不載入 prompt files**。若目前介面沒有 Local 或沒有 `/postal-review`，直接手動選 reviewer，或使用本教材的 skill，不必為了選做題切換受組織限制的設定。

`AGENTS.md` 的發現方式也依 harness 而異；Local 可檢查 `chat.useAgentsMdFile`。有 `.github\copilot-instructions.md` 作為 Copilot 的共用指引入口，但仍應實際查看 References／診斷資訊，不能只憑模型說「已讀取」。

本教材的 custom agents 與 skills 設有 `disable-model-invocation: true`，避免在必做流程自動被挑選。不要把「檔案被發現」「內容被載入」「模型真的遵守」當成同一件事。組織政策或版本不支援時，可手動附加內容練習，但須記錄為手動方式，不能宣稱原生功能已啟用。

## 選做 A：修改 AGENTS.md，觀察指引是否生效

1. 閱讀根目錄 `AGENTS.md`。指出一條有助於避免課堂誤操作的規則，不把整份手冊複製進去。
2. 在新 Chat 提問並保留回覆：

   ```text
   請只分析 shipping.py 的 calculate_fee。
   指出目前可以確認的行為，以及尚未執行驗證的事項，不要修改檔案。
   ```

3. 自行在 `AGENTS.md` 新增一條短規則：

   ```text
   分析回覆最後加上「待驗證事項：」，列出尚未實際執行的檢查。
   ```

4. 儲存後開新 Chat，送出同一個問題。查看 References 或可用的 agent 診斷資訊，再檢查回覆是否符合新增規則。
5. 比較 `git --no-pager diff -- AGENTS.md`，確認沒有改到規格或應用程式。觀察規則是否有幫助，無效或重複的規則不要持續堆疊。

**驗收：** 能說明新增規則、載入證據與回覆差異。若介面不顯示相關資訊，標記「載入情況未確認」；回覆碰巧符合格式不等於證明自動載入。

## 選做 B：使用並客製化一個唯讀 Custom Agent

1. 在 agent 選單選取 **postal-reviewer**，檢查目前工具清單只有預期的讀取／搜尋工具，沒有編修、終端機或瀏覽器執行工具。
2. 指定檔案與階段；若要審查變更，由自己取得 diff 後附加：

   ```text
   我已完成 Lab 1。請 review shipping.py 與 tests/test_shipping.py，
   依 docs/rules.md 檢查完整性及仍缺少的回歸測試。
   請只分析，沒有實際執行的結果標示待驗證。
   ```

3. 對照一般 Chat 的回覆，觀察角色、輸出欄位與工具範圍。需要重現時自己執行建議命令，將結果貼回；這個 reviewer 不代跑測試。
4. 用 VS Code 複製 `.github\agents\postal-reviewer.agent.md` 為 `postal-reviewer-my.agent.md`，把 frontmatter 的 `name` 改為 `postal-reviewer-my`。
5. 保留原本工具限制，在正文新增「每項發現附一個我應向需求提出者確認的問題」。儲存、重新選取新 agent，再用同一個問題比較。

**驗收：** 新角色可被選取、名稱不衝突、回覆符合新增要求，且沒有檔案或程式被修改。工具設定與文字限制不是安全沙箱；若工具不可用或清單不符，先回報，不為了完成選做題開放全部工具。

需要練習 RPA 角色時改選 **postal-rpa-diagnostician**，提供自己的日誌，或指定 `docs\evidence\rpa-delay.log` 與 `docs\evidence\rpa-fast.json`。角色只整理證據與驗證步驟；修正仍由學員決定。

## 選做 C：使用 Skill 與附帶模板

本教材有兩個獨立名稱的 skills：

- `postal-test-design`：將需求與 review 結論整理成測試矩陣，附 `test-matrix.md`。
- `postal-rpa-diagnosis`：整理 RPA 事實、假設與最小驗證步驟，附 `evidence-template.md`。

在支援的 Chat 輸入 `/`，選擇 `postal-test-design`：

```text
/postal-test-design 針對 shipping.py 的 calculate_fee，對照 docs/rules.md
與 tests/test_shipping.py，只列測試矩陣，不修改或執行程式。
```

檢查 skill 是否被載入、是否引用模板、預期值是否來自業務規格，而不是照抄實作。若沒有 slash 選單，可透過 Skills 管理介面找到檔案；仍無法使用時手動附加 `SKILL.md` 與模板，並記錄為替代操作。

接著在 `test-matrix.md` 新增「優先順序」欄，重新使用同一 skill，確認輸出是否反映模板變更。不要修改規格或預期 fixture。

**驗收：** 能說明 skill 的觸發方式、正文與資源模板的分工，並產生有來源的測試矩陣。辨識到 skill 不保證每次都自動使用，本教材也刻意只允許手動啟用。

## 選做 D：重用 Prompt File

此項只在支援 prompt files 的 **Local Chat** 操作，不把它當作全班共同前提。

| 指令 | 用途 | 選用角色 |
|---|---|---|
| `/postal-review` | 指定範圍的唯讀 review | postal-reviewer |
| `/postal-test-plan` | 測試矩陣設計 | ask |
| `/postal-rpa` | 日誌與摘要證據分析 | postal-rpa-diagnostician |

例如：

```text
/postal-review 已完成 Lab 1，請檢查 shipping.py 與 tests/test_shipping.py。
```

開啟 `.github\prompts\postal-review.prompt.md`，指出 frontmatter 的 `agent` 如何選擇角色，以及相對連結如何取得規格。這些 prompts 不另外宣告 `tools`，避免覆蓋唯讀 custom agent 的工具清單。

可增加一條自己的輸出要求，再執行相同指令比較。**不要直接在 reviewer prompt 改成要求修正**，因為所選角色不具備編修工具；要修改程式時明確切回一般 Agent。

Agent Host 使用者可改選 reviewer 後貼上 prompt 正文，或用 `/postal-test-design` 取代 `/postal-test-plan`。不要宣稱 `.prompt.md` 在所有 session 類型都可用。

## 帶回團隊的成果

選擇一個你實際改過的設定，記錄在 [學員作業單](worksheet.md)：

- 解決了什麼重複溝通問題？
- 在哪種 Chat session 中使用，如何確認發現與載入？
- 哪個行為已觀察到，哪些仍需人工檢查？

## 官方參考

- [Custom instructions 與 AGENTS.md](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [Custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Prompt files 與 session 相容性](https://code.visualstudio.com/docs/agent-customization/prompt-files)
