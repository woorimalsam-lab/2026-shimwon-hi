$files = Get-ChildItem -Filter "*_*.html"
if ($files.Count -eq 0) {
    Write-Host "No HTML file found."
    exit
}
$path = $files[0].FullName
$lines = [System.IO.File]::ReadAllLines($path, [System.Text.Encoding]::UTF8)
$correctLines = [System.IO.File]::ReadAllLines("C:\Users\admin\.gemini\antigravity\brain\82c53537-b278-4135-844c-8a2059f5b189\scratch\correct_json.txt", [System.Text.Encoding]::UTF8)

[string[]]$newLines = @()

for ($i = 0; $i -lt $lines.Length; $i++) {
    $lineNum = $i + 1
    
    if ($lineNum -ge 5886 -and $lineNum -le 5974) {
        if ($lineNum -eq 5886) {
            foreach ($cL in $correctLines) {
                $newLines += $cL
            }
        }
        continue
    }

    $newLines += $lines[$i]
}

[System.IO.File]::WriteAllLines($path, $newLines, [System.Text.Encoding]::UTF8)
Write-Host "Replaced lines 5886 to 5974 with correct JSON from file!"
