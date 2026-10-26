
$ErrorActionPreference = "Stop"
$root = "C:\Users\GoeQ\Desktop\项目1"
$stage = Join-Path $root "Linux文件暂存"
$dest = Join-Path $root "最终提交"

# Resolve directory names without source-file encoding issues
$names = @{
    report = [string]::Concat([char[]]@(0x5B9E,0x9A8C,0x62A5,0x544A))
    docs = [string]::Concat([char[]]@(0x6280,0x672F,0x6587,0x6863))
    python = "Python" + [string]::Concat([char[]]@(0x6E90,0x4EE3,0x7801))
    mongo = "MongoDB" + [string]::Concat([char[]]@(0x811A,0x672C,0x4E0E,0x539F,0x59CB,0x6570,0x636E))
    compass = "Compass" + [string]::Concat([char[]]@(0x6570,0x636E,0x5BFC,0x51FA))
    shots = [string]::Concat([char[]]@(0x5B9E,0x9A8C,0x622A,0x56FE))
    logs = [string]::Concat([char[]]@(0x8FD0,0x884C,0x7ED3,0x679C,0x65E5,0x5FD7))
}

foreach ($key in $names.Keys) {
    New-Item -ItemType Directory -Force -Path (Join-Path $dest $names[$key]) | Out-Null
}

function Copy-Safe($source, $targetFolder) {
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { return }
    $name = Split-Path $source -Leaf
    $target = Join-Path $targetFolder $name
    if (-not (Test-Path -LiteralPath $target)) {
        Copy-Item -LiteralPath $source -Destination $target
        Write-Host "[COPIED] $name"
    } else {
        Write-Host "[EXISTS] $name"
    }
}

# Python source files from both folders
foreach ($dir in @($root, $stage)) {
    if (Test-Path $dir) {
        Get-ChildItem -LiteralPath $dir -File -Filter "*.py" |
            ForEach-Object {
                Copy-Safe $_.FullName (Join-Path $dest $names.python)
            }
    }
}

# MongoDB JavaScript and original datasets
foreach ($dir in @($root, $stage)) {
    if (Test-Path $dir) {
        Get-ChildItem -LiteralPath $dir -File |
            Where-Object {
                $_.Extension -eq ".js" -or
                $_.Name -in @("books.txt","readers.txt","borrow_logs.txt")
            } |
            ForEach-Object {
                Copy-Safe $_.FullName (Join-Path $dest $names.mongo)
            }
    }
}

# Compass JSON exports
foreach ($file in @("books_export.json","category_stats_export.json")) {
    Copy-Safe (Join-Path $root $file) (Join-Path $dest $names.compass)
}

# Execution logs
if (Test-Path $stage) {
    Get-ChildItem -LiteralPath $stage -File -Filter "*result*.txt" |
        ForEach-Object {
            Copy-Safe $_.FullName (Join-Path $dest $names.logs)
        }
}

# Word documents in project root
Get-ChildItem -LiteralPath $root -File |
    Where-Object {$_.Extension -eq ".docx"} |
    ForEach-Object {
        Copy-Safe $_.FullName (Join-Path $dest $names.report)
    }

# Screenshot files
$shotDir = Join-Path $root "screenshots"
if (Test-Path $shotDir) {
    Get-ChildItem -LiteralPath $shotDir -File -Recurse |
        Where-Object {$_.Extension -in @(".png",".jpg",".jpeg")} |
        ForEach-Object {
            Copy-Safe $_.FullName (Join-Path $dest $names.shots)
        }
}

# Check six required application modules
$required = @(
    "main.py",
    "mongodb_connect.py",
    "book_manager.py",
    "reader_manager.py",
    "borrow_manager.py",
    "stat_manager.py"
)

Write-Host ""
Write-Host "===== PYTHON MODULE CHECK ====="
$missing = 0
foreach ($file in $required) {
    $p = Join-Path (Join-Path $dest $names.python) $file
    if (Test-Path -LiteralPath $p) {
        Write-Host "[PASS] $file"
    } else {
        Write-Host "[MISSING] $file"
        $missing++
    }
}

Write-Host ""
Write-Host "===== RESULT ====="
if ($missing -eq 0) {
    Write-Host "PASS: All six Python modules are present."
} else {
    Write-Host "FAIL: $missing Python modules are missing."
}
Write-Host "Project organization complete."
