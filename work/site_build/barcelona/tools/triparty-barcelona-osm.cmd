@echo off
title Triparty Barcelona OSM
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex (((Get-Content -Raw -LiteralPath '%~f0') -split '(?m)^#PSBEGIN\r?$',2)[1])"
echo.
pause
exit /b
#PSBEGIN
$ProgressPreference='SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
[Net.ServicePointManager]::Expect100Continue=$false
$ua='Triparty-city-build/1.1 (personal travel guide)'
$desk=[Environment]::GetFolderPath('Desktop'); if(-not $desk){ $desk=$HOME }
$dir=Join-Path $desk 'triparty-bcn-osm'
$zip=Join-Path $desk 'triparty-bcn-osm.zip'
if(Test-Path $dir){ Remove-Item $dir -Recurse -Force }
New-Item -ItemType Directory -Force $dir | Out-Null
$logf=Join-Path $dir '_log.txt'
function Log($s){ Write-Host $s; Add-Content -Path $logf -Value $s }
function ErrText($e){
  $m=$e.Exception.Message
  try{ $r=$e.Exception.Response; if($r){ $m+=' | HTTP '+[int]$r.StatusCode; $sr=New-Object IO.StreamReader($r.GetResponseStream()); $b=$sr.ReadToEnd(); if($b.Length -gt 600){ $b=$b.Substring(0,600) }; $m+=' | '+($b -replace '\s+',' ') } } catch {}
  return $m
}
function Good($f){ if(!(Test-Path $f)){ return $false }; $fs=[IO.File]::OpenRead($f); $b=New-Object byte[] 1; [void]$fs.Read($b,0,1); $len=$fs.Length; $fs.Close(); return ($b[0] -eq 123 -and $len -gt 150) }
$eps=@('https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter','https://maps.mail.ru/osm/tools/overpass/api/interpreter')
$rows=@(
'test|0|%5Bout%3Ajson%5D%5Btimeout%3A25%5D%3Bnode%5B%22tourism%22%3D%22artwork%22%5D%2841.380%2C2.170%2C41.384%2C2.176%29%3Bout%205%3B'
'art|0|%5Bout%3Ajson%5D%5Btimeout%3A180%5D%3B%28area%283600347950%29%3Barea%5B%22wikidata%22%3D%22Q1492%22%5D%5B%22admin_level%22%3D%228%22%5D%3B%29-%3E.a%3B%28nwr%5B%22tourism%22%3D%22artwork%22%5D%28area.a%29%3Bnwr%5B%22historic%22~%22%5E%28memorial%7Cmonument%29%24%22%5D%28area.a%29%3Bnwr%5B%22amenity%22%3D%22fountain%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22amenity%22%3D%22fountain%22%5D%5B%22wikidata%22%5D%28area.a%29%3B%29%3Bout%20center%20tags%3B'
'art|1|%5Bout%3Ajson%5D%5Btimeout%3A180%5D%5Bbbox%3A41.317%2C2.052%2C41.470%2C2.230%5D%3B%28nwr%5B%22tourism%22%3D%22artwork%22%5D%3Bnwr%5B%22historic%22~%22%5E%28memorial%7Cmonument%29%24%22%5D%3Bnwr%5B%22amenity%22%3D%22fountain%22%5D%5B%22name%22%5D%3Bnwr%5B%22amenity%22%3D%22fountain%22%5D%5B%22wikidata%22%5D%3B%29%3Bout%20center%20tags%3B'
'poi|0|%5Bout%3Ajson%5D%5Btimeout%3A180%5D%3B%28area%283600347950%29%3Barea%5B%22wikidata%22%3D%22Q1492%22%5D%5B%22admin_level%22%3D%228%22%5D%3B%29-%3E.a%3B%28nwr%5B%22tourism%22~%22%5E%28attraction%7Cmuseum%7Cgallery%7Cviewpoint%7Czoo%7Caquarium%29%24%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22historic%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22amenity%22~%22%5E%28place_of_worship%7Cmarketplace%7Ctheatre%7Carts_centre%7Cnightclub%29%24%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22leisure%22~%22%5E%28park%7Cgarden%7Cwater_park%29%24%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22building%22%5D%5B%22wikidata%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22shop%22~%22%5E%28mall%7Cdepartment_store%29%24%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22natural%22%3D%22beach%22%5D%28area.a%29%3Bnwr%5B%22place%22%3D%22square%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22aerialway%22%3D%22station%22%5D%28area.a%29%3B%29%3Bout%20center%20tags%3B'
'poi|1|%5Bout%3Ajson%5D%5Btimeout%3A180%5D%5Bbbox%3A41.317%2C2.052%2C41.470%2C2.230%5D%3B%28nwr%5B%22tourism%22~%22%5E%28attraction%7Cmuseum%7Cgallery%7Cviewpoint%7Czoo%7Caquarium%29%24%22%5D%5B%22name%22%5D%3Bnwr%5B%22historic%22%5D%5B%22name%22%5D%3Bnwr%5B%22amenity%22~%22%5E%28place_of_worship%7Cmarketplace%7Ctheatre%7Carts_centre%7Cnightclub%29%24%22%5D%5B%22name%22%5D%3Bnwr%5B%22leisure%22~%22%5E%28park%7Cgarden%7Cwater_park%29%24%22%5D%5B%22name%22%5D%3Bnwr%5B%22building%22%5D%5B%22wikidata%22%5D%5B%22name%22%5D%3Bnwr%5B%22shop%22~%22%5E%28mall%7Cdepartment_store%29%24%22%5D%5B%22name%22%5D%3Bnwr%5B%22natural%22%3D%22beach%22%5D%3Bnwr%5B%22place%22%3D%22square%22%5D%5B%22name%22%5D%3Bnwr%5B%22aerialway%22%3D%22station%22%5D%3B%29%3Bout%20center%20tags%3B'
'fun|0|%5Bout%3Ajson%5D%5Btimeout%3A180%5D%5Bbbox%3A41.15%2C1.55%2C41.80%2C2.65%5D%3B%28nwr%5B%22leisure%22~%22%5E%28escape_game%7Camusement_arcade%7Cbowling_alley%7Chigh_ropes_course%7Cskatepark%7Cwater_park%7Ctrampoline_park%7Cminiature_golf%29%24%22%5D%3Bnwr%5B%22sport%22~%22karting%7Cpaintball%7Claser_tag%7Cbilliards%7Csnooker%7Cbowling%7C10pin%22%5D%3Bnwr%5B%22sport%22~%22climbing%22%5D%5B%22leisure%22%5D%3Bnwr%5B%22tourism%22%3D%22theme_park%22%5D%3Bnwr%5B%22attraction%22~%22summer_toboggan%7Croller_coaster%7Calpine_coaster%22%5D%3Bnwr%5B%22aerialway%22%3D%22zip_line%22%5D%3Bnwr%5B%22theatre%3Agenre%22%3D%22circus%22%5D%3B%29%3Bout%20center%20tags%3B'
'fun2|0|%5Bout%3Ajson%5D%5Btimeout%3A180%5D%5Bbbox%3A41.25%2C1.90%2C41.60%2C2.40%5D%3B%28nwr%5B%22leisure%22%5D%5B%22name%22~%22jet%20ski%7Cjetski%7Cvirtual%7Cquad%7Cbuggy%7Crage%7Ccircus%7Cescape%7Claser%22%2Ci%5D%3Bnwr%5B%22amenity%22%5D%5B%22name%22~%22jet%20ski%7Cjetski%7Cvirtual%7Cquad%7Cbuggy%7Crage%7Ccircus%7Cescape%7Claser%22%2Ci%5D%3Bnwr%5B%22shop%22%5D%5B%22name%22~%22jet%20ski%7Cjetski%7Cvirtual%7Cquad%7Cbuggy%7Crage%7Ccircus%7Cescape%7Claser%22%2Ci%5D%3Bnwr%5B%22tourism%22%5D%5B%22name%22~%22jet%20ski%7Cjetski%7Cvirtual%7Cquad%7Cbuggy%7Crage%7Ccircus%7Cescape%7Claser%22%2Ci%5D%3B%29%3Bout%20center%20tags%3B'
'kosher|0|%5Bout%3Ajson%5D%5Btimeout%3A90%5D%5Bbbox%3A41.30%2C2.05%2C41.47%2C2.25%5D%3B%28nwr%5B%22diet%3Akosher%22%5D%3Bnwr%5B%22amenity%22%3D%22place_of_worship%22%5D%5B%22religion%22%3D%22jewish%22%5D%3Bnwr%5B%22cuisine%22~%22kosher%7Cjewish%7Cisraeli%22%5D%3Bnwr%5B%22name%22~%22kosher%7Cchabad%7Cjabad%7Csinagoga%22%2Ci%5D%3B%29%3Bout%20center%20tags%3B'
)
$done=@{}
Log ('=== Triparty Barcelona OSM, PowerShell ' + $PSVersionTable.PSVersion.ToString() + ' ===')
foreach($row in $rows){
  $k,$v,$q=$row -split '\|',3
  if($done[$k]){ continue }
  $out=Join-Path $dir ('osm_'+$k+'.json')
  foreach($ep in $eps){
    foreach($mode in @('POST','GET')){
      if($done[$k]){ break }
      Log ('OSM ' + $k + ' v' + $v + ' ' + $mode + ' <- ' + $ep)
      try{
        if($mode -eq 'POST'){ Invoke-WebRequest -Uri $ep -Method Post -Body ('data='+$q) -ContentType 'application/x-www-form-urlencoded' -OutFile $out -UseBasicParsing -UserAgent $ua -TimeoutSec 300 -ErrorAction Stop }
        else{ if($q.Length -gt 1800){ Log '  (query too long for GET, skipped)'; continue }; Invoke-WebRequest -Uri ($ep+'?data='+$q) -OutFile $out -UseBasicParsing -UserAgent $ua -TimeoutSec 300 -ErrorAction Stop }
        if(Good $out){ $done[$k]=$true; Log ('  OK ' + [Math]::Round((Get-Item $out).Length/1KB) + ' KB') }
        else{ $t=''; try{ $t=[IO.File]::ReadAllText($out); if($t.Length -gt 400){ $t=$t.Substring(0,400) } } catch {}; Log ('  BAD RESPONSE: ' + ($t -replace '\s+',' ')) }
      } catch { Log ('  ERROR: ' + (ErrText $_)) }
      Start-Sleep -Seconds 3
    }
    if($done[$k]){ break }
  }
  if(-not $done[$k]){ if(Test-Path $out){ Remove-Item $out -Force } }
  Start-Sleep -Seconds 4
}
# Wikidata for artworks
$artFile=Join-Path $dir 'osm_art.json'
if(Test-Path $artFile){
  $txt=[IO.File]::ReadAllText($artFile,[Text.Encoding]::UTF8)
  $ids=@([regex]::Matches($txt,'wikidata"\s*:\s*"([^"]+)"') | ForEach-Object { $_.Groups[1].Value -split '\s*;\s*' } | Where-Object { $_ -match '^Q\d+$' } | Select-Object -Unique)
  Log ('Wikidata ids: ' + $ids.Count); $n=0
  for($i=0;$i -lt $ids.Count;$i+=50){
    $hi=[Math]::Min($i+49,$ids.Count-1); $chunk=$ids[$i..$hi] -join '%7C'
    $u='https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids='+$chunk+'&props=labels%7Cdescriptions%7Csitelinks%7Cclaims&languages=he%7Cen%7Cca%7Ces&sitefilter=hewiki%7Cenwiki%7Ccawiki%7Ceswiki'
    try{ Invoke-WebRequest -Uri $u -OutFile (Join-Path $dir ('wd_'+('{0:d3}' -f $n)+'.json')) -UseBasicParsing -UserAgent $ua -TimeoutSec 120 -ErrorAction Stop; Write-Host ('WD batch ' + ($n+1) + ' OK') } catch { Log ('WD batch ' + ($n+1) + ' ERROR: ' + (ErrText $_)) }
    $n++; Start-Sleep -Milliseconds 400
  }
  Log ('wikidata batches: ' + $n)
}
if(Test-Path $zip){ Remove-Item $zip -Force }
Compress-Archive -Path (Join-Path $dir '*') -DestinationPath $zip -Force
Write-Host ''
Write-Host ('Done. ZIP file: ' + $zip + '  (' + [Math]::Round((Get-Item $zip).Length/1MB,2) + ' MB)') -ForegroundColor Green
