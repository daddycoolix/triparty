# אימות ברשת: טיולי יום ואטרקציות (4.11.2026)

קבצים: batch_10_edge.py, batch_11_out_p1.py, batch_11_out_p2.py, batch_fun.py. כל השינויים נעשו בעריכות נקודתיות בשדות ho/co/ti (ובכרטיס ורסוס גם d ו-story). לא נגעתי בפוניקולרים, במעליות או במספרי קווים. בסוף העבודה כל הבדיקות עברו: check_batch OK x3, check_fun OK (22).

מגבלה: הגעתי למכסה של 25 חיפושים. אתרים רשמיים רבים (regaleira.pt, vertigoclimbing.pt, parquesdesintra.pt/park page) לא היו ברשימת ה-URL המותרים, ולכן חלק מהאימות נעשה מול Time Out, אתרי תיירות או עיתונות. במקרים כאלה המקור מצוין בטקסט, ולא כתבתי "לפי אתר המקום".

## אומת ועודכן

| כרטיס | מה אומת | מקור |
|---|---|---|
| פנה | פארק 9:00-19:00 (כניסה אחרונה 18:00), ארמון 9:30-18:30; ביקור בסיסי 20/18/18 יורו, משפחתי 65, פארק בלבד 12/10; תוספת שאטל 4.5 | [Parques de Sintra, שעות ומחירים](https://www.parquesdesintra.pt/en/plan-your-visit/opening-times-and-prices/) |
| הטירה המורית | 9:30-18:00, כניסה אחרונה 17:30, קופה סגורה 12-13; 12/10/10, משפחתי 33. לפני כן נכתב "בקיץ עד 20:00", והשעה הזאת לא מופיעה באתר | כנ"ל |
| ארמון סינטרה הלאומי | 9:30-18:30, כניסה אחרונה 17:30; 13/10/10, משפחתי 35 | כנ"ל |
| מונסראטה | פארק 9:00-19:00, ארמון 9:30-18:00; 12/10/10, משפחתי 33 | כנ"ל |
| קלוז (batch_10, בונוס) | ארמון 9:00-18:00, גנים 9:00-18:30; 13/10/10/35, גנים בלבד 6 | כנ"ל |
| קינטה דה רגליירה, מחיר | מינואר 2026: 20 מבוגר, 15 נוער (6-17) וגמלאים, משפחתי 60, עד גיל 5 חינם, מדריך קולי 5 | [regaleira.pt, מחירים 2026](https://www.regaleira.pt/en/destaques/2025-entrance-fees-2026/) |
| מאפרה | 9:30-17:30, כניסה אחרונה 16:30, סגור בשלישי ובחגים. **הספרייה נפתחה מחדש בינואר 2026.** **הבזיליקה בשיפוץ ולפי דיווח מאפריל 2026 סגורה כשנתיים** (סיום צפוי ביולי 2026; לא מצאתי אישור שנפתחה) | [VisitLisboa](https://www.visitlisboa.com/pt-pt/locais/palacio-nacional-de-mafra), [Observador 12.1.2026](https://observador.pt/2026/01/12/biblioteca-do-palacio-nacional-de-mafra-reabre-apos-obras-de-restauro/), [RR 17.4.2026](https://rr.pt/noticia/pais/2026/04/17/prr-palacio-nacional-de-mafra-com-primeira-grande-requalificacao/467286/) |
| מחירי MMP: מאפרה, בטליה, אלקובאסה, מנזר ישו בטומאר | 15 יורו מ-2025 (לפני כן נכתב 8-10), 50% הנחה לגילי 13-24 ולמעל 65, עד גיל 12 חינם בליווי מבוגר. לא נמצא מחיר לכרטיס המשולב, ולכן ניסחתי "ייתכן" | [Despacho 13793/2024](https://museusoaresdosreis.gov.pt/wp-content/uploads/2025/03/Despacho-13793_2024-Bilhetica-MMP.pdf), [Notícias ao Minuto](https://www.noticiasaominuto.com/cultura/2699257/precos-de-entrada-em-museus-e-monumentos-sobem-este-ano-quanto) |
| בית הכנסת בטומאר | שלישי-ראשון; בקיץ 10-13 ו-14-18, בחורף 10-12 (לא 13) ו-14-17; סגור בשני. **לא נמצא שיפוץ נוכחי.** השיפוץ האחרון הסתיים באוקטובר 2019 | [תיירות עיריית טומאר](https://www.turismo.cm-tomar.pt/Places/Details/sinagoga-de-tomar?cat=wtd), [Times of Israel 2019](https://www.timesofisrael.com/museum-inside-portugals-oldest-jewish-synagogue-reopens/) |
| בריכת הים של אוארש | פעילה. העונה נפתחה ב-22.5.2026. מחירי 2026: 15/20 יורו ביוני, ספטמבר ואוקטובר (10 יורו מ-16:00); 25/30 ביולי ובאוגוסט. לפני כן נכתב "10 יורו". השעות לא אומתו | [Executive Digest 22.5.2026](https://executivedigest.sapo.pt/?p=765878), [Postal 19.6.2026](https://postal.pt/nacional/fica-em-portugal-uma-das-maiores-piscinas-oceanicas-da-europa-com-100-metros-de-comprimento-e-bilhetes-a-10e/) |
| שביל קאיש דו ז'ינז'אל | נסגר באביב 2025 בגלל בורות ברציף ונפתח מחדש ב-31.7.2025 עם משטח, מעקות ותאורת LED. ההסדר מוגדר "זמני". מחקתי את "בלי תאורה טובה בלילה" | [RTP](https://www.rtp.pt/noticias/pais/passear-pelo-cais-do-ginjal-em-almada-voltou-a-ser-possivel-a-partir-de-hoje_n1673249), [Portugal Post](https://theportugalpost.com/posts/almadas-tagus-side-ginjal-promenade-welcomes-walkers-again-31-july) |
| פונטו פינאל | סגורה בשלישי, פתוחה רביעי-שני 12:30-16:00 ו-19:00-23:00 (מקור: Time Out) | [Time Out](https://www.timeout.pt/lisboa/pt/restaurantes/ponto-final) |
| פיריקיטה | לפי אתר ממשלתי: 9:30-19:00 בימי חול, 9:00-19:30 בסופי שבוע, בלי יום סגירה. **המידע הזה סותר את "סגור ברביעי".** השארתי את שתי הגרסאות עם הסתייגות | [Comércio com História](https://www.comerciocomhistoria.gov.pt/en/?p=24650) |

## אטרקציות (batch_fun) שעודכנו

| כרטיס | מה עודכן | מקור |
|---|---|---|
| Vertigo | פעיל. שעות: שני-שישי 10-23, רביעי מ-7, שבת 10-20, ראשון 10-18 | [Time Out](https://www.timeout.pt/lisboa/pt/desporto/vertigo-climbing-center) |
| Kartódromo Palmela | פעיל. רביעי-ראשון 9-19 (בקיץ עד 20), שלישי 14-19; 11-12 יורו ל-15 דקות (מסלול קטן, גובה 1.20) | [Time Out](https://www.timeout.pt/lisboa/pt/coisas-para-fazer/kartodromo-internacional-de-palmela), [Lisboa Secreta 1/2025](https://lisboasecreta.co/en/karting-lisbon-metropolitan-area/) |
| Escape Hunt | פעיל (באתר הרשת יש עדכון מספטמבר 2025). 55-80 יורו לקבוצה של 2-5, Rua dos Douradores 13 | [Time Out](https://www.timeout.pt/lisboa/pt/coisas-para-fazer/escape-hunt-lisboa), [escapehunt.com](https://escapehunt.com/pt/en/?p=192) |
| Escape2Win | כתובת Rua Ernesto da Silva 54; "מ-50 יורו לזוג" (מקור מ-2024). לא נמצאה הוכחה לפעילות ב-2025-2026 | [Lisboa Secreta 2024](https://lisboasecreta.co/en/the-best-escape-rooms-in-lisbon-en/), [escapethereview](https://escapethereview.co.uk/escape-room/55205/escape2win-dream) |
| Versus Gamecenter | פעיל (טורנירים עד 31.10.2026). **תיקון מהותי: זו חנות ומרכז של משחקי קלפים אספניים (Magic), לא מרכז גיימינג או ארקייד.** עדכנתי את d, ho, co ואת הסיפור. שדה ak ("ארקייד") נשאר, כי הבודק מגביל את הערכים. כדאי לשקול לשנות אותו או להסיר את הכרטיס מהקטגוריה | [Unity League](https://unityleague.gg/organizer/150) |
| Quantum Park Almada | פעיל (מופיע בכתבות Time Out על אירועים). שעות: רביעי-חמישי 16-20, שישי 14-21, סופ"ש 10-20 | [Time Out](https://www.timeout.pt/lisboa/pt/coisas-para-fazer/quantum-park-almada) |

## נמצא אבל לא שונה (המקור ישן מדי או לא רשמי)
- Bowling City Colombo: כל יום 11:00-24:00, 16 מסלולים. Play Bowling Cascais: Rua Chesol 35, שני-חמישי 15:00-01:00, שבת וראשון מ-10:00. המקור מ-2023 ([Lisboa Secreta](https://lisboasecreta.co/es/bowling-en-lisboa/)). הכרטיסים כבר מנוסחים בהסתייגות.
- JumpYard Carnaxide (Av. dos Cavaleiros 35): שני-חמישי 10-21, שישי 10-22, סופ"ש 10-21. המקור מ-2024 ([Lisboa Secreta](https://lisboasecreta.co/en/trampoline-parks-lisbon/)).
- רגליירה, שעות: מקור לא רשמי נותן 9:30-18:00 בחורף ו-9:30-20:00 בקיץ ([idealista](https://www.idealista.pt/en/news/node/61830)), אבל המחירים באותו מקור ישנים. בכרטיס נשאר "בערך 10:00-18:30".

## לא נמצא או לא נבדק (נשאר בהסתייגות)
- **Castelo de Vide**: עמוד VisitPortugal נחסם, ולא נמצאו שעות או מחיר.
- **Óbidos, Fátima, Nazaré (מבצר ומגדלור), Évora (קפלת העצמות, הקתדרלה)**: לא נבדקו, כי מכסת החיפושים נגמרה. הכרטיסים מסויגים. הפוניקולר בנזרה לא נבדק בכוונה, כי הוא לא בתחום שלי.
- שעות פתיחה של בטליה, אלקובאסה ומנזר ישו, ומחיר הכרטיס המשולב: לא אומתו.
- **Parque Aventura Jamor, Emboscada Paintball, City Escape Room (Benfica), Foxtrot, Aldeia José Franco, Chapitô**: לא נבדקו, כי מכסת החיפושים נגמרה. לא מצאתי סימן לסגירה, אבל גם לא אישור לפעילות.

## להסרה
אין עסק שאושר כסגור, ולכן לא נמחק אף כרטיס. שני כרטיסים הם מועמדים להסרה אחרי בדיקה נוספת:
- **Zeitnot (Alvalade)**: לא נמצאה שום עדות ברשת לעסק בשם הזה (החיפוש העלה אפס תוצאות רלוונטיות). הכרטיס מבוסס על OSM בלבד.
- **XLand Fun Park Montijo**: נמצא רק רישום ב-Wanderlog. לא נמצאו אתר, שעות או מחירים. במונטיז'ו פעיל פארק אחר, Feijão Verde Fun Park ב-Forum Montijo ([NiT 6/2026](https://www.nit.pt/fora-de-casa/miudos/atencao-pais-ha-um-novo-parque-de-obstaculos-para-levar-os-miudos-no-montijo)).
