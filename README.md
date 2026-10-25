# 國小素養試題出題 Skill

依臺灣國小國語、數學、社會、自然教材與官方命題依據，製作素養試題、完整詳解，以及學生卷／教師卷各一份Word與PDF。

目前發布版：**Local0.1.2**。源自Gemini V6.1，採MIT授權。Codex已完成五上社會10題的本機正式案例，使用者已初步驗收；OpenCode及跨電腦狀態請看[驗證紀錄](docs/verification.md)，不把格式相容視為全部實測通過。

- [公開說明網站](https://t92016.github.io/elementary-competency-assessment-skill/)
- [給下一台電腦Agent的啟動指引](AGENT-START.md)
- [Codex安裝](docs/install-codex.md)／[OpenCode安裝](docs/install-opencode.md)
- [正式命題流程](docs/workflow.md)／[驗收紀錄](docs/verification.md)
- [完整技能主檔](elementary-competency-assessment-local/SKILL.md)
- [版本與下載](docs/releases.md)／[授權與來源](docs/sources.md)

**OpenCode本輪免費模型正式命題未通過；原生載入、搜尋及四檔技術測試已分別驗證，詳見驗證紀錄。**

## 快速開始

請Codex或OpenCode先讀AGENT-START.md。安裝保留完整技能資料夾，先盤點可用模型、讀圖／搜尋能力、Python、字型及PDF轉換工具，再校驗與安裝、實際載入、小型工具測試，最後使用老師的教材命題。

專案安裝採.agents/skills，使用者全域採~/.agents/skills。不要只複製SKILL.md或混用同名副本。PDF需要已授權可用的Windows Word或可用LibreOffice；pypdfium2只做預覽。各機使用自己的帳戶及路徑。

## Repo內容

elementary-competency-assessment-local是可攜技能來源；docs是Pages文件；tools是封裝與檢查工具。安裝後生成的.agents、教材、試卷、虛擬環境、個人設定及原始執行紀錄不納入版本庫。公開自編小型母稿只供產檔測試，不能當成指定課本已查證的證據。

官方能力及位置會隨產品更新，實際操作以當前版本和能力為準：[Codex技能文件](https://learn.chatgpt.com/docs/build-skills)、[OpenCode技能文件](https://docs.opencode.ai/docs/skills/)、[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)。
