$COMMAND = $args[0]

if ($COMMAND -eq $null) {
    Write-Host "`nGRC: No command passed.`n"
    Exit 0
}

$PYTHON3VERSION = "$(try { python3 --version 2> $Null } catch { })"
if ($PYTHON3VERSION.Contains("Python 3")) {
    Set-Alias -name python -value python3
}

python $PSScriptRoot\.program-files\main.py $args
