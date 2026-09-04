param(
    [string]$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path,
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\supplementary')
)

$ErrorActionPreference = 'Stop'

$shelves = @(
    'Introductory_Chemistry',
    'General_Chemistry',
    'Organic_Chemistry',
    'Inorganic_Chemistry',
    'Analytical_Chemistry',
    'Physical_and_Theoretical_Chemistry_Textbook_Maps',
    'Biological_Chemistry',
    'Environmental_Chemistry'
)

function Get-CanonicalTitleKey {
    param([Parameter(Mandatory)][string]$Title)

    $key = $Title -replace '^(Map|Book):\s*', ''
    $key = $key.ToLowerInvariant() -replace '[^a-z0-9]+', ' '
    return ($key -replace '\s+', ' ').Trim()
}

$memoryRoot = Join-Path $RepositoryRoot 'chem-memory'
$corpusFiles = Get-ChildItem -LiteralPath $memoryRoot -Recurse -File -Include *.md,*.json,*.py,*.txt |
    Where-Object { $_.FullName -notmatch '\\__pycache__\\' }
$corpusText = ($corpusFiles | ForEach-Object {
    try {
        Get-Content -LiteralPath $_.FullName -Raw -ErrorAction Stop
    }
    catch {
        # Binary or concurrently replaced files are outside this text-only audit.
    }
}) -join "`n"

$retrievedAtUtc = [DateTimeOffset]::UtcNow
$rows = foreach ($shelf in $shelves) {
    $pagePath = [Uri]::EscapeDataString("Bookshelves/$shelf")
    $apiUrl = "https://chem.libretexts.org/@api/deki/pages/=$pagePath/subpages?limit=all&dream.out.format=json"
    $response = Invoke-RestMethod -Uri $apiUrl -Method Get -TimeoutSec 90

    foreach ($item in @($response.'page.subpage')) {
        $title = [string]$item.title
        $uri = [string]$item.'uri.ui'
        $decodedUri = [Uri]::UnescapeDataString($uri)
        $slug = ($decodedUri -split '/')[-1]
        $slugWithoutPrefix = $slug -replace '^(Book:|Map:)_?', ''
        $variants = @($uri, $decodedUri, $slug, $slugWithoutPrefix) | Sort-Object -Unique

        $hasExactTrace = $false
        foreach ($variant in $variants) {
            if ($variant.Length -gt 8 -and
                $corpusText.IndexOf($variant, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $hasExactTrace = $true
                break
            }
        }

        [pscustomobject]@{
            shelf = $shelf
            page_id = [string]$item.'@id'
            title = $title
            canonical_title_key = Get-CanonicalTitleKey -Title $title
            uri = $uri
            article_type = (@($item.article) -join ';')
            created_at = ([DateTimeOffset]::Parse([string]$item.'date.created')).ToString('o')
            modified_at = ([DateTimeOffset]::Parse([string]$item.'date.modified')).ToString('o')
            is_supplemental_container = $title -like 'Supplemental Modules*'
            repository_trace = if ($hasExactTrace) { 'exact_title_or_root_trace' } else { 'no_exact_title_or_root_trace' }
            reading_status = 'requires_manual_evidence_adjudication'
        }
    }
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null

$csvPath = Join-Path $OutputDirectory 'libretexts_live_catalog_audit.csv'
$canonicalCsvPath = Join-Path $OutputDirectory 'libretexts_canonical_work_audit.csv'
$jsonPath = Join-Path $OutputDirectory 'libretexts_live_catalog_snapshot.json'
$summaryPath = Join-Path $OutputDirectory 'libretexts_live_catalog_summary.md'

$rows | Sort-Object shelf, title | Export-Csv -LiteralPath $csvPath -NoTypeInformation -Encoding utf8
$snapshot = [ordered]@{
    schema = 'chemtester-libretexts-catalog-snapshot/v1'
    retrieved_at_utc = $retrievedAtUtc.ToString('o')
    source = 'https://chem.libretexts.org/Bookshelves'
    api_scope = 'immediate subpages of the eight curated Chemistry LibreTexts shelves'
    rows = @($rows | Sort-Object shelf, title)
}
$snapshot | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding utf8

$rawCount = @($rows).Count
$supplementalCount = @($rows | Where-Object is_supplemental_container).Count
$namedRows = @($rows | Where-Object { -not $_.is_supplemental_container })
$workGroups = @($namedRows | Group-Object canonical_title_key)
$canonicalCount = $workGroups.Count
$traceCount = @($workGroups | Where-Object { $_.Group.repository_trace -contains 'exact_title_or_root_trace' }).Count
$noTraceCount = $canonicalCount - $traceCount
$canonicalWorks = $workGroups | Sort-Object Name | ForEach-Object {
    $group = $_.Group
    $hasTrace = $group.repository_trace -contains 'exact_title_or_root_trace'
    [pscustomobject]@{
        canonical_title_key = $_.Name
        representative_title = ($group.title | Sort-Object | Select-Object -First 1)
        shelves = (@($group.shelf | Sort-Object -Unique) -join ';')
        catalog_row_count = $_.Count
        titles = (@($group.title | Sort-Object -Unique) -join ';')
        uris = (@($group.uri | Sort-Object -Unique) -join ';')
        repository_trace = if ($hasTrace) { 'exact_title_or_root_trace' } else { 'no_exact_title_or_root_trace' }
        reading_status = 'requires_manual_evidence_adjudication'
    }
}
$canonicalWorks | Export-Csv -LiteralPath $canonicalCsvPath -NoTypeInformation -Encoding utf8
$createdAfterBaseline = @($rows | Where-Object {
    [DateTimeOffset]::Parse($_.created_at) -gt [DateTimeOffset]'2026-04-11T00:00:00Z'
}).Count
$modifiedAfterBaseline = @($rows | Where-Object {
    [DateTimeOffset]::Parse($_.modified_at) -gt [DateTimeOffset]'2026-04-11T00:00:00Z'
}).Count

$shelfTable = $rows | Group-Object shelf | Sort-Object Name | ForEach-Object {
    "| $($_.Name) | $($_.Count) |"
}
$duplicateTable = $workGroups | Where-Object Count -gt 1 | Sort-Object Name | ForEach-Object {
    $titles = ($_.Group | ForEach-Object { ('`{0}`' -f $_.title) }) -join '<br>'
    "| $($_.Name) | $($_.Count) | $titles |"
}

$summary = @"
# Live Chemistry LibreTexts catalog audit

- Retrieved (UTC): $($retrievedAtUtc.ToString('o'))
- Source: https://chem.libretexts.org/Bookshelves
- Raw immediate shelf entries: $rawCount
- Generic supplemental-module containers: $supplementalCount
- Named entries before alias collapse: $($namedRows.Count)
- Canonical named works after title normalization: $canonicalCount
- Canonical works with an exact title or book-root trace in `chem-memory`: $traceCount
- Canonical works with no exact repository trace: $noTraceCount
- Entries created after the 2026-04-11 repository baseline: $createdAfterBaseline
- Entries modified after the 2026-04-11 repository baseline: $modifiedAfterBaseline

## Shelf counts

| Shelf | Raw immediate entries |
|---|---:|
$($shelfTable -join "`n")

## Duplicate or alias title groups

| Canonical key | Rows | Titles |
|---|---:|---|
$($duplicateTable -join "`n")

## Interpretation boundary

An exact repository trace proves only that a title or book root appears in the current project. It does not by itself prove that the book was read completely or that its content entered the active compact skill. A no-exact-trace result can include renamed or moved LibreTexts pages, so it is a screening result rather than proof that a source was never used. Manual adjudication is required to distinguish extracted, partially extracted, assessed-only, blocked, merely discovered, and untraced sources.
"@
$summary | Set-Content -LiteralPath $summaryPath -Encoding utf8

$jsonHash = (Get-FileHash -LiteralPath $jsonPath -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Output "CSV: $csvPath"
Write-Output "Canonical CSV: $canonicalCsvPath"
Write-Output "JSON: $jsonPath"
Write-Output "JSON SHA256: $jsonHash"
Write-Output "Summary: $summaryPath"
Write-Output "Raw=$rawCount Supplemental=$supplementalCount Canonical=$canonicalCount Traced=$traceCount NoTrace=$noTraceCount"
