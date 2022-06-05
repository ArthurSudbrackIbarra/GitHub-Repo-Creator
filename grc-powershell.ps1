$COMMAND = $args[0]
$PARAMETER = $args[1]

if ($COMMAND -eq $null) {
    Write-Host "`nNo command passed.`n"
}

if ($PARAMETER -eq $null) {
    if ($COMMAND -eq "choose") {
        python $PSScriptRoot\.program-files\main.py $COMMAND
    }
} else {
    if ($COMMAND -eq "create" -or $COMMAND -eq "save") {
        $FILE_PATH = "$PWD\$PARAMETER"
        python $PSScriptRoot\.program-files\main.py $COMMAND $FILE_PATH
    }
    if ($COMMAND -eq "authenticate" -or $COMMAND -eq "delete") {
        python $PSScriptRoot\.program-files\main.py $COMMAND $PARAMETER
    }
}
