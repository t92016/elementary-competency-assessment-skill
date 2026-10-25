# 在其他筆電安裝國小素養試題 Codex Skill

適用套件：elementary-competency-assessment-local，Local 0.1.2。
本文件為可直接交給另一台筆電Codex讀取的安裝指引。已驗收的正式案例使用Local0.1.1；0.1.2的改動及各平台結果請看https://t92016.github.io/elementary-competency-assessment-skill/verification.html。2026-10-25已在本機Windows完成專案安裝、載入、教材辨識、官方查證及四份文件產生；另一台電腦仍須按本文件重新驗證，不視為已通過。

## 一 帶到新筆電的內容

複製整份 elementary-competency-assessment-local-0.1.2.zip。解壓後應有一層同名技能資料夾，內含SKILL.md、README.md、requirements.txt、package-manifest.json、references、templates、scripts及examples。

不需要複製原始課本、這次試卷、validation、個人設定、模型憑證或整台電腦的Codex資料夾。正式教材另放使用者自己的工作資料夾，不能混進全域技能目錄。

ZIP的SHA-256請比對同批發布的SHA256SUMS-0.1.2.txt；套件內各檔雜湊則由validate_package.py核對。

## 二 先檢查新電腦能力

請新電腦上的Codex先盤點：

- Codex已可正常使用並登入該使用者自己的帳戶。
- 可用模型能辨識圖片；若讀教材PDF，能開啟PDF文字與必要頁面圖片。
- 有搜尋及讀取官方網頁／PDF正文的能力，不能只拿搜尋摘要當作已讀。
- Python 3.10以上；本輪實測為3.12.14。檢查實際執行檔，不只看python命令名稱。
- 繁體中文字型；Windows可使用Microsoft JhengHei，其他平台指定實際已安裝的字型。
- DOCX轉PDF：Windows有正常啟動且已授權的Word，或另有經確認的LibreOffice。技能不會安裝或授權Office。
- PDF全頁預覽：pypdfium2已列入依賴；有pdftoppm也可使用，不再強制另裝Poppler。

Codex內建文件工具可先透過workspace dependencies工具找它提供的Python與套件；這項能力不是所有CLI或電腦都有，不能把本機C槽路徑抄到另一台。

若一般Python不存在，先從[Python官方Windows下載頁](https://www.python.org/downloads/windows/)完成安裝，再繼續。可優先使用64位元Python 3.12，這是本輪已測版本。

## 三 解壓及校驗

建議先用可正常讀寫的本機工作資料夾測試。若使用雲端／網路磁碟，確認Codex執行環境能讀取該路徑；不能因技能清單看得到就認定沙箱讀得到。

PowerShell範例，在放有ZIP的資料夾執行。資料夾名稱可自行調整；不要覆寫已有工作：

~~~powershell
Get-FileHash -LiteralPath .\elementary-competency-assessment-local-0.1.2.zip -Algorithm SHA256
Expand-Archive -LiteralPath .\elementary-competency-assessment-local-0.1.2.zip -DestinationPath .\skill-source-012
~~~

確認 .\skill-source-012\elementary-competency-assessment-local\SKILL.md 存在。保持整個資料夾，不只複製SKILL.md。

## 四 準備文件工具環境

在將來放教材與輸出的工作資料夾建立獨立環境，不要建立在全域技能資料夾。若Codex內建Python與依賴已可用，可用其實際路徑執行，不必重複安裝。

一般Windows PowerShell範例（使用本輪測過的Python3.12；其他版本需自行驗證）：

~~~powershell
py -0p
$env:PYTHONUTF8='1'
py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r .\skill-source-012\elementary-competency-assessment-local\requirements.txt
& .\.venv\Scripts\python.exe .\skill-source-012\elementary-competency-assessment-local\scripts\validate_package.py .\skill-source-012\elementary-competency-assessment-local
& .\.venv\Scripts\python.exe .\skill-source-012\elementary-competency-assessment-local\scripts\doctor.py --output .\environment-report.json
~~~

上面假設skill-source-012也位於目前工作資料夾；若不同，請換成實際完整路徑。使用明確的虛擬環境Python，不必啟用Activate.ps1。

requirements包含python-docx、pypdf、Pillow、pypdfium2的本輪測過版本。pip會解析必要的間接依賴；作業系統、Office與字型仍另外盤點。


### Windows ZIP 解壓後的腳本信任

若已確認套件來源、ZIP校驗碼及逐檔manifest，且已檢視並信任這兩支腳本，遇到RemoteSigned阻擋可只解除install.ps1與export_pdf.ps1的下載標記。先將下列路徑換成已解壓的完整技能資料夾；不更改執行原則。組織若要求簽署或另有限制，依其政策處理，不略過。

~~~powershell
$taskSkillRoot=(Resolve-Path -LiteralPath '.\skill-source-012\elementary-competency-assessment-local').Path
& .\.venv\Scripts\python.exe (Join-Path $taskSkillRoot 'scripts/validate_package.py') $taskSkillRoot
if($LASTEXITCODE -ne 0){throw '套件校驗未通過'}
Unblock-File -LiteralPath (Join-Path $taskSkillRoot 'scripts/install.ps1')
Unblock-File -LiteralPath (Join-Path $taskSkillRoot 'scripts/export_pdf.ps1')
~~~

[Microsoft Unblock-File說明](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/unblock-file)。Git clone來源不一定有下載標記，依實際情況處理。

## 五 選擇一種安裝範圍

[Codex官方技能文件](https://learn.chatgpt.com/docs/build-skills)於2026-10-25列出專案 .agents/skills 及使用者 ~/.agents/skills。先測專案，再決定是否全域，避免多份同名技能混用。

先預覽專案安裝位置，再安裝：

~~~powershell
& .\skill-source-012\elementary-competency-assessment-local\scripts\install.ps1 -Scope Project -ProjectRoot . -WhatIf
& .\skill-source-012\elementary-competency-assessment-local\scripts\install.ps1 -Scope Project -ProjectRoot .
~~~

結果位於：
<工作資料夾>/.agents/skills/elementary-competency-assessment-local/SKILL.md。

如果希望該使用者在不同專案都能使用，可改為使用者全域安裝：

~~~powershell
& .\skill-source-012\elementary-competency-assessment-local\scripts\install.ps1 -Scope User -WhatIf
& .\skill-source-012\elementary-competency-assessment-local\scripts\install.ps1 -Scope User
~~~

結果位於：
<該使用者個人目錄>/.agents/skills/elementary-competency-assessment-local/SKILL.md。

請擇一維持清楚的實際載入來源。從專案切換全域時，先比對並保留舊版，再由使用者明確選擇如何處理舊副本；不要擅自遞迴刪除。安裝器遇到同名目錄會停止，不會覆寫。手動安裝也必須複製完整技能資料夾。

## 六 新對話的載入驗收

在新筆電上開啟對應工作資料夾與新的Codex對話，貼上：

> 請使用 $elementary-competency-assessment-local。這次只做載入測試，先不要命題或改檔。請回報你從技能清單找到並實際讀取的SKILL.md完整路徑、name及Local版本，確認為0.1.2，再實際讀取references/local-runtime.md、references/material-intake.md、references/assessment-criteria.md、references/revision-flow.md、references/local-delivery.md、references/assessment-data.md，以及templates三份範本。每份說明一項讀到的規則；無法讀取要如實標示，不可憑檔名猜測。

references/install-codex.md是本安裝指引，命題用資源仍是上述9份。

通過條件：實際路徑是選定的專案或使用者技能位置、版本正確、9份命題資源均讀到，不能只回覆「我會使用」。如果更新沒有出現，依官方文件重新啟動Codex後重測，不覆寫其他技能。

## 七 文件工具的獨立測試

已安裝後，先用技能附帶的自編材料，不需上傳正式課本。以下以專案安裝為例：

~~~powershell
& .\.venv\Scripts\python.exe .\.agents\skills\elementary-competency-assessment-local\scripts\build_assessment.py .\.agents\skills\elementary-competency-assessment-local\examples\smoke-assessment.json --output .\output\smoke-001 --pdf-engine word --preview-engine pdfium
~~~

輸出資料夾必須尚不存在。使用者全域安裝時，改用該技能的完整路徑。

LibreOffice替代路徑（本輪尚未在本機測過）：

~~~text
python <技能路徑>/scripts/build_assessment.py <母稿.json> --output <新資料夾> --pdf-engine libreoffice --soffice <已確認的soffice完整路徑> --preview-engine pdfium
~~~

Codex文件技能若要求使用內建LibreOffice，應使用其提供的內建路徑；本機沒有內建時可選已驗證的Word路徑，不擅改其規則。macOS／Linux沒有Windows Word COM，本文件尚未宣稱這些平台完成轉檔重現。

通過條件：

- 學生卷.docx、學生卷.pdf、教師卷.docx、教師卷.pdf實際存在且可開啟。
- QA.json的四份文件與文字核對通過，題數及分數一致。
- 每頁PNG都產生，Agent實際逐頁查看，繁中無亂碼、無裁切、合理分頁、學生卷無答案。
- 目視結果另寫QA-review.md。程式visual_review固定pending，不能把自動訊息當成人工驗收。

pypdfium2只把既有PDF渲染成圖片，不會將DOCX轉成PDF；Word或LibreOffice仍是轉檔前提。[pypdfium2官方使用說明](https://pypdfium2-team.github.io/pypdfium2/readme.html)。

## 八 正式教材測試

提供截圖／PDF，說明科目、年級、單元與出題範圍；能從附件辨識的內容不用重填。指定題數、題型、題組、難度、時間、配分或讓Agent提出具體建議。確認範圍後：

1. 逐頁辨識圖文、圖例、時間及單位，列出已讀與遮蔽／未讀範圍。
2. 搜尋對應領域與學習階段的官方課綱及命題原則，讀正文、記真實URL、日期及定位。
3. 建逐題藍圖、出原創情境題、答案、完整詳解與簡答規準。
4. 完整預覽並修正；若已明確要求直接匯出，不重問同意。
5. 同一母稿產兩卷DOCX，再各自轉PDF，全題及全頁核對後交付。

重新出題需保留舊版，沿用已讀教材與未變設定，更新新題、答案、詳解與配分。

## 九 常見問題

- 看得到技能卻讀不到：分別檢查實際技能路徑、沙箱對磁碟的存取及目前對話版本。本輪J槽一般沙箱失敗，經審核的精確唯讀操作成功；不能直接推論所有雲端磁碟都失敗。不要關閉安全機制或使用略過審核選項。
- model_not_found：檢查該筆電目前帳戶可用模型，不要照抄本機臨時用過的模型名稱，也不要因模型錯誤重裝技能。
- PDF未生成：先檢查Word授權與啟動、或soffice路徑，保留已完成DOCX並標明PDF未完成。
- 只有文字核對：還要查看所有頁面PNG，不能直接宣稱列印版面通過。
- 不支援特殊公式／注音／直排：選合適產檔工具並完整驗證，不能為了符合腳本刪題或省略圖文。

## 十 交給其他電腦Codex的啟動訊息

> 請讀取這份安裝指引與完整Local 0.1.2 ZIP。先盤點本機Codex、圖片／PDF與搜尋能力、Python、字型及DOCX轉PDF工具；核對套件後，先做專案範圍安裝與實際載入測試，再用自編材料確認兩卷Word／PDF及全部頁面。所有位置使用這台電腦的實際路徑，不照抄舊電腦C槽／J槽。通過後再測我提供的課本。若我明確要求跨專案使用，再安裝使用者全域，避免同名副本混用。不要複製個人憑證或自動發布教材、試卷、GitHub／Pages。

以上在本機已測的結果見專案驗證紀錄；其他筆電完成後應另存日期、版本、位置、案例、四份文件與全頁核對結果。
