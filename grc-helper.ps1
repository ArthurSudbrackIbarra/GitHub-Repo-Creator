Set-ExecutionPolicy Unrestricted -Scope Process
Invoke-Expression $PSScriptRoot\venv\Scripts\Activate.ps1
python $PSScriptRoot\.program-files\main.py $args
$exitCode = $?
deactivate
exit $exitCode
