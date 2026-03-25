$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$templatePath = Join-Path $root "brand-template.html"
$dataPath = Join-Path $root "brand-data.json"
$exportPdf = $true

$template = Get-Content $templatePath -Raw -Encoding UTF8
$brands = Get-Content $dataPath -Raw -Encoding UTF8 | ConvertFrom-Json

function Escape-Html {
    param([string]$Value)
    if ($null -eq $Value) { return "" }

    $escaped = $Value.Replace("&", "&amp;")
    $escaped = $escaped.Replace("<", "&lt;")
    $escaped = $escaped.Replace(">", "&gt;")
    $escaped = $escaped.Replace('"', "&quot;")
    return $escaped
}

function Escape-HtmlAttribute {
    param([string]$Value)
    return Escape-Html $Value
}

function Get-TokenNames {
    param([string]$Html)

    $matches = [regex]::Matches($Html, '\{\{([A-Z0-9_]+)\}\}')
    $names = New-Object System.Collections.Generic.HashSet[string]

    foreach ($m in $matches) {
        [void]$names.Add($m.Groups[1].Value)
    }

    return @($names)
}

function Apply-Tokens {
    param(
        [string]$Html,
        [hashtable]$Tokens
    )

    $result = $Html
    foreach ($key in $Tokens.Keys) {
        $result = $result.Replace("{{${key}}}", [string]$Tokens[$key])
    }
    return $result
}

function Validate-Tokens {
    param(
        [string]$Html,
        [hashtable]$Tokens,
        [string]$BrandName
    )

    $templateTokens = Get-TokenNames $Html
    $missing = @()

    foreach ($name in $templateTokens) {
        if (-not $Tokens.ContainsKey($name)) {
            $missing += $name
        }
    }

    if ($missing.Count -gt 0) {
        throw "Missing tokens for ${BrandName}: $($missing -join ', ')"
    }
}

function Get-ChromePath {
    $candidates = @(
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    )

    foreach ($path in $candidates) {
        if (Test-Path $path) {
            return $path
        }
    }

    return $null
}

function Export-PdfIfPossible {
    param(
        [string]$BrowserPath,
        [string]$HtmlPath,
        [string]$PdfPath,
        [string]$Root
    )

    if (-not $BrowserPath) {
        Write-Warning "Skipping PDF export because Chrome/Edge was not found."
        return
    }

    $tempProfile = Join-Path $Root "tmp-chrome-export"
    if (-not (Test-Path $tempProfile)) {
        New-Item -ItemType Directory -Path $tempProfile | Out-Null
    }

    $fileUrl = "file:///" + ($HtmlPath -replace '\\', '/')
    $args = @(
        "--headless=new"
        "--disable-gpu"
        "--allow-file-access-from-files"
        "--user-data-dir=$tempProfile"
        "--print-to-pdf=$PdfPath"
        $fileUrl
    )

    Start-Process -FilePath $BrowserPath -ArgumentList $args -Wait -NoNewWindow
}

$browserPath = Get-ChromePath

foreach ($brand in $brands) {
    if ($brand.amenities.Count -lt 3) {
        throw "$($brand.name) must have at least 3 amenities."
    }

    if ($brand.logoRules.Count -lt 3) {
        throw "$($brand.name) must have at least 3 logo rules."
    }

    $tokens = @{
        BRAND_NAME       = Escape-Html $brand.name
        TAGLINE          = Escape-Html $brand.tagline
        SUBTITLE         = Escape-Html $brand.subtitle
        HEADING          = Escape-Html $brand.heading
        PULL_QUOTE       = Escape-Html $brand.pullQuote
        BODY_COPY        = Escape-Html $brand.bodyCopy
        TONE_1           = Escape-Html $brand.tone1
        TONE_2           = Escape-Html $brand.tone2
        TONE_3           = Escape-Html $brand.tone3
        COLORWAY_NOTE    = Escape-Html $brand.colorwayNote
        LOGO_RULE_1      = Escape-Html $brand.logoRules[0]
        LOGO_RULE_2      = Escape-Html $brand.logoRules[1]
        LOGO_RULE_3      = Escape-Html $brand.logoRules[2]
        FOOTER_CITY      = Escape-Html $brand.footerCity
        FOOTER_YEAR      = Escape-Html ([string]$brand.footerYear)

        AMENITY_1_NAME   = Escape-Html $brand.amenities[0].name
        AMENITY_1_DESC   = Escape-Html $brand.amenities[0].desc
        AMENITY_2_NAME   = Escape-Html $brand.amenities[1].name
        AMENITY_2_DESC   = Escape-Html $brand.amenities[1].desc
        AMENITY_3_NAME   = Escape-Html $brand.amenities[2].name
        AMENITY_3_DESC   = Escape-Html $brand.amenities[2].desc

        IMG_COVER        = Escape-HtmlAttribute $brand.images.cover
        IMG_PHOTO_LEFT   = Escape-HtmlAttribute $brand.images.photoLeft
        IMG_PHOTO_RIGHT  = Escape-HtmlAttribute $brand.images.photoRight
        IMG_AMENITIES_BG = Escape-HtmlAttribute $brand.images.amenitiesBg
        IMG_HOARDING_BG  = Escape-HtmlAttribute $brand.images.hoardingBg
        IMG_BACK_BG      = Escape-HtmlAttribute $brand.images.backBg

        INITIAL          = Escape-Html $brand.name.Substring(0, 1)

        CSS_PRIMARY      = $brand.css.primary
        CSS_SURFACE      = $brand.css.surface
        CSS_ACCENT       = $brand.css.accent
        CSS_LIGHT        = $brand.css.light
        CSS_RESERVE      = $brand.css.reserve
        CSS_TEXT_DARK    = $brand.css.textDark
        CSS_TEXT_LIGHT   = $brand.css.textLight
        CSS_SERIF        = $brand.css.serif
        CSS_SANS         = $brand.css.sans
        CSS_MONO         = $brand.css.mono
    }

    Validate-Tokens -Html $template -Tokens $tokens -BrandName $brand.name

    $html = Apply-Tokens -Html $template -Tokens $tokens

    $unresolvedTokens = Get-TokenNames $html
    if ($unresolvedTokens.Count -gt 0) {
        throw "Unresolved tokens remain in $($brand.name): $($unresolvedTokens -join ', ')"
    }

    $htmlPath = Join-Path $root $brand.file
    Set-Content -Path $htmlPath -Value $html -Encoding UTF8
    Write-Host "Generated HTML: $($brand.file)"

    if ($exportPdf) {
        $pdfFile = [System.IO.Path]::ChangeExtension($brand.file, ".pdf")
        $pdfPath = Join-Path $root $pdfFile
        Export-PdfIfPossible -BrowserPath $browserPath -HtmlPath $htmlPath -PdfPath $pdfPath -Root $root

        if (Test-Path $pdfPath) {
            Write-Host "Generated PDF:  $pdfFile"
        }
        else {
            Write-Warning "PDF export did not produce $pdfFile"
        }
    }
}
