# 國小素養試題本機技能 Local 0.1.2

源自 Gemini V6.1，保留教材盤點、官方查證、素養命題、詳解、評分與同教材重出流程，改為本機 Word／PDF 交付。入口：[SKILL.md](SKILL.md)。

跨筆電完整流程見[Codex安裝](references/install-codex.md)或[OpenCode安裝](references/install-opencode.md)。

## 安裝

解壓後保留整個 elementary-competency-assessment-local 資料夾，不要只複製主檔。在 PowerShell 進入本資料夾：

~~~powershell
# 先看位置；不寫入
& .\scripts\install.ps1 -Scope Project -ProjectRoot <你的工作資料夾> -WhatIf
# 專案安裝
& .\scripts\install.ps1 -Scope Project -ProjectRoot <你的工作資料夾>
# 或使用者全域安裝；擇一，避免同名副本
& .\scripts\install.ps1 -Scope User
~~~

Project 目標為 <專案>/.agents/skills/elementary-competency-assessment-local；User 為 ~/.agents/skills/elementary-competency-assessment-local。安裝器逐檔比對 SHA-256，拒絕覆寫同名資料夾。安裝不會加入 Python 套件、變更 Agent／模型設定或建立網路帳號。

上述共用相容位置已於 2026-10-24 核對：
[Codex 官方](https://learn.chatgpt.com/docs/build-skills)、
[OpenCode V1 官方](https://docs.opencode.ai/docs/skills/)、
[OpenCode V2 官方](https://opencode.ai/v2/docs/skills)。
歷史實測包含Codex CLI0.154.0及OpenCode1.18.18；正式案例與不同版本的測試條件見https://t92016.github.io/elementary-competency-assessment-skill/verification.html。其他電腦仍須重新驗收。

本輪OpenCode受測免費模型的正式命題品質未通過；原生載入、搜尋及原創小型母稿四檔技術測試已驗證。這不是所有OpenCode模型的結論，完整條件見上述驗證紀錄。

## 使用

Codex 新對話可明確要求使用 $elementary-competency-assessment-local；OpenCode V1 明確要求載入同名技能，確認 skill 工具實際讀取。請 Agent 回報本機主檔路徑與 Local 0.1.2，並讀取相關參考資源，避免只口頭聲稱已使用。

提供課本截圖／PDF或單元資訊，確認範圍及題數、題型、難度、時間和配分。Agent 查讀官方正文後命題，預覽完整答案詳解，可匯出學生卷及教師卷各一份 DOCX／PDF。

## 產檔環境

見 [本機依賴](references/local-runtime.md) 及 [母稿格式](references/assessment-data.md)。一般環境用 Python 3.10+ 建立獨立虛擬環境，安裝 [requirements.txt](requirements.txt)。Codex 有內建文件技能時，使用它提供的執行環境與核對流程，不把個人絕對路徑寫進技能。

PDF 須有可用 Word（Windows）或經確認的 LibreOffice。目前測過本機 Word 路徑，LibreOffice 路徑尚未實測。頁面預覽可用已列入依賴的 pypdfium2，亦支援 pdftoppm；中文需適當字型。一般段落、表格和圖片可由腳本處理，複雜公式／注音／直排另選工具並驗證。

在工作資料夾執行，不要將試卷或 .venv 建在全域技能資料夾：

~~~text
python <技能路徑>/scripts/doctor.py --output <工作資料夾>/runtime.json
python <技能路徑>/scripts/build_assessment.py <技能路徑>/examples/smoke-assessment.json --output <新輸出資料夾> --pdf-engine word
python <技能路徑>/scripts/validate_package.py <技能路徑>
~~~

技術試作是原創材料，沒有本輪正式課綱查證，不作為指定課本已驗證的證據。QA.json 不會自動標示視覺通過；查看所有頁面後另寫 QA-review.md。

## 來源與分發狀態

原版 ZIP SHA-256：99D5B5E3E428B5ADF58534D94D740AD98FF65D0702467AEB93E3C86FC5C7D450。

本機套件檔案由 package-manifest.json 記錄。套件不含教材、試卷、使用者設定或憑證；不會自行發布 GitHub／Pages。本技能採[MIT授權](LICENSE)，課本、官方資料及第三方依賴不因本技能授權而改變其權利；不將本機版視為已獲官方認證。
