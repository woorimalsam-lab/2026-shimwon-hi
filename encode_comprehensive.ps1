$files = Get-ChildItem -Path "C:\Users\admin\Downloads\*.xlsm"
foreach ($f in $files) {
    if ($f.Length -eq 462734) {
        Write-Host "Found file matching size 462734: " $f.FullName
        $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
        $b64 = [Convert]::ToBase64String($bytes)
        $content = 'const TEMPLATE_COMPREHENSIVE_B64 = "' + $b64 + '";'
        [System.IO.File]::WriteAllText('template_comprehensive.js', $content, [System.Text.Encoding]::UTF8)
        Write-Host "comprehensive template encoded successfully."
        break
    }
}
