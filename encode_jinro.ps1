$files = Get-ChildItem -Path "C:\Users\admin\Downloads\*.xlsm"
foreach ($f in $files) {
    if ($f.Length -eq 180004) {
        Write-Host "Found file matching size 180004: " $f.FullName
        $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
        $b64 = [Convert]::ToBase64String($bytes)
        $content = 'const TEMPLATE_JINRO_B64 = "' + $b64 + '";'
        [System.IO.File]::WriteAllText('template_jinro.js', $content, [System.Text.Encoding]::UTF8)
        Write-Host "jinro template encoded successfully."
        break
    }
}
