@echo off
title Triparty Porto data
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex (((Get-Content -Raw -LiteralPath '%~f0') -split '(?m)^#PSBEGIN\r?$',2)[1])"
echo.
pause
exit /b
#PSBEGIN
$ProgressPreference='SilentlyContinue'
try{ [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13 } catch { [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12 }
[Net.ServicePointManager]::Expect100Continue=$false
$ua='Triparty-city-build/1.1 (personal travel guide)'
$desk=[Environment]::GetFolderPath('Desktop'); if(-not $desk){ $desk=$HOME }
$dir=Join-Path $desk 'triparty-porto-data'
$zip=Join-Path $desk 'triparty-porto-data.zip'
if(Test-Path $dir){ Remove-Item $dir -Recurse -Force }
New-Item -ItemType Directory -Force $dir | Out-Null
$logf=Join-Path $dir '_log.txt'
function Log($s){ Write-Host $s; Add-Content -Path $logf -Value $s }
function ErrText($e){
  $m=$e.Exception.Message
  try{ $r=$e.Exception.Response; if($r){ $m+=' | HTTP '+[int]$r.StatusCode; $sr=New-Object IO.StreamReader($r.GetResponseStream()); $b=$sr.ReadToEnd(); if($b.Length -gt 600){ $b=$b.Substring(0,600) }; $m+=' | '+($b -replace '\s+',' ') } } catch {}
  return $m
}
$curl=Get-Command curl.exe -ErrorAction SilentlyContinue
function Fetch($u,$out,$body,$tmo){
  if(-not $tmo){ $tmo=300 }
  if($curl){
    $a=@('-sS','-L','-A',$ua,'--max-time',"$tmo",'-o',$out,'-w','%{http_code}')
    if($body -ne $null){ $a+=@('--data',$body) }
    $a+=$u
    $code=((& curl.exe @a 2>&1) | Out-String).Trim()
    if($LASTEXITCODE -ne 0){ throw ('curl exit '+$LASTEXITCODE+': '+$code) }
    if($code -notmatch '^2\d\d'){ $t=''; try{ $t=[IO.File]::ReadAllText($out); if($t.Length -gt 400){ $t=$t.Substring(0,400) } } catch {}; throw ('HTTP '+$code+' | '+($t -replace '\s+',' ')) }
  } else {
    if($body -ne $null){ Invoke-WebRequest -Uri $u -Method Post -Body $body -ContentType 'application/x-www-form-urlencoded' -OutFile $out -UseBasicParsing -UserAgent $ua -TimeoutSec $tmo -ErrorAction Stop }
    else { Invoke-WebRequest -Uri $u -OutFile $out -UseBasicParsing -UserAgent $ua -TimeoutSec $tmo -ErrorAction Stop }
  }
}
function Good($f){ if(!(Test-Path $f)){ return $false }; $fs=[IO.File]::OpenRead($f); $b=New-Object byte[] 1; [void]$fs.Read($b,0,1); $len=$fs.Length; $fs.Close(); return ($b[0] -eq 123 -and $len -gt 150) }
$eps=@('https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter','https://maps.mail.ru/osm/tools/overpass/api/interpreter')
$rows=@(
'test|0|%5Bout%3Ajson%5D%5Btimeout%3A25%5D%3Bnode%5B%22tourism%22%3D%22artwork%22%5D%2841.140%2C-8.620%2C41.150%2C-8.600%29%3Bout%205%3B'
'art|0|%5Bout%3Ajson%5D%5Btimeout%3A180%5D%5Bbbox%3A41.095%2C-8.730%2C41.215%2C-8.540%5D%3B%28nwr%5B%22tourism%22%3D%22artwork%22%5D%3Bnwr%5B%22historic%22~%22%5E%28memorial%7Cmonument%29%24%22%5D%3Bnwr%5B%22amenity%22%3D%22fountain%22%5D%5B%22name%22%5D%3Bnwr%5B%22amenity%22%3D%22fountain%22%5D%5B%22wikidata%22%5D%3B%29%3Bout%20center%20tags%3B'
'poi|0|%5Bout%3Ajson%5D%5Btimeout%3A180%5D%5Bbbox%3A41.095%2C-8.730%2C41.215%2C-8.540%5D%3B%28nwr%5B%22tourism%22~%22%5E%28attraction%7Cmuseum%7Cgallery%7Cviewpoint%7Czoo%7Caquarium%29%24%22%5D%5B%22name%22%5D%3Bnwr%5B%22historic%22%5D%5B%22name%22%5D%3Bnwr%5B%22amenity%22~%22%5E%28place_of_worship%7Cmarketplace%7Ctheatre%7Carts_centre%7Cnightclub%7Ccafe%29%24%22%5D%5B%22name%22%5D%3Bnwr%5B%22leisure%22~%22%5E%28park%7Cgarden%7Cwater_park%29%24%22%5D%5B%22name%22%5D%3Bnwr%5B%22building%22%5D%5B%22wikidata%22%5D%5B%22name%22%5D%3Bnwr%5B%22shop%22~%22%5E%28mall%7Cdepartment_store%7Cwine%7Cbooks%29%24%22%5D%5B%22name%22%5D%3Bnwr%5B%22natural%22%3D%22beach%22%5D%3Bnwr%5B%22place%22%3D%22square%22%5D%5B%22name%22%5D%3Bnwr%5B%22aerialway%22%3D%22station%22%5D%3Bnwr%5B%22railway%22%3D%22tram_stop%22%5D%3B%29%3Bout%20center%20tags%3B'
'fun|0|%5Bout%3Ajson%5D%5Btimeout%3A180%5D%5Bbbox%3A40.95%2C-8.85%2C41.45%2C-8.20%5D%3B%28nwr%5B%22leisure%22~%22%5E%28escape_game%7Camusement_arcade%7Cbowling_alley%7Chigh_ropes_course%7Cskatepark%7Cwater_park%7Ctrampoline_park%7Cminiature_golf%29%24%22%5D%3Bnwr%5B%22sport%22~%22karting%7Cpaintball%7Claser_tag%7Cbilliards%7Csnooker%7Cbowling%7C10pin%7Csurfing%22%5D%3Bnwr%5B%22sport%22~%22climbing%22%5D%5B%22leisure%22%5D%3Bnwr%5B%22tourism%22%3D%22theme_park%22%5D%3Bnwr%5B%22attraction%22~%22summer_toboggan%7Croller_coaster%7Calpine_coaster%22%5D%3Bnwr%5B%22aerialway%22%3D%22zip_line%22%5D%3Bnwr%5B%22theatre%3Agenre%22%3D%22circus%22%5D%3Bnwr%5B%22leisure%22%5D%5B%22name%22~%22jet%20ski%7Cjetski%7Cvirtual%7Cquad%7Cbuggy%7Crage%7Ccircus%7Ccirco%7Cescape%7Claser%22%2Ci%5D%3Bnwr%5B%22amenity%22%5D%5B%22name%22~%22jet%20ski%7Cjetski%7Cvirtual%7Cquad%7Cbuggy%7Crage%7Ccircus%7Ccirco%7Cescape%7Claser%22%2Ci%5D%3Bnwr%5B%22shop%22%5D%5B%22name%22~%22jet%20ski%7Cjetski%7Cvirtual%7Cquad%7Cbuggy%7Crage%7Cescape%7Claser%22%2Ci%5D%3Bnwr%5B%22tourism%22%5D%5B%22name%22~%22jet%20ski%7Cjetski%7Cvirtual%7Cquad%7Cbuggy%7Crage%7Ccirco%7Cescape%7Claser%22%2Ci%5D%3B%29%3Bout%20center%20tags%3B'
'kosher|0|%5Bout%3Ajson%5D%5Btimeout%3A90%5D%5Bbbox%3A41.08%2C-8.75%2C41.25%2C-8.50%5D%3B%28nwr%5B%22diet%3Akosher%22%5D%3Bnwr%5B%22amenity%22%3D%22place_of_worship%22%5D%5B%22religion%22%3D%22jewish%22%5D%3Bnwr%5B%22cuisine%22~%22kosher%7Cjewish%7Cisraeli%22%5D%3Bnwr%5B%22name%22~%22kosher%7Cchabad%7Csinagoga%7Cjudaico%7Cholocausto%22%2Ci%5D%3Bnwr%5B%22tourism%22%3D%22museum%22%5D%5B%22name%22~%22juda%7Cholocaust%22%2Ci%5D%3B%29%3Bout%20center%20tags%3B'
)
$done=@{}
Log ('=== Triparty Porto data v2, PowerShell ' + $PSVersionTable.PSVersion.ToString() + ', curl: ' + ($(if($curl){'yes'}else{'no'})) + ' ===')
foreach($row in $rows){
  $k,$v,$q=$row -split '\|',3
  if($done[$k]){ continue }
  $out=Join-Path $dir ('osm_'+$k+'.json')
  foreach($ep in $eps){
    foreach($mode in @('POST','GET')){
      if($done[$k]){ break }
      Log ('OSM ' + $k + ' v' + $v + ' ' + $mode + ' <- ' + $ep)
      try{
        if($mode -eq 'POST'){ Fetch $ep $out ('data='+$q) 300 }
        else{ if($q.Length -gt 1800){ Log '  (query too long for GET, skipped)'; continue }; Fetch ($ep+'?data='+$q) $out $null 300 }
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
    try{ Fetch $u (Join-Path $dir ('wd_'+('{0:d3}' -f $n)+'.json')) $null 120; Write-Host ('WD batch ' + ($n+1) + ' OK') } catch { Log ('WD batch ' + ($n+1) + ' ERROR: ' + (ErrText $_)) }
    $n++; Start-Sleep -Milliseconds 400
  }
  Log ('wikidata batches: ' + $n)
}

# Wikivoyage
$wv=@(
'wv_en_Porto|https://en.wikivoyage.org/w/index.php?action=raw&title=Porto'
'wv_en_Gaia|https://en.wikivoyage.org/w/index.php?action=raw&title=Vila_Nova_de_Gaia'
'wv_en_Matosinhos|https://en.wikivoyage.org/w/index.php?action=raw&title=Matosinhos'
'wv_he_Porto|https://he.wikivoyage.org/w/index.php?action=raw&title=%D7%A4%D7%95%D7%A8%D7%98%D7%95'
'wv_en_Braga|https://en.wikivoyage.org/w/index.php?action=raw&title=Braga'
'wv_en_Guimaraes|https://en.wikivoyage.org/w/index.php?action=raw&title=Guimar%C3%A3es'
'wv_en_Douro|https://en.wikivoyage.org/w/index.php?action=raw&title=Douro_Valley'
)
foreach($row in $wv){ $k,$u=$row -split '\|',2
  try{ Fetch $u (Join-Path $dir ($k+'.txt')) $null 120; Log ('WV '+$k+' OK') } catch { Log ('WV '+$k+' ERROR: '+(ErrText $_)) } }
# Nominatim
$nom=@(
'000|Pra%C3%A7a%20da%20Ribeira%2C%20Porto'
'001|Ponte%20Lu%C3%ADs%20I%2C%20Porto'
'002|S%C3%A9%20do%20Porto'
'003|Pal%C3%A1cio%20da%20Bolsa%2C%20Porto'
'004|Igreja%20de%20S%C3%A3o%20Francisco%2C%20Porto'
'005|Casa%20do%20Infante%2C%20Porto'
'006|Rua%20das%20Flores%2C%20Porto'
'007|Igreja%20da%20Miseric%C3%B3rdia%20do%20Porto'
'008|Muralha%20Fernandina%2C%20Porto'
'009|Funicular%20dos%20Guindais'
'010|Cais%20da%20Estiva%2C%20Porto'
'011|Rua%20Escura%2C%20Porto'
'012|Mercado%20Ferreira%20Borges'
'013|Pra%C3%A7a%20do%20Infante%20D.%20Henrique%2C%20Porto'
'014|Igreja%20de%20S%C3%A3o%20Nicolau%2C%20Porto'
'015|Casa-Museu%20Guerra%20Junqueiro'
'016|Igreja%20de%20Santa%20Clara%2C%20Porto'
'017|Igreja%20de%20S%C3%A3o%20Louren%C3%A7o%2C%20Porto'
'018|Pa%C3%A7o%20Episcopal%20do%20Porto'
'019|Escadas%20do%20Code%C3%A7al%2C%20Porto'
'020|Museu%20das%20Marionetas%20do%20Porto'
'021|Casa%20Portuguesa%20do%20Pastel%20de%20Bacalhau%2C%20Rua%20das%20Flores%2C%20Porto'
'022|Ponte%20do%20Infante%2C%20Porto'
'023|Rua%20de%20S%C3%A3o%20Miguel%2C%20Porto'
'024|Cais%20da%20Ribeira%2C%20Porto'
'025|Esta%C3%A7%C3%A3o%20de%20S%C3%A3o%20Bento%2C%20Porto'
'026|C%C3%A2mara%20Municipal%20do%20Porto'
'027|Mercado%20do%20Bolh%C3%A3o%2C%20Porto'
'028|Caf%C3%A9%20Majestic%2C%20Porto'
'029|Rua%20de%20Santa%20Catarina%2C%20Porto'
'030|Capela%20das%20Almas%2C%20Porto'
'031|Igreja%20de%20Santo%20Ildefonso%2C%20Porto'
'032|Teatro%20Nacional%20S%C3%A3o%20Jo%C3%A3o'
'033|Confeitaria%20do%20Bolh%C3%A3o'
'034|Caf%C3%A9%20Santiago%2C%20Porto'
'035|Cervejaria%20Gazela%2C%20Porto'
'036|Via%20Catarina%20Shopping%2C%20Porto'
'037|Igreja%20dos%20Congregados%2C%20Porto'
'038|A%20P%C3%A9rola%20do%20Bolh%C3%A3o%2C%20Porto'
'039|Caf%C3%A9%20Guarany%2C%20Porto'
'040|Teatro%20Rivoli%2C%20Porto'
'041|Coliseu%20do%20Porto%2C%20Porto'
'042|Maus%20H%C3%A1bitos%2C%20Porto'
'043|Igreja%20da%20Trindade%2C%20Porto'
'044|Pra%C3%A7a%20da%20Liberdade%2C%20Porto'
'045|Manteigaria%2C%20Porto'
'046|Teatro%20S%C3%A1%20da%20Bandeira%2C%20Porto'
'047|Rua%20do%20Almada%2C%20Porto'
'048|Padaria%20Ribeiro%2C%20Porto'
'049|Pra%C3%A7a%20de%20D.%20Jo%C3%A3o%20I%2C%20Porto'
'050|Rua%20de%2031%20de%20Janeiro%2C%20Porto'
'051|Torre%20dos%20Cl%C3%A9rigos'
'052|Livraria%20Lello%2C%20Porto'
'053|Igreja%20do%20Carmo%2C%20Porto'
'054|Jardim%20da%20Cordoaria%2C%20Porto'
'055|Centro%20Portugu%C3%AAs%20de%20Fotografia'
'056|Miradouro%20da%20Vit%C3%B3ria%2C%20Porto'
'057|Rua%20Galeria%20de%20Paris%2C%20Porto'
'058|Passeio%20dos%20Cl%C3%A9rigos%2C%20Porto'
'059|Reitoria%20da%20Universidade%20do%20Porto'
'060|Mosteiro%20de%20S%C3%A3o%20Bento%20da%20Vit%C3%B3ria'
'061|Plano%20B%2C%20Porto'
'062|Pra%C3%A7a%20de%20Carlos%20Alberto%2C%20Porto'
'063|A%20Vida%20Portuguesa%2C%20Porto'
'064|Casa%20Oriental%2C%20Porto'
'065|Igreja%20de%20S%C3%A3o%20Jos%C3%A9%20das%20Taipas'
'066|Teatro%20Carlos%20Alberto%2C%20Porto'
'067|Pra%C3%A7a%20de%20Guilherme%20Gomes%20Fernandes%2C%20Porto'
'068|Hospital%20de%20Santo%20Ant%C3%B3nio%2C%20Porto'
'069|Jardins%20do%20Pal%C3%A1cio%20de%20Cristal'
'070|Museu%20Nacional%20Soares%20dos%20Reis'
'071|Rua%20de%20Miguel%20Bombarda%2C%20Porto'
'072|Museu%20Rom%C3%A2ntico%20da%20Quinta%20da%20Macieirinha'
'073|Igreja%20da%20Lapa%2C%20Porto'
'074|Igreja%20de%20S%C3%A3o%20Martinho%20de%20Cedofeita'
'075|Rua%20de%20Cedofeita%2C%20Porto'
'076|World%20of%20Discoveries%2C%20Porto'
'077|Alf%C3%A2ndega%20do%20Porto'
'078|Museu%20do%20Vinho%20do%20Porto'
'079|Miragaia%2C%20Porto'
'080|Passeio%20das%20Virtudes%2C%20Porto'
'081|Rua%20do%20Breyner%2C%20Porto'
'082|Igreja%20de%20S%C3%A3o%20Pedro%20de%20Miragaia'
'083|Travessa%20de%20Cedofeita%2C%20Porto'
'084|Casa-Museu%20Marta%20Ortig%C3%A3o%20Sampaio'
'085|Est%C3%A1dio%20do%20Drag%C3%A3o'
'086|Igreja%20do%20Bonfim%2C%20Porto'
'087|Casa%20Guedes%2C%20Porto'
'088|Jardim%20de%20S%C3%A3o%20L%C3%A1zaro%2C%20Porto'
'089|Alameda%20das%20Fontainhas%2C%20Porto'
'090|Cemit%C3%A9rio%20do%20Prado%20do%20Repouso'
'091|Esta%C3%A7%C3%A3o%20de%20Campanh%C3%A3'
'092|Pal%C3%A1cio%20do%20Freixo'
'093|Alameda%20Shop%20%26%20Spot%2C%20Porto'
'094|Museu%20Militar%20do%20Porto'
'095|Rua%20de%20Santa%20Catarina%201000%2C%20Porto'
'096|Museu%20de%20Serralves'
'097|P%C3%A9rgola%20da%20Foz%2C%20Porto'
'098|Farolim%20de%20Felgueiras'
'099|Castelo%20do%20Queijo'
'100|Jardim%20do%20Passeio%20Alegre'
'101|Praia%20dos%20Ingleses%2C%20Porto'
'102|Infante%2C%20Porto%20tram%20stop'
'103|Museu%20do%20Carro%20El%C3%A9ctrico'
'104|Ponte%20da%20Arr%C3%A1bida'
'105|Sea%20Life%20Porto'
'106|Parque%20da%20Cidade%20do%20Porto'
'107|Igreja%20de%20S%C3%A3o%20Jo%C3%A3o%20da%20Foz'
'108|Jardim%20Bot%C3%A2nico%20do%20Porto'
'109|Planet%C3%A1rio%20do%20Porto'
'110|Mercado%20da%20Foz%20do%20Douro'
'111|Praia%20do%20Homem%20do%20Leme'
'112|Forte%20de%20S%C3%A3o%20Jo%C3%A3o%20Baptista%20da%20Foz'
'113|Praia%20do%20Carneiro%2C%20Porto'
'114|Avenida%20do%20Brasil%2C%20Porto'
'115|Rua%20do%20Padr%C3%A3o%2C%20Porto'
'116|Casa%20da%20M%C3%BAsica'
'117|Rotunda%20da%20Boavista'
'118|Mercado%20do%20Bom%20Sucesso'
'119|Sinagoga%20Kadoorie%20Mekor%20Haim'
'120|Museu%20do%20Holocausto%20do%20Porto'
'121|Chabad%20Porto'
'122|Rua%20de%20Guerra%20Junqueiro%20340%2C%20Porto'
'123|Cemit%C3%A9rio%20de%20Agramonte'
'124|Casa-Museu%20Fernando%20de%20Castro'
'125|Avenida%20da%20Boavista%2C%20Porto'
'126|Edif%C3%ADcio%20Vodafone%2C%20Avenida%20da%20Boavista%2C%20Porto'
'127|Igreja%20de%20Santo%20Ant%C3%B3nio%20das%20Antas'
'128|Jardim%20de%20Arca%20d%27%C3%81gua'
'129|Cais%20de%20Gaia'
'130|Mosteiro%20da%20Serra%20do%20Pilar'
'131|Telef%C3%A9rico%20de%20Gaia'
'132|Jardim%20do%20Morro'
'133|Graham%27s%2C%20Vila%20Nova%20de%20Gaia'
'134|Sandeman%2C%20Vila%20Nova%20de%20Gaia'
'135|Taylor%27s%2C%20Vila%20Nova%20de%20Gaia'
'136|C%C3%A1lem%2C%20Vila%20Nova%20de%20Gaia'
'137|World%20of%20Wine%2C%20Vila%20Nova%20de%20Gaia'
'138|Mercado%20Beira-Rio'
'139|Afurada'
'140|Praia%20de%20Lavadores'
'141|Capela%20do%20Senhor%20da%20Pedra'
'142|Zoo%20Santo%20In%C3%A1cio'
'143|El%20Corte%20Ingl%C3%A9s%2C%20Vila%20Nova%20de%20Gaia'
'144|Reserva%20Natural%20Local%20do%20Estu%C3%A1rio%20do%20Douro'
'145|Casa-Museu%20Teixeira%20Lopes'
'146|Espa%C3%A7o%20Porto%20Cruz'
'147|Ramos%20Pinto%2C%20Vila%20Nova%20de%20Gaia'
'148|Ferreira%2C%20Vila%20Nova%20de%20Gaia'
'149|Casa%20Barbot'
'150|Arr%C3%A1bida%20Shopping'
'151|Convento%20Corpus%20Christi%2C%20Vila%20Nova%20de%20Gaia'
'152|Praia%20de%20Matosinhos'
'153|Piscina%20das%20Mar%C3%A9s'
'154|Casa%20de%20Ch%C3%A1%20da%20Boa%20Nova'
'155|Mercado%20Municipal%20de%20Matosinhos'
'156|Rua%20Her%C3%B3is%20de%20Fran%C3%A7a%2C%20Matosinhos'
'157|Farol%20de%20Le%C3%A7a'
'158|Forte%20de%20Nossa%20Senhora%20das%20Neves'
'159|She%20Changes%2C%20Matosinhos'
'160|Terminal%20de%20Cruzeiros%20de%20Leix%C3%B5es'
'161|Igreja%20do%20Bom%20Jesus%20de%20Matosinhos'
'162|NorteShopping'
'163|Quinta%20da%20Concei%C3%A7%C3%A3o%2C%20Matosinhos'
'164|Praia%20de%20Le%C3%A7a%20da%20Palmeira'
'165|Praia%20de%20Matosinhos'
'166|Real%20Vin%C3%ADcola%2C%20Matosinhos'
'167|Zoo%20da%20Maia'
'168|Parque%20Biol%C3%B3gico%20de%20Gaia'
'169|Mosteiro%20de%20Le%C3%A7a%20do%20Balio'
'170|Praia%20da%20Aguda'
'171|Vila%20do%20Conde%20Porto%20Fashion%20Outlet'
'172|S%C3%A9%20de%20Braga'
'173|Castelo%20de%20Guimar%C3%A3es'
'174|Aveiro'
'175|Pinh%C3%A3o'
'176|Amarante'
'177|Universidade%20de%20Coimbra'
'178|Viana%20do%20Castelo'
'179|Santu%C3%A1rio%20de%20Nossa%20Senhora%20dos%20Rem%C3%A9dios%2C%20Lamego'
'180|Castelo%20de%20Santa%20Maria%20da%20Feira'
'181|Barcelos'
'182|Ponte%20de%20Lima'
'183|Vila%20do%20Ger%C3%AAs'
'184|Vila%20do%20Conde'
'185|Casa%20de%20Mateus'
'186|Esta%C3%A7%C3%A3o%20de%20Peso%20da%20R%C3%A9gua'
'187|Espinho'
'188|Cit%C3%A2nia%20de%20Briteiros'
)
$nomFile=Join-Path $dir 'nominatim.tsv'; $okn=0; $cnt=0
Write-Host ('Coordinates: ' + $nom.Count + ' places, about ' + [Math]::Ceiling($nom.Count*1.3/60) + ' minutes...')
foreach($row in $nom){ $k,$q=$row -split '\|',2
  $u='https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&accept-language=en&q='+$q
  $line=$k+"`t"
  try{ $tf=Join-Path $dir '_nom.tmp'; Fetch $u $tf $null 60; $line+=(([IO.File]::ReadAllText($tf,[Text.Encoding]::UTF8) -replace '[\r\n]+',' ')); $okn++ } catch { $line+='ERROR' }
  [IO.File]::AppendAllText($nomFile,$line+"`n",(New-Object Text.UTF8Encoding($false)))
  $cnt++; if(($cnt % 25) -eq 0){ Write-Host ('  ' + $cnt + ' / ' + $nom.Count) }
  Start-Sleep -Milliseconds 1150 }
Log ('nominatim ok: '+$okn+' of '+$nom.Count)

if(Test-Path $zip){ Remove-Item $zip -Force }
Compress-Archive -Path (Join-Path $dir '*') -DestinationPath $zip -Force
Write-Host ''
Write-Host ('Done. ZIP file: ' + $zip + '  (' + [Math]::Round((Get-Item $zip).Length/1MB,2) + ' MB)') -ForegroundColor Green
