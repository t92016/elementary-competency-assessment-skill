# Install a complete copy; never overwrite an existing skill.
[CmdletBinding(SupportsShouldProcess=$true)]
param(
    [ValidateSet('Project','User')][string]$Scope = 'Project',
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$SkillsRoot
)
$ErrorActionPreference = 'Stop'
$taskSource = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskName = 'elementary-competency-assessment-local'
if (!(Test-Path -LiteralPath (Join-Path $taskSource 'SKILL.md'))) { throw 'Source SKILL.md missing' }
if (!$SkillsRoot) {
    if ($Scope -eq 'User') {
        $taskUserRoot = [System.Environment]::GetFolderPath('UserProfile')
        $SkillsRoot = Join-Path $taskUserRoot '.agents/skills'
    } else {
        $taskProject = (Resolve-Path -LiteralPath $ProjectRoot).Path
        $SkillsRoot = Join-Path $taskProject '.agents/skills'
    }
}
$taskDestination = [System.IO.Path]::GetFullPath((Join-Path $SkillsRoot $taskName))
$taskPrefix = $taskSource.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
if ($taskDestination -eq $taskSource -or $taskDestination.StartsWith($taskPrefix, [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Destination must be outside the source skill' }
if (Test-Path -LiteralPath $taskDestination) { throw 'Destination exists. Compare versions before explicitly removing or replacing it.' }
# Reject symbolic links/reparse points in the distributable.
$taskItems = @(Get-ChildItem -LiteralPath $taskSource -Recurse -Force)
if ($taskItems | Where-Object { $_.Attributes -band [System.IO.FileAttributes]::ReparsePoint }) { throw 'Source contains a reparse point' }
$taskFiles = @($taskItems | Where-Object { !$_.PSIsContainer })
$taskSourceHashes = @{}
foreach ($taskFile in $taskFiles) {
    $taskRelative = $taskFile.FullName.Substring($taskPrefix.Length)
    if ($taskRelative -match '(^|[\\/])(__pycache__|\.venv)([\\/]|$)' -or $taskRelative -like '*.pyc') { throw 'Source contains runtime artifacts' }
    $taskSourceHashes[$taskRelative] = (Get-FileHash -LiteralPath $taskFile.FullName -Algorithm SHA256).Hash
}
if ($PSCmdlet.ShouldProcess($taskDestination, 'Install complete local assessment skill')) {
    [System.IO.Directory]::CreateDirectory($taskDestination) | Out-Null
    foreach ($taskRelative in $taskSourceHashes.Keys) {
        $taskTarget = Join-Path $taskDestination $taskRelative
        [System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($taskTarget)) | Out-Null
        Copy-Item -LiteralPath (Join-Path $taskSource $taskRelative) -Destination $taskTarget
        if ((Get-FileHash -LiteralPath $taskTarget -Algorithm SHA256).Hash -ne $taskSourceHashes[$taskRelative]) { throw "Copy verification failed: $taskRelative" }
    }
    Write-Output ('Installed and hash-verified: ' + $taskDestination)
    Write-Output 'File installation is complete. Agent discovery and actual workflow still require a separate new-session test.'
}
