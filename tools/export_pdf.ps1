param(
    [Parameter(Mandatory=$true)][string]$DocxPath,
    [Parameter(Mandatory=$true)][string]$PdfPath
)
$wordApp = $null
$doc = $null
try {
    Write-Output 'Starting Word'
    $wordApp = New-Object -ComObject Word.Application
    Write-Output 'Word started'
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $doc = $wordApp.Documents.Open((Resolve-Path -LiteralPath $DocxPath).Path, $false, $true)
    Write-Output 'Document opened'
    $doc.ExportAsFixedFormat($PdfPath, 17)
    Write-Output 'PDF exported'
} finally {
    if ($doc -ne $null) { $doc.Close($false) | Out-Null }
    if ($wordApp -ne $null) { $wordApp.Quit() | Out-Null }
}
