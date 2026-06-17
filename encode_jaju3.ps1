$files = Get-ChildItem -Path "C:\Users\admin\Downloads\*.xlsm"
foreach ($f in $files) {
    if ($f.Length -eq 126175) {
        Write-Host "Found file matching size 126175: " $f.FullName
        $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
        $b64 = [Convert]::ToBase64String($bytes)
        $content = 'const TEMPLATE_JAJU_B64 = "' + $b64 + '";'
        [System.IO.File]::WriteAllText('c:\Users\admin\Desktop\생활기록부\template_jaju.js', $content, [System.Text.Encoding]::UTF8)
        Write-Host "jaju template encoded."
        break
    }
}
