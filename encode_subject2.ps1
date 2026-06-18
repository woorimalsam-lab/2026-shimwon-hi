$file = "C:\Users\admin\Downloads\2026_나이스_바이트_계산기(교과세특).xlsm"
$bytes = [System.IO.File]::ReadAllBytes($file)
$b64 = [Convert]::ToBase64String($bytes)
$content = 'const TEMPLATE_SUBJECT_B64 = "' + $b64 + '";'
[System.IO.File]::WriteAllText('template_subject.js', $content, [System.Text.Encoding]::UTF8)
Write-Host "Subject template encoded successfully."
