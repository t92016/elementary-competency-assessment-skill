# OpenCode 安裝與驗收

適用：elementary-competency-assessment-local，Local 0.1.2。此技能包含命題流程與本機產檔工具，模型、搜尋、圖片辨識及Office能力仍由執行環境提供。實測範圍與版本見[驗證紀錄](https://t92016.github.io/elementary-competency-assessment-skill/verification.html)。

## 1 先確認模型與工具

先檢查實際OpenCode版本、使用的provider/model、圖片輸入及工具呼叫能力、搜尋／官方PDF正文讀取，以及本機Python、中文字型與PDF轉換器。模型清單列出不等於帳戶可用；先以不含教材的簡短請求測連線。

API金鑰與登入在使用者自己的OpenCode設定；不貼進對話、教材、母稿或公開Repo。金鑰過期、HTTP401、額度不足與skill載入分別記錄，不把供應商錯誤當成技能通過或失敗。若目前帳戶有多種模型，可臨時指定，不擅改全域預設。

~~~powershell
opencode --version
opencode auth list
opencode models
opencode run "只回覆連線測試成功，不使用工具。" --model <已確認可用的provider/model>
~~~

採用現有權限；若工具、技能或資料傳送需授權，依所在平台與使用者已給範圍處理，不使用略過安全審核的選項。

## 2 校驗完整套件並準備Python

取得同版ZIP與SHA256SUMS-0.1.2.txt後比對雜湊，解壓到新的資料夾，保留完整elementary-competency-assessment-local資料夾。不要只下載SKILL.md。若從Repo取得來源，該技能資料夾就在Repo根目錄。

在老師的工作資料夾建立獨立環境，不放進全域技能目錄。Windows下以本輪測過的Python3.12為例；若使用其他版本，需自行驗證依賴：

~~~powershell
py -0p
py -3.12 -m venv .venv
$env:PYTHONUTF8='1'
& .\.venv\Scripts\python.exe -m pip install -r <技能資料夾>\requirements.txt
& .\.venv\Scripts\python.exe <技能資料夾>\scripts\validate_package.py <技能資料夾>
& .\.venv\Scripts\python.exe <技能資料夾>\scripts\doctor.py --output .\environment-report.json
~~~

將所有<技能資料夾>換成實際路徑，含空白時加引號。doctor不檢查模型登入、讀圖、搜尋或Word實際轉檔，這些需各自測試。

PDF轉換需已授權且可正常啟動的Windows Word，或可用LibreOffice；繁中需實際已安裝的字型。pypdfium2只將既有PDF渲染成圖片，不能取代DOCX轉PDF。OpenCode可用獨立Python，不依賴Codex專用連接器或個人C槽路徑。


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

## 3 安裝範圍

[OpenCode技能官方文件](https://docs.opencode.ai/docs/skills/)列出專案.agents/skills及使用者~/.agents/skills，與Codex共用相容位置。也支援OpenCode自己的.opencode/skills及~/.config/opencode/skills；本套件安裝器採共用位置。

在選定工作資料夾執行，下列<技能資料夾>是解壓／clone所得的來源：

~~~powershell
& <技能資料夾>\scripts\install.ps1 -Scope Project -ProjectRoot . -WhatIf
& <技能資料夾>\scripts\install.ps1 -Scope Project -ProjectRoot .
~~~

若使用者已指定跨專案使用，改為：

~~~powershell
& <技能資料夾>\scripts\install.ps1 -Scope User -WhatIf
& <技能資料夾>\scripts\install.ps1 -Scope User
~~~

擇一維持清楚的載入來源。同名已存在時，安裝器會停止；先比較並保留舊版，依已授權範圍處理升級，不刪除不明內容。Windows執行原則若阻擋，先核對政策與來源；可手動複製整個技能資料夾，不全面關閉安全機制。其他作業系統可完整手動複製到選定位置，仍需驗證依賴與轉檔。

## 4 實際載入

在新的OpenCode會話明確要求：

> 請使用原生skill工具載入elementary-competency-assessment-local，回報實際SKILL.md路徑與Local版本，應為0.1.2。實際讀取references的local-runtime、material-intake、assessment-criteria、revision-flow、local-delivery、assessment-data，以及templates的三份範本，各說明一項實際讀到的規則。這次只測載入，不命題。

只用debug skill看到清單，或模型直接讀檔，不能宣稱原生skill呼叫已驗證。載入與資源讀取分開記錄；若該Agent禁用skill或權限ask阻擋，要依使用者授權處理。

需要放行此技能時可在選定設定範圍使用下列精確規則，保留其他權限：

~~~json
{
  "permission": {
    "skill": {
      "elementary-competency-assessment-local": "allow"
    }
  }
}
~~~

這不是所有工具的無條件放行。CLI參數與設定格式須以實際安裝版本為準；OpenCode1與2的專用設定不混用。

## 5 搜尋與官方正文

依[OpenCode工具文件](https://docs.opencode.ai/docs/tools/)，websearch可在OpenCode／Go供應商使用；其他供應商可在當次程序設定OPENCODE_ENABLE_EXA=1啟用Exa搜尋。先確認所在環境允許該連線，勿將此設定寫成所有使用者的全域預設。

~~~powershell
$env:OPENCODE_ENABLE_EXA='1'
opencode
~~~

先搜尋，再webfetch或下載官方正文。PDF若只回二進位，使用Python讀相關頁，必要時渲染表格／圖像；不能只列真實URL就稱已讀。網路失敗保留實際錯誤，不停用TLS驗證。

## 6 Windows命令與產檔測試

先確定OpenCode實際使用PowerShell、cmd或bash。PowerShell不能直接套用bash的<<EOF語法；較長Python內容先寫為UTF-8 .py檔，再用呼叫運算子執行，檔案留在本次工作目錄：

~~~powershell
& "C:\實際Python路徑\python.exe" ".\work\build_case.py"
~~~

使用套件自編小型母稿先驗證工具，下列路徑以專案安裝及工作資料夾.venv為例：

~~~powershell
& .\.venv\Scripts\python.exe .\.agents\skills\elementary-competency-assessment-local\scripts\build_assessment.py .\.agents\skills\elementary-competency-assessment-local\examples\smoke-assessment.json --output .\output\smoke-001 --pdf-engine word --preview-engine pdfium
~~~

輸出資料夾必須尚不存在。LibreOffice分支可用--pdf-engine libreoffice --soffice <已確認完整路徑>；本專案未將該分支標為已通過。

驗收四份檔案、QA文字核對、每頁PNG，以及Agent實際查看全部頁面的QA-review.md。程式的visual_review固定pending。技術母稿測試不等於OpenCode已從課本獨立命題。

## 7 正式命題與重出

提供教材後沿用已知資訊，只補影響命題的缺項。Agent必須自己讀教材、搜尋官方規範、讀正文、做藍圖、原創命題與詳解，再從同一母稿產生兩卷Word與PDF。不要拿預先由其他Agent完成的母稿轉檔，當作完整命題能力的證據。

公開啟動提示：

> 請使用elementary-competency-assessment-local，先讀附件並辨識實際可讀範圍；沿用我指定的題數與配分，缺項集中提出具體建議。查讀適用的官方課綱及素養命題正文後製作題目、逐選項詳解與簡答規準。完成後直接交付學生卷與教師卷各一份Word、PDF，回讀全部內容並查看全部頁面。資料不足或能力缺失要明確標示，不假稱完成。

重新出題沿用已讀教材與未變規格、保留舊版、實質更新題目及答案，不重討已可讀教材。其他筆電需各自留下模型、版本、來源、四份文件與全頁核對紀錄。
