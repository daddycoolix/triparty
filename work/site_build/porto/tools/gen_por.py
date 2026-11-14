# -*- coding: utf-8 -*-
import sys; sys.path.insert(0,'/home/claude/por/site/build/porto')
from urllib.parse import quote
import plan
Q={"Ribeira (Cais da Ribeira and Praça da Ribeira)":"Praça da Ribeira, Porto","Dom Luís I Bridge":"Ponte Luís I, Porto","Porto Cathedral (Sé do Porto)":"Sé do Porto",
"Church of São Francisco":"Igreja de São Francisco, Porto","MMIPO, Misericórdia Museum and Church":"Igreja da Misericórdia do Porto","Fernandine Walls (Muralha Fernandina)":"Muralha Fernandina, Porto",
"Guindais Funicular":"Funicular dos Guindais","Six Bridges Cruise on the Douro (rabelo boats)":"Cais da Estiva, Porto","Barredo and Rua Escura alleys":"Rua Escura, Porto","Mercado Ferreira Borges":"Mercado Ferreira Borges",
"Church of São Nicolau":"Igreja de São Nicolau, Porto","Guerra Junqueiro House Museum":"Casa-Museu Guerra Junqueiro","Church of Santa Clara":"Igreja de Santa Clara, Porto","Church of São Lourenço (Grilos)":"Igreja de São Lourenço, Porto",
"Episcopal Palace of Porto":"Paço Episcopal do Porto","Escadas do Codeçal and Guindais":"Escadas do Codeçal, Porto","Porto Puppet Museum (Museu das Marionetas)":"Museu das Marionetas do Porto","Casa Portuguesa do Pastel de Bacalhau (Rua das Flores)":"Casa Portuguesa do Pastel de Bacalhau, Rua das Flores, Porto",
"Infante D. Henrique Bridge":"Ponte do Infante, Porto","Porto Old Jewish Quarter (Judiaria do Olival, Rua de São Miguel)":"Rua de São Miguel, Porto","Ribeira riverside bars":"Cais da Ribeira, Porto",
"São Bento Railway Station":"Estação de São Bento, Porto","Avenida dos Aliados and City Hall":"Câmara Municipal do Porto","Café Majestic":"Café Majestic, Porto","Capela das Almas":"Capela das Almas, Porto","Church of Santo Ildefonso":"Igreja de Santo Ildefonso, Porto",
"Praça da Batalha and Teatro Nacional São João":"Teatro Nacional São João","Confeitaria do Bolhão":"Confeitaria do Bolhão","Café Santiago (francesinha)":"Café Santiago, Porto","Cervejaria Gazela (cachorrinho)":"Cervejaria Gazela, Porto","Church of the Congregados":"Igreja dos Congregados, Porto",
"Café Guarany":"Café Guarany, Porto","Maus Hábitos":"Maus Hábitos, Porto","Church of the Trindade":"Igreja da Trindade, Porto","Praça da Liberdade and the D. Pedro IV statue":"Praça da Liberdade, Porto","Manteigaria (pastel de nata)":"Manteigaria, Porto",
"Padaria Ribeiro":"Padaria Ribeiro, Porto","Praça de D. João I":"Praça de D. João I, Porto","Rua 31 de Janeiro (jewellers)":"Rua de 31 de Janeiro, Porto","Clérigos Tower and Church":"Torre dos Clérigos","Carmo and Carmelitas Churches":"Igreja do Carmo, Porto",
"Portuguese Centre of Photography (Cadeia da Relação)":"Centro Português de Fotografia","Galerias de Paris and Rua Cândido dos Reis":"Rua Galeria de Paris, Porto","Passeio dos Clérigos (Praça de Lisboa rooftop garden)":"Passeio dos Clérigos, Porto",
"University of Porto Rectory and Natural History Museum":"Reitoria da Universidade do Porto","Church and Monastery of São Bento da Vitória":"Mosteiro de São Bento da Vitória","Plano B":"Plano B, Porto","A Vida Portuguesa (Porto)":"A Vida Portuguesa, Porto","Casa Oriental":"Casa Oriental, Porto",
"Church of São José das Taipas":"Igreja de São José das Taipas","Praça de Guilherme Gomes Fernandes":"Praça de Guilherme Gomes Fernandes, Porto","Hospital de Santo António":"Hospital de Santo António, Porto",
"Jardins do Palácio de Cristal":"Jardins do Palácio de Cristal","Soares dos Reis National Museum":"Museu Nacional Soares dos Reis","Rua de Miguel Bombarda (art galleries)":"Rua de Miguel Bombarda, Porto","Romantic Museum (Quinta da Macieirinha)":"Museu Romântico da Quinta da Macieirinha",
"Church of Nossa Senhora da Lapa":"Igreja da Lapa, Porto","Church of São Martinho de Cedofeita":"Igreja de São Martinho de Cedofeita","Alfândega do Porto (Customs House) and Transport Museum":"Alfândega do Porto","Port Wine Museum (Massarelos)":"Museu do Vinho do Porto",
"Passeio das Virtudes":"Passeio das Virtudes, Porto","Rua do Breyner antique shops":"Rua do Breyner, Porto","Church of São Pedro de Miragaia":"Igreja de São Pedro de Miragaia","Cedofeita bars (Rua da Galeria de Paris north, Travessa de Cedofeita)":"Travessa de Cedofeita, Porto",
"Casa-Museu Marta Ortigão Sampaio":"Casa-Museu Marta Ortigão Sampaio","Estádio do Dragão and FC Porto Museum":"Estádio do Dragão","Church of Bonfim":"Igreja do Bonfim, Porto","Casa Guedes (pork sandwich)":"Casa Guedes, Porto","Jardim de São Lázaro":"Jardim de São Lázaro, Porto",
"Miradouro das Fontainhas":"Alameda das Fontainhas, Porto","Prado do Repouso Cemetery":"Cemitério do Prado do Repouso","Campanhã Station":"Estação de Campanhã","Palácio do Freixo":"Palácio do Freixo","Alameda Shop and Spot":"Alameda Shop & Spot, Porto",
"Military Museum of Porto":"Museu Militar do Porto","Rua de Santa Catarina upper and Bonfim neighbourhood":"Rua de Santa Catarina 1000, Porto","Serralves Foundation (museum, park and villa)":"Museu de Serralves","Foz do Douro waterfront and Pérgola da Foz":"Pérgola da Foz, Porto",
"Felgueiras Lighthouse and Pier":"Farolim de Felgueiras","Castelo do Queijo (Fort of São Francisco Xavier)":"Castelo do Queijo","Jardim do Passeio Alegre":"Jardim do Passeio Alegre","Praia dos Ingleses and Praia do Molhe":"Praia dos Ingleses, Porto",
"Tram Line 1 (Infante to Passeio Alegre)":"Infante, Porto tram stop","Tram Museum (Museu do Carro Eléctrico)":"Museu do Carro Eléctrico","Arrábida Bridge and Porto Bridge Climb":"Ponte da Arrábida","Sea Life Porto":"Sea Life Porto","Parque da Cidade":"Parque da Cidade do Porto",
"Foz Velha (old Foz)":"Igreja de São João da Foz","Porto Botanical Garden":"Jardim Botânico do Porto","Porto Planetarium":"Planetário do Porto","Mercado da Foz":"Mercado da Foz do Douro","Praia do Homem do Leme":"Praia do Homem do Leme","Fort of São João Baptista da Foz":"Forte de São João Baptista da Foz",
"Praia do Carneiro":"Praia do Carneiro, Porto","Avenida do Brasil promenade":"Avenida do Brasil, Porto","Foz restaurants and seafood (general)":"Rua do Padrão, Porto","Casa da Música":"Casa da Música","Rotunda da Boavista":"Rotunda da Boavista","Mercado do Bom Sucesso":"Mercado do Bom Sucesso",
"Kadoorie Mekor Haim Synagogue and Jewish Museum of Porto":"Sinagoga Kadoorie Mekor Haim","Holocaust Museum of Porto":"Museu do Holocausto do Porto","Chabad Porto":"Chabad Porto","Kosher restaurant of the Porto Jewish community":"Rua de Guerra Junqueiro 340, Porto",
"Agramonte Cemetery":"Cemitério de Agramonte","Casa-Museu Fernando de Castro":"Casa-Museu Fernando de Castro","Avenida da Boavista":"Avenida da Boavista, Porto","Vodafone Building (Porto)":"Edifício Vodafone, Avenida da Boavista, Porto","Church of Santo António das Antas":"Igreja de Santo António das Antas",
"Jardim de Arca d'Água":"Jardim de Arca d'Água","Cais de Gaia and the Port Wine Cellars":"Cais de Gaia","Monastery of Serra do Pilar":"Mosteiro da Serra do Pilar","Gaia Cable Car (Teleférico de Gaia)":"Teleférico de Gaia","Jardim do Morro":"Jardim do Morro",
"Graham's Port Lodge":"Graham's, Vila Nova de Gaia","Sandeman Cellars":"Sandeman, Vila Nova de Gaia","Taylor's Port":"Taylor's, Vila Nova de Gaia","Cálem Cellars":"Cálem, Vila Nova de Gaia","WOW, World of Wine":"World of Wine, Vila Nova de Gaia","Mercado Beira-Rio":"Mercado Beira-Rio",
"Afurada fishing village":"Afurada","Lavadores and Canidelo beaches":"Praia de Lavadores","Senhor da Pedra Chapel (Miramar)":"Capela do Senhor da Pedra","Santo Inácio Zoo":"Zoo Santo Inácio","El Corte Inglés Gaia":"El Corte Inglés, Vila Nova de Gaia",
"Douro Estuary Nature Reserve":"Reserva Natural Local do Estuário do Douro","Casa-Museu Teixeira Lopes":"Casa-Museu Teixeira Lopes","Espaço Porto Cruz rooftop":"Espaço Porto Cruz","Ramos Pinto Cellars":"Ramos Pinto, Vila Nova de Gaia","Ferreira Cellars":"Ferreira, Vila Nova de Gaia",
"Casa Barbot":"Casa Barbot","Arrábida Shopping":"Arrábida Shopping","Convent of Corpus Christi":"Convento Corpus Christi, Vila Nova de Gaia","Praia de Matosinhos":"Praia de Matosinhos","Piscina das Marés (Álvaro Siza)":"Piscina das Marés",
"Casa de Chá da Boa Nova":"Casa de Chá da Boa Nova","Mercado de Matosinhos":"Mercado Municipal de Matosinhos","Rua Heróis de França (grilled fish)":"Rua Heróis de França, Matosinhos","Boa Nova Lighthouse (Farol de Leça)":"Farol de Leça","Fort of Nossa Senhora das Neves (Leça)":"Forte de Nossa Senhora das Neves",
"Anémona ('She Changes', Janet Echelman)":"She Changes, Matosinhos","Leixões Cruise Terminal":"Terminal de Cruzeiros de Leixões","Bom Jesus de Matosinhos Church":"Igreja do Bom Jesus de Matosinhos","NorteShopping":"NorteShopping","Quinta da Conceição":"Quinta da Conceição, Matosinhos",
"Praia de Leça da Palmeira":"Praia de Leça da Palmeira","Surf schools at Matosinhos beach":"Praia de Matosinhos","Real Vinícola (cultural hub, Matosinhos)":"Real Vinícola, Matosinhos","Zoo da Maia":"Zoo da Maia","Parque Biológico de Gaia":"Parque Biológico de Gaia",
"Monastery of Leça do Balio":"Mosteiro de Leça do Balio","Praia da Aguda":"Praia da Aguda","Vila do Conde Porto Fashion Outlet":"Vila do Conde Porto Fashion Outlet","Braga and Bom Jesus do Monte":"Sé de Braga","Guimarães":"Castelo de Guimarães","Aveiro and Costa Nova":"Aveiro",
"Douro Valley (Pinhão and Peso da Régua)":"Pinhão","Amarante":"Amarante","Coimbra":"Universidade de Coimbra","Viana do Castelo":"Viana do Castelo","Lamego (Nossa Senhora dos Remédios)":"Santuário de Nossa Senhora dos Remédios, Lamego","Santa Maria da Feira Castle":"Castelo de Santa Maria da Feira",
"Barcelos":"Barcelos","Ponte de Lima":"Ponte de Lima","Peneda-Gerês National Park":"Vila do Gerês","Vila do Conde":"Vila do Conde","Mateus Palace (Vila Real)":"Casa de Mateus","Douro Line train ride (Porto to Pocinho)":"Estação de Peso da Régua","Espinho beach and market":"Espinho","Citânia de Briteiros":"Citânia de Briteiros"}
nom=[]
for i,p in enumerate(plan.PLAN):
    q=Q.get(p[2]) or (p[2]+", Porto"); nom.append("'%03d|%s'"%(i,quote(q,safe='')))
BB='41.095,-8.730,41.215,-8.540'
def art(f): return '(nwr["tourism"="artwork"]%s;nwr["historic"~"^(memorial|monument)$"]%s;nwr["amenity"="fountain"]["name"]%s;nwr["amenity"="fountain"]["wikidata"]%s;);out center tags;'%((f,)*4)
def poi(f): return '(nwr["tourism"~"^(attraction|museum|gallery|viewpoint|zoo|aquarium)$"]["name"]%s;nwr["historic"]["name"]%s;nwr["amenity"~"^(place_of_worship|marketplace|theatre|arts_centre|nightclub|cafe)$"]["name"]%s;nwr["leisure"~"^(park|garden|water_park)$"]["name"]%s;nwr["building"]["wikidata"]["name"]%s;nwr["shop"~"^(mall|department_store|wine|books)$"]["name"]%s;nwr["natural"="beach"]%s;nwr["place"="square"]["name"]%s;nwr["aerialway"="station"]%s;nwr["railway"="tram_stop"]%s;);out center tags;'%((f,)*10)
FUN='(nwr["leisure"~"^(escape_game|amusement_arcade|bowling_alley|high_ropes_course|skatepark|water_park|trampoline_park|miniature_golf)$"];nwr["sport"~"karting|paintball|laser_tag|billiards|snooker|bowling|10pin|surfing"];nwr["sport"~"climbing"]["leisure"];nwr["tourism"="theme_park"];nwr["attraction"~"summer_toboggan|roller_coaster|alpine_coaster"];nwr["aerialway"="zip_line"];nwr["theatre:genre"="circus"];nwr["leisure"]["name"~"jet ski|jetski|virtual|quad|buggy|rage|circus|circo|escape|laser",i];nwr["amenity"]["name"~"jet ski|jetski|virtual|quad|buggy|rage|circus|circo|escape|laser",i];nwr["shop"]["name"~"jet ski|jetski|virtual|quad|buggy|rage|escape|laser",i];nwr["tourism"]["name"~"jet ski|jetski|virtual|quad|buggy|rage|circo|escape|laser",i];);out center tags;'
KOS='(nwr["diet:kosher"];nwr["amenity"="place_of_worship"]["religion"="jewish"];nwr["cuisine"~"kosher|jewish|israeli"];nwr["name"~"kosher|chabad|sinagoga|judaico|holocausto",i];nwr["tourism"="museum"]["name"~"juda|holocaust",i];);out center tags;'
Qs={"art":['[out:json][timeout:180][bbox:%s];'%BB+art('')],"poi":['[out:json][timeout:180][bbox:%s];'%BB+poi('')],
 "fun":['[out:json][timeout:180][bbox:40.95,-8.85,41.45,-8.20];'+FUN],"kosher":['[out:json][timeout:90][bbox:41.08,-8.75,41.25,-8.50];'+KOS],
 "test":['[out:json][timeout:25];node["tourism"="artwork"](41.140,-8.620,41.150,-8.600);out 5;']}
rows=[]
for k in ["test","art","poi","fun","kosher"]:
    for i,q in enumerate(Qs[k]): rows.append("'%s|%d|%s'"%(k,i,quote(q,safe='')))
WV=[("wv_en_Porto","https://en.wikivoyage.org/w/index.php?action=raw&title=Porto"),("wv_en_Gaia","https://en.wikivoyage.org/w/index.php?action=raw&title="+quote("Vila_Nova_de_Gaia")),
 ("wv_en_Matosinhos","https://en.wikivoyage.org/w/index.php?action=raw&title=Matosinhos"),("wv_he_Porto","https://he.wikivoyage.org/w/index.php?action=raw&title="+quote("פורטו")),
 ("wv_en_Braga","https://en.wikivoyage.org/w/index.php?action=raw&title=Braga"),("wv_en_Guimaraes","https://en.wikivoyage.org/w/index.php?action=raw&title="+quote("Guimarães")),("wv_en_Douro","https://en.wikivoyage.org/w/index.php?action=raw&title="+quote("Douro_Valley"))]
wv="\n".join("'%s|%s'"%(a,b) for a,b in WV)
script=open('/home/claude/tool/triparty-barcelona-osm.cmd').read().replace('\r\n','\n')
ps=script.split('#PSBEGIN\n',1)[1]
# replace rows block
a=ps.index('$rows=@(\n'); b=ps.index('\n)\n',a)+3
ps=ps[:a]+'$rows=@(\n'+"\n".join(rows)+'\n)\n'+ps[b:]
ps=ps.replace("'triparty-bcn-osm'","'triparty-porto-data'").replace("'triparty-bcn-osm.zip'","'triparty-porto-data.zip'").replace('Triparty Barcelona OSM','Triparty Porto data')
extra=r'''
# Wikivoyage
$wv=@(
__WV__
)
foreach($row in $wv){ $k,$u=$row -split '\|',2
  try{ Invoke-WebRequest -Uri $u -OutFile (Join-Path $dir ($k+'.txt')) -UseBasicParsing -UserAgent $ua -TimeoutSec 120 -ErrorAction Stop; Log ('WV '+$k+' OK') } catch { Log ('WV '+$k+' ERROR: '+(ErrText $_)) } }
# Nominatim
$nom=@(
__NOM__
)
$nomFile=Join-Path $dir 'nominatim.tsv'; $okn=0; $cnt=0
Write-Host ('Coordinates: ' + $nom.Count + ' places, about ' + [Math]::Ceiling($nom.Count*1.3/60) + ' minutes...')
foreach($row in $nom){ $k,$q=$row -split '\|',2
  $u='https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&accept-language=en&q='+$q
  $line=$k+"`t"
  try{ $resp=Invoke-WebRequest -Uri $u -UseBasicParsing -UserAgent $ua -TimeoutSec 60 -ErrorAction Stop; $line+=(($resp.Content -replace '[\r\n]+',' ')); $okn++ } catch { $line+='ERROR' }
  [IO.File]::AppendAllText($nomFile,$line+"`n",(New-Object Text.UTF8Encoding($false)))
  $cnt++; if(($cnt % 25) -eq 0){ Write-Host ('  ' + $cnt + ' / ' + $nom.Count) }
  Start-Sleep -Milliseconds 1150 }
Log ('nominatim ok: '+$okn+' of '+$nom.Count)
'''.replace('__WV__',wv).replace('__NOM__',"\n".join(nom))
ps=ps.replace("if(Test-Path $zip){ Remove-Item $zip -Force }",extra+"\nif(Test-Path $zip){ Remove-Item $zip -Force }",1)
full=script.split('#PSBEGIN\n',1)[0].replace('Triparty Barcelona OSM','Triparty Porto data')+'#PSBEGIN\n'+ps
assert all(ord(c)<128 for c in full)
open('triparty-porto-data.cmd','w',newline='').write(full.replace('\n','\r\n'))
S='/tmp/claude-0/-home-claude/8c12de7a-8e67-5efa-a37f-cc2e82fcb26a/scratchpad/'
open(S+'test_por.ps1','w').write(ps.replace('-TimeoutSec 300','-TimeoutSec 3').replace('-TimeoutSec 120','-TimeoutSec 3').replace('-TimeoutSec 60','-TimeoutSec 2').replace('Start-Sleep -Seconds 3','').replace('Start-Sleep -Seconds 4','').replace('Start-Sleep -Milliseconds 1150',''))
print(len(nom),len(rows),len(full))
