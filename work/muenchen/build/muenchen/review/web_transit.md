# אימות תחבורה ומחירים ברשת: מדריך מינכן (17.11.2026)

## מה אומת
- **תעריפי MVV 2026** ([muenchen.de](https://www.muenchen.de/verkehr/aktuell/mvv-tickets-aktuelle-preise-fuer-fahrkarten-muenchen)): נסיעה בודדת באזור M 4.20 יורו, Single-Tageskarte לאזור M 10.10 יורו (במדריך כתוב "בערך 10", וזה תקין), Gruppen-Tageskarte לאזורים M-5 32.60 יורו, כרטיס דויטשלנד 63 יורו לחודש.
- **עליית מחירים בינואר 2027** ([הודעת MVV מ־18.09.2026](https://www.mvv-muenchen.de/mvv-im-ueberblick/die-gesellschaft/presse/pressemeldung/neue-fahrpreise-im-mvv-zum-01012027/)): הכרטיס היומי לאזור M יעלה ל־10.80 יורו, ולכן המשפט במדריך נכון.
- **כרטיס יומי** ([mvv-muenchen.de](https://www.mvv-muenchen.de/tickets-abos-preise/single-tageskarte)): תקף עד 6:00 בבוקר שלמחרת. הכרטיס הקבוצתי תקף לעד 5 אנשים. נכון.
- **שדה התעופה** ([european-traveler, עודכן ביוני 2026](https://www.european-traveler.com/germany/ground-transportation-to-munich-airport-muc/), [bahn.de](https://www.bahn.de/angebot/s-bahn-muc/mvv-airport-city-day-ticket), [MVV](https://www.mvv-muenchen.de/en/tickets-subscriptions-prices/airport-city-day-ticket/)): השדה נמצא באזור 5. נסיעה בודדת M-5 עולה 15.10 יורו, ו־Airport-City-Day-Ticket ליחיד 17.50 יורו. S8 מגיעה לתחנה המרכזית בכ־41 דקות ו־S1 בכ־45 דקות, וכל קו יוצא בערך כל 20 דקות.
- **MyRadl** ([הודעת MVV](https://www.mvv-muenchen.de/mvv-im-ueberblick/die-gesellschaft/presse/pressemeldung/flexibel-und-umweltfreundlich-unterwegs-myradl-das-bikesharing-system-fuer-die-region-muenchen-startet-am-7-mai-2026/), [muenchen.de](https://www.muenchen.de/verkehr/aktuell/myradl-muenchen-preise-ausleihe-und-standorte)): המערכת התחילה לפעול ב־7.5.2026 ומופעלת בידי Nextbike. אופניים רגילים עולים יורו אחד לכל 30 דקות, ולבעלי מינוי תחבורה מתאים 30 הדקות הראשונות בחינם. MVG Rad הופסקה בסתיו 2025 ([secretmuenchen](https://secretmuenchen.com/en/myradl-rental-bikes-munich/)). מה שכתוב על כך ב־guide.py נכון.
- **מס לינה** ([hogapage](https://www.hogapage.de/nachrichten/politik/branchenpolitik/klage-gescheitert-bettensteuer-in-bayern-bleibt-verboten/), [beck-aktuell, פברואר 2026](https://www.beck-aktuell.de/heute-im-recht/rechtspolitik-gesetzgebung/muenchen-ob-reiter-bettensteuer-bverfg-uebernachtungsteuer-2026-02-26)): לא הוכנס. בוואריה אסרה מס לינה מקומי, ובנובמבר 2025 דחה בית המשפט החוקתי של בוואריה את העתירה של מינכן. בפברואר 2026 העירייה הציעה לפנות לבית המשפט החוקתי הפדרלי, ולא מצאתי שהתקבלה החלטה. המדריך לא מזכיר מס לינה, ולכן אין מה לתקן.
- **חנויות ביום ראשון** ([stadt.muenchen.de](https://stadt.muenchen.de/news/neues-bayerisches-ladenschlussgesetz.html)): חוק שעות הפתיחה החדש של בוואריה נכנס לתוקף ב־1.8.2025. שעות הפתיחה בימי חול לא השתנו, וההגנה על ימי ראשון וחגים נשארה. החידושים הם עד 4 ערבי קניות בשנה ומרכולים קטנים לשירות עצמי, עד 150 מ"ר, שרשאים לפתוח גם בימי ראשון. מה שכתוב במדריך ("רוב החנויות סגורות") נכון.
- **הקו השני של ה־S-Bahn**: הוא עדיין בבנייה, וזה מה שכתוב במדריך. בנוסף נפתח בתחילת 2026 הקטע הראשון של חשמלית 14 (Tram-Westtangente) ([SWM](https://www.swm.de/unternehmen/presse/pressemitteilungen/2026/02-2026/mvg-inbetriebnahme-tram-14-twt-erster-abschnitt)). הקטע אינו רלוונטי לתיירים, ולא הוספתי אותו.
- **זמני נסיעה בשדות ti** (S8 להרשינג כ־50 דקות, S1 לפרייזינג 40-45 דקות, קווי U לתחנה המרכזית, לאודאונספלאץ ולקרלספלאץ): תואמים את מה שידוע על הרשת.

## מה תוקן
1. ב־`guide.py` (תחבורה): כרטיס בודד באזור M שונה מ"בערך 4 יורו" ל"בערך 4.20 יורו".
2. ב־`guide.py`: נסיעה בודדת לשדה התעופה שונתה מ"בערך 14-15 יורו" ל"בערך 15 יורו", לפי המחיר 15.10 יורו.
3. ב־`guide.py`: Airport-City-Day-Ticket שונה מ"בערך 16 יורו" ל"בערך 17.50 יורו".
4. ב־`batch_6_ludwig.py` (וסטפארק): במקור נכתב "U4 ו-U5 לתחנת הסוף וסטנדשטראסה", אבל רק U4 מסתיים שם, ו־U5 ממשיך ללאימר פלאץ. התיקון: "לתחנת וסטנדשטראסה (תחנת הסוף של U4)".
- עוד ממצא: אזכורי MVG Rad ב־batch_3_schwabing וב־batch_5_au כבר הוחלפו ב־MyRadl על ידי סוקר אחר, ולכן לא נגעתי בהם.
- הבדיקות check_guide ו־check_batch batch_6_ludwig עברו (OK).

## מה לא ניתן לאמת
- המחיר הנוכחי של Airport-City-Day-Ticket בגרסה הקבוצתית: ב־bahn.de מופיע 30.50 יורו, כנראה נתון ישן, ובטבלאות של MVV מוצג 0.00 בגלל תקלת תצוגה. המדריך לא מציין מחיר לגרסה הזו.
- הקנס של בערך 60 יורו והמחיר של מונית מהשדה (70-100 יורו לפי המדריך, 80-90 לפי european-traveler): לא נבדקו מול מקור רשמי. הניסוח המסויג במדריך נשאר כמו שהוא.
- אם כרטיס דויטשלנד לבדו מזכה ב־30 דקות חינם ב־MyRadl: המקור הרשמי מדבר על "מינוי תחבורה מתאים", ולכן הניסוח המסויג במדריך נשאר.
- סגירות ספציפיות של U-Bahn בסוף 2026: לא נמצא מידע רלוונטי לתיירים.
