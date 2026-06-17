$files = Get-ChildItem -Path "C:\Users\admin\Downloads\*.xlsm"
foreach ($f in $files) {
    if ($f.Length -eq 17618) {
        Write-Host "Found file matching size 17618: " $f.FullName
        $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
        $b64 = [Convert]::ToBase64String($bytes)
        $content = 'const TEMPLATE_SUBJECT_B64 = "' + $b64 + '";'
        [System.IO.File]::WriteAllText('template_subject.js', $content, [System.Text.Encoding]::UTF8)
        Write-Host "subject template encoded successfully."
        break
    }
}
