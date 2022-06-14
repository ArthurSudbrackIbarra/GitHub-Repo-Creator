# Checking dependencies.

# Checking pip3 dependency.
try {
  if (-not (Get-Command pip3 2> $null)) { throw }
} catch {
  Write-Host "[ERROR] " -ForegroundColor Red -NoNewline
  Write-Host "You don't have pip3 installed!"
  Exit 1
}

# Creating install folder (Windows does not allow "GRC" dir creation because shell script "grc" already exists on this dir).
New-Item GRC-Win-Install -type directory -Force > $null
cd GRC-Win-Install
Write-Host "[INFO] " -ForegroundColor Magenta -NoNewline
Write-Host "Created folder 'GRC-Win-Install', please do not move this folder to another path."

# Cloning repository.
Remove-Item GitHub-Repo-Creator -Force -Recurse 2> $null
git clone https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator.git 2> $null
cd GitHub-Repo-Creator
Write-Host "[INFO] " -ForegroundColor Magenta -NoNewline
Write-Host "Cloned GRC GitHub repository."

# Adding GRC to path if not already added.
$OldPath = [System.Environment]::GetEnvironmentVariable('Path',[System.EnvironmentVariableTarget]::User)
if ($OldPath.Length -lt 1) {
  # Invalid PATH length, abort addition.
  Write-Host "[ERROR] " -ForegroundColor Red -NoNewline
  Write-Host "Path environment variable getting failed! Please, open an issue reporting the problem!"
  Exit 1
}
$ToAdd = "$PWD;"
if ($OldPath.Contains($ToAdd)) {
  Write-Host "[INFO] " -ForegroundColor Magenta -NoNewline
  Write-Host "Repository directory already added to your PATH."
} else {
  $NewPath = "${OldPath}${ToAdd}"
  [System.Environment]::SetEnvironmentVariable('Path',$NewPath,[System.EnvironmentVariableTarget]::User)
  Write-Host "[INFO] " -ForegroundColor Magenta -NoNewline
  Write-Host "Added repository directory to your PATH."
}

# Installing python dependencies.
Write-Host "[INFO] " -ForegroundColor Magenta -NoNewline
Write-Host "Installing Python dependencies."
pip3 install -r ./.program-files/requirements.txt
Write-Host "[INFO] " -ForegroundColor Magenta -NoNewline
Write-Host "Installed Python dependencies."

Write-Host "[SUCCESS] " -ForegroundColor Green -NoNewline
Write-Host "You may close this terminal now for the changes to take effect."

cd ../..
