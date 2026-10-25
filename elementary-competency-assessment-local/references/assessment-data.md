# 結構化母稿格式

產檔工具只負責排版與一致性檢查，不代替命題。以 UTF-8 JSON 儲存，根目錄以外的圖片用相對於 JSON 的路徑。完整可執行例子見 [技術試作母稿](../examples/smoke-assessment.json)，它是原創轉檔測試材料，未做正式課綱查證。

## 根欄位

- title、subject、grade、unit、version：非空字串；試題版次例如 試題第1版。
- minutes、total_score：正數。difficulty：非空字串。
- instructions：學生作答說明字串陣列；materials：卷首共用內容區塊陣列。
- questions：依最終題序排列，每小題一筆。題號 id 從 1 連續。
- blueprint：每題一筆 id、locator（教材定位）、goal（能力與知識）、task（判斷任務）、basis（答案或評分依據）、minutes（估計分鐘）。題型與配分取自題目本身，避免重複欄位衝突。
- sources：每筆 institution、document、year、url、accessed、locator、used_for、status、kind。kind 為 official 或 material。status 如 已讀正文、僅摘要／目錄、無法讀取、尚未核對、技能內既有查讀摘要，非本次連線讀取。本機附件（含老師提供的課本截圖與自編教材）可用 url 空字串，但 official 來源必須是真實 http(s) URL。日期 YYYY-MM-DD；不明年份寫 未核對。每份正式卷仍由 Agent 查證正文與適用階段，腳本無法驗證 URL 實際可讀或代碼正確。

## 題目欄位

每筆 id、type（single 或 short）、score、stem、answer、explanation、locator、misconception。explanation 為完整解析字串陣列，不能只有答案。materials 是本題前的共用內容；題組第一小題先放材料和適用題號，後續小題直接緊接。group 可寫 題組一，題組必須連續，單一小題最多隸屬一組。

single：options 為 A、B、C、D 四個非空字串；answer 為 A～D；option_explanations 同樣是 A～D 四個非空解析。

short：answer_lines 正整數，預設 4；accepted_answers 非空字串陣列；rubric 為 criterion、points 陣列，正分且合計等於題目分數；partial_credit_examples 為 response、points、reason 陣列，至少一筆 0 < points < 題分，說明如何部分給分。

## 內容區塊

可出現在卷首 materials、題目前 materials、stem 中；stem 也可直接用字串。

- {"type":"paragraph","text":"完整材料或題幹"}
- {"type":"table","headers":["項目","數值"],"rows":[["甲","3"],["乙","5"]],"caption":"必要圖說與單位"}
- {"type":"image","path":"images/chart.png","caption":"圖說、單位與圖例","width_cm":12}

圖片需真實存在、無外部 URL，寬度不超過可印範圍；文字內容要有可讀標籤，Agent 必須核對圖片。不要把教師詳解放進學生區塊；工具只排除教師專用欄位，不能判斷所有語意洩答。

## 執行

~~~text
python <技能路徑>/scripts/build_assessment.py <母稿.json> --output <新目錄> --pdf-engine word
python <技能路徑>/scripts/build_assessment.py <母稿.json> --output <新目錄> --pdf-engine libreoffice --soffice <完整路徑>
~~~

可加 --preview-engine pdfium 使用Python直接渲染頁面，或auto優先pdftoppm、否則pypdfium2。可加 --font 字型名、--font-size 點數、--pdftoppm 完整路徑；--validate-only 只檢查母稿，不產檔。預設不覆寫已存在目錄。QA.json 記錄文件 SHA-256、逐段文字回讀、各 PDF 頁數與渲染檔；visual_review 永遠標 pending，實際目視後另寫紀錄。build_manifest.json 保存母稿雜湊與工具版本。

此版本支援一般段落、表格和圖片；不支援的區塊會報錯。遇公式、直排、注音等需求，可擴充母稿與工具或採替代工具並完整核對。
