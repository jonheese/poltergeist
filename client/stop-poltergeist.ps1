Get-Process | Where-Object {$_.ProcessName -eq "pythonw"} | Stop-Process -Force
