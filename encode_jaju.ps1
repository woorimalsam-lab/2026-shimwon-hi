$bytes = [System.IO.File]::ReadAllBytes('C:\Users\admin\Downloads\2026_나이스_바이트_계산기(자율).xlsm')
$b64 = [Convert]::ToBase64String($bytes)
$content = 'const TEMPLATE_JAJU_B64 = "' + $b64 + '";'
[System.IO.File]::WriteAllText('c:\Users\admin\Desktop\생활기록부\template_jaju.js', $content, [System.Text.Encoding]::UTF8)
Write-Host "jaju template encoded."
