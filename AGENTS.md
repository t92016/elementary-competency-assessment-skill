# 維護此 Repo

此Repo只保存公開技能、原創小型範例、安裝／命題文件與封裝工具。先讀README、AGENT-START及docs/verification，區分歷史結果與本機實測。

修改技能後同步主檔metadata版本與scripts/build_assessment.py的VERSION，更新套件manifest，執行tools/validate_release.py及tools/test_assessment.py。新發布版使用tools/package_skill.py產同版ZIP／SHA，不覆寫已發布的不同內容版本。使用者教材、正式試卷、個人設定、憑證與原始事件不納入版本庫。

命題使用者已授權的工作直接執行；新電腦依指引使用自己的帳戶與路徑。未完成的模型、平台、來源或視覺檢查如實標示。修改Repo不自動授權另外發布、推送或更改全域設定。
