# Automated Daily Earnings Runner Script
# Sets directory, executes daily_runner.py with 60s multi-company stagger delay

$WorkingDir = "C:\Users\nitin\.earningreport"
Set-Location -Path $WorkingDir

$PythonExe = "C:\Python314\python.exe"
$RunnerScript = "$WorkingDir\daily_runner.py"

& $PythonExe $RunnerScript 60
