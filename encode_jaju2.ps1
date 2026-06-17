$files = Get-ChildItem -Path 'C:\Users\admin\Downloads\*자율*.xlsm'
if ($files.Count -eq 0) {
    Write-Host "File not found"
    exit
}
$path = $files[0].FullName
$bytes = [System.IO.File]::ReadAllBytes($path)
$b64 = [Convert]::ToBase64String($bytes)
$content = 'const TEMPLATE_JAJU_B64 = "' + $b64 + '";'
[System.IO.File]::WriteAllText('c:\Users\admin\Desktop\생활기록부\template_jaju.js', $content, [System.Text.Encoding]::UTF8)
Write-Host "jaju template encoded."
