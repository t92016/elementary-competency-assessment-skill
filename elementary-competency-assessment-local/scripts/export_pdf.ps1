param(
    [Parameter(Mandatory=$true)][string]$InputDocx,
    [Parameter(Mandatory=$true)][string]$OutputPdf
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$taskInput = (Resolve-Path -LiteralPath $InputDocx).Path
$taskOutput = [System.IO.Path]::GetFullPath($OutputPdf)
if ([System.IO.Path]::GetExtension($taskInput) -ne '.docx') { throw 'Expected a DOCX file' }
if (Test-Path -LiteralPath $taskOutput) { throw 'Refusing to overwrite a PDF' }
$taskWord = $null
$taskDoc = $null
$taskOwnsWord = $false
try {
    $taskWord = New-Object -ComObject Word.Application
    if ($taskWord.Documents.Count -ne 0) { throw 'Word object has existing documents; stopping without closing them' }
    $taskOwnsWord = $true
    $taskWord.Visible = $false
    $taskWord.DisplayAlerts = 0
    $taskWord.AutomationSecurity = 3
    $taskDoc = $taskWord.Documents.Open($taskInput, $false, $true, $false)
    $taskDoc.Repaginate()
    $taskDoc.ExportAsFixedFormat($taskOutput, 17)
    if (!(Test-Path -LiteralPath $taskOutput)) { throw 'Word did not create the PDF' }
    Write-Output $taskOutput
} finally {
    $taskNoSave = 0
    try {
        if ($null -ne $taskDoc) {
            try { $taskDoc.Close([ref]$taskNoSave) }
            finally { [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($taskDoc) }
        }
    } finally {
        if ($null -ne $taskWord) {
            try { if ($taskOwnsWord) { $taskWord.Quit([ref]$taskNoSave) } }
            finally { [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($taskWord) }
        }
    }
}
