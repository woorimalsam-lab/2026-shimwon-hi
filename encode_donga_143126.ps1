$files = Get-ChildItem -Path "C:\Users\admin\Downloads\*.xlsm"
foreach ($f in $files) {
    if ($f.Length -eq 143126) {
        Write-Host "Found donga file matching size 143126: " $f.FullName
        $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
        $b64 = [Convert]::ToBase64String($bytes)
        $content = "const TEMPLATE_DONGA_B64 = `"" + $b64 + "`";"
        [System.IO.File]::WriteAllText("template_donga.js", $content, [System.Text.Encoding]::UTF8)
        Write-Host "Donga template encoded successfully."
        break
    }
}
