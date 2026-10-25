---
layout: default
title: 國小素養試題出題 Skill
---

# 國小素養試題出題 Skill

讓Codex或OpenCode依教材與官方命題依據，協助教師製作原創素養試題、完整詳解，以及可編輯的Word與可列印的PDF。

**Local0.1.2 · 繁體中文 · MIT授權**

[取得完整套件](releases.md)　[查看已測範圍](verification.md)

**OpenCode本輪免費模型正式命題未通過；原生載入、搜尋及四檔技術測試已分別驗證，詳見驗證紀錄。**

## 從另一台電腦開始

1. 開啟Codex或OpenCode及使用者自己的帳戶。
2. 把下方啟動訊息交給Agent，先盤點環境、校驗、安裝與驗收。
3. 小型測試通過後，再提供自己的課本截圖／PDF與命題規格。

~~~text
請讀取 https://raw.githubusercontent.com/t92016/elementary-competency-assessment-skill/v0.1.2/AGENT-START.md
依目前Agent使用同版安裝指引，盤點本機能力、校驗完整技能、安裝到我選定的範圍，
實際載入及讀取參考資源，先驗證兩卷Word／PDF與全部頁面，再處理我提供的正式教材。
使用這台電腦自己的帳戶與路徑；已知教材與規格直接沿用，保留舊版，不讀出或複製憑證。
~~~

[原始Agent啟動文件](https://github.com/t92016/elementary-competency-assessment-skill/blob/v0.1.2/AGENT-START.md)

## 可以交付什麼

學生卷含完整材料、題幹、選項及作答區；教師卷含同版全部試題、逐題答案、每個選項解析、簡答評分規準與部分給分例、命題藍圖及來源查讀紀錄。兩卷各有真正DOCX及PDF，並做逐題回讀與全部頁面核對。

## 先準備哪些能力

模型須能讀實際教材、使用工具並查官方正文；本機需Python與套件、中文字型，以及Word或可用LibreOffice做PDF轉換。技能提供做法與腳本，這些能力仍需在各機確認。Pages提供說明及下載，實際出題與產檔在使用者的Agent及工作電腦執行。

## 使用入口

| 需求 | 指引 |
| --- | --- |
| 使用Codex | [Codex完整安裝](install-codex.md) |
| 使用OpenCode | [OpenCode完整安裝](install-opencode.md) |
| 了解教材到文件的流程 | [正式命題流程](workflow.md) |
| 查已通過與待驗證 | [驗收紀錄](verification.md) |
| 更新、下載與校驗 | [版本與下載](releases.md) |
| 授權及官方入口 | [授權與來源](sources.md) |

公開Repo只包含技能、工具、原創測試材料與說明；老師的課本、正式試卷及個人資料保留在各自工作資料夾。


---

[首頁](index.md) · [Codex安裝](install-codex.md) · [OpenCode安裝](install-opencode.md) · [命題流程](workflow.md) · [驗收紀錄](verification.md) · [下載](releases.md)
