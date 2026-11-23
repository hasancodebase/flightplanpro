$ErrorActionPreference = 'Stop'
if (-not (Test-Path .\index.html) -or -not (Test-Path .\guides\index.html)) {
  Write-Host 'Run this script inside D:\flightplanpro (the folder with index.html).' -ForegroundColor Red
  exit 1
}
$enc = New-Object System.Text.UTF8Encoding($false)
$root = (Resolve-Path .).Path
$stamp = '2026-11-18'
$new = @(
  @{ slug='far-part-117-flight-duty-period-tables'; title='FAR Part 117 Limits: Flight Time and Flight Duty Period Tables Explained'; desc='The FAR Part 117 tables in one place: flight time, FDP for two-pilot and augmented crews, rest facility classes and key rest rules.' },
  @{ slug='what-is-a-tmi-number-aviation'; title='What Is a TMI Number in Aviation? NAT Track Message Number Explained'; desc='A TMI is the three-digit number of a NAT track message, based on the day of the year. See how it works and what a letter suffix means.' },
  @{ slug='edto-vs-etops-difference'; title='EDTO vs ETOPS: What Is the Difference?'; desc='EDTO and ETOPS compared: who uses each term, which aeroplanes are covered, how thresholds and diversion time work.' },
  @{ slug='flight-plan-fuel-calculation-worked-example'; title='Flight Plan Fuel Calculation: A Worked Example with Block Fuel'; desc='A complete worked example of block fuel: trip, contingency, alternate, final reserve and taxi, with every step shown.' }
)
function Read-Utf8($p) { [System.IO.File]::ReadAllText($p, [System.Text.Encoding]::UTF8) }
function Write-Utf8($p, $t) { [System.IO.File]::WriteAllText($p, $t, $enc) }
function Row($g) { '<a class="row" href="/guides/' + $g.slug + '/" data-a="pilot student dispatcher engineer hobbyist"><span class="n">' + $g.title + '</span><span class="d">' + $g.desc + '</span><span class="t">Guide</span></a>' }
function Li($g) { '<li><a href="/guides/' + $g.slug + '/">' + $g.title + '</a></li>' }
$missing = @($new | Where-Object { -not (Test-Path (Join-Path $root ('guides\' + $_.slug + '\index.html'))) })
if ($missing.Count -gt 0) { Write-Host 'The new guide pages are not in the site folder yet. Copy them first.' -ForegroundColor Red; exit 1 }
$done = 0

# 1. sitemap.xml
$p = Join-Path $root 'sitemap.xml'; $t = Read-Utf8 $p; $n = $t
foreach ($g in $new) {
  if ($n -notmatch [regex]::Escape('/guides/' + $g.slug + '/')) {
    $n = $n.Replace('</urlset>', '<url><loc>https://flightplanpro.net/guides/' + $g.slug + '/</loc><lastmod>' + $stamp + '</lastmod></url>' + "`n" + '</urlset>')
  }
}
if ($n -ne $t) { Write-Utf8 $p $n; $done++ }

# 2. Guides index and home page rows
$rows = ''
foreach ($g in $new) { $rows += (Row $g) }
foreach ($pair in @(@('guides\index.html', '</div></main>'), @('index.html', '</div><h2>Why trust the numbers</h2>'))) {
  $p = Join-Path $root $pair[0]; $t = Read-Utf8 $p
  if ($t -notmatch 'what-is-a-tmi-number-aviation' -and $t.Contains($pair[1])) {
    $i = $t.LastIndexOf($pair[1])
    Write-Utf8 $p ($t.Substring(0, $i) + $rows + $t.Substring($i)); $done++
  } elseif (-not $t.Contains($pair[1]) -and $t -notmatch 'what-is-a-tmi-number-aviation') {
    Write-Host ('Could not find the insert point in ' + $pair[0] + ' (skipped).') -ForegroundColor Yellow
  }
}

# 3. Site map page
$p = Join-Path $root 'site-map\index.html'; $t = Read-Utf8 $p
if ($t -notmatch 'what-is-a-tmi-number-aviation' -and $t.Contains('</ul><h2>About the site</h2>')) {
  $lis = ''; foreach ($g in $new) { $lis += (Li $g) }
  Write-Utf8 $p ($t.Replace('</ul><h2>About the site</h2>', $lis + '</ul><h2>About the site</h2>')); $done++
}

# 4. Links from related guides and tools
$map = @{
  'guides\faa-part-117-explained' = @('far-part-117-flight-duty-period-tables');
  'guides\easa-flight-time-limitations-basics' = @('far-part-117-flight-duty-period-tables');
  'tools\crew-duty-limits' = @('far-part-117-flight-duty-period-tables');
  'guides\nat-track-message-and-tmi-explained' = @('what-is-a-tmi-number-aviation');
  'guides\north-atlantic-organised-track-system-explained' = @('what-is-a-tmi-number-aviation');
  'guides\nat-oceanic-clearance-explained' = @('what-is-a-tmi-number-aviation');
  'guides\nat-hla-requirements-explained' = @('what-is-a-tmi-number-aviation');
  'guides\nat-contingency-and-slop-explained' = @('what-is-a-tmi-number-aviation');
  'tools\nat-tmi-calculator' = @('what-is-a-tmi-number-aviation');
  'guides\edto-explained' = @('edto-vs-etops-difference');
  'guides\edto-approval-and-dispatch' = @('edto-vs-etops-difference');
  'guides\adequate-vs-suitable-aerodrome' = @('edto-vs-etops-difference');
  'guides\polar-routes-explained' = @('edto-vs-etops-difference');
  'guides\equal-time-point-explained' = @('edto-vs-etops-difference');
  'tools\edto-planner' = @('edto-vs-etops-difference');
  'guides\flight-fuel-planning-explained' = @('flight-plan-fuel-calculation-worked-example');
  'guides\how-to-file-a-flight-plan' = @('flight-plan-fuel-calculation-worked-example');
  'guides\what-is-in-an-icao-flight-plan' = @('flight-plan-fuel-calculation-worked-example');
  'tools\fuel-planning-calculator' = @('flight-plan-fuel-calculation-worked-example')
}
foreach ($k in $map.Keys) {
  $p = Join-Path $root ($k + '\index.html')
  if (-not (Test-Path $p)) { continue }
  $t = Read-Utf8 $p; $n = $t
  foreach ($slug in $map[$k]) {
    $g = $new | Where-Object { $_.slug -eq $slug }
    if ($n -notmatch [regex]::Escape('/guides/' + $slug + '/')) {
      foreach ($a in @('<h2>More guides</h2><ul class="links">', '<h2>Related guides</h2><ul class="links">')) {
        if ($n.Contains($a)) { $n = $n.Replace($a, $a + (Li $g)); break }
      }
    }
  }
  if ($n -ne $t) { Write-Utf8 $p $n; $done++ }
}

# 5. Report
$sm = Read-Utf8 (Join-Path $root 'sitemap.xml')
Write-Host ''
Write-Host ('Files updated: ' + $done) -ForegroundColor Green
Write-Host ('Pages in sitemap: ' + ([regex]::Matches($sm, '<loc>')).Count + ' (should be 54)')
Write-Host 'Done. Delete this script, then deploy.'
