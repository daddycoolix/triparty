# -*- coding: utf-8 -*-
# בונה קובץ HTML יחיד עם כל הערים מוטמעות, לשימוש בלי אתר ובלי רשת (פתיחה ישירה מהמחשב או מהטלפון)
import io,json,os,re,sys
S=sys.argv[1] if len(sys.argv)>1 else 'site'
OUT=sys.argv[2] if len(sys.argv)>2 else 'Triparty-all-cities.html'
h=io.open(os.path.join(S,'index.html'),encoding='utf-8').read()
files=['cities.json','triparty-art-settings.json']
c=json.load(open(os.path.join(S,'cities.json'),encoding='utf-8'))
for x in c['cities']:
    files.append(x['file'])
    a=x['file'].replace('.json','-art.json')
    if os.path.exists(os.path.join(S,a)): files.append(a)
blocks=[]
for f in files:
    t=io.open(os.path.join(S,f),encoding='utf-8').read().strip()
    json.loads(t)
    blocks.append('<script type="application/json" class="tpFile" data-name="%s">%s</script>'%(f,t.replace('</','<\\/')))
shim='''<script>
/* Triparty: כל הערים מוטמעות בקובץ. כשהקובץ נפתח ישירות (לא מהאתר), קריאות לקובצי הערים נענות מהעותק המוטמע. */
(function(){
  if(/^https?:$/.test(location.protocol))return;
  var F={};
  function idx(){document.querySelectorAll("script.tpFile").forEach(function(s){F[s.getAttribute("data-name")]=s;});}
  var orig=window.fetch?window.fetch.bind(window):null;
  window.fetch=function(u,o){
    try{
      if(!Object.keys(F).length)idx();
      var s=String(u&&u.url?u.url:u), m=s.match(/(?:^|\\/)([A-Za-z0-9._-]+\\.json)(?:[?#]|$)/);
      if(m&&F[m[1]])return Promise.resolve(new Response(F[m[1]].textContent,{status:200,headers:{"Content-Type":"application/json"}}));
    }catch(e){}
    return orig?orig(u,o):Promise.reject(new Error("no fetch"));
  };
})();
</script>'''
m=re.search(r'<head[^>]*>',h)
out=h[:m.end()]+'\n'+'\n'.join(blocks)+'\n'+shim+h[m.end():]
io.open(OUT,'w',encoding='utf-8').write(out)
print(len(files),'files embedded:',files); print('%.1f MB'%(len(out.encode())/1e6))
