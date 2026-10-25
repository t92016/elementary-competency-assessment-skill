# 本機執行與依賴

## 能力盤點

記錄日期、作業系統、Agent 與版本、實際模型（無法確認就標未確認）、實際命令殼層（PowerShell／bash等）、搜尋／網頁正文讀取、圖片辨識、PDF 讀取、Python、文件套件、PDF 轉換器、中文字型、輸出位置。命令可執行、檔案可讀與模型實際使用能力分別記錄。

可執行 scripts/doctor.py --output 環境報告.json。此工具只檢查本機執行與套件，不會驗證模型、搜尋、OCR 或命題品質，也不會讀取憑證。

## 文件工具鏈

基本需求：Python 3.10+、python-docx、pypdf、Pillow、pypdfium2。使用 [requirements.txt](../requirements.txt) 建立獨立虛擬環境；不要假設 PATH 中的 python 是一般 Python，可能是其他軟體的內建版本。

建議在老師的工作資料夾建立 .venv，不要在全域技能目錄安裝依賴。Windows 範例：

~~~powershell
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r <技能完整路徑>\requirements.txt
~~~

產檔腳本使用當前 Python 環境，沒有內嵌個人絕對路徑。Codex 有內建文件／PDF技能時，遵循其產檔與視覺核對要求，使用它提供的執行環境；不能把這項內建能力當成 OpenCode 或其他電腦的既定前提。

## PDF 轉換與預覽

- Windows 有 Microsoft Word 時，可明確選 --pdf-engine word。使用套件 export_pdf.ps1，建立獨立且隱藏的 Word 自動化物件，只開啟剛產生的 DOCX，以 PDF 格式匯出。Word 需要可正常啟動及授權的桌面環境。偵測到既有文件就停止，不關閉使用者的文件。
- 其他環境可選 --pdf-engine libreoffice --soffice <經確認的完整路徑>。使用獨立暫存 profile 轉檔，不依賴使用者既有設定。Codex 文件技能要求使用內建 LibreOffice 時，必須遵守，不能擅自用使用者安裝版本替代；若內建缺失，可採已驗證的 Word 路徑。
- auto 優先使用明確提供的 soffice，否則 Windows 嘗試 Word；無能力則保留 DOCX、清楚報 PDF 未完成並以非零碼結束。--pdf-engine none 是明確的僅產 DOCX 模式，不等於四份交付完成。
- 可用 --pdftoppm <完整路徑> 產生每頁 PNG；PATH 已有則自動找到。未找到pdftoppm時使用pypdfium2；可加 --preview-engine pdfium 明確選擇。兩種渲染器都無法使用時，視覺驗收仍待完成。

每次輸出 QA.json 的 visual_review 固定為 pending，須由 Agent 實際查看所有頁面後另寫 QA-review.md；腳本不能自動宣稱版面通過。

## 限制

腳本不做教材 OCR、官方搜尋或自動命題；由 Agent 先讀教材、查正文、確認規格並完成母稿。語意正確、素養任務品質、各選項解析、簡答規準公平性與年級適切性必須人工／Agent 逐題檢查。特殊公式、注音、直排或精密圖形需另外處理並驗證，不允許默默降級成不完整文字。

Windows先確認實際殼層；PowerShell不使用bash的<<EOF。長程式先寫成UTF-8 .py檔，留在本次工作目錄，再以 & "<Python完整路徑>" "<腳本路徑>" 執行。不為下載公開PDF停用TLS驗證；網路錯誤另行處理。
