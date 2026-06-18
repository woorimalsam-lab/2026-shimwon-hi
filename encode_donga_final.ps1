$file = Get-ChildItem -Path "C:\Users\admin\Downloads\2026_나이스_바이트_계산기(동아리).xlsm" | Select-Object -First 1
Write-Host "Found file: " $file.FullName
$bytes = [System.IO.File]::ReadAllBytes($file.FullName)
$b64 = [Convert]::ToBase64String($bytes)
$content = "const TEMPLATE_DONGA_B64 = `"" + $b64 + "`";"
[System.IO.File]::WriteAllText("template_donga.js", $content, [System.Text.Encoding]::UTF8)
Write-Host "Donga template encoded successfully."
