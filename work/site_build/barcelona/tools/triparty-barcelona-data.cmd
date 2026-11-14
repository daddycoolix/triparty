@echo off
title Triparty Barcelona data
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex (((Get-Content -Raw -LiteralPath '%~f0') -split '(?m)^#PSBEGIN\r?$',2)[1])"
echo.
pause
exit /b
#PSBEGIN
$ProgressPreference='SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
$ua='Triparty-city-build/1.0 (personal travel guide)'
$desk=[Environment]::GetFolderPath('Desktop'); if(-not $desk){ $desk=$HOME }
$dir=Join-Path $desk 'triparty-bcn-data'
$zip=Join-Path $desk 'triparty-bcn-data.zip'
if(Test-Path $dir){ Remove-Item $dir -Recurse -Force }
New-Item -ItemType Directory -Force $dir | Out-Null
$log=@()
function Get-Url($url,$out){
  for($i=0;$i -lt 3;$i++){
    try{ Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing -UserAgent $ua -TimeoutSec 300 -ErrorAction Stop; return $true } catch { Start-Sleep -Seconds 4 }
  }
  return $false
}
Write-Host ''
Write-Host '=== Triparty: collecting Barcelona source data (about 10 minutes) ===' -ForegroundColor Cyan

# 1. Overpass (OpenStreetMap)
$ov=@(
'art|%5Bout%3Ajson%5D%5Btimeout%3A240%5D%3B%28area%283600347950%29%3Barea%5B%22wikidata%22%3D%22Q1492%22%5D%5B%22admin_level%22%3D%228%22%5D%3B%29-%3E.a%3B%28nwr%5B%22tourism%22%3D%22artwork%22%5D%28area.a%29%3Bnwr%5B%22historic%22~%22%5E%28memorial%7Cmonument%29%24%22%5D%28area.a%29%3Bnwr%5B%22amenity%22%3D%22fountain%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22amenity%22%3D%22fountain%22%5D%5B%22wikidata%22%5D%28area.a%29%3B%29%3Bout%20center%20tags%3B'
'fun|%5Bout%3Ajson%5D%5Btimeout%3A240%5D%5Bbbox%3A41.15%2C1.55%2C41.80%2C2.65%5D%3B%28nwr%5B%22leisure%22~%22%5E%28escape_game%7Camusement_arcade%7Cbowling_alley%7Chigh_ropes_course%7Cskatepark%7Cwater_park%7Ctrampoline_park%7Cminiature_golf%29%24%22%5D%3Bnwr%5B%22sport%22~%22karting%7Cpaintball%7Claser_tag%7Cbilliards%7Csnooker%7Cbowling%7C10pin%22%5D%3Bnwr%5B%22sport%22~%22climbing%22%5D%5B%22leisure%22%5D%3Bnwr%5B%22tourism%22%3D%22theme_park%22%5D%3Bnwr%5B%22attraction%22~%22summer_toboggan%7Croller_coaster%7Calpine_coaster%22%5D%3Bnwr%5B%22aerialway%22%3D%22zip_line%22%5D%3Bnwr%5B%22theatre%3Agenre%22%3D%22circus%22%5D%3Bnwr%5B%22name%22~%22jet%20ski%7Cjetski%7Cvirtual%20reality%7Crealitat%20virtual%7Crealidad%20virtual%7Cquad%7Cbuggy%7Crage%20room%7Ccircus%7Cescape%20room%7Croom%20escape%7Claser%22%2Ci%5D%5B~%22%5E%28leisure%7Camenity%7Ctourism%7Csport%7Cshop%7Coffice%7Cclub%29%24%22~%22.%22%5D%3B%29%3Bout%20center%20tags%3B'
'poi|%5Bout%3Ajson%5D%5Btimeout%3A240%5D%3B%28area%283600347950%29%3Barea%5B%22wikidata%22%3D%22Q1492%22%5D%5B%22admin_level%22%3D%228%22%5D%3B%29-%3E.a%3B%28nwr%5B%22tourism%22~%22%5E%28attraction%7Cmuseum%7Cgallery%7Cviewpoint%7Czoo%7Caquarium%29%24%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22historic%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22amenity%22~%22%5E%28place_of_worship%7Cmarketplace%7Ctheatre%7Carts_centre%7Cnightclub%29%24%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22leisure%22~%22%5E%28park%7Cgarden%7Cwater_park%29%24%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22building%22%5D%5B%22wikidata%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22shop%22~%22%5E%28mall%7Cdepartment_store%29%24%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22natural%22%3D%22beach%22%5D%28area.a%29%3Bnwr%5B%22place%22%3D%22square%22%5D%5B%22name%22%5D%28area.a%29%3Bnwr%5B%22aerialway%22%3D%22station%22%5D%28area.a%29%3B%29%3Bout%20center%20tags%3B'
'kosher|%5Bout%3Ajson%5D%5Btimeout%3A120%5D%5Bbbox%3A41.30%2C2.05%2C41.47%2C2.25%5D%3B%28nwr%5B%22diet%3Akosher%22%5D%3Bnwr%5B%22amenity%22%3D%22place_of_worship%22%5D%5B%22religion%22%3D%22jewish%22%5D%3Bnwr%5B%22cuisine%22~%22kosher%7Cjewish%7Cisraeli%22%5D%3Bnwr%5B%22name%22~%22kosher%7Cchabad%7Cjabad%7Csinagoga%22%2Ci%5D%3B%29%3Bout%20center%20tags%3B'
)
$eps=@('https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter')
foreach($row in $ov){
  $k,$q=$row -split '\|',2
  $out=Join-Path $dir ('osm_'+$k+'.json'); $done=$false
  foreach($round in 1..2){
    foreach($ep in $eps){
      Write-Host ('OSM ' + $k + ' <- ' + $ep)
      try{
        Invoke-WebRequest -Uri $ep -Method Post -Body ('data='+$q) -ContentType 'application/x-www-form-urlencoded' -OutFile $out -UseBasicParsing -UserAgent $ua -TimeoutSec 400 -ErrorAction Stop
        $fs=[IO.File]::OpenRead($out); $b=New-Object byte[] 1; [void]$fs.Read($b,0,1); $len=$fs.Length; $fs.Close()
        if($b[0] -eq 123 -and $len -gt 200){ $done=$true; Write-Host ('  OK ' + [Math]::Round($len/1KB) + ' KB'); break }
      } catch { Write-Host '  failed, trying next server' -ForegroundColor Yellow }
      Start-Sleep -Seconds 6
    }
    if($done){ break }
  }
  $log+=('osm_'+$k+': '+$done)
  Start-Sleep -Seconds 5
}

# 2. Wikivoyage
$wv=@(
'wv_en_Barcelona|https://en.wikivoyage.org/w/index.php?action=raw&title=Barcelona'
'wv_en_Ciutat_Vella|https://en.wikivoyage.org/w/index.php?action=raw&title=Barcelona/Ciutat_Vella'
'wv_en_Eixample|https://en.wikivoyage.org/w/index.php?action=raw&title=Barcelona/Eixample'
'wv_en_Gracia|https://en.wikivoyage.org/w/index.php?action=raw&title=Barcelona/Gr%C3%A0cia'
'wv_en_Sants-Montjuic|https://en.wikivoyage.org/w/index.php?action=raw&title=Barcelona/Sants-Montju%C3%AFc'
'wv_en_Sant_Marti|https://en.wikivoyage.org/w/index.php?action=raw&title=Barcelona/Sant_Mart%C3%AD'
'wv_en_Inland_Suburbs|https://en.wikivoyage.org/w/index.php?action=raw&title=Barcelona/Inland_Suburbs'
'wv_he_Barcelona|https://he.wikivoyage.org/w/index.php?action=raw&title=%D7%91%D7%A8%D7%A6%D7%9C%D7%95%D7%A0%D7%94'
'wv_en_search|https://en.wikivoyage.org/w/api.php?action=query&format=json&list=allpages&apprefix=Barcelona/&aplimit=50'
)
foreach($row in $wv){
  $k,$u=$row -split '\|',2
  $r=Get-Url $u (Join-Path $dir ($k+'.txt')); $log+=($k+': '+$r); Write-Host ('WV  ' + $k + ' ' + $r)
}

# 3. Wikidata for artworks
$artFile=Join-Path $dir 'osm_art.json'
if(Test-Path $artFile){
  $txt=[IO.File]::ReadAllText($artFile,[Text.Encoding]::UTF8)
  $ids=@([regex]::Matches($txt,'wikidata"\s*:\s*"([^"]+)"') | ForEach-Object { $_.Groups[1].Value -split '\s*;\s*' } | Where-Object { $_ -match '^Q\d+$' } | Select-Object -Unique)
  Write-Host ('Wikidata ids: ' + $ids.Count)
  $n=0
  for($i=0;$i -lt $ids.Count;$i+=50){
    $hi=[Math]::Min($i+49,$ids.Count-1); $chunk=$ids[$i..$hi] -join '%7C'
    $u='https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids='+$chunk+'&props=labels%7Cdescriptions%7Csitelinks%7Cclaims&languages=he%7Cen%7Cca%7Ces&sitefilter=hewiki%7Cenwiki%7Ccawiki%7Ceswiki'
    $r=Get-Url $u (Join-Path $dir ('wd_'+('{0:d3}' -f $n)+'.json')); $n++
    Write-Host ('WD  batch ' + $n + ' ' + $r); Start-Sleep -Milliseconds 400
  }
  $log+=('wikidata ids: '+$ids.Count+', batches: '+$n)
}

# 4. Nominatim coordinates (1 request per second)
$nom=@(
'000|Catedral%20de%20Barcelona'
'001|Pla%C3%A7a%20del%20Rei%2C%20Barcelona'
'002|Museu%20d%27Hist%C3%B2ria%20de%20Barcelona%2C%20Pla%C3%A7a%20del%20Rei'
'003|Pla%C3%A7a%20de%20Sant%20Jaume%2C%20Barcelona'
'004|Temple%20d%27August%2C%20Barcelona'
'005|Pla%C3%A7a%20Nova%2C%20Barcelona'
'006|Pont%20del%20Bisbe%2C%20Barcelona'
'007|Carrer%20del%20Call%2C%20Barcelona'
'008|Carrer%20de%20Marlet%205%2C%20Barcelona'
'009|Pla%C3%A7a%20de%20Sant%20Felip%20Neri%2C%20Barcelona'
'010|Pla%C3%A7a%20Reial%2C%20Barcelona'
'011|La%20Rambla%2C%20Barcelona'
'012|Santa%20Maria%20del%20Pi%2C%20Barcelona'
'013|Museu%20Frederic%20Mar%C3%A8s%2C%20Barcelona'
'014|Casa%20de%20l%27Ardiaca%2C%20Barcelona'
'015|Portal%20de%20l%27%C3%80ngel%2C%20Barcelona'
'016|Els%20Quatre%20Gats%2C%20Barcelona'
'017|Bas%C3%ADlica%20de%20la%20Merc%C3%A8%2C%20Barcelona'
'018|Bas%C3%ADlica%20dels%20Sants%20Just%20i%20Pastor%2C%20Barcelona'
'019|Esgl%C3%A9sia%20de%20Santa%20Anna%2C%20Barcelona'
'020|Pla%C3%A7a%20de%20la%20Vila%20de%20Madrid%2C%20Barcelona'
'021|Museu%20de%20Cera%20de%20Barcelona%2C%20Barcelona'
'022|Big%20Fun%20Museum%20Barcelona'
'023|Mirador%20de%20Colom%2C%20Barcelona'
'024|Gran%20Teatre%20del%20Liceu%2C%20Barcelona'
'025|Casa%20Bruno%20Cuadros%2C%20Barcelona'
'026|Carrer%20de%20Petritxol%2C%20Barcelona'
'027|Can%20Culleretes%2C%20Barcelona'
'028|Antiga%20Casa%20Figueras%2C%20Barcelona'
'029|Cereria%20Subir%C3%A0%2C%20Barcelona'
'030|La%20Manual%20Alpargatera%2C%20Barcelona'
'031|Jamboree%2C%20Pla%C3%A7a%20Reial%2C%20Barcelona'
'032|Harlem%20Jazz%20Club%2C%20Barcelona'
'033|Museu%20de%20l%27Er%C3%B2tica%2C%20Barcelona'
'034|Maccabi%2C%20La%20Rambla%2C%20Barcelona'
'035|Bas%C3%ADlica%20de%20Santa%20Maria%20del%20Mar%2C%20Barcelona'
'036|Museu%20Picasso%2C%20Barcelona'
'037|Palau%20de%20la%20M%C3%BAsica%20Catalana%2C%20Barcelona'
'038|El%20Born%20Centre%20de%20Cultura%20i%20Mem%C3%B2ria%2C%20Barcelona'
'039|Passeig%20del%20Born%2C%20Barcelona'
'040|Carrer%20de%20Montcada%2C%20Barcelona'
'041|Mercat%20de%20Santa%20Caterina%2C%20Barcelona'
'042|Parc%20de%20la%20Ciutadella%2C%20Barcelona'
'043|Cascada%20Monumental%2C%20Barcelona'
'044|Arc%20de%20Triomf%2C%20Barcelona'
'045|Zoo%20de%20Barcelona'
'046|Parlament%20de%20Catalunya'
'047|Castell%20dels%20Tres%20Dragons%2C%20Barcelona'
'048|Hivernacle%2C%20Parc%20de%20la%20Ciutadella%2C%20Barcelona'
'049|Museu%20de%20la%20Xocolata%2C%20Barcelona'
'050|Moco%20Museum%20Barcelona%2C%20Barcelona'
'051|Museu%20de%20Cultures%20del%20M%C3%B3n%2C%20Barcelona'
'052|Museu%20Europeu%20d%27Art%20Modern%2C%20Barcelona'
'053|Fossar%20de%20les%20Moreres%2C%20Barcelona'
'054|La%20Llotja%20de%20Mar%2C%20Barcelona'
'055|Estaci%C3%B3%20de%20Fran%C3%A7a%2C%20Barcelona'
'056|El%20Xampanyet%2C%20Barcelona'
'057|Casa%20Gispert%2C%20Barcelona'
'058|Vila%20Viniteca%2C%20Barcelona'
'059|Capella%20d%27en%20Marc%C3%BAs%2C%20Barcelona'
'060|Sant%20Pere%20de%20les%20Puel%C2%B7les%2C%20Barcelona'
'061|Paradiso%2C%20Barcelona'
'062|Palau%20Dalmases%2C%20Barcelona'
'063|Museum%20of%20Illusions%20Barcelona'
'064|Museu%20del%20Mamut%2C%20Barcelona'
'065|Mercat%20de%20la%20Boqueria%2C%20Barcelona'
'066|MACBA%2C%20Barcelona'
'067|CCCB%2C%20Barcelona'
'068|Palau%20G%C3%BCell%2C%20Barcelona'
'069|Sant%20Pau%20del%20Camp%2C%20Barcelona'
'070|Antic%20Hospital%20de%20la%20Santa%20Creu%2C%20Barcelona'
'071|Rambla%20del%20Raval%2C%20Barcelona'
'072|Museu%20Mar%C3%ADtim%20de%20Barcelona%2C%20Barcelona'
'073|Bar%20Marsella%2C%20Barcelona'
'074|Carrer%20dels%20Tallers%2C%20Barcelona'
'075|Hotel%20Espa%C3%B1a%2C%20Barcelona'
'076|Filmoteca%20de%20Catalunya%2C%20Barcelona'
'077|Granja%20M.%20Viader%2C%20Barcelona'
'078|Reial%20Acad%C3%A8mia%20de%20Medicina%20de%20Catalunya%2C%20Barcelona'
'079|Esgl%C3%A9sia%20de%20Betlem%2C%20Barcelona'
'080|Palau%20de%20la%20Virreina%2C%20Barcelona'
'081|Carrer%20de%20Joaqu%C3%ADn%20Costa%2C%20Barcelona'
'082|Rambla%20de%20Mar%2C%20Barcelona'
'083|L%27Aqu%C3%A0rium%20de%20Barcelona%2C%20Barcelona'
'084|Maremagnum%2C%20Barcelona'
'085|Museu%20d%27Hist%C3%B2ria%20de%20Catalunya%2C%20Barcelona'
'086|Platja%20de%20la%20Barceloneta%2C%20Barcelona'
'087|Platja%20de%20Sant%20Sebasti%C3%A0%2C%20Barcelona'
'088|Platja%20del%20Somorrostro%2C%20Barcelona'
'089|Pla%C3%A7a%20de%20la%20Barceloneta%2C%20Barcelona'
'090|Mercat%20de%20la%20Barceloneta%2C%20Barcelona'
'091|Can%20Paixano%2C%20Barcelona'
'092|Can%20Sol%C3%A9%2C%20Barcelona'
'093|Torre%20de%20Sant%20Sebasti%C3%A0%2C%20Barcelona'
'094|W%20Barcelona%2C%20Barcelona'
'095|Club%20Nataci%C3%B3%20Atl%C3%A8tic-Barceloneta%2C%20Barcelona'
'096|Passeig%20Mar%C3%ADtim%20de%20la%20Barceloneta%2C%20Barcelona'
'097|Las%20Golondrinas%2C%20Portal%20de%20la%20Pau%2C%20Barcelona'
'098|Torre%20del%20Rellotge%2C%20Moll%20dels%20Pescadors%2C%20Barcelona'
'099|Casa%20de%20la%20Barceloneta%201761'
'100|Opium%20Barcelona'
'101|Casino%20Barcelona%2C%20Barcelona'
'102|Sagrada%20Fam%C3%ADlia'
'103|Casa%20Batll%C3%B3%2C%20Barcelona'
'104|Casa%20Mil%C3%A0%2C%20Barcelona'
'105|Casa%20Amatller%2C%20Barcelona'
'106|Casa%20Lle%C3%B3%20Morera%2C%20Barcelona'
'107|Passeig%20de%20Gr%C3%A0cia%2C%20Barcelona'
'108|Recinte%20Modernista%20de%20Sant%20Pau%2C%20Barcelona'
'109|Avinguda%20de%20Gaud%C3%AD%2C%20Barcelona'
'110|Casa%20de%20les%20Punxes%2C%20Barcelona'
'111|Palau%20del%20Bar%C3%B3%20de%20Quadras%2C%20Barcelona'
'112|Casa%20Calvet%2C%20Barcelona'
'113|Fundaci%C3%B3%20Antoni%20T%C3%A0pies%2C%20Barcelona'
'114|Museu%20Egipci%20de%20Barcelona%2C%20Barcelona'
'115|Museu%20del%20Modernisme%20de%20Barcelona%2C%20Barcelona'
'116|Casa%20Comalat%2C%20Barcelona'
'117|Palau%20Macaya%2C%20Barcelona'
'118|Rambla%20de%20Catalunya%2C%20Barcelona'
'119|Passatge%20de%20Permanyer%2C%20Barcelona'
'120|Pla%C3%A7a%20de%20Catalunya%2C%20Barcelona'
'121|El%20Corte%20Ingl%C3%A9s%2C%20Pla%C3%A7a%20de%20Catalunya%2C%20Barcelona'
'122|Edifici%20Hist%C3%B2ric%20de%20la%20Universitat%20de%20Barcelona'
'123|Mercat%20de%20Sant%20Antoni%2C%20Barcelona'
'124|Mercat%20de%20la%20Concepci%C3%B3%2C%20Barcelona'
'125|Plaza%20de%20Toros%20Monumental%2C%20Barcelona'
'126|Museu%20de%20la%20M%C3%BAsica%2C%20Barcelona'
'127|Jardins%20de%20la%20Torre%20de%20les%20Aig%C3%BCes%2C%20Barcelona'
'128|Parc%20de%20Joan%20Mir%C3%B3%2C%20Barcelona'
'129|Parc%20de%20l%27Estaci%C3%B3%20del%20Nord%2C%20Barcelona'
'130|El%20Nacional%2C%20Barcelona'
'131|Cacao%20Sampaka%2C%20Barcelona'
'132|Colmado%20Qu%C3%ADlez%2C%20Barcelona'
'133|Mercat%20del%20Ninot%2C%20Barcelona'
'134|Dry%20Martini%2C%20Barcelona'
'135|Carrer%20del%20Consell%20de%20Cent%20255%2C%20Barcelona'
'136|Teatre%20Nacional%20de%20Catalunya'
'137|Casa%20Golferichs%2C%20Barcelona'
'138|Carrer%20de%20l%27Avenir%2024%2C%20Barcelona'
'139|Park%20G%C3%BCell'
'140|Casa%20Museu%20Gaud%C3%AD%2C%20Barcelona'
'141|Casa%20Vicens%2C%20Barcelona'
'142|Pla%C3%A7a%20del%20Sol%2C%20Barcelona'
'143|Pla%C3%A7a%20de%20la%20Vila%20de%20Gr%C3%A0cia%2C%20Barcelona'
'144|Pla%C3%A7a%20de%20la%20Virreina%2C%20Barcelona'
'145|Carrer%20de%20Verdi%2C%20Barcelona'
'146|Tur%C3%B3%20de%20la%20Rovira%2C%20Barcelona'
'147|Casa%20Fuster%2C%20Barcelona'
'148|Mercat%20de%20la%20Llibertat%2C%20Barcelona'
'149|Parc%20de%20la%20Creueta%20del%20Coll%2C%20Barcelona'
'150|Jardins%20del%20Tur%C3%B3%20del%20Putxet%2C%20Barcelona'
'151|Parc%20del%20Guinard%C3%B3%2C%20Barcelona'
'152|Carrer%20del%20Torrent%20de%20l%27Olla%2C%20Barcelona'
'153|Viaducte%20de%20Vallcarca%2C%20Barcelona'
'154|Carrer%20Gran%20de%20Gr%C3%A0cia%2C%20Barcelona'
'155|Museu%20Nacional%20d%27Art%20de%20Catalunya'
'156|Font%20M%C3%A0gica%20de%20Montju%C3%AFc%2C%20Barcelona'
'157|Torres%20Venecianes%2C%20Barcelona'
'158|Arenas%20de%20Barcelona%2C%20Barcelona'
'159|Fundaci%C3%B3%20Joan%20Mir%C3%B3%2C%20Barcelona'
'160|Castell%20de%20Montju%C3%AFc%2C%20Barcelona'
'161|Telef%C3%A8ric%20de%20Montju%C3%AFc%2C%20Barcelona'
'162|Poble%20Espanyol%2C%20Barcelona'
'163|CaixaForum%20Barcelona%2C%20Barcelona'
'164|Pavell%C3%B3%20Mies%20van%20der%20Rohe%2C%20Barcelona'
'165|Estadi%20Ol%C3%ADmpic%20Llu%C3%ADs%20Companys%2C%20Barcelona'
'166|Palau%20Sant%20Jordi'
'167|Museu%20Ol%C3%ADmpic%20i%20de%20l%27Esport%2C%20Barcelona'
'168|Museu%20d%27Arqueologia%20de%20Catalunya%2C%20Barcelona'
'169|Jard%C3%AD%20Bot%C3%A0nic%20de%20Barcelona%2C%20Barcelona'
'170|Jardins%20de%20Moss%C3%A8n%20Costa%20i%20Llobera%2C%20Barcelona'
'171|Teatre%20Grec%2C%20Barcelona'
'172|Mirador%20de%20l%27Alcalde%2C%20Barcelona'
'173|Cementiri%20de%20Montju%C3%AFc%2C%20Barcelona'
'174|Mirador%20de%20l%27Alcalde%2C%20Barcelona'
'175|Piscina%20Municipal%20de%20Montju%C3%AFc%2C%20Barcelona'
'176|Piscines%20Bernat%20Picornell%2C%20Barcelona'
'177|Carrer%20de%20Blai%2C%20Barcelona'
'178|Quimet%20%26%20Quimet%2C%20Barcelona'
'179|Sala%20Apolo%2C%20Barcelona'
'180|El%20Molino%2C%20Barcelona'
'181|Refugi%20307%2C%20Barcelona'
'182|Parc%20de%20l%27Espanya%20Industrial%2C%20Barcelona'
'183|Les%20Tres%20Xemeneies%2C%20Barcelona'
'184|Port%20Ol%C3%ADmpic%2C%20Barcelona'
'185|Platja%20de%20la%20Nova%20Ic%C3%A0ria%2C%20Barcelona'
'186|Platja%20del%20Bogatell%2C%20Barcelona'
'187|Platja%20de%20la%20Mar%20Bella%2C%20Barcelona'
'188|Rambla%20del%20Poblenou%2C%20Barcelona'
'189|Torre%20Gl%C3%B2ries%2C%20Barcelona'
'190|Disseny%20Hub%20Barcelona'
'191|Mercat%20dels%20Encants%2C%20Barcelona'
'192|Westfield%20Gl%C3%B2ries%2C%20Barcelona'
'193|Diagonal%20Mar%20Centre%20Comercial'
'194|Parc%20del%20F%C3%B2rum%2C%20Barcelona'
'195|Museu%20Blau%2C%20Barcelona'
'196|Zona%20de%20Banys%20del%20F%C3%B2rum%2C%20Barcelona'
'197|Parc%20de%20Diagonal%20Mar%2C%20Barcelona'
'198|Cementiri%20del%20Poblenou%2C%20Barcelona'
'199|Museu%20Can%20Framis%2C%20Barcelona'
'200|Sala%20Razzmatazz%2C%20Barcelona'
'201|Hotel%20Arts%20Barcelona'
'202|El%20T%C3%ADo%20Che%2C%20Barcelona'
'203|Palo%20Alto%2C%20Carrer%20dels%20Pellaires%2C%20Barcelona'
'204|Torre%20de%20les%20Aig%C3%BCes%20del%20Bes%C3%B2s%2C%20Barcelona'
'205|Parc%20del%20Centre%20del%20Poblenou%2C%20Barcelona'
'206|Can%20Ricart%2C%20Barcelona'
'207|Temple%20Expiatori%20del%20Sagrat%20Cor%2C%20Barcelona'
'208|Torre%20de%20Collserola%2C%20Barcelona'
'209|CosmoCaixa%2C%20Barcelona'
'210|Carretera%20de%20les%20Aig%C3%BCes%2C%20Barcelona'
'211|Funicular%20del%20Tibidabo'
'212|Torre%20Bellesguard%2C%20Barcelona'
'213|Monestir%20de%20Pedralbes'
'214|Jardins%20del%20Palau%20de%20Pedralbes%2C%20Barcelona'
'215|Pavellons%20G%C3%BCell%2C%20Barcelona'
'216|Camp%20Nou%2C%20Barcelona'
'217|L%27Illa%20Diagonal%2C%20Barcelona'
'218|Carrer%20Major%20de%20Sarri%C3%A0%2C%20Barcelona'
'219|Col%C2%B7legi%20de%20les%20Teresianes%2C%20Barcelona'
'220|Parc%20de%20l%27Oreneta%2C%20Barcelona'
'221|Observatori%20Fabra%2C%20Barcelona'
'222|Tur%C3%B3%20Park%2C%20Barcelona'
'223|Luz%20de%20Gas%2C%20Barcelona'
'224|Bikini%2C%20Barcelona'
'225|Centre%20d%27Informaci%C3%B3%20del%20Parc%20de%20Collserola'
'226|Chabad%20Lubavitch%20Barcelona'
'227|Pla%C3%A7a%20del%20Tibidabo%2C%20Barcelona'
'228|Parc%20del%20Laberint%20d%27Horta%2C%20Barcelona'
'229|Sant%20Andreu%20de%20Palomar%2C%20Barcelona'
'230|La%20Maquinista%2C%20Barcelona'
'231|Monestir%20de%20Montserrat'
'232|Sitges'
'233|Catedral%20de%20Girona'
'234|Teatre-Museu%20Dal%C3%AD%2C%20Figueres'
'235|Amfiteatre%20de%20Tarragona'
'236|Cripta%20de%20la%20Col%C3%B2nia%20G%C3%BCell'
'237|Codorn%C3%ADu%2C%20Sant%20Sadurn%C3%AD%20d%27Anoia'
'238|Vila%20Vella%2C%20Tossa%20de%20Mar'
'239|Cadaqu%C3%A9s'
'240|Pont%20de%20Besal%C3%BA'
'241|Pla%C3%A7a%20Major%2C%20Vic'
'242|Monestir%20de%20Sant%20Cugat'
'243|Platja%20de%20Castelldefels'
'244|Catalunya%20en%20Miniatura'
'245|Illa%20Fantasia'
'246|La%20Roca%20Village'
)
$nomFile=Join-Path $dir 'nominatim.tsv'; $okn=0; $cnt=0
Write-Host ('Coordinates: ' + $nom.Count + ' places, about ' + [Math]::Ceiling($nom.Count*1.3/60) + ' minutes...')
foreach($row in $nom){
  $k,$q=$row -split '\|',2
  $u='https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&accept-language=en&q='+$q
  $line=$k+"`t"
  try{ $resp=Invoke-WebRequest -Uri $u -UseBasicParsing -UserAgent $ua -TimeoutSec 60 -ErrorAction Stop; $line+=(($resp.Content -replace '[\r\n]+',' ')); $okn++ } catch { $line+='ERROR' }
  [IO.File]::AppendAllText($nomFile,$line+"`n",(New-Object Text.UTF8Encoding($false)))
  $cnt++; if(($cnt % 25) -eq 0){ Write-Host ('  ' + $cnt + ' / ' + $nom.Count) }
  Start-Sleep -Milliseconds 1150
}
$log+=('nominatim ok: '+$okn+' of '+$nom.Count)

Set-Content -Path (Join-Path $dir '_report.txt') -Value $log
if(Test-Path $zip){ Remove-Item $zip -Force }
Compress-Archive -Path (Join-Path $dir '*') -DestinationPath $zip -Force
Write-Host ''
$log | ForEach-Object { Write-Host $_ }
Write-Host ''
Write-Host ('Done. ZIP file: ' + $zip + '  (' + [Math]::Round((Get-Item $zip).Length/1MB,1) + ' MB)') -ForegroundColor Green
