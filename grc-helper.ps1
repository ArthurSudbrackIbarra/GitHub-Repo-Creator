$COMMAND = $args[0]

if ($COMMAND -eq $null) {
    Write-Host "`nGRC: No command passed.`n"
    Exit 0
}

$PYTHON3VERSION = "$(try { python3 --version 2> $Null } catch { })"
if ($PYTHON3VERSION.Contains("Python 3")) {
    Set-Alias -name python -value python3
}

if ($COMMAND -eq "create" -or $COMMAND -eq "save") {
    $USER_FILE_PATH = $args[1]
    if ([System.IO.Path]::IsPathRooted($USER_FILE_PATH)) {
        python $PSScriptRoot\.program-files\main.py $args
    } else {
        $ABSOLUTE_FILE_PATH = "$PWD\$USER_FILE_PATH"
        python $PSScriptRoot\.program-files\main.py $COMMAND $ABSOLUTE_FILE_PATH
    }   
} else {
    python $PSScriptRoot\.program-files\main.py $args
}
