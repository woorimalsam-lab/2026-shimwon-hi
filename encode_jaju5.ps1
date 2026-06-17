$files = Get-ChildItem -Path "C:\Users\admin\Downloads\*.xlsm"
foreach ($f in $files) {
    if ($f.Length -eq 760132) {
        Write-Host "Found file matching size 760132: " $f.FullName
        $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
        $b64 = [Convert]::ToBase64String($bytes)
        $content = 'const TEMPLATE_JAJU_B64 = "' + $b64 + '";'
        [System.IO.File]::WriteAllText('template_jaju.js', $content, [System.Text.Encoding]::UTF8)
        Write-Host "jaju template encoded successfully."
        break
    }
}
