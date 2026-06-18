$file = Get-ChildItem -Path "C:\Users\admin\Downloads\*교과세특*.xlsm" | Select-Object -First 1
Write-Host "Found file:" $file.FullName
$bytes = [System.IO.File]::ReadAllBytes($file.FullName)
$b64 = [Convert]::ToBase64String($bytes)
$content = "const TEMPLATE_SUBJECT_B64 = `"$b64`";"
[System.IO.File]::WriteAllText("template_subject.js", $content, [System.Text.Encoding]::UTF8)
Write-Host "Done"
