# בדיקת היישום בדפדפן: טעינת אמסטרדם, לשוניות, יצירות, חיפוש, הרחבת כרטיס, אירועים ומדריך
import subprocess,time,sys
from playwright.sync_api import sync_playwright
SITE=sys.argv[1] if len(sys.argv)>1 else '/home/claude/ams/site'
srv=subprocess.Popen(['python3','-m','http.server','8791','--directory',SITE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':412,'height':900},locale='he-IL').new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    bad=[]; pg.on('response',lambda r: bad.append((r.status,r.url[-60:])) if 'localhost' in r.url and r.status>=400 else None)
    pg.route('**/*',lambda r: r.continue_() if 'localhost' in r.request.url else r.abort())
    pg.goto('http://localhost:8791/index.html',wait_until='load'); pg.wait_for_timeout(2000)
    pg.click('#cityOpen'); pg.wait_for_timeout(400)
    names=pg.evaluate("()=>[...document.querySelectorAll('#builtinCities button')].map(b=>b.textContent.trim().slice(0,20))"); print('cities',names)
    idx=[i for i,n in enumerate(names) if 'אמסטרדם' in n][0]
    pg.click('#builtinCities button[data-bi="%d"]'%idx); pg.wait_for_timeout(3500)
    print('items',pg.evaluate("()=>[items.length,(items[0]||{}).he]"))
    print('cards',pg.evaluate("()=>document.querySelectorAll('#out .card').length"))
    for s in ['cat','dist','area','cost','rate']:
        x=pg.query_selector(f'#seg button[data-s="{s}"]')
        if x: x.click(); pg.wait_for_timeout(500); print(s,pg.evaluate("()=>[document.querySelectorAll('#out .card').length,[...document.querySelectorAll('#out h2')].length]"))
    pg.fill('#q','אנה פרנק'); pg.wait_for_timeout(700)
    print('search',pg.evaluate("()=>[...document.querySelectorAll('#out .card .head')].slice(0,3).map(e=>e.textContent.replace(/\\s+/g,' ').slice(0,50))"))
    pg.click('#out .card .head'); pg.wait_for_timeout(400)
    xb=pg.query_selector('#out .card button:has-text("הרחב")')
    if xb:
        xb.click(); pg.wait_for_timeout(800)
        print('xtabs',pg.evaluate("()=>document.getElementById('xtabs').textContent"),pg.evaluate("()=>document.getElementById('xbody').textContent.length"))
        pg.screenshot(path='/home/claude/ams/tests/s_expand.png')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.fill('#q',''); pg.wait_for_timeout(400)
    ch=pg.query_selector('#chips .chip[data-k="art"]')
    if ch:
        ch.click(); pg.wait_for_timeout(600)
        bt=pg.query_selector('button:has-text("בחר יצירות")')
        if bt:
            bt.click(); pg.wait_for_timeout(600)
            print('artdlg',pg.evaluate("()=>document.getElementById('artdlg').textContent.replace(/\\s+/g,' ').slice(0,300)"))
            a=pg.query_selector('#artdlg :text("כל היצירות")')
            if a: a.click(); pg.wait_for_timeout(2500)
            for lab in ['החל','הצג','סגור']:
                x=pg.query_selector(f'#artdlg button:has-text("{lab}")')
                if x: x.click(); break
            pg.wait_for_timeout(2000)
            print('art cards',pg.evaluate("()=>[document.querySelectorAll('#out .card').length,(document.getElementById('resN')||{}).textContent]"))
            pg.screenshot(path='/home/claude/ams/tests/s_art.png')
    print('castle',pg.evaluate("()=>{const it=items.find(i=>i.en==='Anne Frank House');return it?[it.he,!!(it.x&&it.x.kids),it.x&&it.x.quiz?it.x.quiz.length:0,it.x&&it.x.timeline?it.x.timeline.length:0]:'missing'}"))
    pg.reload(); pg.wait_for_timeout(2500)
    print('after reload',pg.evaluate("()=>[CITY,items.length]"))
    print('pageerrors',errs); print('http errors',bad)
    b.close()
finally: srv.terminate()
