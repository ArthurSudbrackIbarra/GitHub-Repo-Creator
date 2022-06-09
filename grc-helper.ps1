$COMMAND = $args[0]
$PARAMETER = $args[1]

if ($COMMAND -eq $null) {
    Write-Host "`nGRC: No command passed.`n"
    Exit 0
}

if ($PARAMETER -eq $null) {
    python $PSScriptRoot\.program-files\main.py $COMMAND
} else {
    if ($COMMAND -eq "create" -or $COMMAND -eq "save") {
        if ([System.IO.Path]::IsPathRooted($PARAMETER)) {
            python $PSScriptRoot\.program-files\main.py $COMMAND $PARAMETER
        } else {
            $FILE_PATH = "$PWD\$PARAMETER"
            python $PSScriptRoot\.program-files\main.py $COMMAND $FILE_PATH
        }   
    }
    else {
        python $PSScriptRoot\.program-files\main.py $COMMAND $PARAMETER
    }
}
