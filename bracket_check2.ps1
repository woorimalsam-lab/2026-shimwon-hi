$files = Get-ChildItem -Filter "*_*.html"
if ($files.Count -eq 0) {
    Write-Host "No HTML file found."
    exit
}
$path = $files[0].FullName
$lines = [System.IO.File]::ReadAllLines($path, [System.Text.Encoding]::UTF8)

$open = 0
$close = 0
for ($i=0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    $open += ($line.ToCharArray() | Where-Object { $_ -eq '{' }).Count
    $close += ($line.ToCharArray() | Where-Object { $_ -eq '}' }).Count
    if ($close -gt $open) {
        Write-Host "Mismatch at line $(($i+1)): Open=$open, Close=$close"
        Write-Host "Line content: $line"
        break
    }
}
Write-Host "Total Open: $open, Total Close: $close"
