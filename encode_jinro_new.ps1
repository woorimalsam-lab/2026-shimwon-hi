$file = "C:\Users\admin\Downloads\2026_나이스_바이트_계산기(진로).xlsm"
Write-Host "File is: " $file
$bytes = [System.IO.File]::ReadAllBytes($file)
$b64 = [Convert]::ToBase64String($bytes)
$content = "const TEMPLATE_JINRO_B64 = `"" + $b64 + "`";"
[System.IO.File]::WriteAllText("template_jinro.js", $content, [System.Text.Encoding]::UTF8)
Write-Host "Jinro template encoded successfully."
