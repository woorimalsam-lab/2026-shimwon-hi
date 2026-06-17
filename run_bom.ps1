$scriptPath = "c:\Users\admin\Desktop\생활기록부\clean_html7.ps1"
$bomPath = "c:\Users\admin\Desktop\생활기록부\clean_html7_bom.ps1"
$bytes = [System.IO.File]::ReadAllBytes($scriptPath)
$bom = [byte[]](239,187,191)
$newBytes = $bom + $bytes
[System.IO.File]::WriteAllBytes($bomPath, $newBytes)
& powershell -ExecutionPolicy Bypass -File $bomPath
